# BILINGUAL HUMAN ANNOTATION GUIDE: TRANSLATION FIDELITY IN CLAIM VERIFICATION

**Language Pair:** Hindi (Source) $\rightarrow$ English (Target)  
**Task:** Diagnostic Evaluation of Machine-Translated Evidence for Automated Fact Verification

---

## 1. Objective of the Annotation

In cross-lingual automated fact-checking, non-English evidence passages are frequently translated into English before being evaluated by an automated verifier. When an automated verifier makes an error, the failure could be caused by:
1. **Translation-Fidelity Corruption:** The machine translation altered, dropped, or distorted claim-critical factual details (e.g., numbers, negation, named entities, dates).
2. **Verifier-Reasoning Shortcoming:** The machine translation faithfully conveyed the factual meaning of the Hindi passage, but the computer model failed to comprehend or deduce the correct conclusion.

Your role as a bilingual annotator is to read the original Hindi claim and evidence passage alongside the machine-translated English passage, and determine whether the translation faithfully preserved the factual semantics relevant to verifying the claim.

---

## 2. Blinded Annotation Protocol

To prevent bias:
- You will **NOT** be shown whether the model was right or wrong.
- You will **NOT** be shown the automated prediction or the proposed error category.
- You will judge each translation purely on its linguistic and semantic fidelity relative to the original Hindi source text and the claim.

---

## 3. Annotation Taxonomy and Codes

For each item, assign exactly one primary **Fidelity Code (Col D)** and indicate any **Specific Distortion Types (Col E)**:

### Primary Fidelity Code (Col D):
- **`PRESERVED` (Faithful):** The English translation preserves the essential factual meaning of the Hindi evidence. A human or verifier reading only the English text would reach the exact same factual conclusion about the claim as one reading the original Hindi. Minor grammatical awkwardness or stylistic imperfections that do not alter factual claims should still be marked `PRESERVED`.
- **`ALTERED` (Meaning Corrupted):** The English translation distorts, inverts, or garbles claim-critical factual semantics. An English reader would be misled or unable to deduce the truth of the claim due to the translation.
- **`AMBIGUOUS` (Insufficient / Garbled):** The original Hindi evidence itself is fundamentally ambiguous, incomplete, or truncated, such that no clear judgment can be formed regardless of translation quality.
- **`UNABLE_TO_DECIDE`:** The annotator is uncertain or context is missing.

### Specific Distortion Types (Col E, select all that apply if `ALTERED`):
1. **`NUM_DATE` (Numerical or Date Distortion):** A quantity, monetary figure, percentage, or date was changed, dropped, or corrupted (e.g., Devanagari numerals mis-transliterated, millions confused with crores).
2. **`NEGATION` (Polarity Inversion):** A negation marker (e.g., नहीं, मत, ना) was omitted, added, or neutralized, flipping the factual stance from denial to affirmation.
3. **`ENTITY` (Named Entity Corruption):** A person, organization, political party, location, or acronym was mistranslated into an unrelated common word or scrambled (e.g., proper nouns translated literally).
4. **`OMISSION` (Critical Content Dropped):** Crucial clauses or qualifiers present in the Hindi evidence are missing from the English translation.
5. **`HALLUCINATION` (Fabricated Content):** The translation introduces assertions or words not present in the original Hindi text.

---

## 4. Concrete Examples

### Example 1: `ALTERED` (Distortion: `ENTITY`, `HALLUCINATION`)
- **Claim (Hindi):** शामली की एक मस्जिद में हथियारों का जखीरा बरामद हुआ। (A cache of weapons was recovered from a mosque in Shamli.)
- **Evidence (Hindi):** शामली पुलिस ने मस्जिद में हथियारों के मिलने की खबर का खंडन किया है।
- **Machine Translation:** Shamim fuck welded from a moustik police refuted...
- **Annotation:**
  - `Fidelity_Code`: **`ALTERED`**
  - `Distortion_Type`: **`ENTITY, HALLUCINATION`**
  - `Rationale`: Scrambled named entity 'शामली' and garbled translation introduced vulgarity and destroyed the semantic context of the police refutation.

### Example 2: `ALTERED` (Distortion: `NUM_DATE`, `NEGATION`)
- **Claim (Hindi):** सरकार ने 500 रुपये के नोट बंद करने का फैसला लिया।
- **Evidence (Hindi):** आरबीआई ने स्पष्ट किया कि 500 रुपये के नोट बंद नहीं किए जा रहे हैं।
- **Machine Translation:** RBI clarified that Rs 500 notes are being closed.
- **Annotation:**
  - `Fidelity_Code`: **`ALTERED`**
  - `Distortion_Type`: **`NEGATION`**
  - `Rationale`: The negation marker 'नहीं' was dropped in translation, making the statement affirm the closure rather than refute it.

### Example 3: `PRESERVED`
- **Claim (Hindi):** वायरल वीडियो में दिख रहा व्यक्ति भाजपा नेता है।
- **Evidence (Hindi):** जांच में पाया गया कि वीडियो में मौजूद व्यक्ति आम नागरिक है और उसका किसी राजनीतिक दल से संबंध नहीं है।
- **Machine Translation:** Investigation revealed that the person present in the video is a common citizen and has no connection with any political party.
- **Annotation:**
  - `Fidelity_Code`: **`PRESERVED`**
  - `Distortion_Type`: **`NONE`**
  - `Rationale`: The factual meaning and negation are completely and accurately preserved.
