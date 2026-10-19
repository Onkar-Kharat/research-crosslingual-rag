import json
import csv
import pandas as pd
import numpy as np
from pathlib import Path

WORKSPACE = Path(r"c:\Users\Onkar\OneDrive\Desktop\Research_crosslingual_rag_research")
ANN_DIR = WORKSPACE / "annotation"
ANN_DIR.mkdir(parents=True, exist_ok=True)

def generate_sample():
    preds_df = pd.read_csv(WORKSPACE / "experiments" / "results" / "test_predictions.csv")
    
    # Load original texts from test_translated.jsonl
    test_jsonl = WORKSPACE / "data" / "processed" / "test_translated.jsonl"
    item_texts = {}
    with open(test_jsonl, "r", encoding="utf-8") as f:
        for line in f:
            d = json.loads(line)
            item_texts[d["item_id"]] = {
                "claim": d["claim"],
                "original_evidence": d["original_evidence"],
                "translated_evidence": d.get("translated_evidence", "")
            }
            
    yt = preds_df["gold_label"].to_numpy()
    pt = preds_df["pred_translated"].to_numpy()
    po = preds_df["pred_original"].to_numpy()
    
    # Identify strata
    # Stratum 1: E_trans (pt wrong, po correct)
    idx_e_trans = preds_df.index[(pt != yt) & (po == yt)].tolist()
    # Stratum 2: E_verif (pt wrong, po wrong, yt == CONTRADICTED)
    idx_e_verif = preds_df.index[(pt != yt) & (po != yt) & (yt == "CONTRADICTED")].tolist()
    # Stratum 3: Both correct (pt correct, po correct)
    idx_both_corr = preds_df.index[(pt == yt) & (po == yt)].tolist()
    
    print(f"Strata sizes: E_trans={len(idx_e_trans)}, E_verif={len(idx_e_verif)}, Both_Correct={len(idx_both_corr)}")
    
    rng = np.random.default_rng(42)
    sample_trans = rng.choice(idx_e_trans, size=20, replace=False).tolist()
    sample_verif = rng.choice(idx_e_verif, size=20, replace=False).tolist()
    sample_corr = rng.choice(idx_both_corr, size=10, replace=False).tolist()
    
    all_sampled_indices = sample_trans + sample_verif + sample_corr
    rng.shuffle(all_sampled_indices)
    
    blinded_rows = []
    audit_key_rows = []
    
    for i, idx in enumerate(all_sampled_indices, 1):
        sample_id = f"ANN-{i:02d}"
        row = preds_df.iloc[idx]
        item_id = row["item_id"]
        txt = item_texts.get(item_id, {})
        
        # Determine stratum name for internal key
        if idx in sample_trans:
            stratum = "E_trans (Recovered by original)"
        elif idx in sample_verif:
            stratum = "E_verif (Reasoning failure on contradicted)"
        else:
            stratum = "Control (Both correct)"
            
        blinded_rows.append({
            "Sample_ID": sample_id,
            "Item_ID": item_id,
            "Claim_Hindi": txt.get("claim", row["claim"]),
            "Original_Evidence_Hindi": txt.get("original_evidence", ""),
            "Machine_Translation_English": txt.get("translated_evidence", ""),
            "Annotator_1_Fidelity": "",
            "Annotator_1_Distortion_Types": "",
            "Annotator_1_Notes": "",
            "Annotator_2_Fidelity": "",
            "Annotator_2_Distortion_Types": "",
            "Annotator_2_Notes": "",
            "Adjudication_Consensus": "",
            "Final_Distortion_Types": ""
        })
        
        audit_key_rows.append({
            "Sample_ID": sample_id,
            "Item_ID": item_id,
            "Sampling_Stratum": stratum,
            "Gold_Label": row["gold_label"],
            "Pred_Translated": row["pred_translated"],
            "Pred_Original": row["pred_original"]
        })
        
    # Write blinded CSV
    blinded_csv = ANN_DIR / "blinded_annotation_sample.csv"
    pd.DataFrame(blinded_rows).to_csv(blinded_csv, index=False)
    print(f"Wrote 50 blinded annotation items to {blinded_csv}")
    
    # Write internal audit key
    key_csv = ANN_DIR / "internal_audit_sampling_key.csv"
    pd.DataFrame(audit_key_rows).to_csv(key_csv, index=False)
    print(f"Wrote internal audit sampling key to {key_csv}")

if __name__ == "__main__":
    generate_sample()
