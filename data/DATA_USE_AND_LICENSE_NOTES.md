# DATA USE, PROVENANCE, AND LICENSING NOTES

**Project:** Cross-Lingual Claim Verification Diagnostic Study  
**Document Identifier:** `data/DATA_USE_AND_LICENSE_NOTES.md`  
**Date:** 2026-10-19  
**Status:** COMPLETE (Addresses Independent Audit Issue 8 / P1)

---

## 1. Multi-Tier Intellectual Property & Licensing Breakdown

Rather than relying on an undifferentiated, blanket assertion of "fair use," this document delineates the specific licenses, data provenance, and terms of use across all four tiers of the research pipeline:

```
+-----------------------------------------------------------------------------------+
|                                 RESEARCH TIERS                                    |
+--------------------------+----------------------------+---------------------------+
| 1. Research Code         | 2. Foundation Models       | 3. Source Benchmark       |
|    - MIT / Apache 2.0    |    - MarianMT (CC-BY-4.0)  |    - X-Fact (Apache 2.0)  |
|    - Fully Open Source   |    - mDeBERTa-v3 (MIT)     |    - Third-Party Snippets |
+--------------------------+----------------------------+---------------------------+
```

---

## 2. Component-by-Component Licensing Details

### Tier 1: Project Software and Analysis Scripts
- **Artifacts:** All python code in `scripts/`, test suites in `tests/`, and protocol specifications in `protocol/`.
- **License:** Apache License 2.0 / MIT License.
- **Terms:** Freely redistributable and modifiable for academic and commercial research with attribution.
- **Redaction:** Absolute local file paths, personal usernames, and environment tokens have been completely sanitized.

### Tier 2: Pre-trained Foundation Models
1. **Machine Translation Engine:**
   - **Model Identifier:** `Helsinki-NLP/opus-mt-hi-en` (MarianMT architecture; Tiedemann & Thottingal, EAMT 2020).
   - **Provenance:** HuggingFace Model Hub (`https://huggingface.co/Helsinki-NLP/opus-mt-hi-en`).
   - **License:** CC-BY-4.0 (Creative Commons Attribution 4.0 International).
   - **Usage:** Run locally in offline inference mode on CPU.
2. **Cross-Lingual Verifier Engine:**
   - **Model Identifier:** `MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7` (Laurer et al., 2024).
   - **Provenance:** HuggingFace Model Hub (`https://huggingface.co/MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7`).
   - **License:** MIT License.
   - **Training Data Provenance:** mDeBERTa-v3 base pretrained on CC100, fine-tuned on multilingual NLI (XNLI).
   - **Usage:** Run locally in offline evaluation mode on CPU.

### Tier 3: Benchmark Datasets and Evidence Snippets
1. **Benchmark Metadata & Structural Annotations:**
   - **Dataset:** X-Fact (Gupta & Srikumar, ACL-IJCNLP 2021).
   - **Provenance:** University of Utah NLP (`https://github.com/utahnlp/x-fact`).
   - **License:** Apache License 2.0.
   - **Scope:** Claim text, fact-checking organization URL, verification dates, and raw categorical veracity labels.
2. **Web Evidence Snippets:**
   - **Nature:** Short text excerpts (search engine snippets) automatically extracted by the X-Fact authors from public fact-checking articles (e.g., Aaj Tak, Factly, Vishwas News).
   - **Legal Basis for Research Use:**
     - In accordance with standard NLP benchmark conventions, these snippets are processed strictly for non-commercial, transformative academic evaluation of factual consistency.
     - Direct permalinks to the original publishing sources (`source_url`) are preserved for every example in `data/processed/` and `data/raw/` to ensure attribution to original journalistic fact-checkers.
     - No full copyrighted article texts are cached or distributed.

---

## 3. Computational and Offline Privacy Assurances
- **No Cloud API Calls:** All inference is executed locally using pre-downloaded model checkpoints via PyTorch and HuggingFace Transformers.
- **No Data Exfiltration:** Neither claim texts, evidence snippets, nor generated predictions are transmitted to external proprietary endpoints (e.g., OpenAI, Google Cloud, Anthropic).
- **Audit Reproduction:** Any researcher running the reproduction bundle can replicate the environment completely offline without active internet connectivity once weights are cached.
