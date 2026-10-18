# Bilingual Annotator Instructions: Translation Fidelity Evaluation

**Language Pair:** Hindi (Source) $\rightarrow$ English (Target)  
**Study Task:** Evaluating semantic fidelity of machine-translated evidence in claim verification  
**Estimated Effort:** ~45 to 60 minutes (50 items)  

---

## 1. Welcome and Purpose

Thank you for participating as an independent bilingual evaluator!

In automated fact-checking systems, evidence documents in Hindi are often automatically translated into English before being analyzed by automated verification algorithms. If an automated verifier makes an error, that error might be caused by:
1. **Translation Distortion:** The machine translation altered, dropped, or distorted factual meaning (e.g., numbers, negation, named entities).
2. **Algorithm Shortcoming:** The machine translation was faithful, but the computer reasoning model made a mistake.

**Your Goal:** Read the Hindi claim and evidence alongside the machine-translated English evidence, and decide whether the English translation faithfully preserved the factual meaning relevant to the claim.

> **CRITICAL RULE:** Do NOT decide whether the claim is true or false in the real world. Your job is ONLY to judge translation accuracy: **Does the English translation say what the Hindi evidence says?**

---

## 2. Decision Taxonomy

### Primary Fidelity Labels (Choose exactly one per item):

1. **`PRESERVED` (Faithful):**
   - The English translation preserves the essential factual meaning of the Hindi evidence.
   - An English reader would reach the exact same factual conclusion about the claim as a Hindi reader.
   - *Note:* Minor grammatical awkwardness or unnatural phrasing that does not alter factual meaning should still be marked `PRESERVED`.
   - *Requirement:* Select `NONE` under distortion types.

2. **`ALTERED` (Meaning Corrupted):**
   - The English translation changes, omits, inverts, or garbles claim-critical factual details.
   - An English reader would be misled or unable to deduce the claim's factual status accurately.
   - *Requirement:* Check at least one substantive distortion type below and write a short rationale.

3. **`AMBIGUOUS_SOURCE` (Source Problem):**
   - The original Hindi text itself is too incomplete, garbled, or ambiguous to form a reliable factual judgment.
   - *Requirement:* Write a short rationale noting the source defect.

4. **`UNABLE_TO_DECIDE` (Uncertain):**
   - You cannot decide due to specialized domain context or lack of sufficient context.
   - *Requirement:* Write a short rationale explaining why.

---

## 3. Specific Distortion Types (For `ALTERED` Items)

Select all that apply:
- **`NUM_DATE` (Numerical or Date Distortion):** A quantity, monetary figure, percentage, or date was changed, dropped, or corrupted (e.g., Devanagari numerals mis-transliterated, millions confused with crores).
- **`NEGATION` (Polarity Inversion):** A negation marker (e.g., नहीं, मत, ना) was omitted, added, or neutralized, flipping the factual stance from denial to affirmation.
- **`ENTITY` (Named Entity Corruption):** A person, organization, political party, location, or acronym was mistranslated into an unrelated common word or scrambled (e.g., proper nouns translated literally).
- **`OMISSION` (Critical Content Dropped):** Crucial clauses or qualifiers present in the Hindi evidence are missing from the English translation.
- **`HALLUCINATION` (Fabricated Content):** The translation introduces assertions or words not present in the original Hindi text.
- **`QUALIFIER` (Hedge or Modality Shift):** Modals or certainty qualifiers (e.g., "alleged", "may", "confirmed") were shifted.
- **`TIME` (Temporal Sequence Distortion):** Tense, chronology, or event sequencing was altered.
- **`OTHER`:** Any other substantive semantic change.

---

## 4. How to Use the Interface

1. **Launch Interface:**
   - Unzip your packet folder.
   - Double-click `index.html` to open it in Chrome, Edge, Firefox, or Safari (no internet connection required).
2. **Annotate:**
   - Review each item from 1 to 50 using the navigation grid.
   - Your responses are saved automatically in your browser as you type.
3. **Validate & Export:**
   - When all 50 items are complete, click **"Validate & Export Submission"**.
   - The tool will verify that all required fields are filled.
   - It will automatically download your submission file: `submission_{annotator_code}.json` (and `.csv`).
4. **Return:**
   - Email or send the downloaded submission file to the study coordinator.

---

## 5. Independence and Confidentiality

- **Work Independently:** Please do not consult or compare answers with other evaluators.
- **Privacy:** You are identified solely by a pseudonymous code (e.g., `A1` or `A2`). Do not include your real name or personal information in the submission files.
