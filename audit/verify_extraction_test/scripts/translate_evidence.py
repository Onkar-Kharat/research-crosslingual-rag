"""
Translate Hindi evidence passages into English using Helsinki-NLP/opus-mt-hi-en.
Caches outputs into data/processed/dev_translated.jsonl and test_translated.jsonl.
Extracts translation fidelity features (number and entity preservation).
"""
import re
import json
import time
from pathlib import Path
from tqdm import tqdm
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

MODEL_NAME = "Helsinki-NLP/opus-mt-hi-en"

def extract_numbers(text: str) -> set[str]:
    # Extracts Western and Devanagari numerals
    devanagari_nums = {"०": "0", "१": "1", "२": "2", "३": "3", "४": "4", "५": "5", "६": "6", "७": "7", "८": "8", "९": "9"}
    norm_text = "".join(devanagari_nums.get(c, c) for c in text)
    return set(re.findall(r"\b\d+(?:[\.,]\d+)?\b", norm_text))

def translate_dataset(input_file: Path, output_file: Path, tokenizer, model, device):
    if output_file.exists():
        print(f"{output_file} already exists. Skipping translation.")
        return

    with open(input_file, "r", encoding="utf-8") as f:
        items = [json.loads(line) for line in f]

    print(f"Translating {len(items)} items from {input_file}...")
    start_time = time.time()
    
    translated_items = []
    # Process in batches of 8 for CPU efficiency
    batch_size = 8
    for i in tqdm(range(0, len(items), batch_size), desc=f"Translating {input_file.stem}"):
        batch = items[i:i+batch_size]
        # Clean evidence to reasonable length for MarianMT (truncate to 512 tokens)
        texts_to_trans = [item["original_evidence"][:1000] for item in batch]
        
        inputs = tokenizer(texts_to_trans, return_tensors="pt", padding=True, truncation=True, max_length=512).to(device)
        with torch.no_grad():
            outputs = model.generate(**inputs, max_length=512, num_beams=2)
        
        translations = [tokenizer.decode(t, skip_special_tokens=True) for t in outputs]
        
        for item, trans in zip(batch, translations):
            item_copy = dict(item)
            item_copy["translated_evidence"] = trans
            
            # Compute heuristic entity & number preservation
            orig_nums = extract_numbers(item["original_evidence"])
            trans_nums = extract_numbers(trans)
            num_overlap = len(orig_nums.intersection(trans_nums)) / max(1, len(orig_nums)) if orig_nums else 1.0
            
            item_copy["feature_number_overlap"] = round(num_overlap, 4)
            item_copy["feature_char_ratio"] = round(len(trans) / max(1, len(item["original_evidence"])), 4)
            translated_items.append(item_copy)

    elapsed = time.time() - start_time
    print(f"Finished {len(translated_items)} items in {elapsed:.2f}s ({elapsed/len(translated_items):.3f}s/item).")
    
    with open(output_file, "w", encoding="utf-8") as f:
        for item in translated_items:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
    print(f"Wrote {output_file}")

def main():
    device = torch.device("cpu")
    print(f"Loading {MODEL_NAME} on {device}...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME).to(device)
    model.eval()

    dev_in = Path("data/processed/dev.jsonl")
    dev_out = Path("data/processed/dev_translated.jsonl")
    translate_dataset(dev_in, dev_out, tokenizer, model, device)

    test_in = Path("data/processed/test.jsonl")
    test_out = Path("data/processed/test_translated.jsonl")
    translate_dataset(test_in, test_out, tokenizer, model, device)

if __name__ == "__main__":
    main()
