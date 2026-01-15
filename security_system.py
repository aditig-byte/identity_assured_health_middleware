import hashlib
import json
import datetime
import logging
from cryptography.fernet import Fernet

# --- CONFIGURATION & LOGGING ---
# Tracking events
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [SECURITY] - %(message)s')

class HealthSecuritySystem:
    def __init__(self):
        """
        INITIALIZATION: Setting up the Cryptographic Foundation.
        """
        # In production, this key would be fetched from a Secure Vault (KMS)
        self.master_key = Fernet.generate_key()
        self.cipher = Fernet(self.master_key)
        self.blockchain_ledger = [] # Simulating a tamper-proof audit trail

    # --- CORE SECURITY ENGINE ---

    def generate_integrity_seal(self, data):
        """
        INTEGRITY (SHA-256): Creates a unique digital fingerprint.
        sort_keys=True is CRITICAL for deterministic hashing.
        """
        serialized_data = json.dumps(data, sort_keys=True).encode()
        return hashlib.sha256(serialized_data).hexdigest()

    def encrypt_record(self, data):
        """
        CONFIDENTIALITY (AES-128): Locks the data.
        """
        serialized_data = json.dumps(data).encode()
        return self.cipher.encrypt(serialized_data)

    def decrypt_record(self, encrypted_blob):
        """
        DECRYPTION: Unlocks the data.
        """
        decrypted_bytes = self.cipher.decrypt(encrypted_blob)
        return json.loads(decrypted_bytes.decode())

    # --- THE "BIG SYSTEM" LOGIC ---

    def process_new_report(self, patient_id, clinical_data):
        """
        LIFECYCLE: This is the high-level 'Big' function.
        It seals, locks, and logs the data in one flow.
        """
        # 1. Add metadata (Zero-Trust Principle)
        clinical_data['patient_id'] = patient_id
        clinical_data['processed_at'] = str(datetime.datetime.now())

        # 2. Creating the Integrity Seal
        seal = self.generate_integrity_seal(clinical_data)

        # 3. Encrypting the Record
        encrypted_blob = self.encrypt_record(clinical_data)

        # 4. Record to Audit Ledger (The 'Chain of Custody')
        self.blockchain_ledger.append({
            "patient_id": patient_id,
            "seal": seal,
            "timestamp": clinical_data['processed_at']
        })

        logging.info(f"Report for {patient_id} secured. Seal: {seal[:12]}...")
        return encrypted_blob, seal

    def verify_and_read(self, encrypted_blob, original_seal):
        """
        ZERO-TRUST VERIFICATION: Recalculates hash before showing data.
        """
        # 1. Decrypt
        decrypted_data = self.decrypt_record(encrypted_blob)

        # 2. Re-calculate Seal
        current_seal = self.generate_integrity_seal(decrypted_data)

        # 3. Compare (The core security check)
        if current_seal == original_seal:
            logging.info("Verification Successful: Data is authentic.")
            return decrypted_data
        else:
            logging.error("CRITICAL: DATA TAMPERING DETECTED!")
            return None

# --- DEMONSTRATION OF A 'BIG' SYSTEM ---
if __name__ == "__main__":
    vault = HealthSecuritySystem()

    # 1. Data Ingestion
    print("\n[STEP 1: INGESTION]")
    raw_data = {"diagnosis": "Healthy", "blood_group": "O+"}
    encrypted_record, master_seal = vault.process_new_report("PATIENT-101", raw_data)

    # 2. Normal Access
    print("\n[STEP 2: NORMAL ACCESS]")
    data = vault.verify_and_read(encrypted_record, master_seal)
    if data: print(f"Decrypted Data: {data['diagnosis']}")

    # 3. Simulated Tamper Attack
    print("\n[STEP 3: ATTACK SIMULATION]")
    # We simulate a hacker modifying the record in the database
    # Since we can't easily edit the blob, we show what happens if the seal is wrong
    hacker_modified_seal = "wrong_seal_12345"
    vault.verify_and_read(encrypted_record, hacker_modified_seal)