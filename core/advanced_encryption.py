#!/usr/bin/env python3
"""
PHANTOM PROTOCOL - Advanced Encryption System
Military-grade AES-256-GCM encryption with specific passphrase requirement
Secure storage and decryption of logs, reports, and extracted data
"""

import os
import json
import time
import hashlib
import base64
import logging
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
import secrets
import getpass
import argparse

class EncryptionLevel(Enum):
    STANDARD = "standard"
    MILITARY = "military"
    PHANTOM = "phantom"

class DataType(Enum):
    LOGS = "logs"
    REPORTS = "reports"
    EXTRACTED_DATA = "extracted_data"
    SYSTEM_CONFIG = "system_config"
    CREDENTIALS = "credentials"

@dataclass
class EncryptedData:
    data_type: DataType
    encrypted_content: bytes
    salt: bytes
    nonce: bytes
    tag: bytes
    timestamp: float
    metadata: Dict[str, Any]

@dataclass
class DecryptionResult:
    success: bool
    decrypted_data: Optional[bytes]
    data_type: Optional[DataType]
    timestamp: Optional[float]
    metadata: Optional[Dict[str, Any]]
    error_message: Optional[str]

class AdvancedEncryption:
    """
    Military-grade encryption system with specific passphrase requirement
    Uses AES-256-GCM for symmetric encryption with PBKDF2 key derivation
    """
    
    # EXACT PASSPHRASE REQUIREMENT - DO NOT MODIFY
    REQUIRED_PASSPHRASE = "WILL TOOL KILL OPEN NEVER WILL AGAIN NEVER ZERO WELCOME DUE AND NEVER"
    
    def __init__(self, encryption_level: EncryptionLevel = EncryptionLevel.PHANTOM):
        self.encryption_level = encryption_level
        self.backend = default_backend()
        
        # Encryption parameters based on level
        self.encryption_params = {
            EncryptionLevel.STANDARD: {
                "key_length": 32,  # 256 bits
                "iterations": 100000,
                "salt_length": 16
            },
            EncryptionLevel.MILITARY: {
                "key_length": 32,  # 256 bits
                "iterations": 500000,
                "salt_length": 32
            },
            EncryptionLevel.PHANTOM: {
                "key_length": 32,  # 256 bits
                "iterations": 1000000,
                "salt_length": 64
            }
        }
        
        # Storage paths
        self.encrypted_storage_path = Path("encrypted_data")
        self.encrypted_storage_path.mkdir(exist_ok=True)
        
        # Create subdirectories for different data types
        for data_type in DataType:
            (self.encrypted_storage_path / data_type.value).mkdir(exist_ok=True)
        
        # RSA key pair for additional security (optional)
        self.rsa_private_key = None
        self.rsa_public_key = None
        self.generate_rsa_keys()
        
        logging.info(f"Advanced Encryption initialized with {encryption_level.value} level")
    
    def generate_rsa_keys(self):
        """Generate RSA key pair for additional encryption layer"""
        try:
            self.rsa_private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=4096,
                backend=self.backend
            )
            self.rsa_public_key = self.rsa_private_key.public_key()
            
            logging.info("RSA key pair generated (4096-bit)")
            
        except Exception as e:
            logging.error(f"RSA key generation failed: {e}")
    
    def verify_passphrase(self, passphrase: str) -> bool:
        """
        Verify that the provided passphrase matches the exact requirement
        CRITICAL: Must match exactly including capitalization and spacing
        """
        return passphrase == self.REQUIRED_PASSPHRASE
    
    def derive_key(self, passphrase: str, salt: bytes) -> bytes:
        """Derive encryption key from passphrase using PBKDF2"""
        if not self.verify_passphrase(passphrase):
            raise ValueError("Invalid passphrase. Access denied.")
        
        params = self.encryption_params[self.encryption_level]
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=params["key_length"],
            salt=salt,
            iterations=params["iterations"],
            backend=self.backend
        )
        
        return kdf.derive(passphrase.encode('utf-8'))
    
    def encrypt_data(self, data: Union[str, bytes, Dict[str, Any]], 
                    data_type: DataType, 
                    passphrase: str,
                    metadata: Optional[Dict[str, Any]] = None) -> EncryptedData:
        """
        Encrypt data using AES-256-GCM
        """
        if not self.verify_passphrase(passphrase):
            raise ValueError("Invalid passphrase. Encryption denied.")
        
        try:
            # Convert data to bytes if necessary
            if isinstance(data, str):
                data_bytes = data.encode('utf-8')
            elif isinstance(data, dict):
                data_bytes = json.dumps(data, indent=2).encode('utf-8')
            else:
                data_bytes = data
            
            # Generate salt and nonce
            params = self.encryption_params[self.encryption_level]
            salt = secrets.token_bytes(params["salt_length"])
            nonce = secrets.token_bytes(12)  # 96-bit nonce for GCM
            
            # Derive key
            key = self.derive_key(passphrase, salt)
            
            # Create cipher
            cipher = Cipher(
                algorithms.AES(key),
                modes.GCM(nonce),
                backend=self.backend
            )
            encryptor = cipher.encryptor()
            
            # Encrypt data
            encrypted_content = encryptor.update(data_bytes) + encryptor.finalize()
            tag = encryptor.tag
            
            # Create encrypted data object
            encrypted_data = EncryptedData(
                data_type=data_type,
                encrypted_content=encrypted_content,
                salt=salt,
                nonce=nonce,
                tag=tag,
                timestamp=time.time(),
                metadata=metadata or {}
            )
            
            logging.info(f"Data encrypted successfully ({len(data_bytes)} bytes -> {len(encrypted_content)} bytes)")
            return encrypted_data
            
        except Exception as e:
            logging.error(f"Encryption failed: {e}")
            raise
    
    def decrypt_data(self, encrypted_data: EncryptedData, passphrase: str) -> DecryptionResult:
        """
        Decrypt data using AES-256-GCM
        """
        if not self.verify_passphrase(passphrase):
            return DecryptionResult(
                success=False,
                decrypted_data=None,
                data_type=None,
                timestamp=None,
                metadata=None,
                error_message="Invalid passphrase. Access denied."
            )
        
        try:
            # Derive key
            key = self.derive_key(passphrase, encrypted_data.salt)
            
            # Create cipher
            cipher = Cipher(
                algorithms.AES(key),
                modes.GCM(encrypted_data.nonce, encrypted_data.tag),
                backend=self.backend
            )
            decryptor = cipher.decryptor()
            
            # Decrypt data
            decrypted_data = decryptor.update(encrypted_data.encrypted_content) + decryptor.finalize()
            
            logging.info(f"Data decrypted successfully ({len(encrypted_data.encrypted_content)} bytes -> {len(decrypted_data)} bytes)")
            
            return DecryptionResult(
                success=True,
                decrypted_data=decrypted_data,
                data_type=encrypted_data.data_type,
                timestamp=encrypted_data.timestamp,
                metadata=encrypted_data.metadata,
                error_message=None
            )
            
        except Exception as e:
            logging.error(f"Decryption failed: {e}")
            return DecryptionResult(
                success=False,
                decrypted_data=None,
                data_type=None,
                timestamp=None,
                metadata=None,
                error_message=str(e)
            )
    
    def save_encrypted_data(self, encrypted_data: EncryptedData, filename: Optional[str] = None) -> str:
        """Save encrypted data to file"""
        try:
            if not filename:
                timestamp = int(time.time())
                filename = f"{encrypted_data.data_type.value}_{timestamp}.enc"
            
            file_path = self.encrypted_storage_path / encrypted_data.data_type.value / filename
            
            # Serialize encrypted data
            serialized_data = {
                "data_type": encrypted_data.data_type.value,
                "encrypted_content": base64.b64encode(encrypted_data.encrypted_content).decode('utf-8'),
                "salt": base64.b64encode(encrypted_data.salt).decode('utf-8'),
                "nonce": base64.b64encode(encrypted_data.nonce).decode('utf-8'),
                "tag": base64.b64encode(encrypted_data.tag).decode('utf-8'),
                "timestamp": encrypted_data.timestamp,
                "metadata": encrypted_data.metadata,
                "encryption_level": self.encryption_level.value
            }
            
            # Save to file
            with open(file_path, 'w') as f:
                json.dump(serialized_data, f, indent=2)
            
            logging.info(f"Encrypted data saved to: {file_path}")
            return str(file_path)
            
        except Exception as e:
            logging.error(f"Failed to save encrypted data: {e}")
            raise
    
    def load_encrypted_data(self, file_path: str) -> EncryptedData:
        """Load encrypted data from file"""
        try:
            with open(file_path, 'r') as f:
                serialized_data = json.load(f)
            
            # Deserialize encrypted data
            encrypted_data = EncryptedData(
                data_type=DataType(serialized_data["data_type"]),
                encrypted_content=base64.b64decode(serialized_data["encrypted_content"]),
                salt=base64.b64decode(serialized_data["salt"]),
                nonce=base64.b64decode(serialized_data["nonce"]),
                tag=base64.b64decode(serialized_data["tag"]),
                timestamp=serialized_data["timestamp"],
                metadata=serialized_data["metadata"]
            )
            
            logging.info(f"Encrypted data loaded from: {file_path}")
            return encrypted_data
            
        except Exception as e:
            logging.error(f"Failed to load encrypted data: {e}")
            raise
    
    def encrypt_and_save(self, data: Union[str, bytes, Dict[str, Any]], 
                        data_type: DataType, 
                        passphrase: str,
                        filename: Optional[str] = None,
                        metadata: Optional[Dict[str, Any]] = None) -> str:
        """Encrypt data and save to file in one operation"""
        encrypted_data = self.encrypt_data(data, data_type, passphrase, metadata)
        return self.save_encrypted_data(encrypted_data, filename)
    
    def load_and_decrypt(self, file_path: str, passphrase: str) -> DecryptionResult:
        """Load encrypted data from file and decrypt in one operation"""
        encrypted_data = self.load_encrypted_data(file_path)
        return self.decrypt_data(encrypted_data, passphrase)
    
    def encrypt_logs(self, log_data: str, passphrase: str, log_level: str = "INFO") -> str:
        """Encrypt log data with specific metadata"""
        metadata = {
            "log_level": log_level,
            "source": "phantom_protocol",
            "encrypted_at": time.time()
        }
        return self.encrypt_and_save(log_data, DataType.LOGS, passphrase, metadata=metadata)
    
    def encrypt_report(self, report_data: Dict[str, Any], passphrase: str, report_type: str = "extraction") -> str:
        """Encrypt report data with specific metadata"""
        metadata = {
            "report_type": report_type,
            "generated_at": time.time(),
            "phantom_protocol_version": "1.0"
        }
        return self.encrypt_and_save(report_data, DataType.REPORTS, passphrase, metadata=metadata)
    
    def encrypt_extracted_data(self, extracted_data: Dict[str, Any], passphrase: str, vulnerability_id: int) -> str:
        """Encrypt extracted vulnerability data"""
        metadata = {
            "vulnerability_id": vulnerability_id,
            "extraction_timestamp": time.time(),
            "data_classification": "TOP_SECRET"
        }
        return self.encrypt_and_save(extracted_data, DataType.EXTRACTED_DATA, passphrase, metadata=metadata)
    
    def list_encrypted_files(self, data_type: Optional[DataType] = None) -> List[Dict[str, Any]]:
        """List all encrypted files"""
        files = []
        
        try:
            if data_type:
                search_paths = [self.encrypted_storage_path / data_type.value]
            else:
                search_paths = [self.encrypted_storage_path / dt.value for dt in DataType]
            
            for search_path in search_paths:
                if search_path.exists():
                    for file_path in search_path.glob("*.enc"):
                        try:
                            # Load metadata without decrypting
                            with open(file_path, 'r') as f:
                                data = json.load(f)
                            
                            files.append({
                                "file_path": str(file_path),
                                "data_type": data["data_type"],
                                "timestamp": data["timestamp"],
                                "metadata": data["metadata"],
                                "encryption_level": data.get("encryption_level", "unknown"),
                                "file_size": file_path.stat().st_size
                            })
                            
                        except Exception as e:
                            logging.warning(f"Failed to read metadata from {file_path}: {e}")
                            continue
            
            # Sort by timestamp (newest first)
            files.sort(key=lambda x: x["timestamp"], reverse=True)
            
        except Exception as e:
            logging.error(f"Failed to list encrypted files: {e}")
        
        return files
    
    def create_secure_folder(self, folder_name: str, passphrase: str) -> str:
        """Create a secure encrypted folder"""
        if not self.verify_passphrase(passphrase):
            raise ValueError("Invalid passphrase. Folder creation denied.")
        
        try:
            folder_path = self.encrypted_storage_path / folder_name
            folder_path.mkdir(exist_ok=True)
            
            # Create folder metadata
            metadata = {
                "folder_name": folder_name,
                "created_at": time.time(),
                "encryption_level": self.encryption_level.value,
                "access_controlled": True
            }
            
            # Save encrypted metadata
            metadata_file = folder_path / ".folder_metadata.enc"
            self.encrypt_and_save(metadata, DataType.SYSTEM_CONFIG, passphrase, str(metadata_file))
            
            logging.info(f"Secure folder created: {folder_path}")
            return str(folder_path)
            
        except Exception as e:
            logging.error(f"Secure folder creation failed: {e}")
            raise
    
    def verify_folder_access(self, folder_path: str, passphrase: str) -> bool:
        """Verify access to secure folder"""
        try:
            metadata_file = Path(folder_path) / ".folder_metadata.enc"
            
            if not metadata_file.exists():
                return False
            
            result = self.load_and_decrypt(str(metadata_file), passphrase)
            return result.success
            
        except Exception as e:
            logging.error(f"Folder access verification failed: {e}")
            return False
    
    def get_encryption_stats(self) -> Dict[str, Any]:
        """Get encryption system statistics"""
        stats = {
            "encryption_level": self.encryption_level.value,
            "total_encrypted_files": 0,
            "files_by_type": {},
            "total_storage_size": 0,
            "encryption_params": self.encryption_params[self.encryption_level]
        }
        
        try:
            files = self.list_encrypted_files()
            stats["total_encrypted_files"] = len(files)
            
            for file_info in files:
                data_type = file_info["data_type"]
                stats["files_by_type"][data_type] = stats["files_by_type"].get(data_type, 0) + 1
                stats["total_storage_size"] += file_info["file_size"]
            
        except Exception as e:
            logging.error(f"Failed to get encryption stats: {e}")
        
        return stats

class EncryptionCLI:
    """Command-line interface for encryption operations"""
    
    def __init__(self):
        self.encryption = AdvancedEncryption()
    
    def get_passphrase(self) -> str:
        """Get passphrase from user with verification"""
        print("\n" + "="*80)
        print("PHANTOM PROTOCOL - ENCRYPTED DATA ACCESS")
        print("="*80)
        print("\nEnter the exact passphrase to access encrypted data:")
        print("(Passphrase is case-sensitive and must match exactly)")
        print()
        
        passphrase = getpass.getpass("Passphrase: ")
        
        if not self.encryption.verify_passphrase(passphrase):
            print("\n❌ ACCESS DENIED: Invalid passphrase")
            print("The passphrase must match exactly including capitalization and spacing.")
            return None
        
        print("\n✅ ACCESS GRANTED: Passphrase verified")
        return passphrase
    
    def encrypt_file(self, input_file: str, data_type: str):
        """Encrypt a file"""
        passphrase = self.get_passphrase()
        if not passphrase:
            return
        
        try:
            with open(input_file, 'r') as f:
                data = f.read()
            
            encrypted_file = self.encryption.encrypt_and_save(
                data, 
                DataType(data_type), 
                passphrase,
                filename=f"{Path(input_file).stem}.enc"
            )
            
            print(f"\n✅ File encrypted successfully: {encrypted_file}")
            
        except Exception as e:
            print(f"\n❌ Encryption failed: {e}")
    
    def decrypt_file(self, encrypted_file: str):
        """Decrypt a file"""
        passphrase = self.get_passphrase()
        if not passphrase:
            return
        
        try:
            result = self.encryption.load_and_decrypt(encrypted_file, passphrase)
            
            if result.success:
                # Save decrypted data
                output_file = encrypted_file.replace('.enc', '_decrypted.txt')
                with open(output_file, 'wb') as f:
                    f.write(result.decrypted_data)
                
                print(f"\n✅ File decrypted successfully: {output_file}")
                print(f"Data type: {result.data_type.value}")
                print(f"Timestamp: {time.ctime(result.timestamp)}")
                
                if result.metadata:
                    print(f"Metadata: {json.dumps(result.metadata, indent=2)}")
            else:
                print(f"\n❌ Decryption failed: {result.error_message}")
                
        except Exception as e:
            print(f"\n❌ Decryption failed: {e}")
    
    def list_files(self):
        """List encrypted files"""
        files = self.encryption.list_encrypted_files()
        
        if not files:
            print("\nNo encrypted files found.")
            return
        
        print(f"\nFound {len(files)} encrypted files:")
        print("-" * 80)
        
        for file_info in files:
            print(f"File: {file_info['file_path']}")
            print(f"  Type: {file_info['data_type']}")
            print(f"  Size: {file_info['file_size']} bytes")
            print(f"  Created: {time.ctime(file_info['timestamp'])}")
            print(f"  Level: {file_info['encryption_level']}")
            print()
    
    def show_stats(self):
        """Show encryption statistics"""
        stats = self.encryption.get_encryption_stats()
        
        print("\nEncryption System Statistics:")
        print("-" * 40)
        print(f"Encryption Level: {stats['encryption_level']}")
        print(f"Total Files: {stats['total_encrypted_files']}")
        print(f"Total Storage: {stats['total_storage_size']} bytes")
        print()
        
        if stats['files_by_type']:
            print("Files by Type:")
            for data_type, count in stats['files_by_type'].items():
                print(f"  {data_type}: {count}")
        
        print()
        print("Encryption Parameters:")
        for param, value in stats['encryption_params'].items():
            print(f"  {param}: {value}")

def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(description="PHANTOM PROTOCOL - Encryption System")
    parser.add_argument("command", choices=["encrypt", "decrypt", "list", "stats"], 
                       help="Command to execute")
    parser.add_argument("--file", help="File to encrypt/decrypt")
    parser.add_argument("--type", choices=[dt.value for dt in DataType], 
                       help="Data type for encryption")
    
    args = parser.parse_args()
    
    cli = EncryptionCLI()
    
    if args.command == "encrypt":
        if not args.file or not args.type:
            print("Error: --file and --type are required for encryption")
            return
        cli.encrypt_file(args.file, args.type)
    
    elif args.command == "decrypt":
        if not args.file:
            print("Error: --file is required for decryption")
            return
        cli.decrypt_file(args.file)
    
    elif args.command == "list":
        cli.list_files()
    
    elif args.command == "stats":
        cli.show_stats()

if __name__ == "__main__":
    main()