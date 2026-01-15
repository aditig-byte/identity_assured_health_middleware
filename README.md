# Identity-Assured Health Middleware

A dual-tier cryptographic pipeline for medical data integrity and confidentiality using Python.
This repository demonstrates the evolution of a security system designed to protect sensitive medical records.

## Project Structure

### 1. Core Security Layer (`security_layer.py`)
- **Focus:** Fundamental Cryptographic Logic.
- **Tech:** SHA-256 Hashing, AES-128 Encryption.
- **Goal:** Proves that any data tampering (e.g., changing a diagnosis) triggers an immediate integrity failure.

### 2. Enterprise Security System (`security_system.py`)
- **Focus:** System Architecture & Production Readiness.
- **Tech:** Python `logging`, Authenticated Encryption (Fernet), Deterministic Serialization.
- **Key Features:**
    - **Audit Logging:** Maintains a chronological "Chain of Custody" for every record.
    - **Zero-Trust:** Re-verifies the digital seal on every single access request.
    - **Lifecycle Management:** Automates the Ingest -> Seal -> Lock -> Log pipeline.

## Installation & Usage
```bash
pip install cryptography
python security_system.py
