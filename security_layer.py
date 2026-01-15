import hashlib
import json
import base64
from cryptography.fernet import Fernet

class HealthSecurityLayer:
    def __init__(self):
        # 1. KEY MANAGEMENT
        # In a real app, this Key is stored in a Hardware Security Module (HSM), not code
        # This uses AES (Symmetric Encryption)
        self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)

    def generate_integrity_hash(self, data_dict):
        """
        Creates a 'Digital Fingerprint' using SHA-256.
        Used to detect TAMPERING.
        """
        # We convert the JSON data to a stable string format
        data_string = json.dumps(data_dict, sort_keys=True).encode()
        
        # SHA-256 creates a fixed-size string unique to this data
        integrity_hash = hashlib.sha256(data_string).hexdigest()
        return integrity_hash

    def encrypt_data(self, data_dict):
        """
        Locks the data using AES (Fernet).
        Used for CONFIDENTIALITY.
        """
        data_string = json.dumps(data_dict).encode()
        encrypted_blob = self.cipher_suite.encrypt(data_string)
        return encrypted_blob

    def decrypt_data(self, encrypted_blob):
        """
        Unlocks the data.
        Only possible if you have self.key.
        """
        decrypted_string = self.cipher_suite.decrypt(encrypted_blob).decode()
        return json.loads(decrypted_string)

    def verify_integrity(self, data_dict, old_hash):
        """
        The Zero-Trust Check.
        Recalculates the hash and compares it with the original.
        """
        new_hash = self.generate_integrity_hash(data_dict)
        return new_hash == old_hash

# DEMONSTRATION
if __name__ == "__main__":
    security = HealthSecurityLayer()

    # Step 1: Original Data from the Lab
    medical_record = {
        "patient_id": "ABC",
        "diagnosis": "Typhoid Negative",
        "timestamp": "2026-01-15T10:00:00Z"
    }
    print(f"Original Data: {medical_record}")

    # Step 2: Hashing (Sealing the data)
    original_hash = security.generate_integrity_hash(medical_record)
    print(f"Integrity Hash: {original_hash}")

    # Step 3: Encryption (Locking the data)
    encrypted_blob = security.encrypt_data(medical_record)
    print(f"Encrypted Database Entry: {encrypted_blob[:20]}... [Hidden]")

    # --- SCENARIO: A HACKER ATTACKS ---
    print("\n--- SIMULATING ATTACK ---")
    
    # Hacker decrypts it (somehow) and changes the diagnosis
    # Note: In real life, they can't decrypt without the key, 
    # but let's say they corrupted the file storage
    tampered_record = medical_record.copy()
    tampered_record['diagnosis'] = "Typhoid POSITIVE" # <--- The Hack

    # Step 4: Zero-Trust Verification
    print(f"Tampered Data: {tampered_record}")
    is_safe = security.verify_integrity(tampered_record, original_hash)
    if is_safe:
        print("System: Data is Valid.")
    else:
        print("System: SECURITY ALERT! Tampering Detected. Hash Mismatch.")