# DATA PROVENANCE AND LICENSES

**Date:** 2026-10-19  
**Repository:** `research-crosslingual-rag`  
**License Compliance:** Fully Permissible Open-Source / Academic Use

---

## 1. Upstream Data Sources and Provenance

### Primary Dataset: X-Fact (Multilingual Fact Checking Benchmark)
- **Source Repository:** `https://github.com/utahnlp/x-fact`
- **Citation:**
  ```bibtex
  @inproceedings{gupta-srikumar-2021-x-fact,
      title = "{X}-{FACT}: A New Benchmark Dataset for Multilingual Fact Checking",
      author = "Gupta, Ashkan  and  Srikumar, Vivek",
      booktitle = "Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing (Volume 2: Short Papers)",
      year = "2021",
      pages = "675--682",
      doi = "10.18653/v1/2021.acl-short.86"
  }
  ```
- **License:** MIT License. Full text preserved in `data/raw/LICENSE_xfact.txt`.
- **Redistribution Terms:** The MIT License grants free permission to use, copy, modify, merge, publish, distribute, sublicense, and sell copies of the software and associated documentation files, subject to preserving the copyright notice and permission notice.

---

## 2. Model Checkpoints and Licenses

### Machine Translation Model
- **Model:** `Helsinki-NLP/opus-mt-hi-en`
- **Source:** HuggingFace Hub (`https://huggingface.co/Helsinki-NLP/opus-mt-hi-en`)
- **License:** CC-BY-4.0 (Creative Commons Attribution 4.0 International)
- **Usage:** Pretrained translation on public OPUS corpora; executed entirely locally on CPU without external API calls.

### Cross-Lingual Verifier Model
- **Model:** `MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7`
- **Source:** HuggingFace Hub (`https://huggingface.co/MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7`)
- **Base Architecture:** Microsoft mDeBERTa-v3-base (Apache 2.0 License)
- **Fine-Tuning:** Multilingual NLI (XNLI, CC-BY-NC 4.0 / Open Research)
- **Usage:** Sequence classification inference executed locally on CPU.

---

## 3. Data File Integrity and Hashes

| File | Relative Path | Size (Bytes) | SHA-256 Checksum |
|:---|:---|:---:|:---|
| **Raw Dev** | `data/raw/dev.all.tsv` | 5,245,528 | `78e348981dfc3eaee8b8ea5f72cf0eec45c11bc0beeb5d6a2f3beee4fa5f0ae8` |
| **Raw Test** | `data/raw/test.all.tsv` | 7,874,799 | `a93b4a20b0805c862bcbe6a9485b0d5c48b26002f5a60e0a5c0bf33cfd95b584` |
| **Processed Dev** | `data/processed/dev.jsonl` | 398,404 | `7995a8507ba3ca368e73ee034983a48e7156955a1532ff7754b2d493ba4f74d0` |
| **Processed Test** | `data/processed/test.jsonl` | 620,904 | `b7bb577e1136bfe611a938b8c5ff21dbbe5b9ea426fe413009761e155bc8ee4a` |
| **Translated Dev** | `data/processed/dev_translated.jsonl` | 424,801 | `d2d9ecb9b940e4f454f76274e1d5306637ef8fa176a928ba5691f1a5477d9c66` |
| **Translated Test** | `data/processed/test_translated.jsonl` | 661,969 | `f1db55c197fa1481cfd2fb7ddc4a969fba75323a7bbec42cbfb9d0b67ff9b94b` |

All processed and raw dataset files are legally redistributable within the final reproducibility research package.
