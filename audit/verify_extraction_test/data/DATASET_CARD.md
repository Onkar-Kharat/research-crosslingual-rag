# Dataset Card: X-Fact Hindi Claim Verification Benchmark

## 1. Dataset Description
- **Dataset Name:** X-Fact (Hindi Partition)
- **Primary Authors:** Ashkan Gupta, Vivek Srikumar (University of Utah)
- **Publication:** ACL-IJCNLP 2021 (*"X-FACT: A New Benchmark Dataset for Multilingual Fact Checking"*)
- **Repository:** `https://github.com/utahnlp/x-fact`
- **License:** MIT License
- **Language:** Hindi (`hi`) with target translation into English (`en`)

## 2. Dataset Structure and Instances
The dataset consists of authentic claims evaluated by professional fact-checking organizations in India (e.g., Aaj Tak, Newschecker Hindi, Dainik Bhaskar), paired with pre-retrieved web search snippets.

### Instance Schema:
- `item_id`: Unique persistent identifier (`xfact-hi-{split}-{index:04d}`)
- `claim`: Natural language claim in Hindi
- `original_evidence`: Concatenated search result snippets in Hindi
- `original_language`: `hi`
- `translated_evidence`: English translation generated via `Helsinki-NLP/opus-mt-hi-en`
- `target_language`: `en`
- `gold_label`: Standardized veracity classification (`CONTRADICTED`, `INSUFFICIENT_EVIDENCE`)
- `raw_gold_label`: Original rating from fact-checking source
- `split`: `dev` or `test`
- `source_dataset`: `utahnlp/x-fact`
- `source_url`: URL of the debunking article

## 3. Label Distribution and Class Balance
Authentic fact-checks in Hindi almost exclusively target false rumors and misleading misinformation. Verified true statements are unrepresented in the corpus.

| Partition | Total Items | CONTRADICTED (`false` / `mostly false`) | INSUFFICIENT_EVIDENCE (`partly true` / `misleading`) | SUPPORTED (`true` / `mostly true`) |
|:---|:---:|:---:|:---:|:---:|
| **Development** | 103 | 89 (86.41%) | 14 (13.59%) | **0 (0.00%)** |
| **Held-Out Test** | 163 | 142 (87.12%) | 21 (12.88%) | **0 (0.00%)** |
| **Combined** | 266 | 231 (86.84%) | 35 (13.16%) | **0 (0.00%)** |

### Critical Usage Note:
Because positive claims are absent, evaluating standard 3-class NLI models results in severe class imbalance and penalizes 3-class Macro-F1 scores (due to 0 recall on `SUPPORTED`). Researchers must evaluate and report observed 2-class metrics alongside 3-class metrics.

## 4. Evidence Pipeline Caveat
Evidence passages are static web search snippets captured at benchmark creation time. The dataset does not include a dynamic document index; experiments evaluate claim verification given evidence, not live document retrieval.
