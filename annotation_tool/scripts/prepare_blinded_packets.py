"""
Prepares independent, randomized, blinded annotation packets for real bilingual annotators.
Deterministic stratified sampling with fixed seed 42 from canonical test predictions.
Generates Packet A (Annotator 1) and Packet B (Annotator 2) with distinct opaque IDs and orders.
"""
import json
import csv
import shutil
import zipfile
from pathlib import Path
import pandas as pd
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
CANONICAL_PREDS = PROJECT_ROOT / "experiments" / "results_canonical" / "canonical_test_predictions.csv"
PACKETS_DIR = PROJECT_ROOT / "annotation_tool" / "packets"
TOOL_DIR = PROJECT_ROOT / "annotation_tool"
KEY_PATH = TOOL_DIR / "internal_analysis_key.csv"

def generate_packets():
    assert CANONICAL_PREDS.exists(), f"Canonical predictions not found: {CANONICAL_PREDS}"
    df = pd.read_csv(CANONICAL_PREDS)
    
    yt = df["gold_label"].values
    pt = df["pred_translated"].values
    po = df["pred_original"].values

    s_trans_df = df[(pt != yt) & (po == yt)].copy()
    s_verif_df = df[(pt != yt) & (po != yt)].copy()
    control_df = df[(pt == yt) & (po == yt)].copy()

    s_trans_df["sampling_stratum"] = "Stratum_1_S_trans (Operational Translation Error)"
    s_verif_df["sampling_stratum"] = "Stratum_2_S_verif (Operational Verifier Error)"
    control_df["sampling_stratum"] = "Stratum_3_Control (Both Languages Correct)"

    sample_trans = s_trans_df.sample(n=20, random_state=42)
    sample_verif = s_verif_df.sample(n=20, random_state=42)
    sample_ctrl = control_df.sample(n=10, random_state=42)

    sample_50 = pd.concat([sample_trans, sample_verif, sample_ctrl], ignore_index=True)
    assert len(sample_50) == 50
    assert len(sample_50["item_id"].unique()) == 50

    # Create Packet A with random permutation (seed 101)
    perm_a = np.random.default_rng(101).permutation(50)
    df_a = sample_50.iloc[perm_a].copy().reset_index(drop=True)
    df_a["opaque_item_id"] = [f"OPQ-A-{i+1:02d}" for i in range(50)]

    # Create Packet B with independent random permutation (seed 202)
    perm_b = np.random.default_rng(202).permutation(50)
    df_b = sample_50.iloc[perm_b].copy().reset_index(drop=True)
    df_b["opaque_item_id"] = [f"OPQ-B-{i+1:02d}" for i in range(50)]

    # Analysis Key mapping
    key_rows = []
    for _, row in sample_50.iterrows():
        iid = row["item_id"]
        opq_a = df_a[df_a["item_id"] == iid]["opaque_item_id"].values[0]
        opq_b = df_b[df_b["item_id"] == iid]["opaque_item_id"].values[0]
        key_rows.append({
            "item_id": iid,
            "opaque_item_id_A": opq_a,
            "opaque_item_id_B": opq_b,
            "sampling_stratum": row["sampling_stratum"],
            "gold_label": row["gold_label"],
            "pred_translated": row["pred_translated"],
            "pred_original": row["pred_original"]
        })
    key_df = pd.DataFrame(key_rows).sort_values("item_id")
    key_df.to_csv(KEY_PATH, index=False)
    print(f"Saved secret analysis key to {KEY_PATH}")

    # Prepare sanitized public packet payloads
    blinded_cols = ["opaque_item_id", "claim_hindi", "original_evidence_hindi", "translated_evidence_english"]
    
    # Packet A export
    df_a_clean = df_a.rename(columns={
        "claim": "claim_hindi",
        "original_evidence": "original_evidence_hindi",
        "gen_translated_evidence": "translated_evidence_english"
    })[blinded_cols]
    
    # Packet B export
    df_b_clean = df_b.rename(columns={
        "claim": "claim_hindi",
        "original_evidence": "original_evidence_hindi",
        "gen_translated_evidence": "translated_evidence_english"
    })[blinded_cols]

    # Save JSON and CSV formats
    packet_a_json = PACKETS_DIR / "packet_A.json"
    packet_a_csv = PACKETS_DIR / "packet_A.csv"
    packet_b_json = PACKETS_DIR / "packet_B.json"
    packet_b_csv = PACKETS_DIR / "packet_B.csv"

    payload_a = {
        "packet_id": "PACKET-A",
        "annotator_code": "A1",
        "protocol_version": "2.0",
        "total_items": 50,
        "items": df_a_clean.to_dict(orient="records")
    }
    payload_b = {
        "packet_id": "PACKET-B",
        "annotator_code": "A2",
        "protocol_version": "2.0",
        "total_items": 50,
        "items": df_b_clean.to_dict(orient="records")
    }

    with open(packet_a_json, "w", encoding="utf-8") as f:
        json.dump(payload_a, f, indent=2, ensure_ascii=False)
    df_a_clean.to_csv(packet_a_csv, index=False)

    with open(packet_b_json, "w", encoding="utf-8") as f:
        json.dump(payload_b, f, indent=2, ensure_ascii=False)
    df_b_clean.to_csv(packet_b_csv, index=False)

    print(f"Generated Packet A: {packet_a_json.name} ({len(df_a_clean)} items)")
    print(f"Generated Packet B: {packet_b_json.name} ({len(df_b_clean)} items)")

if __name__ == "__main__":
    generate_packets()
