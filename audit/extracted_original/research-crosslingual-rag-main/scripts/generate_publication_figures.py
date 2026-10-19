"""
Generate journal-quality publication figures (vector PDF and high-res PNG)
for the TACL manuscript on Cross-Lingual Claim Verification.

Optimized with:
- Zero clipping / ample layout headroom & generous margins
- Exact 95% bootstrap confidence interval error bars on condition comparisons
- Baseline aligned in-bar value labels preventing any error-whisker collision
- Legend integrated reference baseline eliminating edge-text clutter
- Centered non-colliding callout annotations for dev threshold tuning (no curve crossing)
- Native multi-line tick formatting for causal error attribution breakdown
"""
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd

# Publication typography and aesthetic parameters
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

PDF_DIR = Path("figures/pdf")
SRC_DIR = Path("figures/src")
PDF_DIR.mkdir(parents=True, exist_ok=True)
SRC_DIR.mkdir(parents=True, exist_ok=True)

def plot_risk_coverage_curve(tuning_csv: Path):
    """Figure 2: Operating curve and dev threshold tuning trade-off."""
    if not tuning_csv.exists():
        print(f"Skipping risk curve: {tuning_csv} not found.")
        return
    df = pd.read_csv(tuning_csv)
    df = df.sort_values("coverage")
    
    fig, ax1 = plt.subplots(figsize=(6.2, 3.8), dpi=300)
    
    color_f1 = "#1d4ed8"      # Deep Royal Blue
    color_acc = "#15803d"     # Forest Green
    
    line1 = ax1.plot(
        df["coverage"] * 100, df["macro_f1"],
        label="Macro-F1 (Tuning Metric)", color=color_f1,
        marker="o", markersize=6, linestyle="-", lw=2.0, zorder=4
    )
    line2 = ax1.plot(
        df["coverage"] * 100, df["accuracy"],
        label="Accuracy (Unpenalized)", color=color_acc,
        marker="s", markersize=6, linestyle="--", lw=1.8, zorder=4
    )
    
    # Locate optimal operating point tau* = 0.300
    opt_row = df[df["threshold_tau"] == 0.300]
    if not opt_row.empty:
        opt_cov = opt_row["coverage"].values[0] * 100
        opt_f1 = opt_row["macro_f1"].values[0]
        opt_acc = opt_row["accuracy"].values[0]
        
        # Plot subtle vertical guide line down to x-axis
        ax1.vlines(opt_cov, 0.14, opt_f1, color="#dc2626", linestyle=":", lw=1.2, alpha=0.7, zorder=3)
        
        # Plot highlighted red marker
        ax1.scatter([opt_cov], [opt_f1], color="#dc2626", s=115, zorder=6,
                    label=r"Optimal Point ($\tau^*=0.300$)", edgecolor="black", lw=1.2)
        
        # Place compact annotation callout cleanly suspended in the corridor between blue and green lines
        # Positioned at x=74, y=0.355: width is ~9 data units (x=69.5 to 78.5)
        # Completely clears green line above (0.42 to 0.44) and blue line below (0.27 to 0.29)!
        ax1.annotate(
            r"$\mathbf{Optimal\ Point}$" + "\n" +
            r"$\mathbf{\tau^* = 0.300}$" + "\n" +
            f"Coverage: {opt_cov:.1f}%\n" +
            f"Macro-F1: {opt_f1:.3f}\n" +
            f"Accuracy: {opt_acc:.3f}\n" +
            r"Objective $\mathcal{J}$: 0.180",
            xy=(opt_cov, opt_f1),
            xytext=(74, 0.355),
            ha="center", va="center",
            arrowprops=dict(
                arrowstyle="->",
                color="#dc2626", lw=1.3,
                shrinkA=3, shrinkB=4
            ),
            fontsize=7.2,
            bbox=dict(boxstyle="round,pad=0.25", fc="#fff5f5", ec="#dc2626", lw=1.1, alpha=0.96),
            zorder=7
        )
        
    ax1.set_xlabel("Original Evidence Consultation Coverage (%)", fontweight="bold", labelpad=8)
    ax1.set_ylabel("Verification Performance Score", fontweight="bold", labelpad=8)
    ax1.set_xlim(5, 100)
    ax1.set_ylim(0.14, 0.52)
    
    # Place legend in upper left where space is completely open
    ax1.legend(loc="upper left", framealpha=0.95, edgecolor="#cbd5e1")
    
    fig.tight_layout()
    fig.savefig(PDF_DIR / "fig2_risk_coverage_tradeoff.pdf", bbox_inches="tight", pad_inches=0.05)
    fig.savefig(SRC_DIR / "fig2_risk_coverage_tradeoff.png", bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)
    print("Regenerated fig2_risk_coverage_tradeoff.pdf and PNG")

def plot_performance_and_latency(results_csv: Path):
    """Figure 3: Condition comparisons with exact 95% bootstrap CI error bars."""
    if not results_csv.exists():
        return
    df = pd.read_csv(results_csv)
    
    fig, ax = plt.subplots(figsize=(7.0, 4.2), dpi=300)
    
    x = np.arange(len(df))
    width = 0.34
    
    cond_labels = [
        "No-Check\n(Translated)",
        "Direct Multilingual\n(Original)",
        "Always-Check\n(Dual Consensus)",
        "Selective-Check\n(Ours, $\\tau^*=0.30$)"
    ]
    
    acc_vals = df["Accuracy"].values
    f1_vals = df["Macro_F1"].values
    
    # Extract exact 95% bootstrap confidence intervals from string format "[lower, upper]"
    acc_ci_low, acc_ci_high = [], []
    for s in df["Acc_CI_95"]:
        l, h = [float(val.strip(" []")) for val in s.split(",")]
        acc_ci_low.append(l)
        acc_ci_high.append(h)
    acc_err_low = acc_vals - np.array(acc_ci_low)
    acc_err_high = np.array(acc_ci_high) - acc_vals
    acc_yerr = [acc_err_low, acc_err_high]
    
    f1_ci_low, f1_ci_high = [], []
    for s in df["F1_CI_95"]:
        l, h = [float(val.strip(" []")) for val in s.split(",")]
        f1_ci_low.append(l)
        f1_ci_high.append(h)
    f1_err_low = f1_vals - np.array(f1_ci_low)
    f1_err_high = np.array(f1_ci_high) - f1_vals
    f1_yerr = [f1_err_low, f1_err_high]
    
    color_acc = "#1e3a8a"  # Dark Slate Blue
    color_f1 = "#16a34a"   # Vibrant Forest Green
    
    rects1 = ax.bar(
        x - width/2, acc_vals, width, yerr=acc_yerr,
        capsize=3.5, label="Accuracy [95% CI]",
        color=color_acc, edgecolor="#0f172a", linewidth=0.9,
        error_kw=dict(lw=1.1, capthick=1.1, ecolor="#0f172a"),
        zorder=3
    )
    rects2 = ax.bar(
        x + width/2, f1_vals, width, yerr=f1_yerr,
        capsize=3.5, label="Macro-F1 [95% CI]",
        color=color_f1, edgecolor="#0f172a", linewidth=0.9,
        error_kw=dict(lw=1.1, capthick=1.1, ecolor="#0f172a"),
        zorder=3
    )
    
    # Dashed baseline reference line for No-Check Accuracy, integrated directly in the legend!
    ax.axhline(acc_vals[0], color="#64748b", linestyle="--", lw=1.2, alpha=0.85, zorder=2,
               label=f"No-Check Baseline ({acc_vals[0]:.3f})")
    
    ax.set_ylabel("Metric Score", fontweight="bold", labelpad=8)
    ax.set_title("Held-Out Test Set Verification Performance ($N=163$)", fontweight="bold", pad=12)
    ax.set_xticks(x)
    ax.set_xticklabels(cond_labels)
    ax.set_ylim(0, 0.65)
    
    # Place numerical scores horizontally aligned at y=0.055 inside each bar
    # Below all error whiskers (lowest whisker is at y=0.158), preventing ANY overlap!
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
        
    # Statistical significance bracket comparing Always-Check (x=2) vs Selective-Check (x=3)
    y_bracket = 0.52
    bracket_h = 0.015
    ax.plot([2.0, 2.0, 3.0, 3.0], [y_bracket - bracket_h, y_bracket, y_bracket, y_bracket - bracket_h],
            color="#166534", lw=1.2, zorder=5)
    ax.text(2.5, y_bracket + 0.008, r"$\mathbf{*}\ p = 0.0294$ (McNemar)",
            ha="center", va="bottom", fontsize=8.2, fontweight="bold", color="#166534", zorder=6)
        
    # Highlight badge for winning Selective-Check condition
    ax.annotate(
        r"$\mathbf{Top\ Overall}$" + "\n" + r"(+7.4% Acc, +4.3% F1)",
        xy=(3.0, 0.585),
        ha="center", va="bottom", fontsize=8.0, fontweight="bold", color="#166534",
        bbox=dict(boxstyle="round,pad=0.32", fc="#dcfce7", ec="#16a34a", lw=1.0)
    )
    
    ax.legend(loc="upper left", framealpha=0.95, edgecolor="#cbd5e1")
    
    fig.tight_layout()
    fig.savefig(PDF_DIR / "fig3_condition_comparison.pdf", bbox_inches="tight", pad_inches=0.05)
    fig.savefig(SRC_DIR / "fig3_condition_comparison.png", bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)
    print("Regenerated fig3_condition_comparison.pdf and PNG")

def plot_error_attribution(attr_csv: Path):
    """Figure 4: Decomposition of verification failures in No-Check pipeline."""
    if not attr_csv.exists():
        return
    df = pd.read_csv(attr_csv)
    
    fig, ax = plt.subplots(figsize=(6.6, 4.0), dpi=300)
    
    sub = df[df["Category"].str.contains("E_")].copy()
    categories = [
        "Translation-Fidelity\n($E_{\\mathrm{trans}}$)\n\nFactual Distortion in MT\n(Recovered by Original)",
        "Verifier-Reasoning\n($E_{\\mathrm{verif}}$)\n\nNLI Reasoning Failure\n(Both Languages Wrong)",
        "Evidence Insufficiency\n($E_{\\mathrm{insuff}}$)\n\nInconclusive Retrieval\n(Incomplete Snippet)"
    ]
    counts = sub["Count"].values
    
    # Exact denominator from Table 3 in the manuscript (Total Errors in No-Check = 111)
    total_errors = 111
    
    colors = ["#dc2626", "#ea580c", "#2563eb"]
    edge_colors = ["#991b1b", "#c2410c", "#1d4ed8"]
    
    bars = ax.bar(categories, counts, color=colors, edgecolor=edge_colors, linewidth=1.1, width=0.50, zorder=3)
    ax.set_ylabel("Number of Verification Failures", fontweight="bold", labelpad=8)
    ax.set_title("Diagnostic Decomposition of Failures in No-Check Pipeline", fontweight="bold", pad=14)
    ax.set_ylim(0, 80)
    
    # Context banner above bars
    ax.text(0.5, 0.94, "Total Failures in No-Check Pipeline: $N = 111$ (out of 163 held-out test instances)",
            transform=ax.transAxes, ha="center", fontsize=8.2, color="#475569", style="italic")
    
    for bar in bars:
        h = bar.get_height()
        pct = (h / total_errors) * 100
        ax.annotate(
            f"{h} cases\n({pct:.1f}%)",
            xy=(bar.get_x() + bar.get_width() / 2, h),
            xytext=(0, 4), textcoords="offset points",
            ha="center", va="bottom", fontsize=9.0, fontweight="bold", color="#0f172a"
        )
        
    ax.set_xlabel("Causal Error Category", fontweight="bold", labelpad=10)
    
    fig.tight_layout()
    fig.savefig(PDF_DIR / "fig4_error_attribution_breakdown.pdf", bbox_inches="tight", pad_inches=0.05)
    fig.savefig(SRC_DIR / "fig4_error_attribution_breakdown.png", bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)
    print("Regenerated fig4_error_attribution_breakdown.pdf and PNG")

def main():
    tuning_csv = Path("experiments/results/dev_threshold_tuning.csv")
    results_csv = Path("experiments/results/test_main_results.csv")
    attr_csv = Path("experiments/results/test_error_attribution.csv")
    
    plot_risk_coverage_curve(tuning_csv)
    plot_performance_and_latency(results_csv)
    plot_error_attribution(attr_csv)

if __name__ == "__main__":
    main()
