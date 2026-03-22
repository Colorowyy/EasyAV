"""
Utility functions for the antivirus application
"""

import hashlib
from pathlib import Path


def calculate_file_hash(file_path: str, algorithm: str = "sha256") -> str:
    """
    Calculate hash of a file
    
    Args:
        file_path: Path to the file
        algorithm: Hash algorithm to use (md5, sha1, sha256, etc.)
        
    Returns:
        Hex digest of the file hash
    """
    hash_obj = hashlib.new(algorithm)

    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_obj.update(chunk)
        return hash_obj.hexdigest()
    except Exception:
        return None


def is_valid_path(path: str) -> bool:
    """
    Check if a path is valid
    
    Args:
        path: Path to validate
        
    Returns:
        True if path is valid and accessible
    """
    return Path(path).exists()


def get_file_info(file_path: str) -> dict:
    """
    Get detailed information about a file
    
    Args:
        file_path: Path to the file
        
    Returns:
        Dictionary containing file information
    """
    path = Path(file_path)

    if not path.exists():
        return None

    try:
        return {
            "name": path.name,
            "size": path.stat().st_size,
            "modified": path.stat().st_mtime,
            "is_dir": path.is_dir(),
            "is_file": path.is_file()
        }
    except Exception:
        return None
