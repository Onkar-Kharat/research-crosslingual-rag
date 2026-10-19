"""
Generate Figure 1: Publication-Grade System Architecture & Workflow Diagram
Modular 4-column layout with 100% collision-free routing:
- Col 1: Input Fact-Check (Hindi Claim & Retrieved Evidence)
- Col 2: Evidence Processing (MarianMT vs Original Hindi)
- Col 3: Cross-Lingual Verifiers (mDeBERTa-v3) & Naive Always-Check Consensus
- Col 4: Risk Trigger Engine & Selective-Check Decision Cascade
- Bottom-Left: Disentangled Causal Error Attribution Taxonomy
Outputs: figures/pdf/fig1_study_workflow.pdf & figures/src/fig1_study_workflow.png
"""
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib as mpl

mpl.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif"],
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})

PDF_DIR = Path("figures/pdf")
SRC_DIR = Path("figures/src")
PDF_DIR.mkdir(parents=True, exist_ok=True)
SRC_DIR.mkdir(parents=True, exist_ok=True)

def draw_card(ax, x, y, w, h, title, subtitle_lines, bg="#F8FAFC", border="#334155", title_color="#0F172A", corner_radius=0.022):
    """Draws a clean, rounded card with title, divider line, and multi-line body text."""
    box = patches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0.0,rounding_size={corner_radius}",
        facecolor=bg,
        edgecolor=border,
        linewidth=1.3,
        zorder=3
    )
    ax.add_patch(box)
    
    # Title
    ax.text(x + w / 2, y + h - 0.030, title, ha="center", va="top",
            fontsize=8.8, fontweight="bold", color=title_color, zorder=4)
    
    # Divider line under title
    ax.plot([x + 0.015, x + w - 0.015], [y + h - 0.052, y + h - 0.052],
            color=border, lw=0.6, alpha=0.45, zorder=4)
    
    # Body lines
    n_lines = len(subtitle_lines)
    if n_lines > 0:
        line_spacing = (h - 0.072) / (n_lines + 0.3)
        for idx, line in enumerate(subtitle_lines):
            line_y = y + h - 0.072 - (idx * line_spacing)
            ax.text(x + w / 2, line_y, line, ha="center", va="top",
                    fontsize=7.1, color="#334155", zorder=4)

def draw_arrow(ax, p_start, p_end, color="#475569", lw=1.3, rad=0.0):
    """Draws a clean directional arrow from p_start to p_end."""
    arrow = patches.FancyArrowPatch(
        posA=p_start, posB=p_end,
        arrowstyle="-|>,head_length=4.5,head_width=3.0",
        color=color,
        linewidth=lw,
        connectionstyle=f"arc3,rad={rad}",
        zorder=5
    )
    ax.add_patch(arrow)

def main():
    fig, ax = plt.subplots(figsize=(8.0, 4.5), dpi=300)
    
    ax.set_xlim(-0.015, 1.015)
    ax.set_ylim(-0.015, 1.015)
    ax.axis("off")

    # -------------------------------------------------------------
    # Column 1: Input Fact-Check (Top Left)
    # -------------------------------------------------------------
    draw_card(
        ax, x=0.015, y=0.48, w=0.165, h=0.47,
        title="Input Fact-Check",
        subtitle_lines=[
            "Claim $c$ (Hindi)",
            "Retrieved Snippets $e_{\\mathrm{orig}}$",
            "from Search Engines",
            "────────────────",
            "Benchmark: X-Fact",
            "Authentic News Claims",
            "($N=266$ instances)"
        ],
        bg="#F1F5F9", border="#475569", title_color="#0F172A"
    )

    # -------------------------------------------------------------
    # Column 2: Evidence Processing (Center-Left)
    # -------------------------------------------------------------
    # Top: Neural MT
    draw_card(
        ax, x=0.210, y=0.75, w=0.205, h=0.20,
        title="Neural MT ($M_{\\mathrm{trans}}$)",
        subtitle_lines=[
            "Local MarianMT (OPUS)",
            "Hindi $\\rightarrow$ English Pivot",
            "$e_{\\mathrm{trans}} = M_{\\mathrm{trans}}(e_{\\mathrm{orig}})$"
        ],
        bg="#F0FDFA", border="#0D9488", title_color="#115E59"
    )

    # Bottom: Original Evidence
    draw_card(
        ax, x=0.210, y=0.48, w=0.205, h=0.20,
        title="Original Evidence",
        subtitle_lines=[
            "Unmodified Hindi Snippets",
            "Direct Multilingual Route",
            "$e_{\\mathrm{orig}}$ (Source Language)"
        ],
        bg="#FEFCE8", border="#CA8A04", title_color="#854D0E"
    )

    # -------------------------------------------------------------
    # Column 3: Verifiers & Always-Check Consensus (Center-Right)
    # -------------------------------------------------------------
    # Top: Verifier on Translation
    draw_card(
        ax, x=0.445, y=0.75, w=0.225, h=0.20,
        title="Verifier on Translation",
        subtitle_lines=[
            "mDeBERTa-v3 ($e_{\\mathrm{trans}}, c$)",
            "Posterior $P_V(y \\mid e_{\\mathrm{trans}}, c)$",
            "Predicted: $\\hat{y}_{\\mathrm{trans}}$ (No-Check)"
        ],
        bg="#F0FDFA", border="#0D9488", title_color="#115E59"
    )

    # Middle: Verifier on Original
    draw_card(
        ax, x=0.445, y=0.48, w=0.225, h=0.20,
        title="Verifier on Original",
        subtitle_lines=[
            "mDeBERTa-v3 ($e_{\\mathrm{orig}}, c$)",
            "Posterior $P_V(y \\mid e_{\\mathrm{orig}}, c)$",
            "Predicted: $\\hat{y}_{\\mathrm{orig}}$ (Direct)"
        ],
        bg="#FEFCE8", border="#CA8A04", title_color="#854D0E"
    )

    # Bottom: Always-Check Consensus Baseline
    draw_card(
        ax, x=0.445, y=0.06, w=0.225, h=0.35,
        title="Always-Check (Consensus)",
        subtitle_lines=[
            "Uniform Probability Average",
            "$\\bar{P} = 0.5(P_{\\mathrm{trans}} + P_{\\mathrm{orig}})$",
            "────────────────",
            "Critical Empirical Finding:",
            "Suffers Error Contamination!",
            "Accuracy degrades to 0.313",
            "(-6.1% vs Direct, $p=0.029$)"
        ],
        bg="#FEF2F2", border="#DC2626", title_color="#991B1B"
    )

    # -------------------------------------------------------------
    # Column 4: Risk Trigger Engine & Selective-Check (Right)
    # -------------------------------------------------------------
    # Top: Risk Trigger Engine
    draw_card(
        ax, x=0.715, y=0.64, w=0.275, h=0.31,
        title="Risk Trigger Engine",
        subtitle_lines=[
            "$R = 0.70(1 - p_{\\max}) + 0.30(1 - O_{\\mathrm{num}})$",
            "Evaluates uncertainty & entity mismatch",
            "────────────────",
            "Operating Threshold: $\\tau^* = 0.300$",
            "(Tuned strictly on Dev partition,",
            "Trade-off Score $\\mathcal{J} = 0.180$)"
        ],
        bg="#EFF6FF", border="#2563EB", title_color="#1E40AF"
    )

    # Bottom: Selective-Check Decision Cascade
    draw_card(
        ax, x=0.715, y=0.06, w=0.275, h=0.48,
        title="Selective-Check (Ours)",
        subtitle_lines=[
            "$\\bullet$ If $R < \\tau^*$: Fast Output $\\hat{y}_{\\mathrm{trans}}$",
            "$\\bullet$ If $R \\geq \\tau^*$: Consult $e_{\\mathrm{orig}}$ & Average",
            "────────────────",
            "Test Set Evaluation ($N=163$):",
            "Top Test Accuracy: 0.394 (+7.4%)",
            "Macro-F1: 0.270 (+4.3%)",
            "Coverage: 83.4% of instances",
            "────────────────",
            "Statistically beats Always-Check",
            "McNemar $p = 0.0294$, Perm $p = 0.0370$"
        ],
        bg="#F0FDF4", border="#16A34A", title_color="#166534"
    )

    # -------------------------------------------------------------
    # Bottom Left: Disentangled Error Attribution Taxonomy
    # -------------------------------------------------------------
    draw_card(
        ax, x=0.015, y=0.06, w=0.400, h=0.36,
        title="Causal Error Taxonomy ($N=111$)",
        subtitle_lines=[
            "Attribution of No-Check Pipeline Failures:",
            "  1. Translation ($E_{\\mathrm{trans}}$: 36.9%, 41 cases)",
            "     MT corrupted entities; original recovers truth.",
            "  2. Reasoning ($E_{\\mathrm{verif}}$: 55.0%, 61 cases)",
            "     Translation faithful; entailment failed.",
            "  3. Insufficiency ($E_{\\mathrm{insuff}}$: 10.8%, 12 cases)",
            "     Search snippets lacked factual basis.",
            "Overall Flip Rate: 62.6% (102 / 163 instances)"
        ],
        bg="#F8FAFC", border="#64748B", title_color="#1E293B"
    )

    # -------------------------------------------------------------
    # Clean, 100% Collision-Free Connection Arrows
    # -------------------------------------------------------------
    # 1. Input -> MT & Original
    draw_arrow(ax, (0.180, 0.79), (0.210, 0.85), color="#0D9488", lw=1.4)
    draw_arrow(ax, (0.180, 0.60), (0.210, 0.58), color="#CA8A04", lw=1.4)

    # 2. MT & Original -> Verifiers
    draw_arrow(ax, (0.415, 0.85), (0.445, 0.85), color="#0D9488", lw=1.4)
    draw_arrow(ax, (0.415, 0.58), (0.445, 0.58), color="#CA8A04", lw=1.4)

    # 3. Verifier Trans -> Risk Trigger Engine
    draw_arrow(ax, (0.670, 0.85), (0.715, 0.85), color="#2563EB", lw=1.4)

    # 4. Risk Trigger Engine -> Selective-Check
    # Straight vertical line with single arrowhead at destination
    draw_arrow(ax, (0.852, 0.64), (0.852, 0.54), color="#16A34A", lw=1.5)
    # Gated routing badge centered on line with white masking box
    ax.text(0.852, 0.59, "Gated Routing ($R \\geq \\tau^*$)", ha="center", va="center",
            fontsize=6.8, fontweight="bold", color="#166534",
            bbox=dict(boxstyle="round,pad=0.22", fc="#FFFFFF", ec="#16A34A", lw=0.8, zorder=6))

    # 5. Dual Inputs into Always-Check Consensus (Orthogonal Corridor Routing)
    # A) Vertical arrow from Verifier on Original into Always-Check top
    draw_arrow(ax, (0.557, 0.48), (0.557, 0.41), color="#DC2626", lw=1.3)
    ax.text(0.557, 0.445, "Dual Consensus", ha="center", va="center",
            fontsize=6.7, fontweight="bold", color="#DC2626",
            bbox=dict(boxstyle="round,pad=0.20", fc="#FFFFFF", ec="#DC2626", lw=0.7, zorder=6))
    
    # B) Stepped orthogonal line from Verifier on Translation down through open corridor (x=0.692)
    # Line steps right from (0.670, 0.77) to (0.692, 0.77), then down to (0.692, 0.35), then left into Always-Check
    ax.plot([0.670, 0.692, 0.692, 0.670], [0.77, 0.77, 0.35, 0.35], color="#DC2626", lw=1.2, zorder=5)
    draw_arrow(ax, (0.692, 0.35), (0.670, 0.35), color="#DC2626", lw=1.2)
    # Small label on the corridor line, perfectly centered in open space
    ax.text(0.692, 0.56, "$P_{\\mathrm{trans}}$", ha="center", va="center",
            fontsize=6.5, fontweight="bold", color="#DC2626",
            bbox=dict(boxstyle="round,pad=0.15", fc="#FFFFFF", ec="#DC2626", lw=0.6, zorder=6))

    # 6. Always-Check -> Causal Error Attribution
    draw_arrow(ax, (0.445, 0.24), (0.415, 0.24), color="#64748B", lw=1.3)
    # Badge placed neatly ABOVE the arrow so line passes completely unobstructed
    ax.text(0.430, 0.275, "Paired Matrix", ha="center", va="center",
            fontsize=6.5, fontweight="bold", color="#334155",
            bbox=dict(boxstyle="round,pad=0.20", fc="#FFFFFF", ec="#64748B", lw=0.6, zorder=6))

    fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
    fig.savefig(PDF_DIR / "fig1_study_workflow.pdf", bbox_inches="tight", pad_inches=0.03, dpi=300)
    fig.savefig(SRC_DIR / "fig1_study_workflow.png", bbox_inches="tight", pad_inches=0.03, dpi=300)
    plt.close(fig)
    print("Regenerated fig1_study_workflow.pdf and fig1_study_workflow.png successfully.")

if __name__ == "__main__":
    main()
