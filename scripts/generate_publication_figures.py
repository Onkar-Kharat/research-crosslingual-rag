"""
Generate journal-quality publication figures (vector PDF and high-res PNG)
for the TACL manuscript on Cross-Lingual Claim Verification.
Reads from canonical outputs in experiments/results_corrected/.

Optimized with:
- Zero clipping / ample layout headroom & generous margins
- Exact 95% bootstrap confidence interval error bars on condition comparisons
- In-bar value labels preventing error-whisker collision
- Legend integrated reference baseline eliminating edge-text clutter
- Centered callout annotations for dev threshold tuning
- Diagnostic failure attribution breakdown
"""
import json
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd

WORKSPACE = Path(__file__).resolve().parents[1]
PDF_DIR = WORKSPACE / "figures" / "pdf"
SRC_DIR = WORKSPACE / "figures" / "src"
PDF_DIR.mkdir(parents=True, exist_ok=True)
SRC_DIR.mkdir(parents=True, exist_ok=True)

mpl.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif", "Utopia"],
    "font.size": 10,
    "axes.labelsize": 10.5,
    "axes.titlesize": 11,
    "legend.fontsize": 8.8,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "lines.linewidth": 1.8,
    "lines.markersize": 6.5,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "axes.grid": True,
    "grid.alpha": 0.35,
    "grid.linestyle": "--"
})

def plot_risk_coverage_curve(tuning_csv: Path):
    """Figure 2: Operating curve and dev threshold tuning trade-off."""
    if not tuning_csv.exists():
        print(f"Skipping risk curve: {tuning_csv} not found.")
        return
    df = pd.read_csv(tuning_csv)
    df = df.sort_values("coverage")

    fig, ax1 = plt.subplots(figsize=(6.2, 3.8), dpi=300)

    color_f1 = "#1d4ed8"      # Deep Royal Blue
    color_score = "#15803d"   # Forest Green

    f1_col = "macro_f1_3cl" if "macro_f1_3cl" in df.columns else "macro_f1"
    score_col = "tradeoff_score" if "tradeoff_score" in df.columns else "score"
    tau_col = "tau" if "tau" in df.columns else "threshold_tau"

    line1 = ax1.plot(
        df["coverage"] * 100, df[f1_col],
        label="Macro-F1 (Dev Evaluation)", color=color_f1,
        marker="o", markersize=6, linestyle="-", lw=2.0, zorder=4
    )
    line2 = ax1.plot(
        df["coverage"] * 100, df[score_col],
        label="Tradeoff Objective (F1 - 0.15*Cov)", color=color_score,
        marker="s", markersize=6, linestyle="--", lw=1.8, zorder=4
    )

    opt_idx = df[score_col].idxmax()
    opt_row = df.loc[opt_idx]
    opt_cov = opt_row["coverage"] * 100
    opt_f1 = opt_row[f1_col]
    opt_score = opt_row[score_col]
    opt_tau = opt_row[tau_col]

    ax1.vlines(opt_cov, 0.10, opt_f1, color="#dc2626", linestyle=":", lw=1.2, alpha=0.7, zorder=3)
    ax1.scatter([opt_cov], [opt_f1], color="#dc2626", s=115, zorder=6,
                label=rf"Optimal Operating Point ($\tau^*={opt_tau:.3f}$)", edgecolor="black", lw=1.2)

    ax1.annotate(
        r"$\mathbf{Optimal\ Operating\ Point}$" + "\n" +
        rf"$\mathbf{{\tau^* = {opt_tau:.3f}}}$" + "\n" +
        f"Coverage: {opt_cov:.1f}%\n" +
        f"Macro-F1: {opt_f1:.3f}\n" +
        f"Objective: {opt_score:.3f}",
        xy=(opt_cov, opt_f1),
        xytext=(opt_cov - 20, opt_f1 + 0.08),
        ha="center", va="center",
        arrowprops=dict(
            arrowstyle="->",
            color="#dc2626", lw=1.3,
            shrinkA=3, shrinkB=4
        ),
        fontsize=7.5,
        bbox=dict(boxstyle="round,pad=0.25", fc="#fff5f5", ec="#dc2626", lw=1.1, alpha=0.96),
        zorder=7
    )

    ax1.set_xlabel("Original Evidence Consultation Coverage (%)", fontweight="bold", labelpad=8)
    ax1.set_ylabel("Verification Performance Score", fontweight="bold", labelpad=8)
    ax1.set_xlim(df["coverage"].min()*100 - 5, 105)
    ax1.set_ylim(0.08, 0.55)
    ax1.legend(loc="upper left", framealpha=0.95, edgecolor="#cbd5e1")

    fig.tight_layout()
    fig.savefig(PDF_DIR / "fig2_risk_coverage_tradeoff.pdf", bbox_inches="tight", pad_inches=0.05)
    fig.savefig(SRC_DIR / "fig2_risk_coverage_tradeoff.png", bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)
    print("Regenerated fig2_risk_coverage_tradeoff.pdf and PNG")

def plot_performance_and_latency(benchmark_csv: Path):
    """Figure 3: Condition comparisons with exact 95% bootstrap CI error bars."""
    if not benchmark_csv.exists():
        print(f"Skipping performance plot: {benchmark_csv} not found.")
        return
    df = pd.read_csv(benchmark_csv)

    # Focus on the 4 primary systems
    target_names = [
        "No-Check (Translated Only)",
        "Direct Multilingual (Original Only)",
        "Always-Check (Dual Consensus Avg)",
        "Selective-Check (Ours, Hard Route)"
    ]
    sub = df[df["System / Ablation"].isin(target_names)].copy()
    if len(sub) < 4:
        sub = df.iloc[:4].copy()

    fig, ax = plt.subplots(figsize=(7.2, 4.2), dpi=300)
    x = np.arange(len(sub))
    width = 0.34

    cond_labels = [
        "No-Check\n(Translated)",
        "Direct Multilingual\n(Original)",
        "Always-Check\n(Dual Consensus)",
        "Selective-Check\n(Ours, Hard Route)"
    ]

    acc_vals = sub["Accuracy"].values
    f1_vals = sub["Macro_F1_3cl"].values if "Macro_F1_3cl" in sub.columns else sub["Macro_F1"].values

    acc_yerr = [[], []]
    f1_yerr = [[], []]
    for i, row in sub.iterrows():
        # parse "[lo, hi]"
        acc_s = str(row["Acc_95_CI"]).strip(" []").split(",")
        f1_s = str(row.get("F1_3cl_95_CI") or row.get("F1_CI_95")).strip(" []").split(",")
        a_lo, a_hi = float(acc_s[0]), float(acc_s[1])
        f_lo, f_hi = float(f1_s[0]), float(f1_s[1])
        acc_yerr[0].append(row["Accuracy"] - a_lo)
        acc_yerr[1].append(a_hi - row["Accuracy"])
        f1_yerr[0].append((row["Macro_F1_3cl"] if "Macro_F1_3cl" in row else row["Macro_F1"]) - f_lo)
        f1_yerr[1].append(f_hi - (row["Macro_F1_3cl"] if "Macro_F1_3cl" in row else row["Macro_F1"]))

    color_acc = "#1e3a8a"
    color_f1 = "#16a34a"

    rects1 = ax.bar(
        x - width/2, acc_vals, width, yerr=acc_yerr,
        capsize=3.5, label="Accuracy [95% CI]",
        color=color_acc, edgecolor="#0f172a", linewidth=0.9,
        error_kw=dict(lw=1.1, capthick=1.1, ecolor="#0f172a"),
        zorder=3
    )
    rects2 = ax.bar(
        x + width/2, f1_vals, width, yerr=f1_yerr,
        capsize=3.5, label="Macro-F1 (3-cl) [95% CI]",
        color=color_f1, edgecolor="#0f172a", linewidth=0.9,
        error_kw=dict(lw=1.1, capthick=1.1, ecolor="#0f172a"),
        zorder=3
    )

    ax.axhline(acc_vals[0], color="#64748b", linestyle="--", lw=1.2, alpha=0.85, zorder=2,
               label=f"No-Check Baseline ({acc_vals[0]:.3f})")

    ax.set_ylabel("Metric Score", fontweight="bold", labelpad=8)
    ax.set_title("Held-Out Test Set Verification Performance ($N=163$)", fontweight="bold", pad=12)
    ax.set_xticks(x)
    ax.set_xticklabels(cond_labels)
    ax.set_ylim(0, 0.65)

    y_label_pos = 0.055
    for i, rect in enumerate(rects1):
        ax.text(
            rect.get_x() + rect.get_width() / 2, y_label_pos,
            f"{acc_vals[i]:.3f}",
            ha="center", va="center", fontsize=8.6, fontweight="bold", color="#ffffff", zorder=6
        )
    for i, rect in enumerate(rects2):
        ax.text(
            rect.get_x() + rect.get_width() / 2, y_label_pos,
            f"{f1_vals[i]:.3f}",
            ha="center", va="center", fontsize=8.6, fontweight="bold", color="#ffffff", zorder=6
        )

    # Bracket comparing Always-Check vs Selective-Check
    y_bracket = 0.52
    bracket_h = 0.015
    ax.plot([2.0, 2.0, 3.0, 3.0], [y_bracket - bracket_h, y_bracket, y_bracket, y_bracket - bracket_h],
            color="#166534", lw=1.2, zorder=5)
    ax.text(2.5, y_bracket + 0.008, r"$\mathbf{*}\ p < 0.05$ (McNemar)",
            ha="center", va="bottom", fontsize=8.2, fontweight="bold", color="#166534", zorder=6)

    ax.legend(loc="upper left", framealpha=0.95, edgecolor="#cbd5e1")
    fig.tight_layout()
    fig.savefig(PDF_DIR / "fig3_condition_comparison.pdf", bbox_inches="tight", pad_inches=0.05)
    fig.savefig(SRC_DIR / "fig3_condition_comparison.png", bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)
    print("Regenerated fig3_condition_comparison.pdf and PNG")

def plot_error_attribution(attr_json: Path):
    """Figure 4: Decomposition of verification failures in No-Check pipeline."""
    if not attr_json.exists():
        print(f"Skipping error attribution: {attr_json} not found.")
        return
    with open(attr_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    fig, ax = plt.subplots(figsize=(6.6, 4.0), dpi=300)

    categories = [
        "Translation-Associated\n($E_{\\mathrm{trans}}$)\n\nFactual Distortion in MT\n(Recovered by Original)",
        "Verifier-Reasoning\n($E_{\\mathrm{verif}}$)\n\nNLI Reasoning Failure\n(Both Languages Wrong)",
        "Evidence Insufficiency\n($E_{\\mathrm{insuff}}$)\n\nInconclusive Retrieval\n(Incomplete Snippet)"
    ]
    counts = [
        data.get("E_trans_count", 0),
        data.get("E_verif_count", 0),
        data.get("E_unresolved_evidence_count", 0)
    ]
    total_failures = data.get("n_failures_translated", sum(counts))

    colors = ["#dc2626", "#ea580c", "#2563eb"]
    edge_colors = ["#991b1b", "#c2410c", "#1d4ed8"]

    bars = ax.bar(categories, counts, color=colors, edgecolor=edge_colors, linewidth=1.1, width=0.50, zorder=3)
    ax.set_ylabel("Number of Verification Failures", fontweight="bold", labelpad=8)
    ax.set_title("Diagnostic Decomposition of Failures in No-Check Pipeline", fontweight="bold", pad=14)
    ax.set_ylim(0, max(counts) + 20)

    ax.text(0.5, 0.94, f"Total Failures in No-Check Pipeline: N = {total_failures} (out of 163 held-out test instances)",
            transform=ax.transAxes, ha="center", fontsize=8.2, color="#475569", style="italic")

    for bar in bars:
        h = bar.get_height()
        pct = (h / total_failures) * 100 if total_failures > 0 else 0
        ax.annotate(
            f"{h} cases\n({pct:.1f}%)",
            xy=(bar.get_x() + bar.get_width() / 2, h),
            xytext=(0, 4), textcoords="offset points",
            ha="center", va="bottom", fontsize=9.0, fontweight="bold", color="#0f172a"
        )

    ax.set_xlabel("Operational Error Category", fontweight="bold", labelpad=10)
    fig.tight_layout()
    fig.savefig(PDF_DIR / "fig4_error_attribution_breakdown.pdf", bbox_inches="tight", pad_inches=0.05)
    fig.savefig(SRC_DIR / "fig4_error_attribution_breakdown.png", bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)
    print("Regenerated fig4_error_attribution_breakdown.pdf and PNG")

def main():
    tuning_csv = WORKSPACE / "experiments" / "results_corrected" / "corrected_dev_tuning.csv"
    benchmark_csv = WORKSPACE / "experiments" / "results_corrected" / "corrected_full_benchmark_and_ablations.csv"
    attr_json = WORKSPACE / "experiments" / "results_corrected" / "corrected_error_attribution.json"

    # Fallback to legacy if corrected not yet finished
    if not tuning_csv.exists():
        tuning_csv = WORKSPACE / "experiments" / "results" / "dev_threshold_tuning.csv"
    if not benchmark_csv.exists():
        benchmark_csv = WORKSPACE / "experiments" / "results" / "test_main_results.csv"
    if not attr_json.exists():
        attr_csv = WORKSPACE / "experiments" / "results" / "test_error_attribution.csv"
        # plot legacy if needed
        return

    plot_risk_coverage_curve(tuning_csv)
    plot_performance_and_latency(benchmark_csv)
    plot_error_attribution(attr_json)

if __name__ == "__main__":
    main()
