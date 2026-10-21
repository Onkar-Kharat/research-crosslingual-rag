# Release Archive Documentation & Verification Guide

**Release Archive:** `CROSS_LINGUAL_EVIDENCE_VERIFICATION_RESEARCH_FREEZE_FINAL.zip`  
**Bitwise Synchronized Alias:** `CROSS_LINGUAL_EVIDENCE_VERIFICATION_RESEARCH_COMPUTATIONAL_FROZEN_EXPLORATORY_v6.zip`  
**Archive SHA-256:** `70fa5148f69cfed661cedec2990ebb7b9b79bd0a50ecb278b8e55d4eb6f5efa5`  
**Research Status:** `FROZEN — EXPLORATORY COMPUTATIONAL STUDY`  
**Protocol Version:** `v1.0-observational`  

---

## 1. Release Archive Identification

The authoritative computational freeze release artifact is located in the repository root:
- Primary Name: `CROSS_LINGUAL_EVIDENCE_VERIFICATION_RESEARCH_FREEZE_FINAL.zip`
- Alias Name: `CROSS_LINGUAL_EVIDENCE_VERIFICATION_RESEARCH_COMPUTATIONAL_FROZEN_EXPLORATORY_v6.zip`

Both archive files are bit-for-bit identical (exact same SHA-256 hash).

## 2. Cryptographic Checksum Verification

### PowerShell (Windows):
```powershell
Get-FileHash -Path ./CROSS_LINGUAL_EVIDENCE_VERIFICATION_RESEARCH_FREEZE_FINAL.zip -Algorithm SHA256
```
Expected output:
```
70FA5148F69CFED661CEDEC2990EBB7B9B79BD0A50ECB278B8E55D4EB6F5EFA5
```

### Linux / macOS:
```bash
sha256sum CROSS_LINGUAL_EVIDENCE_VERIFICATION_RESEARCH_FREEZE_FINAL.zip
```
Expected output:
```
70fa5148f69cfed661cedec2990ebb7b9b79bd0a50ecb278b8e55d4eb6f5efa5  CROSS_LINGUAL_EVIDENCE_VERIFICATION_RESEARCH_FREEZE_FINAL.zip
```

## 3. Internal Payload Manifest Verification

Every file included in the release archive is indexed with its SHA-256 hash in `audit/RELEASE_MANIFEST_SHA256.txt`. Only the manifest file itself is intentionally excluded from its own internal hash list.

To extract and verify 100% hash parity:
```powershell
python scripts/package_and_validate_final_release.py
```
This runs clean-room extraction, validates all 405 individual files against `RELEASE_MANIFEST_SHA256.txt`, and executes the 47-test regression suite.
