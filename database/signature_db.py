"""
Signature Database Module
Manages threat signatures and scan history
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional


class SignatureDatabase:
    """Manages virus signatures and scan history"""

    def __init__(self, db_path: str = "data"):
        """
        Initialize the signature database
        
        Args:
            db_path: Path to store database files
        """
        self.db_path = db_path
        self.signatures_file = os.path.join(db_path, "signatures.json")
        self.history_file = os.path.join(db_path, "scan_history.json")

        self._ensure_directories()
        self._load_signatures()

    def _ensure_directories(self):
        """Ensure database directories exist"""
        os.makedirs(self.db_path, exist_ok=True)

    def _load_signatures(self):
        """Load signatures from file"""
        if not os.path.exists(self.signatures_file):
            self._create_default_signatures()

    def _create_default_signatures(self):
        """Create default signature database"""
        signatures = {
            "version": "1.0",
            "last_update": datetime.now().isoformat(),
            "signatures": [
                {
                    "name": "EICAR-Test-File",
                    "hash": "44d88612fea8a8f36de82e1278a8ef48",
                    "type": "test",
                    "severity": "high"
                }
            ]
        }

        os.makedirs(self.db_path, exist_ok=True)
        with open(self.signatures_file, "w") as f:
            json.dump(signatures, f, indent=2)

    def update_signatures(self, new_signatures: List[Dict]):
        """Update the signature database"""
        data = {
            "version": "1.0",
            "last_update": datetime.now().isoformat(),
            "signatures": new_signatures
        }

        os.makedirs(self.db_path, exist_ok=True)
        with open(self.signatures_file, "w") as f:
            json.dump(data, f, indent=2)

    def get_signatures(self) -> List[Dict]:
        """Get all signatures from database"""
        if not os.path.exists(self.signatures_file):
            self._create_default_signatures()

        with open(self.signatures_file, "r") as f:
            data = json.load(f)
            return data.get("signatures", [])

    def add_scan_history(self, scan_info: Dict):
        """Add a scan to the history"""
        history = self._load_history()
        scan_info["timestamp"] = datetime.now().isoformat()
        history.append(scan_info)

        os.makedirs(self.db_path, exist_ok=True)
        with open(self.history_file, "w") as f:
            json.dump(history, f, indent=2)

    def _load_history(self) -> List[Dict]:
        """Load scan history from file"""
        if not os.path.exists(self.history_file):
            return []

        with open(self.history_file, "r") as f:
            return json.load(f)

    def get_scan_history(self, limit: int = 10) -> List[Dict]:
        """Get scan history"""
        history = self._load_history()
        return history[-limit:]

    def clear_history(self):
        """Clear scan history"""
        os.makedirs(self.db_path, exist_ok=True)
        with open(self.history_file, "w") as f:
            json.dump([], f)
