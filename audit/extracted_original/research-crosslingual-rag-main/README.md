# Cross-Lingual RAG Verification Research — Antigravity Project

**Working topic:** Separating Translation-Fidelity and Verifier-Reasoning Errors in Cross-Lingual RAG: A Controlled Study with Selective Original-Evidence Checking.

This is a provisional research topic, not proven novelty.

## User constraints
- Windows 10/11.
- Dedicated `.venv`; prefer Python 3.11, fallback to 3.12.
- Free tools/public datasets only; no paid API calls.
- Detect RAM, CPU, GPU, disk and Python version before heavy work.
- Start English–Hindi; expand to 3+ languages only if pilot results, annotation capability and resources justify it.
- Autonomous with checkpoints. Ask before paid services, destructive actions, external sharing/submissions, or large downloads.

## Setup
1. Extract ZIP and open folder in Antigravity.
2. Paste `ANTIGRAVITY_MASTER_PROMPT.md` as project instructions.
3. In PowerShell:
   ```powershell
   Set-ExecutionPolicy -Scope Process Bypass
   .\scripts\setup_windows.ps1
   .\.venv\Scripts\Activate.ps1
   python scripts\preflight.py
   ```
4. Start with the literature audit. Do not jump straight to large experiments.

## Rules
Never invent citations, data, results, or fee policies. Keep raw data separate, respect licenses, record commands/seeds/versions, and do not submit externally without explicit approval. If evidence undermines the gap, revise or abandon it rather than forcing a positive conclusion.
