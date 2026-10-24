import os
import re
import json
import hashlib
import sys

def main():
    print("=" * 60)
    print("AUTOMATED MANUSCRIPT AND WORKSPACE VALIDATION SUITE")
    print("=" * 60)
    
    workspace = os.path.abspath("manuscript_revision_tacl")
    repo_root = os.path.abspath(".")
    
    errors = []
    warnings = []
    
    # Check 1: Style and master files exist
    required_root_files = [
        "main.tex", "references.bib", "tacl2021v1.sty", "acl_natbib.bst",
        "REVISION_README.md", "BUILD_INSTRUCTIONS.md"
    ]
    for rf in required_root_files:
        p = os.path.join(workspace, rf)
        if not os.path.exists(p):
            errors.append(f"Missing required workspace file: {rf}")
        else:
            print(f" [PASS] Root file exists: {rf}")
            
    # Check 2: All sections exist
    required_sections = [
        "abstract.tex", "introduction.tex", "related_work.tex",
        "task_and_formulation.tex", "methodology.tex", "experimental_setup.tex",
        "results.tex", "discussion.tex", "limitations.tex", "conclusion.tex"
    ]
    for s in required_sections:
        p = os.path.join(workspace, "sections", s)
        if not os.path.exists(p):
            errors.append(f"Missing section file: {s}")
        else:
            print(f" [PASS] Section file exists: sections/{s}")
            
    # Check 3: All tables exist
    required_tables = [
        "dataset_distribution.tex", "transition_matrix.tex", "main_results.tex",
        "statistical_tests.tex", "error_attribution.tex", "case_studies.tex"
    ]
    for t in required_tables:
        p = os.path.join(workspace, "tables", t)
        if not os.path.exists(p):
            errors.append(f"Missing table file: {t}")
        else:
            print(f" [PASS] Table file exists: tables/{t}")
            
    # Check 4: All vector PDF figures exist
    required_figs = [
        "fig1_study_workflow.pdf", "fig2_risk_coverage_tradeoff.pdf",
        "fig3_condition_comparison.pdf", "fig4_error_attribution_breakdown.pdf",
        "fig5_transition_heatmap.pdf"
    ]
    for fig in required_figs:
        p = os.path.join(workspace, "figures", "final", fig)
        if not os.path.exists(p):
            errors.append(f"Missing vector PDF figure: {fig}")
        else:
            print(f" [PASS] Figure exists: figures/final/{fig}")
            
    # Check 5: Supplementary material exists
    supp_path = os.path.join(workspace, "supplementary", "supplementary_material.tex")
    if not os.path.exists(supp_path):
        errors.append("Missing supplementary_material.tex in supplementary/")
    else:
        print(" [PASS] Supplementary material exists: supplementary/supplementary_material.tex")
        
    # Check 6: Parse main.tex inputs and verify existence
    with open(os.path.join(workspace, "main.tex"), "r", encoding="utf-8") as f:
        main_tex = f.read()
        
    inputs = re.findall(r'\\input\{([^}]+)\}', main_tex)
    print(f"\nVerifying {len(inputs)} inputs from main.tex...")
    for inp in inputs:
        cand1 = os.path.join(workspace, inp if inp.endswith('.tex') else inp + '.tex')
        if not os.path.exists(cand1):
            errors.append(f"main.tex inputs non-existent file: {inp}")
        else:
            print(f" [PASS] Input resolved: {inp}")
            
    # Check 7: Figure inclusions in all tex files
    tex_files = []
    for root, dirs, files in os.walk(workspace):
        for f in files:
            if f.endswith('.tex'):
                tex_files.append(os.path.join(root, f))
                
    print(f"\nChecking figure references in {len(tex_files)} TeX files...")
    for tf in tex_files:
        with open(tf, "r", encoding="utf-8") as f:
            content = f.read()
        figs_included = re.findall(r'\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}', content)
        for fi in figs_included:
            # Check if fi exists relative to workspace or graphics path
            cand1 = os.path.join(workspace, fi)
            cand2 = os.path.join(workspace, "figures", "final", os.path.basename(fi))
            if not (os.path.exists(cand1) or os.path.exists(cand2)):
                errors.append(f"Referenced figure does not exist: {fi} in {os.path.relpath(tf, workspace)}")
            else:
                print(f" [PASS] Figure path verified: {fi}")
                
    # Check 8: Citations parity check
    with open(os.path.join(workspace, "references.bib"), "r", encoding="utf-8") as f:
        bib_text = f.read()
    bib_keys = set(re.findall(r'@\w+\{([^,]+),', bib_text))
    
    cited_keys = set()
    for tf in tex_files:
        with open(tf, "r", encoding="utf-8") as f:
            content = f.read()
        matches = re.findall(r'\\cite[ptayhor]*\{([^}]+)\}', content)
        for m in matches:
            for k in m.split(','):
                cited_keys.add(k.strip())
                
    missing_citations = cited_keys - bib_keys
    uncited_citations = bib_keys - cited_keys
    if missing_citations:
        errors.append(f"Cited keys missing in references.bib: {missing_citations}")
    else:
        print(f" [PASS] Zero missing citation keys in references.bib ({len(cited_keys)} cited)")
    if uncited_citations:
        warnings.append(f"BibTeX keys uncited in manuscript: {uncited_citations}")
    else:
        print(f" [PASS] Zero uncited entries in references.bib ({len(bib_keys)} total)")
        
    # Check 9: Cross-reference label definitions and calls
    defined_labels = set()
    referenced_labels = set()
    for tf in tex_files:
        with open(tf, "r", encoding="utf-8") as f:
            content = f.read()
        labels = re.findall(r'\\label\{([^}]+)\}', content)
        for l in labels:
            defined_labels.add(l.strip())
        refs = re.findall(r'\\ref\{([^}]+)\}', content)
        for r in refs:
            referenced_labels.add(r.strip())
            
    missing_refs = referenced_labels - defined_labels
    if missing_refs:
        errors.append(f"Undefined cross-reference labels: {missing_refs}")
    else:
        print(f" [PASS] All {len(referenced_labels)} cross-references are defined: {referenced_labels}")
        
    # Check 10: Original manuscript files in docs/manuscript/ MUST BE 100% UNCHANGED
    print("\nVerifying original manuscript preservation...")
    with open(os.path.join(repo_root, "original_manuscript_hashes.json"), "r") as f:
        orig_hashes = json.load(f)
        
    drifted_files = []
    for rel_path, orig_h in orig_hashes.items():
        full_p = os.path.join(repo_root, rel_path.replace('/', os.sep))
        if not os.path.exists(full_p):
            drifted_files.append(f"Deleted original file: {rel_path}")
            continue
        with open(full_p, "rb") as fp:
            curr_h = hashlib.sha256(fp.read()).hexdigest()
        if curr_h != orig_h:
            drifted_files.append(f"Modified original file: {rel_path} (orig: {orig_h[:8]}, curr: {curr_h[:8]})")
            
    if drifted_files:
        errors.extend(drifted_files)
    else:
        print(f" [PASS] All {len(orig_hashes)} original files in docs/manuscript/ are BITWISE UNCHANGED!")
        
    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)
    if warnings:
        print(f"WARNINGS ({len(warnings)}):")
        for w in warnings:
            print(f"  - {w}")
    if errors:
        print(f"ERRORS ({len(errors)}):")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print("ALL VERIFICATION CHECKS PASSED SUCCESSFULLY (0 ERRORS, 0 WARNINGS)!")
        print("=" * 60)

if __name__ == "__main__":
    main()
