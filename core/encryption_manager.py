#!/usr/bin/env python3
"""
PHANTOM PROTOCOL - Encryption Manager
Military-grade AES-256-GCM encryption system with specific passphrase handling
"""

import os
import base64
import json
import hashlib
import secrets
import time
from typing import Dict, List, Any, Optional, Union
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import logging

class EncryptionManager:
    """
    Military-grade encryption manager using AES-256-GCM
    Specific passphrase: "WILL TOOL KILL OPEN NEVER WILL AGAIN NEVER ZERO WELCOME DUE AND NEVER"
    """
    
    def __init__(self):
        self.passphrase = "WILL TOOL KILL OPEN NEVER WILL AGAIN NEVER ZERO WELCOME DUE AND NEVER"
        self.salt = b'phantom_protocol_salt_2024_military_grade'
        self.iterations = 100000
        self.key_cache = {}
        
    def derive_key(self, passphrase: str = None) -> bytes:
        """Derive encryption key from passphrase using PBKDF2"""
        if passphrase is None:
            passphrase = self.passphrase
            
        # Check cache first
        passphrase_hash = hashlib.sha256(passphrase.encode()).hexdigest()
        if passphrase_hash in self.key_cache:
            return self.key_cache[passphrase_hash]
        
        # Derive key
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,  # 256 bits
            salt=self.salt,
            iterations=self.iterations,
        )
        key = kdf.derive(passphrase.encode())
        
        # Cache the key
        self.key_cache[passphrase_hash] = key
        
        return key
    
    def encrypt_data(self, data: Union[str, bytes], passphrase: str = None) -> bytes:
        """Encrypt data using AES-256-GCM"""
        try:
            if isinstance(data, str):
                data = data.encode('utf-8')
            
            # Derive key
            key = self.derive_key(passphrase)
            
            # Generate random nonce (12 bytes for GCM)
            nonce = secrets.token_bytes(12)
            
            # Create AESGCM cipher
            aesgcm = AESGCM(key)
            
            # Encrypt data
            ciphertext = aesgcm.encrypt(nonce, data, None)
            
            # Combine nonce and ciphertext
            encrypted_data = nonce + ciphertext
            
            return encrypted_data
            
        except Exception as e:
            logging.error(f"Encryption failed: {e}")
            raise
    
    def decrypt_data(self, encrypted_data: bytes, passphrase: str = None) -> bytes:
        """Decrypt data using AES-256-GCM"""
        try:
            # Derive key
            key = self.derive_key(passphrase)
            
            # Extract nonce and ciphertext
            nonce = encrypted_data[:12]
            ciphertext = encrypted_data[12:]
            
            # Create AESGCM cipher
            aesgcm = AESGCM(key)
            
            # Decrypt data
            plaintext = aesgcm.decrypt(nonce, ciphertext, None)
            
            return plaintext
            
        except Exception as e:
            logging.error(f"Decryption failed: {e}")
            raise
    
    def encrypt_file(self, file_path: str, output_path: str = None, passphrase: str = None) -> str:
        """Encrypt file and save to output path"""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
            
            # Read file data
            with open(file_path, 'rb') as f:
                file_data = f.read()
            
            # Encrypt data
            encrypted_data = self.encrypt_data(file_data, passphrase)
            
            # Determine output path
            if output_path is None:
                output_path = str(file_path) + '.encrypted'
            
            # Write encrypted data
            with open(output_path, 'wb') as f:
                f.write(encrypted_data)
            
            logging.info(f"File encrypted: {file_path} -> {output_path}")
            return output_path
            
        except Exception as e:
            logging.error(f"File encryption failed: {e}")
            raise
    
    def decrypt_file(self, encrypted_file_path: str, output_path: str = None, passphrase: str = None) -> str:
        """Decrypt file and save to output path"""
        try:
            encrypted_file_path = Path(encrypted_file_path)
            if not encrypted_file_path.exists():
                raise FileNotFoundError(f"Encrypted file not found: {encrypted_file_path}")
            
            # Read encrypted data
            with open(encrypted_file_path, 'rb') as f:
                encrypted_data = f.read()
            
            # Decrypt data
            decrypted_data = self.decrypt_data(encrypted_data, passphrase)
            
            # Determine output path
            if output_path is None:
                output_path = str(encrypted_file_path).replace('.encrypted', '')
            
            # Write decrypted data
            with open(output_path, 'wb') as f:
                f.write(decrypted_data)
            
            logging.info(f"File decrypted: {encrypted_file_path} -> {output_path}")
            return output_path
            
        except Exception as e:
            logging.error(f"File decryption failed: {e}")
            raise
    
    def encrypt_json(self, data: Dict[str, Any], passphrase: str = None) -> bytes:
        """Encrypt JSON data"""
        try:
            json_str = json.dumps(data, indent=2, ensure_ascii=False)
            return self.encrypt_data(json_str, passphrase)
        except Exception as e:
            logging.error(f"JSON encryption failed: {e}")
            raise
    
    def decrypt_json(self, encrypted_data: bytes, passphrase: str = None) -> Dict[str, Any]:
        """Decrypt JSON data"""
        try:
            decrypted_bytes = self.decrypt_data(encrypted_data, passphrase)
            json_str = decrypted_bytes.decode('utf-8')
            return json.loads(json_str)
        except Exception as e:
            logging.error(f"JSON decryption failed: {e}")
            raise
    
    def encrypt_folder(self, folder_path: str, output_folder: str = None, passphrase: str = None) -> str:
        """Encrypt entire folder recursively"""
        try:
            folder_path = Path(folder_path)
            if not folder_path.exists():
                raise FileNotFoundError(f"Folder not found: {folder_path}")
            
            # Determine output folder
            if output_folder is None:
                output_folder = str(folder_path) + '_encrypted'
            
            output_folder = Path(output_folder)
            output_folder.mkdir(parents=True, exist_ok=True)
            
            encrypted_files = []
            
            # Recursively encrypt all files
            for file_path in folder_path.rglob('*'):
                if file_path.is_file():
                    # Calculate relative path
                    relative_path = file_path.relative_to(folder_path)
                    output_file_path = output_folder / relative_path
                    
                    # Create parent directories
                    output_file_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    # Encrypt file
                    encrypted_file = self.encrypt_file(
                        str(file_path),
                        str(output_file_path) + '.encrypted',
                        passphrase
                    )
                    encrypted_files.append(encrypted_file)
            
            logging.info(f"Folder encrypted: {folder_path} -> {output_folder} ({len(encrypted_files)} files)")
            return str(output_folder)
            
        except Exception as e:
            logging.error(f"Folder encryption failed: {e}")
            raise
    
    def decrypt_folder(self, encrypted_folder_path: str, output_folder: str = None, passphrase: str = None) -> str:
        """Decrypt entire folder recursively"""
        try:
            encrypted_folder_path = Path(encrypted_folder_path)
            if not encrypted_folder_path.exists():
                raise FileNotFoundError(f"Encrypted folder not found: {encrypted_folder_path}")
            
            # Determine output folder
            if output_folder is None:
                output_folder = str(encrypted_folder_path).replace('_encrypted', '_decrypted')
            
            output_folder = Path(output_folder)
            output_folder.mkdir(parents=True, exist_ok=True)
            
            decrypted_files = []
            
            # Recursively decrypt all .encrypted files
            for encrypted_file_path in encrypted_folder_path.rglob('*.encrypted'):
                # Calculate relative path
                relative_path = encrypted_file_path.relative_to(encrypted_folder_path)
                output_file_path = output_folder / relative_path
                
                # Remove .encrypted extension
                output_file_path = output_file_path.with_suffix('')
                
                # Create parent directories
                output_file_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Decrypt file
                decrypted_file = self.decrypt_file(
                    str(encrypted_file_path),
                    str(output_file_path),
                    passphrase
                )
                decrypted_files.append(decrypted_file)
            
            logging.info(f"Folder decrypted: {encrypted_folder_path} -> {output_folder} ({len(decrypted_files)} files)")
            return str(output_folder)
            
        except Exception as e:
            logging.error(f"Folder decryption failed: {e}")
            raise
    
    def verify_passphrase(self, test_passphrase: str) -> bool:
        """Verify if provided passphrase matches the required one"""
        return test_passphrase == self.passphrase
    
    def create_encrypted_archive(self, data: Dict[str, Any], archive_name: str, passphrase: str = None) -> str:
        """Create encrypted archive with metadata"""
        try:
            # Add metadata
            archive_data = {
                "metadata": {
                    "created_at": str(int(time.time())),
                    "version": "1.0",
                    "encryption": "AES-256-GCM",
                    "phantom_protocol": True
                },
                "data": data
            }
            
            # Encrypt archive
            encrypted_data = self.encrypt_json(archive_data, passphrase)
            
            # Save to file
            archive_path = f"encrypted_data/{archive_name}.phantom"
            Path("encrypted_data").mkdir(exist_ok=True)
            
            with open(archive_path, 'wb') as f:
                f.write(encrypted_data)
            
            logging.info(f"Encrypted archive created: {archive_path}")
            return archive_path
            
        except Exception as e:
            logging.error(f"Archive creation failed: {e}")
            raise
    
    def extract_encrypted_archive(self, archive_path: str, passphrase: str = None) -> Dict[str, Any]:
        """Extract encrypted archive"""
        try:
            if not Path(archive_path).exists():
                raise FileNotFoundError(f"Archive not found: {archive_path}")
            
            # Read encrypted data
            with open(archive_path, 'rb') as f:
                encrypted_data = f.read()
            
            # Decrypt archive
            archive_data = self.decrypt_json(encrypted_data, passphrase)
            
            # Verify it's a phantom protocol archive
            if not archive_data.get("metadata", {}).get("phantom_protocol"):
                raise ValueError("Not a valid Phantom Protocol archive")
            
            logging.info(f"Encrypted archive extracted: {archive_path}")
            return archive_data["data"]
            
        except Exception as e:
            logging.error(f"Archive extraction failed: {e}")
            raise
    
    def secure_delete(self, file_path: str, passes: int = 3) -> bool:
        """Securely delete file by overwriting multiple times"""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return True
            
            file_size = file_path.stat().st_size
            
            # Overwrite file multiple times
            with open(file_path, 'r+b') as f:
                for _ in range(passes):
                    f.seek(0)
                    f.write(secrets.token_bytes(file_size))
                    f.flush()
                    os.fsync(f.fileno())
            
            # Delete file
            file_path.unlink()
            
            logging.info(f"File securely deleted: {file_path}")
            return True
            
        except Exception as e:
            logging.error(f"Secure deletion failed: {e}")
            return False

class DecryptionTool:
    """
    Standalone decryption tool for accessing encrypted data
    """
    
    def __init__(self):
        self.encryption_manager = EncryptionManager()
    
    def decrypt_with_passphrase_prompt(self, encrypted_file_path: str) -> Optional[Dict[str, Any]]:
        """Decrypt file with passphrase prompt"""
        try:
            print("PHANTOM PROTOCOL - Decryption Tool")
            print("=" * 50)
            print(f"Encrypted file: {encrypted_file_path}")
            print()
            
            # Prompt for passphrase
            passphrase = input("Enter decryption passphrase: ")
            
            # Verify passphrase
            if not self.encryption_manager.verify_passphrase(passphrase):
                print("ERROR: Invalid passphrase!")
                return None
            
            # Decrypt file
            if encrypted_file_path.endswith('.phantom'):
                # Archive format
                data = self.encryption_manager.extract_encrypted_archive(encrypted_file_path, passphrase)
            else:
                # Regular encrypted file
                decrypted_bytes = self.encryption_manager.decrypt_data(
                    open(encrypted_file_path, 'rb').read(),
                    passphrase
                )
                data = json.loads(decrypted_bytes.decode('utf-8'))
            
            print("SUCCESS: File decrypted successfully!")
            return data
            
        except Exception as e:
            print(f"ERROR: Decryption failed - {e}")
            return None
    
    def decrypt_folder_with_prompt(self, encrypted_folder_path: str) -> Optional[str]:
        """Decrypt folder with passphrase prompt"""
        try:
            print("PHANTOM PROTOCOL - Folder Decryption Tool")
            print("=" * 50)
            print(f"Encrypted folder: {encrypted_folder_path}")
            print()
            
            # Prompt for passphrase
            passphrase = input("Enter decryption passphrase: ")
            
            # Verify passphrase
            if not self.encryption_manager.verify_passphrase(passphrase):
                print("ERROR: Invalid passphrase!")
                return None
            
            # Decrypt folder
            output_folder = self.encryption_manager.decrypt_folder(encrypted_folder_path, None, passphrase)
            
            print(f"SUCCESS: Folder decrypted to: {output_folder}")
            return output_folder
            
        except Exception as e:
            print(f"ERROR: Folder decryption failed - {e}")
            return None

# CLI tool for decryption
def main():
    """Main CLI interface for decryption tool"""
    import sys
    import time
    
    if len(sys.argv) < 2:
        print("Usage: python encryption_manager.py <encrypted_file_or_folder>")
        sys.exit(1)
    
    target_path = sys.argv[1]
    decryption_tool = DecryptionTool()
    
    if Path(target_path).is_dir():
        # Decrypt folder
        result = decryption_tool.decrypt_folder_with_prompt(target_path)
        if result:
            print(f"\nDecrypted folder available at: {result}")
    else:
        # Decrypt file
        result = decryption_tool.decrypt_with_passphrase_prompt(target_path)
        if result:
            print("\nDecrypted data:")
            print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()