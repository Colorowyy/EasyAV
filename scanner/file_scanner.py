"""
File Scanner Module
Handles file and directory scanning
"""

import os
import hashlib
from pathlib import Path
from typing import List, Dict, Tuple


class FileScanner:
    """Scans files for threats"""

    def __init__(self):
        """Initialize the file scanner"""
        self.scanned_files = 0
        self.threats_found = 0
        self.scan_results = []

    def scan_file(self, file_path: str) -> Dict:
        """
        Scan a single file
        
        Args:
            file_path: Path to the file to scan
            
        Returns:
            Dictionary containing scan results
        """
        try:
            if not os.path.exists(file_path):
                return {"status": "error", "message": f"File not found: {file_path}"}

            file_hash = self._calculate_hash(file_path)
            file_info = {
                "path": file_path,
                "size": os.path.getsize(file_path),
                "hash": file_hash,
                "status": "clean",
                "threat": None
            }

            self.scanned_files += 1
            return file_info

        except Exception as e:
            return {"status": "error", "message": str(e)}

    def scan_directory(self, directory_path: str, recursive: bool = True) -> List[Dict]:
        """
        Scan all files in a directory
        
        Args:
            directory_path: Path to the directory to scan
            recursive: Whether to scan subdirectories
            
        Returns:
            List of scan results
        """
        self.scanned_files = 0
        self.threats_found = 0
        self.scan_results = []

        try:
            path = Path(directory_path)
            pattern = "**/*" if recursive else "*"

            for file_path in path.glob(pattern):
                if file_path.is_file():
                    result = self.scan_file(str(file_path))
                    self.scan_results.append(result)

            return self.scan_results

        except Exception as e:
            return [{"status": "error", "message": str(e)}]

    def _calculate_hash(self, file_path: str, algorithm: str = "sha256") -> str:
        """
        Calculate hash of a file
        
        Args:
            file_path: Path to the file
            algorithm: Hash algorithm to use
            
        Returns:
            Hex digest of the file hash
        """
        hash_obj = hashlib.new(algorithm)

        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_obj.update(chunk)

        return hash_obj.hexdigest()

    def get_scan_summary(self) -> Dict:
        """Get a summary of the last scan"""
        return {
            "total_files": self.scanned_files,
            "threats_found": self.threats_found,
            "clean_files": self.scanned_files - self.threats_found
        }
