"""
Threat Detector Module
Identifies and classifies threats
"""

from typing import Dict, List, Optional


class ThreatDetector:
    """Detects threats in files"""

    # Sample threat signatures (in real application, these would be loaded from database)
    MALWARE_SIGNATURES = {
        "eicar": "X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*",
        "eicar_hash": "44d88612fea8a8f36de82e1278a8ef48",  # MD5 of EICAR
    }

    def __init__(self):
        """Initialize the threat detector"""
        self.detected_threats = []

    def check_file_hash(self, file_hash: str) -> Optional[Dict]:
        """
        Check if a file hash matches known malware
        
        Args:
            file_hash: Hash of the file to check
            
        Returns:
            Threat information if found, None otherwise
        """
        for threat_name, threat_hash in self.MALWARE_SIGNATURES.items():
            if file_hash.lower() == threat_hash.lower():
                return {
                    "name": threat_name,
                    "severity": "high",
                    "type": "known_malware"
                }
        return None

    def check_file_content(self, file_path: str) -> Optional[Dict]:
        """
        Check file content for threat patterns
        
        Args:
            file_path: Path to the file to check
            
        Returns:
            Threat information if found, None otherwise
        """
        try:
            with open(file_path, "rb") as f:
                content = f.read(10000)  # Read first 10KB

            # Check for EICAR test string
            if b"EICAR" in content:
                return {
                    "name": "eicar_test",
                    "severity": "high",
                    "type": "test_file"
                }

            return None

        except Exception:
            return None

    def analyze_file(self, file_info: Dict) -> Dict:
        """
        Analyze a file for threats
        
        Args:
            file_info: File information dictionary
            
        Returns:
            Updated file info with threat status
        """
        # Check hash against known malware
        threat = self.check_file_hash(file_info.get("hash", ""))

        if not threat:
            # Check file content
            threat = self.check_file_content(file_info["path"])

        if threat:
            file_info["status"] = "infected"
            file_info["threat"] = threat
            self.detected_threats.append(file_info)

        return file_info

    def get_threat_report(self) -> Dict:
        """Get a report of all detected threats"""
        return {
            "total_threats": len(self.detected_threats),
            "threats": self.detected_threats
        }
