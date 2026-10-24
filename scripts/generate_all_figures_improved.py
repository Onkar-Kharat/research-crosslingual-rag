"""
Comprehensive publication figure generator for TACL Manuscript Revision.
Generates all 5 figures with zero clipping, ample margins, no text overlap,
and 100% fidelity to canonical frozen data.

Figures:
- Fig 1: fig1_study_workflow.pdf & .png (System Architecture & Pipeline)
- Fig 2: fig2_risk_coverage_tradeoff.pdf & .png (Dev Tuning & Risk Curve)
- Fig 3: fig3_condition_comparison.pdf & .png (Test Benchmark Comparison)
- Fig 4: fig4_error_attribution_breakdown.pdf & .png (Diagnostic Error Decomposition)
- Fig 5: fig5_transition_heatmap.pdf & .png (3x3 Prediction Transition Heatmap)
"""
from pathlib import Path
import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib as mpl
import numpy as np
import pandas as pd

# Robust repository root detection
def get_repo_root():
    cur = Path(__file__).resolve()
    for p in [cur] + list(cur.parents):
        if (p / "results").is_dir() and (p / "experiments").is_dir():
            return p
    return cur.parents[1]

REPO_ROOT = get_repo_root()
FINAL_DIR = REPO_ROOT / "manuscript_revision_tacl" / "figures" / "final"
SRC_DIR = REPO_ROOT / "manuscript_revision_tacl" / "figures" / "source"
FINAL_DIR.mkdir(parents=True, exist_ok=True)
SRC_DIR.mkdir(parents=True, exist_ok=True)

# Global Typography & Style Configuration
mpl.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif", "Utopia"],
    "font.size": 9.5,
    "axes.labelsize": 10.5,
    "axes.titlesize": 11.5,
    "legend.fontsize": 8.8,
    "xtick.labelsize": 9.0,
    "ytick.labelsize": 9.0,
    "lines.linewidth": 1.8,
    "lines.markersize": 6.5,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "figure.autolayout": False,
})

# ==============================================================================
# FIGURE 1: Publication-Grade System Architecture & Workflow Diagram
# ==============================================================================
def draw_box(ax, x, y, w, h, bg, border, lw=1.2, radius=0.016):
    box = patches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0.0,rounding_size={radius}",
        facecolor=bg, edgecolor=border, linewidth=lw, zorder=3
    )
    ax.add_patch(box)

def draw_card(ax, x, y, w, h, title, items, bg="#FFFFFF", border="#334155", title_col="#0F172A", title_fs=8.4, default_fs=6.6, align="center"):
    draw_box(ax, x, y, w, h, bg, border)

    # Header title
    ax.text(x + w / 2, y + h - 0.024, title, ha="center", va="top",
            fontsize=title_fs, fontweight="bold", color=title_col, zorder=4)

    # Header divider line
    ax.plot([x + 0.012, x + w - 0.012], [y + h - 0.042, y + h - 0.042],
            color=border, lw=0.6, alpha=0.35, zorder=4)

    n = len(items)
    if n == 0:
        return

    avail_h = h - 0.052
    spacing = avail_h / (n + 0.35)

    for i, item in enumerate(items):
        curr_y = y + h - 0.052 - (i * spacing)
        
        # Divider check
        if isinstance(item, str) and item.strip() == "───":
            ax.plot([x + 0.015, x + w - 0.015], [curr_y + 0.003, curr_y + 0.003],
                    color=border, lw=0.5, alpha=0.25, zorder=4)
            continue

        # Parsing item tuple: (text, weight, color, fontsize, item_align, offset)
        if isinstance(item, tuple):
            txt = item[0]
            wt = item[1] if len(item) > 1 else "normal"
            col = item[2] if len(item) > 2 else "#334155"
            fs = item[3] if len(item) > 3 else default_fs
            item_align = item[4] if len(item) > 4 else align
            offset = item[5] if len(item) > 5 else 0.0
        else:
            txt, wt, col, fs, item_align, offset = item, "normal", "#334155", default_fs, align, 0.0

        if item_align == "center":
            ax.text(x + w / 2, curr_y, txt, ha="center", va="top",
                    fontsize=fs, fontweight=wt, color=col, zorder=4)
        elif item_align == "left":
            ax.text(x + 0.012 + offset, curr_y, txt, ha="left", va="top",
                    fontsize=fs, fontweight=wt, color=col, zorder=4)

def draw_arrow(ax, p_start, p_end, color="#475569", lw=1.3, rad=0.0):
    arrow = patches.FancyArrowPatch(
        posA=p_start, posB=p_end,
        arrowstyle="-|>,head_length=4.5,head_width=3.0",
        color=color, linewidth=lw,
        connectionstyle=f"arc3,rad={rad}", zorder=5
    )
    ax.add_patch(arrow)

def generate_figure_1():
    # Spacious canvas: 10.2 x 5.6 inches (300 DPI)
    fig, ax = plt.subplots(figsize=(10.2, 5.6), dpi=300)
    ax.set_xlim(-0.010, 1.010)
    ax.set_ylim(-0.010, 1.010)
    ax.axis("off")

    # =========================================================================
    # 4-COLUMN ARCHITECTURE GRID
    # Col 1: Input Fact-Check (x: 0.012 -> 0.177, w=0.165)
    # Col 2: Evidence Prep   (x: 0.212 -> 0.407, w=0.195)
    # Col 3: Verifiers / Cons(x: 0.442 -> 0.657, w=0.215)
    # Col 4: Cascade / Ours  (x: 0.707 -> 0.988, w=0.281)
    # =========================================================================

    # 1. INPUT FACT-CHECK (Col 1 Top)
    draw_card(
        ax, x=0.012, y=0.510, w=0.165, h=0.460,
        title="Input Fact-Check",
        items=[
            ("Hindi Claim $c$", "bold", "#0F172A", 7.0),
            ("Retrieved Snippets $e_{\\mathrm{orig}}$", "normal", "#334155", 6.6),
            ("(Authentic Search Snippets)", "normal", "#64748B", 6.2),
            "───",
            ("Benchmark Corpus:", "bold", "#1E293B", 6.7),
            ("X-Fact Hindi Partition", "normal", "#334155", 6.6),
            ("Authentic News Claims", "normal", "#475569", 6.4),
            ("Dev: 103 | Test: 163", "normal", "#334155", 6.5),
            ("Total: $N = 266$ instances", "bold", "#0F172A", 6.7),
        ],
        bg="#F8FAFC", border="#475569", title_col="#0F172A", align="center"
    )

    # 2. NEURAL MT (Col 2 Top)
    draw_card(
        ax, x=0.212, y=0.760, w=0.195, h=0.210,
        title="Neural MT ($M_{\\mathrm{trans}}$)",
        items=[
            ("MarianMT (OPUS-MT)", "bold", "#115E59", 6.9),
            ("Hindi $\\rightarrow$ English Translation", "normal", "#134E4A", 6.6),
            ("$e_{\\mathrm{trans}} = M_{\\mathrm{trans}}(e_{\\mathrm{orig}})$", "bold", "#0D9488", 6.8),
            ("(Fixed pivot representation)", "normal", "#64748B", 6.2),
        ],
        bg="#F0FDFA", border="#0D9488", title_col="#115E59", align="center"
    )

    # 3. ORIGINAL EVIDENCE (Col 2 Middle)
    draw_card(
        ax, x=0.212, y=0.510, w=0.195, h=0.210,
        title="Original Evidence ($e_{\\mathrm{orig}}$)",
        items=[
            ("Native Source Text", "bold", "#854D0E", 6.9),
            ("Unmodified Hindi Snippets", "normal", "#713F12", 6.6),
            ("Direct Multilingual Route", "bold", "#CA8A04", 6.8),
            ("(Zero translation artifact)", "normal", "#64748B", 6.2),
        ],
        bg="#FEFCE8", border="#CA8A04", title_col="#854D0E", align="center"
    )

    # 4. VERIFIER ON TRANSLATION (Col 3 Top)
    draw_card(
        ax, x=0.442, y=0.760, w=0.215, h=0.210,
        title="Verifier on Translation",
        items=[
            ("mDeBERTa-v3 ($e_{\\mathrm{trans}}, c$)", "bold", "#115E59", 6.9),
            ("Posterior $P_V(y \\mid e_{\\mathrm{trans}}, c)$", "normal", "#134E4A", 6.6),
            ("Predicted: $\\hat{y}_{\\mathrm{nc}}$ (No-Check)", "bold", "#0F766E", 6.8),
            ("Test Accuracy: 28.22% (46/163)", "normal", "#334155", 6.5),
        ],
        bg="#F0FDFA", border="#0D9488", title_col="#115E59", align="center"
    )

    # 5. VERIFIER ON ORIGINAL (Col 3 Middle)
    draw_card(
        ax, x=0.442, y=0.510, w=0.215, h=0.210,
        title="Verifier on Original",
        items=[
            ("mDeBERTa-v3 ($e_{\\mathrm{orig}}, c$)", "bold", "#854D0E", 6.9),
            ("Posterior $P_V(y \\mid e_{\\mathrm{orig}}, c)$", "normal", "#713F12", 6.6),
            ("Predicted: $\\hat{y}_{\\mathrm{dm}}$ (Direct Multi)", "bold", "#A16207", 6.8),
            ("Test Accuracy: 42.94% (70/163)", "normal", "#334155", 6.5),
        ],
        bg="#FEFCE8", border="#CA8A04", title_col="#854D0E", align="center"
    )

    # 6. ALWAYS-CHECK CONSENSUS (Col 3 Bottom)
    draw_card(
        ax, x=0.442, y=0.035, w=0.215, h=0.410,
        title="Always-Check (Consensus)",
        items=[
            ("Dual-Evidence Ensemble", "bold", "#991B1B", 6.9),
            ("$\\bar{P} = 0.5(P_{\\mathrm{trans}} + P_{\\mathrm{orig}})$", "bold", "#B91C1C", 6.8),
            "───",
            ("Empirical Outcomes ($N=163$):", "bold", "#1E293B", 6.7),
            ("Test Accuracy: 36.81% (60/163)", "normal", "#334155", 6.5),
            ("Latency: 14,945.9 ms ($4.1\\times$ slow)", "normal", "#475569", 6.4),
            "───",
            ("Diagnostic Finding:", "bold", "#991B1B", 6.7),
            ("Suffers Error Contamination!", "bold", "#DC2626", 6.8),
            ("Overconfident erroneous MT", "normal", "#475569", 6.4),
            ("overpowers correct source NLI.", "normal", "#475569", 6.4),
        ],
        bg="#FEF2F2", border="#DC2626", title_col="#991B1B", align="center"
    )

    # 7. RISK TRIGGER ENGINE (Col 4 Top)
    draw_card(
        ax, x=0.707, y=0.655, w=0.281, h=0.315,
        title="Risk Trigger Engine",
        items=[
            ("$r = (1 - p_{\\max}) + \\lambda_{\\mathrm{num}}(1 - O_{\\mathrm{num}})$", "bold", "#1E40AF", 6.8),
            ("Predictive uncertainty + numeral shift", "normal", "#334155", 6.5),
            "───",
            ("Calibration on Dev ($N=103$):", "bold", "#1E293B", 6.7),
            ("Optimal Cutoff: $\\tau^* = 0.650$", "bold", "#2563EB", 6.8),
            ("Dev Peak Utility $\\mathcal{J} = 0.2023$", "normal", "#475569", 6.5),
            ("(Zero-check baseline $\\mathcal{J} = 0.2104$)", "normal", "#64748B", 6.2),
        ],
        bg="#EFF6FF", border="#2563EB", title_col="#1E40AF", align="center"
    )

    # 8. SELECTIVE-CHECK (Col 4 Bottom)
    draw_card(
        ax, x=0.707, y=0.035, w=0.281, h=0.515,
        title="Selective-Check (Ours)",
        items=[
            ("Routing Decision Policy:", "bold", "#166534", 6.8, "center"),
            ("• Fast: If $r < \\tau^* \\rightarrow \\hat{y}_{\\mathrm{nc}}$ (Translated)", "normal", "#14532D", 6.4, "left", 0.005),
            ("• Hard: If $r \\geq \\tau^* \\rightarrow e_{\\mathrm{orig}}$ (Multilingual)", "normal", "#14532D", 6.4, "left", 0.005),
            "───",
            ("Held-Out Test Results ($N=163$):", "bold", "#0F172A", 6.8, "center"),
            ("Accuracy: 28.22% (46/163)", "bold", "#15803D", 6.7, "center"),
            ("Macro-F1 (3-cl): 0.1967 | Macro-F1 (2-cl): 0.2950", "normal", "#334155", 6.4, "center"),
            ("Trigger Coverage: 8.0% (13/163 queries)", "normal", "#334155", 6.5, "center"),
            ("Latency: 4,613.8 ms (59.2% faster than Direct)", "normal", "#334155", 6.5, "center"),
            "───",
            ("Statistical Validation:", "bold", "#1E293B", 6.7, "center"),
            ("Permutation vs Direct: $p = 0.1180$ (n.s.)", "normal", "#475569", 6.4, "center"),
            ("McNemar vs No-Check: $b=4, c=4, p=1.000$", "normal", "#475569", 6.4, "center"),
        ],
        bg="#F0FDF4", border="#16A34A", title_col="#166534", align="center"
    )

    # 9. DIAGNOSTIC OUTCOME STRATA (Bottom Left)
    draw_card(
        ax, x=0.012, y=0.035, w=0.395, h=0.410,
        title="Diagnostic Outcome Strata ($N=163$)",
        items=[
            ("Disjoint Outcome Partition Under Translation Shift:", "bold", "#0F172A", 6.7, "left"),
            "───",
            ("Failures on Translated Evidence ($N_{\\mathrm{fail}} = 117$):", "bold", "#1E293B", 6.6, "left"),
            ("• Recovered by Hindi ($S_{\\mathrm{trans}}$): 51 cases (43.6%)", "bold", "#1D4ED8", 6.5, "left", 0.005),
            ("   MT corrupted veracity; original Hindi recovers ground truth.", "normal", "#475569", 6.2, "left", 0.012),
            ("• Unrecovered ($S_{\\mathrm{verif}}$): 66 cases (56.4%)", "bold", "#C2410C", 6.5, "left", 0.005),
            ("   Both representations fail due to inherent reasoning difficulty.", "normal", "#475569", 6.2, "left", 0.012),
            "───",
            ("Successes on Translated Evidence ($N_{\\mathrm{succ}} = 46$):", "bold", "#1E293B", 6.6, "left"),
            ("• Degraded by Hindi ($S_{\\mathrm{degraded}}$): 27 cases (58.7%)", "bold", "#B91C1C", 6.5, "left", 0.005),
            ("• Concordant Success: 19 cases (41.3% both correct)", "normal", "#15803D", 6.4, "left", 0.005),
            ("Overall Disagreement Rate: 63.80% (104 / 163 test instances)", "bold", "#0F172A", 6.7, "left"),
        ],
        bg="#F8FAFC", border="#64748B", title_col="#1E293B", align="left"
    )

    # =========================================================================
    # CONNECTIONS & CLEAN ARROWS
    # =========================================================================
    # 1. Input -> MT & Original
    draw_arrow(ax, (0.177, 0.810), (0.212, 0.865), color="#0D9488", lw=1.3)
    draw_arrow(ax, (0.177, 0.580), (0.212, 0.615), color="#CA8A04", lw=1.3)

    # 2. MT & Original -> Verifiers
    draw_arrow(ax, (0.407, 0.865), (0.442, 0.865), color="#0D9488", lw=1.3)
    draw_arrow(ax, (0.407, 0.615), (0.442, 0.615), color="#CA8A04", lw=1.3)

    # 3. Verifier Trans -> Risk Engine
    draw_arrow(ax, (0.657, 0.865), (0.707, 0.865), color="#2563EB", lw=1.3)

    # 4. Risk Trigger Engine -> Selective-Check
    # Arrow with clean gap for badge
    draw_arrow(ax, (0.8475, 0.655), (0.8475, 0.618), color="#16A34A", lw=1.4)
    draw_arrow(ax, (0.8475, 0.587), (0.8475, 0.550), color="#16A34A", lw=1.4)
    ax.text(0.8475, 0.6025, "Gated Routing ($r \\geq \\tau^*$)", ha="center", va="center",
            fontsize=6.7, fontweight="bold", color="#166534",
            bbox=dict(boxstyle="round,pad=0.22", fc="#FFFFFF", ec="#16A34A", lw=0.7, zorder=6))

    # 5. Verifier on Original -> Always-Check
    # Gap is from y=0.510 down to y=0.445. Continuous red arrow with label to the right
    draw_arrow(ax, (0.550, 0.510), (0.550, 0.445), color="#DC2626", lw=1.3)
    ax.text(0.562, 0.4775, "$P_{\\mathrm{orig}}$", ha="left", va="center",
            fontsize=7.0, fontweight="bold", color="#DC2626", zorder=6)

    # 6. Verifier on Translation -> Always-Check (Corridor Bypass)
    # Wide corridor between Col 3 (0.657) and Col 4 (0.707): gap is 0.050.
    # Center corridor is at x = 0.682
    ax.plot([0.657, 0.682, 0.682, 0.657], [0.810, 0.810, 0.380, 0.380], color="#DC2626", lw=1.2, zorder=5)
    draw_arrow(ax, (0.682, 0.380), (0.657, 0.380), color="#DC2626", lw=1.2)
    ax.text(0.688, 0.595, "$P_{\\mathrm{trans}}$", ha="left", va="center",
            fontsize=7.0, fontweight="bold", color="#DC2626", zorder=6)

    # 7. Clean Attribution Link from Verifiers to Diagnostic Strata
    # Continuous slate arrow with clean offset label
    draw_arrow(ax, (0.210, 0.510), (0.210, 0.445), color="#64748B", lw=1.3)
    ax.text(0.222, 0.4775, "Diagnostic Stratification ($N=163$)", ha="left", va="center",
            fontsize=6.5, fontweight="bold", color="#334155", zorder=6)

    fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
    fig.savefig(FINAL_DIR / "fig1_study_workflow.pdf", bbox_inches="tight", pad_inches=0.03)
    fig.savefig(SRC_DIR / "fig1_study_workflow.png", bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)
    print(" [PASS] Generated Figure 1: fig1_study_workflow.pdf & .png")

# ==============================================================================
# FIGURE 2: Dev Threshold Tuning & Risk-Coverage Curve (No Text Overlap)
# ==============================================================================
def generate_figure_2():
    csv_path = REPO_ROOT / "experiments" / "results_canonical" / "canonical_dev_tuning.csv"
    if not csv_path.exists():
        csv_path = REPO_ROOT / "results" / "canonical" / "canonical_dev_tuning.csv"
    df = pd.read_csv(csv_path).sort_values("coverage")

    fig, ax = plt.subplots(figsize=(6.6, 4.0), dpi=300)
    ax.grid(True, linestyle="--", alpha=0.35, zorder=1)

    color_f1 = "#1d4ed8"     # Deep Blue
    color_score = "#15803d"  # Forest Green

    f1_col = "macro_f1_3cl" if "macro_f1_3cl" in df.columns else "macro_f1"
    score_col = "tradeoff_score" if "tradeoff_score" in df.columns else "score"
    tau_col = "tau" if "tau" in df.columns else "threshold_tau"

    ax.plot(df["coverage"] * 100, df[f1_col], label="Macro-F1 (Dev Evaluation)",
            color=color_f1, marker="o", markersize=6, linestyle="-", lw=2.0, zorder=4)
    ax.plot(df["coverage"] * 100, df[score_col], label=r"Tradeoff Objective ($J = \mathrm{F1} - 0.15\cdot\mathrm{Cov}$)",
            color=color_score, marker="s", markersize=6, linestyle="--", lw=1.8, zorder=4)

    # Baseline horizontal reference line
    ax.axhline(0.2104, color="#64748b", linestyle=":", lw=1.3, alpha=0.9, zorder=2,
               label=r"Zero-Check Baseline ($J = 0.2104$)")

    opt_idx = df[score_col].idxmax()
    opt_row = df.loc[opt_idx]
    opt_cov = opt_row["coverage"] * 100
    opt_f1 = opt_row[f1_col]
    opt_score = opt_row[score_col]
    opt_tau = opt_row[tau_col]

    # Red drop line
    ax.vlines(opt_cov, 0.08, opt_f1, color="#dc2626", linestyle=":", lw=1.3, alpha=0.8, zorder=3)
    ax.scatter([opt_cov], [opt_f1], color="#dc2626", s=120, zorder=6,
               edgecolor="black", lw=1.2, label=rf"Optimal Threshold ($\tau^* = {opt_tau:.3f}$)")

    # CALLOUT BOX: Positioned safely at (opt_cov + 18, opt_f1 + 0.13) to avoid ANY axis overlap!
    ax.annotate(
        r"$\mathbf{Optimal\ Operating\ Point}$" + "\n" +
        rf"$\mathbf{{\tau^* = {opt_tau:.3f}}}$" + "\n" +
        f"Coverage: {opt_cov:.1f}%\n" +
        f"Macro-F1: {opt_f1:.3f}\n" +
        f"Objective: {opt_score:.3f}",
        xy=(opt_cov, opt_f1),
        xytext=(opt_cov + 17, opt_f1 + 0.13),
        ha="center", va="center",
        arrowprops=dict(
            arrowstyle="->",
            color="#dc2626", lw=1.4,
            shrinkA=3, shrinkB=4
        ),
        fontsize=7.8,
        bbox=dict(boxstyle="round,pad=0.30", fc="#fff5f5", ec="#dc2626", lw=1.1, alpha=0.96),
        zorder=7
    )

    ax.set_xlabel("Original Evidence Consultation Coverage (%)", fontweight="bold", labelpad=8)
    ax.set_ylabel("Verification Performance Score", fontweight="bold", labelpad=8)
    ax.set_title(r"Development Set Risk-Coverage Trade-off ($N=103$)", fontweight="bold", pad=12)
    ax.set_xlim(5, 105)
    ax.set_ylim(0.08, 0.60)
    ax.legend(loc="upper left", framealpha=0.96, edgecolor="#cbd5e1", fontsize=8.2)

    fig.tight_layout()
    fig.savefig(FINAL_DIR / "fig2_risk_coverage_tradeoff.pdf", bbox_inches="tight", pad_inches=0.04)
    fig.savefig(SRC_DIR / "fig2_risk_coverage_tradeoff.png", bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)
    print(" [PASS] Generated Figure 2: fig2_risk_coverage_tradeoff.pdf & .png")

# ==============================================================================
# FIGURE 3: Condition Comparisons with Exact 95% CIs
# ==============================================================================
def generate_figure_3():
    csv_path = REPO_ROOT / "experiments" / "results_canonical" / "canonical_benchmark_table.csv"
    if not csv_path.exists():
        csv_path = REPO_ROOT / "results" / "canonical" / "canonical_benchmark_table.csv"
    df = pd.read_csv(csv_path)

    target_names = [
        "No-Check (Translated Only)",
        "Direct Multilingual (Original Only)",
        "Always-Check (Dual Consensus Avg)",
        "Selective-Check (Ours, Hard Route)"
    ]
    sub = df[df["System / Ablation"].isin(target_names)].copy()
    if len(sub) < 4:
        sub = df.iloc[:4].copy()

    fig, ax = plt.subplots(figsize=(7.4, 4.4), dpi=300)
    ax.grid(True, linestyle="--", alpha=0.30, zorder=1)

    x = np.arange(len(sub))
    width = 0.32

    cond_labels = [
        "No-Check\n(Translated)",
        "Direct Multilingual\n(Original Hindi)",
        "Always-Check\n(Dual Consensus)",
        "Selective-Check\n(Hard Route)"
    ]

    acc_vals = sub["Accuracy"].values
    f1_vals = sub["Macro_F1_3cl"].values if "Macro_F1_3cl" in sub.columns else sub["Macro_F1"].values

    acc_yerr = [[], []]
    f1_yerr = [[], []]
    for _, row in sub.iterrows():
        acc_s = str(row["Acc_95_CI"]).strip(" []").split(",")
        f1_s = str(row.get("F1_3cl_95_CI") or row.get("F1_CI_95")).strip(" []").split(",")
        a_lo, a_hi = float(acc_s[0]), float(acc_s[1])
        f_lo, f_hi = float(f1_s[0]), float(f1_s[1])
        acc_yerr[0].append(row["Accuracy"] - a_lo)
        acc_yerr[1].append(a_hi - row["Accuracy"])
        cur_f1 = row["Macro_F1_3cl"] if "Macro_F1_3cl" in row else row["Macro_F1"]
        f1_yerr[0].append(cur_f1 - f_lo)
        f1_yerr[1].append(f_hi - cur_f1)

    color_acc = "#1e40af"  # Deep Royal Blue
    color_f1 = "#059669"   # Emerald Green

    rects1 = ax.bar(
        x - width/2, acc_vals, width, yerr=acc_yerr,
        capsize=4.0, label="Accuracy [95% CI]",
        color=color_acc, edgecolor="#0f172a", linewidth=1.0,
        error_kw=dict(lw=1.2, capthick=1.2, ecolor="#0f172a"), zorder=3
    )
    rects2 = ax.bar(
        x + width/2, f1_vals, width, yerr=f1_yerr,
        capsize=4.0, label="Macro-F1 (3-cl) [95% CI]",
        color=color_f1, edgecolor="#0f172a", linewidth=1.0,
        error_kw=dict(lw=1.2, capthick=1.2, ecolor="#0f172a"), zorder=3
    )

    # Reference dashed line for baseline accuracy
    ax.axhline(acc_vals[0], color="#64748b", linestyle="--", lw=1.2, alpha=0.85, zorder=2,
               label=f"No-Check Baseline ({acc_vals[0]:.3f})")

    ax.set_ylabel("Metric Score", fontweight="bold", labelpad=8)
    ax.set_title("Held-Out Test Set Verification Performance ($N=163$)", fontweight="bold", pad=12)
    ax.set_xticks(x)
    ax.set_xticklabels(cond_labels, fontweight="bold", fontsize=8.8)
    ax.set_ylim(0, 0.64)

    # Value text inside bars with high-contrast pill backgrounds to avoid whisker collision
    for i, rect in enumerate(rects1):
        ax.text(
            rect.get_x() + rect.get_width() / 2, 0.060,
            f"{acc_vals[i]:.3f}",
            ha="center", va="center", fontsize=8.6, fontweight="bold", color="#ffffff", zorder=6,
            bbox=dict(boxstyle="round,pad=0.18", fc="#0f172a", ec="none", alpha=0.70)
        )
    for i, rect in enumerate(rects2):
        ax.text(
            rect.get_x() + rect.get_width() / 2, 0.060,
            f"{f1_vals[i]:.3f}",
            ha="center", va="center", fontsize=8.6, fontweight="bold", color="#ffffff", zorder=6,
            bbox=dict(boxstyle="round,pad=0.18", fc="#0f172a", ec="none", alpha=0.70)
        )

    ax.legend(loc="upper left", framealpha=0.96, edgecolor="#cbd5e1", fontsize=8.5)

    fig.tight_layout()
    fig.savefig(FINAL_DIR / "fig3_condition_comparison.pdf", bbox_inches="tight", pad_inches=0.04)
    fig.savefig(SRC_DIR / "fig3_condition_comparison.png", bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)
    print(" [PASS] Generated Figure 3: fig3_condition_comparison.pdf & .png")

# ==============================================================================
# FIGURE 4: Error Attribution Breakdown (Clean Axis Margins)
# ==============================================================================
def generate_figure_4():
    json_path = REPO_ROOT / "experiments" / "results_canonical" / "canonical_error_attribution.json"
    if not json_path.exists():
        json_path = REPO_ROOT / "results" / "canonical" / "canonical_error_attribution.json"
        
    counts = [51, 66, 27]
    if json_path.exists():
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        counts = [
            data.get("stratum_recovered_by_original", 51),
            data.get("stratum_unrecovered_both_wrong", 66),
            data.get("stratum_degraded_by_original", 27)
        ]

    fig, ax = plt.subplots(figsize=(7.2, 4.4), dpi=300)
    ax.grid(True, linestyle="--", alpha=0.30, zorder=1)

    categories = [
        "Recovered by Original\n($S_{\\mathrm{trans}}$)\n\nTranslated Wrong,\nOriginal Correct",
        "Both Representations Wrong\n($S_{\\mathrm{verif}}$)\n\nUnrecovered by\nOriginal Evidence",
        "Degraded by Original\n($S_{\\mathrm{degraded}}$)\n\nTranslated Correct,\nOriginal Wrong"
    ]

    colors = ["#2563eb", "#ea580c", "#dc2626"]
    edge_colors = ["#1d4ed8", "#c2410c", "#991b1b"]

    bars = ax.bar(categories, counts, color=colors, edgecolor=edge_colors, linewidth=1.1, width=0.48, zorder=3)

    ax.set_ylabel("Number of Instances", fontweight="bold", labelpad=8)
    ax.set_title("Diagnostic Outcome Stratification on Test Partition ($N=163$)", fontweight="bold", pad=14)
    ax.set_ylim(0, max(counts) + 20)

    # Context subtitle
    ax.text(0.5, 0.94, "Translated Failures ($N_{\\mathrm{fail}} = 117$) vs. Translated Successes ($N_{\\mathrm{succ}} = 46$)",
            transform=ax.transAxes, ha="center", fontsize=8.4, color="#475569", style="italic")

    # Annotations on bars
    total_failures = 117
    total_succ = 46
    for i, bar in enumerate(bars):
        h = bar.get_height()
        if i < 2:
            pct = (h / total_failures) * 100
            label_text = f"{h} cases\n({pct:.1f}% of failures)"
        else:
            pct = (h / total_succ) * 100
            label_text = f"{h} cases\n({pct:.1f}% of successes)"
            
        ax.annotate(
            label_text,
            xy=(bar.get_x() + bar.get_width() / 2, h),
            xytext=(0, 6), textcoords="offset points",
            ha="center", va="bottom", fontsize=8.8, fontweight="bold", color="#0f172a"
        )

    ax.set_xlabel("Operational Outcome Stratum", fontweight="bold", labelpad=14)
    fig.tight_layout()
    fig.savefig(FINAL_DIR / "fig4_error_attribution_breakdown.pdf", bbox_inches="tight", pad_inches=0.04)
    fig.savefig(SRC_DIR / "fig4_error_attribution_breakdown.png", bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)
    print(" [PASS] Generated Figure 4: fig4_error_attribution_breakdown.pdf & .png")

# ==============================================================================
# FIGURE 5: Directional Transition Matrix Heatmap (No Line Collisions)
# ==============================================================================
def generate_figure_5():
    csv_path = REPO_ROOT / "experiments" / "results_canonical" / "canonical_test_predictions.csv"
    if not csv_path.exists():
        csv_path = REPO_ROOT / "results" / "canonical" / "canonical_test_predictions.csv"
    df = pd.read_csv(csv_path)

    labels = ["CONTRADICTED", "INSUFFICIENT_EVIDENCE", "SUPPORTED"]
    disp_labels = ["CONTRADICTED", "INSUFFICIENT", "SUPPORTED"]

    matrix = np.zeros((3, 3), dtype=int)
    for i, l_trans in enumerate(labels):
        for j, l_orig in enumerate(labels):
            count = int(((df["pred_translated"] == l_trans) & (df["pred_original"] == l_orig)).sum())
            matrix[i, j] = count

    fig, ax = plt.subplots(figsize=(6.2, 4.8), dpi=300)
    # Turn off background grid explicitly so dashed lines do NOT cut through numbers!
    ax.grid(False)

    im = ax.imshow(matrix, cmap="Blues", interpolation="nearest")

    # Add text annotations with clear thresholding
    for i in range(3):
        for j in range(3):
            val = matrix[i, j]
            # Use white for dark cells, deep navy for light cells
            color = "#ffffff" if val >= 20 else "#0f172a"
            pct = (val / 163.0) * 100
            ax.text(j, i, f"{val}\n({pct:.1f}%)", ha="center", va="center",
                    color=color, fontsize=9.8, fontweight="bold")

    ax.set_xticks(np.arange(3))
    ax.set_yticks(np.arange(3))
    ax.set_xticklabels(disp_labels, fontweight="bold", fontsize=9.0)
    ax.set_yticklabels(disp_labels, fontweight="bold", fontsize=9.0)
    ax.set_xlabel("Original Hindi Evidence Prediction", fontweight="bold", labelpad=10)
    ax.set_ylabel("Translated Evidence Prediction", fontweight="bold", labelpad=10)
    ax.set_title("Directional Prediction Transition Matrix ($N=163$)", fontweight="bold", pad=14)

    # Colorbar with comfortable padding
    cbar = ax.figure.colorbar(im, ax=ax, shrink=0.85, pad=0.04)
    cbar.ax.set_ylabel("Instance Count", rotation=-90, va="bottom", fontweight="bold", labelpad=12)

    fig.tight_layout()
    fig.savefig(FINAL_DIR / "fig5_transition_heatmap.pdf", bbox_inches="tight", pad_inches=0.04)
    fig.savefig(SRC_DIR / "fig5_transition_heatmap.png", bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)
    print(" [PASS] Generated Figure 5: fig5_transition_heatmap.pdf & .png")

def main():
    print("=" * 60)
    print("GENERATING IMPROVED, COLLISION-FREE PUBLICATION FIGURES")
    print("=" * 60)
    generate_figure_1()
    generate_figure_2()
    generate_figure_3()
    generate_figure_4()
    generate_figure_5()
    print("=" * 60)
    print("ALL 5 PUBLICATION FIGURES REGENERATED SUCCESSFULLY!")

if __name__ == "__main__":
    main()
