"""
Canonical Corrected Experimental Pipeline for Cross-Lingual Evidence Verification.

Research Integrations & Validity Repairs:
1. True token-based truncation (tokenizer max_length=512, truncation=True, no character slicing).
2. Direct MT-Verifier coupling: MarianMT generates translation text, which is decoded and
   passed directly to the mDeBERTa verifier. Timing and prediction use the exact same text.
3. True numeral Jaccard overlap (|A ∩ B| / |A ∪ B|) computed between Hindi evidence and generated translation.
4. Exact end-to-end latency accounting per instance on CPU (warmup included, 8 threads).
5. Threshold tuning strictly on Dev data across grid [0.10, 0.65, 0.025] with pre-specified
   tradeoff objective J(tau) = Macro_F1_3cl - 0.15 * Coverage.
6. Multi-seed Random Routing Control: evaluated across 100 reproducible seeds (s=0..99)
   with exact matched item count round(N * cov_target), reporting mean, SD, and 95% CI.
7. Rigorous paired statistical significance testing: exact binomial McNemar test,
   5,000-permutation paired F1 test, bootstrap 95% CIs (2,000 resamples), and Benjamini-Hochberg FDR correction.
8. Output consistency: all metrics, tables, and raw per-instance predictions saved deterministically.
"""
import re
import json
import time
import numpy as np
import pandas as pd
import scipy.stats as stats
from pathlib import Path
from tqdm import tqdm

try:
    import torch
    from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoModelForSeq2SeqLM
    HAS_TORCH_TRANSFORMERS = True
except ImportError:
    torch = None
    AutoTokenizer = None
    AutoModelForSequenceClassification = None
    AutoModelForSeq2SeqLM = None
    HAS_TORCH_TRANSFORMERS = False

from sklearn.metrics import accuracy_score, f1_score, confusion_matrix

WORKSPACE = Path(__file__).resolve().parents[1]
RES_DIR = WORKSPACE / "experiments" / "results_canonical"
RES_DIR.mkdir(parents=True, exist_ok=True)

MODEL_VERIFIER = "MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7"
MODEL_MT = "Helsinki-NLP/opus-mt-hi-en"

LABELS_3CL = ["SUPPORTED", "INSUFFICIENT_EVIDENCE", "CONTRADICTED"]
LABELS_2CL = ["INSUFFICIENT_EVIDENCE", "CONTRADICTED"]
ID2LABEL = {0: "SUPPORTED", 1: "INSUFFICIENT_EVIDENCE", 2: "CONTRADICTED"}

def extract_numbers(text: str) -> set[str]:
    devanagari_nums = {"०": "0", "१": "1", "२": "2", "३": "3", "४": "4", "५": "5", "६": "6", "७": "7", "८": "8", "९": "9"}
    norm_text = "".join(devanagari_nums.get(c, c) for c in text)
    return set(re.findall(r"\b\d+(?:[\.,]\d+)?\b", norm_text))

def compute_numeral_jaccard(orig_text: str, trans_text: str) -> float:
    orig_nums = extract_numbers(orig_text)
    trans_nums = extract_numbers(trans_text)
    union = orig_nums | trans_nums
    if not union:
        return 1.0  # No numerals in either text
    intersection = orig_nums & trans_nums
    return float(len(intersection) / len(union))

def compute_risk(probs_trans: np.ndarray, num_jaccard: float) -> float:
    max_p = float(np.max(probs_trans))
    num_mismatch = 1.0 - float(num_jaccard)
    return float(0.70 * (1.0 - max_p) + 0.30 * num_mismatch)

def mcnemar_exact(y_true, y_pred_a, y_pred_b):
    corr_a = (y_pred_a == y_true)
    corr_b = (y_pred_b == y_true)
    b = int(np.sum(corr_a & ~corr_b))
    c = int(np.sum(~corr_a & corr_b))
    n_disc = b + c
    if n_disc == 0:
        return 0.0, 1.0, b, c
    stat = float((abs(b - c) - 1.0)**2 / n_disc)
    p_val = float(min(1.0, 2.0 * stats.binom.cdf(min(b, c), n_disc, 0.5)))
    return stat, p_val, b, c

def paired_permutation_f1(y_true, y_pred_a, y_pred_b, labels, n_perm=5000, seed=42):
    rng = np.random.default_rng(seed)
    f1_a = f1_score(y_true, y_pred_a, labels=labels, average="macro", zero_division=0)
    f1_b = f1_score(y_true, y_pred_b, labels=labels, average="macro", zero_division=0)
    diff_obs = f1_a - f1_b
    n = len(y_true)
    diffs = []
    for _ in range(n_perm):
        swap = rng.choice([True, False], size=n)
        s_a = np.where(swap, y_pred_b, y_pred_a)
        s_b = np.where(swap, y_pred_a, y_pred_b)
        f1_sa = f1_score(y_true, s_a, labels=labels, average="macro", zero_division=0)
        f1_sb = f1_score(y_true, s_b, labels=labels, average="macro", zero_division=0)
        diffs.append(f1_sa - f1_sb)
    diffs = np.array(diffs)
    p_val = float(np.mean(np.abs(diffs) >= np.abs(diff_obs)))
    return float(diff_obs), p_val

def bootstrap_ci(y_true, y_pred, metric_fn, n_resamples=2000, seed=42, alpha=0.05):
    rng = np.random.default_rng(seed)
    n = len(y_true)
    scores = []
    for _ in range(n_resamples):
        idx = rng.choice(n, size=n, replace=True)
        scores.append(metric_fn(y_true[idx], y_pred[idx]))
    scores = np.array(scores)
    lo = float(np.percentile(scores, 100 * (alpha / 2.0)))
    hi = float(np.percentile(scores, 100 * (1.0 - alpha / 2.0)))
    return lo, hi

def fdr_bh(p_values: list[float]) -> list[float]:
    """Benjamini-Hochberg False Discovery Rate correction."""
    n = len(p_values)
    if n == 0:
        return []
    sorted_indices = np.argsort(p_values)
    sorted_p = np.array(p_values)[sorted_indices]
    adjusted = np.zeros(n)
    running_min = 1.0
    for i in range(n - 1, -1, -1):
        rank = i + 1
        adj = min(1.0, sorted_p[i] * n / rank)
        running_min = min(running_min, adj)
        adjusted[i] = running_min
    result = np.zeros(n)
    result[sorted_indices] = adjusted
    return [float(x) for x in result]

def run_dataset_inference(file_path: Path, mt_tok, mt_model, v_tok, v_model, device) -> pd.DataFrame:
    with open(file_path, "r", encoding="utf-8") as f:
        items = [json.loads(line) for line in f]

    print(f"\nExecuting canonical inference on {len(items)} items from {file_path.name}...")
    records = []

    # Warmup runs on dummy items to avoid JIT / memory initialization skewing instance 0 latency
    dummy_hi = "यह एक प्रारंभिक परीक्षण वाक्य है।"
    dummy_cl = "This is a warm-up sentence."
    for _ in range(2):
        w_inp = mt_tok(dummy_hi, return_tensors="pt", truncation=True, max_length=512).to(device)
        with torch.no_grad():
            w_out = mt_model.generate(**w_inp, max_length=512, num_beams=2)
            w_dec = mt_tok.decode(w_out[0], skip_special_tokens=True)
            w_v = v_tok(w_dec, dummy_cl, return_tensors="pt", truncation=True, max_length=512).to(device)
            _ = v_model(**w_v)

    for idx, item in enumerate(tqdm(items, desc=f"Inference {file_path.stem}")):
        claim = item["claim"]
        orig_ev = item["original_evidence"]
        gold = item["gold_label"]

        # 1. Fresh Machine Translation Pass (True token truncation max_length=512, no character slicing)
        mt_inp = mt_tok(orig_ev, return_tensors="pt", truncation=True, max_length=512).to(device)
        t_mt_0 = time.perf_counter()
        with torch.no_grad():
            gen_tokens = mt_model.generate(**mt_inp, max_length=512, num_beams=2)
        lat_mt = (time.perf_counter() - t_mt_0) * 1000.0

        # Exact decoded text generated by MT
        gen_trans_text = mt_tok.decode(gen_tokens[0], skip_special_tokens=True)

        # True Jaccard numeral overlap between original Hindi and exact generated translation
        num_jaccard = compute_numeral_jaccard(orig_ev, gen_trans_text)

        # 2. Translated Evidence Pass (Verifying the EXACT generated translation)
        inp_trans = v_tok(gen_trans_text, claim, return_tensors="pt", truncation=True, max_length=512).to(device)
        trans_tok_len = int(inp_trans.input_ids.shape[1])
        trans_trunc = int(trans_tok_len >= 512)

        t_trans_0 = time.perf_counter()
        with torch.no_grad():
            out_trans = v_model(**inp_trans)
            p_trans = torch.softmax(out_trans.logits, dim=-1)[0].cpu().numpy()
        lat_trans = (time.perf_counter() - t_trans_0) * 1000.0

        pred_trans = ID2LABEL[int(np.argmax(p_trans))]
        risk = compute_risk(p_trans, num_jaccard)

        # 3. Original Hindi Evidence Pass (Direct multilingual verification)
        inp_orig = v_tok(orig_ev, claim, return_tensors="pt", truncation=True, max_length=512).to(device)
        orig_tok_len = int(inp_orig.input_ids.shape[1])
        orig_trunc = int(orig_tok_len >= 512)

        t_orig_0 = time.perf_counter()
        with torch.no_grad():
            out_orig = v_model(**inp_orig)
            p_orig = torch.softmax(out_orig.logits, dim=-1)[0].cpu().numpy()
        lat_orig = (time.perf_counter() - t_orig_0) * 1000.0

        pred_orig = ID2LABEL[int(np.argmax(p_orig))]

        # 4. Dual Consensus (Always-Check posterior average)
        p_always = 0.5 * (p_trans + p_orig)
        pred_always = ID2LABEL[int(np.argmax(p_always))]

        records.append({
            "item_id": item["item_id"],
            "split": item["split"],
            "claim": claim,
            "original_evidence": orig_ev,
            "gen_translated_evidence": gen_trans_text,
            "gold_label": gold,
            "raw_gold_label": item.get("raw_gold_label", ""),
            "site": item.get("site", ""),
            # Token lengths and truncation flags
            "trans_token_length": trans_tok_len,
            "trans_is_truncated": trans_trunc,
            "orig_token_length": orig_tok_len,
            "orig_is_truncated": orig_trunc,
            # Latency (ms)
            "latency_mt_ms": round(lat_mt, 2),
            "latency_trans_ms": round(lat_trans, 2),
            "latency_orig_ms": round(lat_orig, 2),
            "latency_trans_e2e_ms": round(lat_mt + lat_trans, 2),
            "latency_orig_e2e_ms": round(lat_orig, 2),
            "latency_always_e2e_ms": round(lat_mt + lat_trans + lat_orig, 2),
            # Features and Risk
            "feature_number_jaccard": round(num_jaccard, 4),
            "risk_score": round(risk, 5),
            # Translated predictions
            "pred_translated": pred_trans,
            "p_trans_supp": round(float(p_trans[0]), 5),
            "p_trans_insuff": round(float(p_trans[1]), 5),
            "p_trans_contra": round(float(p_trans[2]), 5),
            "conf_translated": round(float(np.max(p_trans)), 5),
            # Original predictions
            "pred_original": pred_orig,
            "p_orig_supp": round(float(p_orig[0]), 5),
            "p_orig_insuff": round(float(p_orig[1]), 5),
            "p_orig_contra": round(float(p_orig[2]), 5),
            "conf_original": round(float(np.max(p_orig)), 5),
            # Always predictions
            "pred_always": pred_always,
            "p_always_supp": round(float(p_always[0]), 5),
            "p_always_insuff": round(float(p_always[1]), 5),
            "p_always_contra": round(float(p_always[2]), 5),
            "conf_always": round(float(np.max(p_always)), 5),
            # Flip indicator
            "label_flip_orig_vs_trans": int(pred_trans != pred_orig)
        })

    return pd.DataFrame(records)

def tune_tau_on_dev(dev_df: pd.DataFrame) -> float:
    """
    Mechanically select optimal operating threshold tau* on Dev split.
    Objective: J(tau) = Macro_F1_3cl - 0.15 * Coverage
    Grid: [0.10, 0.65] step 0.025
    Tie-breaking: Choose higher tau (lower coverage) if scores are tied.
    """
    grid = np.arange(0.10, 0.65001, 0.025)
    best_tau = 0.30
    best_score = -1.0
    best_cov = 1.0
    rows = []

    for tau in grid:
        tau_val = round(float(tau), 3)
        trig = dev_df["risk_score"] >= tau_val
        cov = float(trig.mean())
        pred_sel = np.where(trig, dev_df["pred_original"], dev_df["pred_translated"])
        f1_3 = float(f1_score(dev_df["gold_label"], pred_sel, labels=LABELS_3CL, average="macro", zero_division=0))
        f1_2 = float(f1_score(dev_df["gold_label"], pred_sel, labels=LABELS_2CL, average="macro", zero_division=0))
        score = f1_3 - 0.15 * cov
        rows.append({
            "tau": tau_val,
            "coverage": round(cov, 4),
            "macro_f1_3cl": round(f1_3, 4),
            "macro_f1_2cl": round(f1_2, 4),
            "tradeoff_score": round(score, 4)
        })
        if score > best_score or (abs(score - best_score) < 1e-6 and cov < best_cov):
            best_score = score
            best_tau = tau_val
            best_cov = cov

    tuning_df = pd.DataFrame(rows)
    tuning_df.to_csv(RES_DIR / "canonical_dev_tuning.csv", index=False)
    tuning_df.to_csv(RES_DIR / "corrected_dev_tuning.csv", index=False)
    print(f"\n[DEV TUNING] Selected tau* = {best_tau:.3f} (Tradeoff score: {best_score:.4f}, Dev coverage: {best_cov*100:.2f}%)")
    return float(best_tau)

def apply_selective_and_ablations(df: pd.DataFrame, tau: float) -> tuple[pd.DataFrame, pd.DataFrame]:
    df = df.copy()

    # 1. Main Selective-Check (Hard Routing)
    trig_sel = df["risk_score"] >= tau
    df["selective_triggered"] = trig_sel.astype(int)
    df["pred_selective"] = np.where(trig_sel, df["pred_original"], df["pred_translated"])
    df["latency_selective_e2e_ms"] = np.where(
        trig_sel,
        df["latency_always_e2e_ms"],
        df["latency_trans_e2e_ms"]
    )

    cov_target = float(trig_sel.mean())
    n_items = len(df)
    k_items = int(round(cov_target * n_items))

    # 2. Ablation: Triggered Posterior Averaging
    p_trans = df[["p_trans_supp", "p_trans_insuff", "p_trans_contra"]].values
    p_orig = df[["p_orig_supp", "p_orig_insuff", "p_orig_contra"]].values
    p_avg = 0.5 * (p_trans + p_orig)
    pred_avg = [LABELS_3CL[i] for i in np.argmax(p_avg, axis=1)]
    df["pred_ablation_triggered_avg"] = np.where(trig_sel, pred_avg, df["pred_translated"])

    # 3. Ablation: Uncertainty-Only Routing (Exact matched coverage count)
    uncert = 1.0 - df["conf_translated"].values
    if k_items > 0:
        top_k_threshold = np.partition(uncert, n_items - k_items)[n_items - k_items]
        trig_u = np.zeros(n_items, dtype=bool)
        top_k_indices = np.argsort(uncert)[::-1][:k_items]
        trig_u[top_k_indices] = True
    else:
        trig_u = np.zeros(n_items, dtype=bool)
    df["pred_ablation_uncertainty_only"] = np.where(trig_u, df["pred_original"], df["pred_translated"])

    # 4. Ablation: Numeral-Only Routing (trigger if Jaccard < 1.0)
    trig_num = df["feature_number_jaccard"] < 1.0
    df["pred_ablation_numeral_only"] = np.where(trig_num, df["pred_original"], df["pred_translated"])

    # 5. Control: Multi-Seed Random Routing across 100 seeds (s=0..99) with exact matched item count k_items
    random_eval_records = []
    yt = df["gold_label"].values
    for s in range(100):
        rng = np.random.default_rng(s)
        rand_idx = rng.choice(n_items, size=k_items, replace=False)
        r_trig = np.zeros(n_items, dtype=bool)
        r_trig[rand_idx] = True
        r_pred = np.where(r_trig, df["pred_original"].values, df["pred_translated"].values)
        r_acc = accuracy_score(yt, r_pred)
        r_f1_3 = f1_score(yt, r_pred, labels=LABELS_3CL, average="macro", zero_division=0)
        r_f1_2 = f1_score(yt, r_pred, labels=LABELS_2CL, average="macro", zero_division=0)
        random_eval_records.append({
            "seed": s,
            "k_triggered": k_items,
            "coverage_pct": round(cov_target * 100.0, 2),
            "accuracy": r_acc,
            "macro_f1_3cl": r_f1_3,
            "macro_f1_2cl": r_f1_2
        })

    random_df = pd.DataFrame(random_eval_records)
    random_df.to_csv(RES_DIR / "canonical_random_control_100seeds.csv", index=False)

    # Attach seed 42 as representative deterministic column in the dataframe
    rng_repr = np.random.default_rng(42)
    repr_idx = rng_repr.choice(n_items, size=k_items, replace=False)
    repr_trig = np.zeros(n_items, dtype=bool)
    repr_trig[repr_idx] = True
    df["pred_control_random_routing"] = np.where(repr_trig, df["pred_original"], df["pred_translated"])

    # 6. Non-deployable Oracle Upper Bound
    po = df["pred_original"].values
    pt = df["pred_translated"].values
    oracle = np.where(po == yt, po, pt)
    df["pred_oracle_upper_bound"] = oracle

    return df, random_df

def generate_evaluation_deliverables(test_df: pd.DataFrame, random_df: pd.DataFrame, tau_star: float):
    yt = test_df["gold_label"].to_numpy()
    cov_sel = float(test_df["selective_triggered"].mean() * 100.0)

    # Multi-seed random summary statistics
    rand_acc_mean = float(random_df["accuracy"].mean())
    rand_acc_sd = float(random_df["accuracy"].std())
    rand_acc_p025 = float(np.percentile(random_df["accuracy"], 2.5))
    rand_acc_p975 = float(np.percentile(random_df["accuracy"], 97.5))

    rand_f1_3_mean = float(random_df["macro_f1_3cl"].mean())
    rand_f1_3_sd = float(random_df["macro_f1_3cl"].std())
    rand_f1_3_p025 = float(np.percentile(random_df["macro_f1_3cl"], 2.5))
    rand_f1_3_p975 = float(np.percentile(random_df["macro_f1_3cl"], 97.5))

    rand_f1_2_mean = float(random_df["macro_f1_2cl"].mean())
    rand_f1_2_sd = float(random_df["macro_f1_2cl"].std())
    rand_f1_2_p025 = float(np.percentile(random_df["macro_f1_2cl"], 2.5))
    rand_f1_2_p975 = float(np.percentile(random_df["macro_f1_2cl"], 97.5))

    systems = [
        ("No-Check (Translated Only)", "pred_translated", test_df["latency_trans_e2e_ms"].to_numpy(), 0.0),
        ("Direct Multilingual (Original Only)", "pred_original", test_df["latency_orig_e2e_ms"].to_numpy(), 100.0),
        ("Always-Check (Dual Consensus Avg)", "pred_always", test_df["latency_always_e2e_ms"].to_numpy(), 100.0),
        ("Selective-Check (Ours, Hard Route)", "pred_selective", test_df["latency_selective_e2e_ms"].to_numpy(), cov_sel),
        ("Ablation: Triggered Post. Averaging", "pred_ablation_triggered_avg", test_df["latency_selective_e2e_ms"].to_numpy(), cov_sel),
        ("Ablation: Uncertainty-Only Routing", "pred_ablation_uncertainty_only", test_df["latency_selective_e2e_ms"].to_numpy(), cov_sel),
        ("Ablation: Numeral-Only Routing", "pred_ablation_numeral_only", test_df["latency_selective_e2e_ms"].to_numpy(), float((test_df["feature_number_jaccard"] < 1.0).mean() * 100.0)),
        ("Control: Random Routing (100 Seeds)", "pred_control_random_routing", test_df["latency_selective_e2e_ms"].to_numpy(), cov_sel),
        ("Oracle Upper Bound (Non-Deployable)", "pred_oracle_upper_bound", test_df["latency_always_e2e_ms"].to_numpy(), 100.0)
    ]

    bench_rows = []
    stat_rows = []
    sel_preds = test_df["pred_selective"].to_numpy()

    acc_fn = lambda y_t, y_p: accuracy_score(y_t, y_p)
    f1_3_fn = lambda y_t, y_p: f1_score(y_t, y_p, labels=LABELS_3CL, average="macro", zero_division=0)
    f1_2_fn = lambda y_t, y_p: f1_score(y_t, y_p, labels=LABELS_2CL, average="macro", zero_division=0)

    for name, col, lats, cov in systems:
        yp = test_df[col].to_numpy()
        acc = float(accuracy_score(yt, yp))
        f1_3 = float(f1_score(yt, yp, labels=LABELS_3CL, average="macro", zero_division=0))
        f1_2 = float(f1_score(yt, yp, labels=LABELS_2CL, average="macro", zero_division=0))

        if name == "Control: Random Routing (100 Seeds)":
            acc_disp = round(rand_acc_mean, 4)
            acc_ci_disp = f"[{rand_acc_p025:.4f}, {rand_acc_p975:.4f}]"
            f1_3_disp = round(rand_f1_3_mean, 4)
            f1_3_ci_disp = f"[{rand_f1_3_p025:.4f}, {rand_f1_3_p975:.4f}]"
            f1_2_disp = round(rand_f1_2_mean, 4)
            f1_2_ci_disp = f"[{rand_f1_2_p025:.4f}, {rand_f1_2_p975:.4f}]"
        else:
            acc_lo, acc_hi = bootstrap_ci(yt, yp, acc_fn)
            f1_3_lo, f1_3_hi = bootstrap_ci(yt, yp, f1_3_fn)
            f1_2_lo, f1_2_hi = bootstrap_ci(yt, yp, f1_2_fn)
            acc_disp = round(acc, 4)
            acc_ci_disp = f"[{acc_lo:.4f}, {acc_hi:.4f}]"
            f1_3_disp = round(f1_3, 4)
            f1_3_ci_disp = f"[{f1_3_lo:.4f}, {f1_3_hi:.4f}]"
            f1_2_disp = round(f1_2, 4)
            f1_2_ci_disp = f"[{f1_2_lo:.4f}, {f1_2_hi:.4f}]"

        bench_rows.append({
            "System / Ablation": name,
            "Accuracy": acc_disp,
            "Acc_95_CI": acc_ci_disp,
            "Macro_F1_3cl": f1_3_disp,
            "F1_3cl_95_CI": f1_3_ci_disp,
            "Macro_F1_2cl": f1_2_disp,
            "F1_2cl_95_CI": f1_2_ci_disp,
            "Coverage_Pct": round(cov, 1),
            "Mean_E2E_Latency_ms": round(float(np.mean(lats)), 1),
            "Median_E2E_Latency_ms": round(float(np.median(lats)), 1),
            "P95_E2E_Latency_ms": round(float(np.percentile(lats, 95)), 1)
        })

        if name != "Selective-Check (Ours, Hard Route)":
            mcn_stat, mcn_p, b, c = mcnemar_exact(yt, sel_preds, yp)
            diff_3, perm_p3 = paired_permutation_f1(yt, sel_preds, yp, LABELS_3CL)
            diff_2, perm_p2 = paired_permutation_f1(yt, sel_preds, yp, LABELS_2CL)
            stat_rows.append({
                "Comparison": f"Selective-Check vs. {name}",
                "McNemar_Stat": round(mcn_stat, 4),
                "McNemar_p_val_raw": round(mcn_p, 5),
                "Selective_Correct_Other_Wrong (b)": b,
                "Selective_Wrong_Other_Correct (c)": c,
                "Delta_Macro_F1_3cl": round(diff_3, 4),
                "Permutation_p_val_3cl_raw": round(perm_p3, 5),
                "Delta_Macro_F1_2cl": round(diff_2, 4),
                "Permutation_p_val_2cl_raw": round(perm_p2, 5)
            })

    # Apply Benjamini-Hochberg FDR correction across pairwise comparisons
    mcn_raw = [r["McNemar_p_val_raw"] for r in stat_rows]
    perm3_raw = [r["Permutation_p_val_3cl_raw"] for r in stat_rows]
    perm2_raw = [r["Permutation_p_val_2cl_raw"] for r in stat_rows]

    mcn_fdr = fdr_bh(mcn_raw)
    perm3_fdr = fdr_bh(perm3_raw)
    perm2_fdr = fdr_bh(perm2_raw)

    for i in range(len(stat_rows)):
        stat_rows[i]["McNemar_p_val_fdr"] = round(mcn_fdr[i], 5)
        stat_rows[i]["Permutation_p_val_3cl_fdr"] = round(perm3_fdr[i], 5)
        stat_rows[i]["Permutation_p_val_2cl_fdr"] = round(perm2_fdr[i], 5)

    bench_df = pd.DataFrame(bench_rows)
    bench_df.to_csv(RES_DIR / "canonical_benchmark_table.csv", index=False)
    bench_df.to_csv(RES_DIR / "corrected_full_benchmark_and_ablations.csv", index=False)

    stat_df = pd.DataFrame(stat_rows)
    stat_df.to_csv(RES_DIR / "canonical_statistical_tests.csv", index=False)
    stat_df.to_csv(RES_DIR / "corrected_statistical_tests.csv", index=False)

    # Diagnostic Outcome Strata (Neutral diagnostic categories under representation shift)
    corr_trans = (test_df["pred_translated"].to_numpy() == yt)
    corr_orig = (test_df["pred_original"].to_numpy() == yt)

    s_control = int(np.sum(corr_trans & corr_orig))
    s_recovered = int(np.sum(~corr_trans & corr_orig))  # E_trans stratum
    s_unrecovered = int(np.sum(~corr_trans & ~corr_orig))  # E_verif stratum
    s_degraded = int(np.sum(corr_trans & ~corr_orig))

    strata_report = {
        "dataset": "X-Fact Hindi Exploratory Test Split",
        "n_total": len(yt),
        "tau_star": tau_star,
        "n_translated_failures": int(np.sum(~corr_trans)),
        "stratum_both_correct_control": s_control,
        "stratum_recovered_by_original": s_recovered,
        "stratum_unrecovered_both_wrong": s_unrecovered,
        "stratum_degraded_by_original": s_degraded,
        "recovered_pct_of_failures": round(s_recovered / max(1, np.sum(~corr_trans)) * 100.0, 2),
        "unrecovered_pct_of_failures": round(s_unrecovered / max(1, np.sum(~corr_trans)) * 100.0, 2)
    }
    with open(RES_DIR / "canonical_error_attribution.json", "w", encoding="utf-8") as f:
        json.dump(strata_report, f, indent=2)
    with open(RES_DIR / "corrected_error_attribution.json", "w", encoding="utf-8") as f:
        json.dump(strata_report, f, indent=2)

    # Latency Summary JSON
    lat_summary = {
        "device": "CPU",
        "cpu_threads": torch.get_num_threads(),
        "mt_model": MODEL_MT,
        "verifier_model": MODEL_VERIFIER,
        "per_instance_measured": True,
        "warmup_executed": True,
        "mean_latency_mt_ms": round(float(test_df["latency_mt_ms"].mean()), 2),
        "median_latency_mt_ms": round(float(test_df["latency_mt_ms"].median()), 2),
        "mean_latency_trans_verifier_ms": round(float(test_df["latency_trans_ms"].mean()), 2),
        "mean_latency_orig_verifier_ms": round(float(test_df["latency_orig_ms"].mean()), 2),
        "mean_latency_trans_e2e_ms": round(float(test_df["latency_trans_e2e_ms"].mean()), 2),
        "mean_latency_orig_e2e_ms": round(float(test_df["latency_orig_e2e_ms"].mean()), 2),
        "mean_latency_always_e2e_ms": round(float(test_df["latency_always_e2e_ms"].mean()), 2),
        "mean_latency_selective_e2e_ms": round(float(test_df["latency_selective_e2e_ms"].mean()), 2)
    }
    with open(RES_DIR / "canonical_latency_summary.json", "w", encoding="utf-8") as f:
        json.dump(lat_summary, f, indent=2)
    with open(RES_DIR / "corrected_latency_summary.json", "w", encoding="utf-8") as f:
        json.dump(lat_summary, f, indent=2)

    print("\n=== CANONICAL BENCHMARK TABLE ===")
    print(bench_df.to_string())

    print("\n=== CANONICAL STATISTICAL SIGNIFICANCE TESTS (WITH FDR CORRECTION) ===")
    print(stat_df.to_string())

def main():
    torch.set_num_threads(8)
    device = torch.device("cpu")
    print(f"Hardware: CPU ({torch.get_num_threads()} threads)")
    print(f"Loading MT model: {MODEL_MT}...")
    mt_tok = AutoTokenizer.from_pretrained(MODEL_MT)
    mt_model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_MT).to(device)
    mt_model.eval()

    print(f"Loading Verifier model: {MODEL_VERIFIER}...")
    v_tok = AutoTokenizer.from_pretrained(MODEL_VERIFIER)
    v_model = AutoModelForSequenceClassification.from_pretrained(MODEL_VERIFIER).to(device)
    v_model.eval()

    # Step 1: Run Dev Inference
    dev_path = WORKSPACE / "data" / "processed" / "dev_translated.jsonl"
    dev_df = run_dataset_inference(dev_path, mt_tok, mt_model, v_tok, v_model, device)

    # Step 2: Tune Tau exclusively on Dev
    tau_star = tune_tau_on_dev(dev_df)
    dev_df, dev_random_df = apply_selective_and_ablations(dev_df, tau_star)
    dev_df.to_csv(RES_DIR / "canonical_dev_predictions.csv", index=False)
    dev_df.to_csv(RES_DIR / "corrected_dev_predictions.csv", index=False)
    print(f"Saved Dev predictions to {RES_DIR / 'canonical_dev_predictions.csv'}")

    # Step 3: Run Test Inference (Exploratory evaluation with frozen tau*)
    test_path = WORKSPACE / "data" / "processed" / "test_translated.jsonl"
    test_df = run_dataset_inference(test_path, mt_tok, mt_model, v_tok, v_model, device)
    test_df, test_random_df = apply_selective_and_ablations(test_df, tau_star)

    # Programmatic assertion: verify every row matches threshold logic
    assert (test_df["selective_triggered"] == (test_df["risk_score"] >= tau_star)).all(), \
        "Integrity failure: test selective trigger does not match risk >= tau_star!"

    test_df.to_csv(RES_DIR / "canonical_test_predictions.csv", index=False)
    test_df.to_csv(RES_DIR / "corrected_test_predictions.csv", index=False)
    print(f"Saved Test predictions to {RES_DIR / 'canonical_test_predictions.csv'}")

    # Step 4: Generate All Deliverables
    generate_evaluation_deliverables(test_df, test_random_df, tau_star)
    print("\nCanonical experiment pipeline completed successfully.")

if __name__ == "__main__":
    main()
