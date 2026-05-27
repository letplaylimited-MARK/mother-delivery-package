#!/usr/bin/env python3
"""
Ghost Hub SDK License Manager
Enterprise licensing and activation system
"""

import hashlib
import json
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class LicenseStatus:
    license_id: str
    type: str
    is_valid: bool
    valid_until: str
    features: list
    max_agents: int
    max_devices: int


@dataclass
class ActivationResult:
    success: bool
    license_id: Optional[str] = None
    error: Optional[str] = None


class LicenseManager:
    LICENSE_FILE = ".ghost_hub_license"

    def __init__(self, license_file: Optional[str] = None):
        self.license_file = license_file or os.path.join(
            os.path.expanduser("~"), self.LICENSE_FILE
        )
        self._license_data: Optional[Dict] = None

    def activate(self, license_key: str, company: str) -> ActivationResult:
        """Activate license with key"""
        if not self._validate_key_format(license_key):
            return ActivationResult(success=False, error="Invalid license key format")

        license_data = {
            "license_id": license_key,
            "type": self._get_license_type(license_key),
            "issued_to": company,
            "valid_from": datetime.now().isoformat(),
            "valid_until": (datetime.now() + timedelta(days=365)).isoformat(),
            "max_agents": self._get_agent_limit(license_key),
            "max_devices": self._get_device_limit(license_key),
            "features": self._get_features(license_key),
            "support_tier": self._get_support_tier(license_key),
        }

        self._save_license(license_data)
        self._license_data = license_data

        return ActivationResult(success=True, license_id=license_key)

    def activate_offline(self, response_file: str) -> ActivationResult:
        """Activate using offline response file"""
        try:
            with open(response_file, "r") as f:
                data = json.load(f)

            if data.get("status") == "approved":
                return self.activate(data["license_key"], data["company"])
            else:
                return ActivationResult(success=False, error="Activation rejected")
        except Exception as e:
            return ActivationResult(success=False, error=str(e))

    def get_status(self) -> Optional[LicenseStatus]:
        """Get current license status"""
        if self._license_data is None:
            self._load_license()

        if self._license_data is None:
            return None

        return LicenseStatus(
            license_id=self._license_data["license_id"],
            type=self._license_data["type"],
            is_valid=self._is_valid(),
            valid_until=self._license_data["valid_until"],
            features=self._license_data["features"],
            max_agents=self._license_data["max_agents"],
            max_devices=self._license_data["max_devices"],
        )

    def has_feature(self, feature: str) -> bool:
        """Check if feature is enabled"""
        status = self.get_status()
        if status is None:
            return feature == "intention_bank"
        return feature in status.features

    def get_agent_limit(self) -> int:
        """Get maximum allowed agents"""
        status = self.get_status()
        return status.max_agents if status else 10

    def get_device_limit(self) -> int:
        """Get maximum allowed devices"""
        status = self.get_status()
        return status.max_devices if status else 100

    def generate_activation_request(self) -> str:
        """Generate offline activation request"""
        machine_id = self._get_machine_id()
        return json.dumps(
            {
                "machine_id": machine_id,
                "timestamp": datetime.now().isoformat(),
                "product": "ghost-hub-sdk",
                "version": "1.0.0",
            }
        )

    def check_renewal(self) -> Optional[Dict]:
        """Check for license renewal"""
        status = self.get_status()
        if status and self._days_until_expiry() < 30:
            return {
                "available": True,
                "price": self._get_renewal_price(status.type),
                "discount": 10 if self._days_until_expiry() < 7 else 0,
            }
        return None

    def renew(self, token: str) -> bool:
        """Renew license"""
        return True

    def deactivate(self) -> bool:
        """Deactivate current license"""
        try:
            if os.path.exists(self.license_file):
                os.remove(self.license_file)
            self._license_data = None
            return True
        except Exception:
            return False

    def _load_license(self):
        """Load license from file"""
        try:
            if os.path.exists(self.license_file):
                with open(self.license_file, "r") as f:
                    self._license_data = json.load(f)
        except Exception:
            self._license_data = None

    def _save_license(self, data: Dict):
        """Save license to file"""
        os.makedirs(os.path.dirname(self.license_file), exist_ok=True)
        with open(self.license_file, "w") as f:
            json.dump(data, f, indent=2)

    def _is_valid(self) -> bool:
        """Check if license is valid"""
        if self._license_data is None:
            return False
        expiry = datetime.fromisoformat(self._license_data["valid_until"])
        return datetime.now() < expiry

    def _days_until_expiry(self) -> int:
        """Days until license expires"""
        if self._license_data is None:
            return 0
        expiry = datetime.fromisoformat(self._license_data["valid_until"])
        return (expiry - datetime.now()).days

    def _validate_key_format(self, key: str) -> bool:
        """Validate license key format"""
        parts = key.split("-")
        return len(parts) == 4 and all(len(p) == 4 for p in parts)

    def _get_license_type(self, key: str) -> str:
        """Determine license type from key"""
        if key.startswith("GH-COM"):
            return "community"
        elif key.startswith("GH-PRO"):
            return "professional"
        elif key.startswith("GH-ENT"):
            return "enterprise"
        return "trial"

    def _get_agent_limit(self, key: str) -> int:
        """Get agent limit from key"""
        if key.startswith("GH-COM"):
            return 5
        elif key.startswith("GH-PRO"):
            return 50
        return -1

    def _get_device_limit(self, key: str) -> int:
        """Get device limit from key"""
        if key.startswith("GH-COM"):
            return 10
        elif key.startswith("GH-PRO"):
            return 500
        return -1

    def _get_features(self, key: str) -> list:
        """Get enabled features from key"""
        base = ["intention_bank"]
        if key.startswith(("GH-PRO", "GH-ENT")):
            base.append("no_ui_adapter")
        if key.startswith("GH-ENT"):
            base.append("agent_federation")
        return base

    def _get_support_tier(self, key: str) -> str:
        """Get support tier from key"""
        if key.startswith("GH-ENT"):
            return "priority"
        elif key.startswith("GH-PRO"):
            return "email"
        return "community"

    def _get_renewal_price(self, license_type: str) -> float:
        """Get renewal price"""
        prices = {"community": 0, "professional": 399, "enterprise": 1999}
        return prices.get(license_type, 0)

    def _get_machine_id(self) -> str:
        """Get unique machine identifier"""
        import platform

        data = f"{platform.node()}-{platform.machine()}-{platform.processor()}"
        return hashlib.md5(data.encode()).hexdigest()[:16]


def main():
    """CLI interface"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python license_manager.py <command> [args]")
        print("Commands: activate, status, deactivate, offline")
        sys.exit(1)

    cmd = sys.argv[1]
    manager = LicenseManager()

    if cmd == "activate":
        if len(sys.argv) < 4:
            print("Usage: license_manager.py activate <key> <company>")
            sys.exit(1)
        result = manager.activate(sys.argv[2], sys.argv[3])
        print(f"Success: {result.success}")
        if result.error:
            print(f"Error: {result.error}")

    elif cmd == "status":
        status = manager.get_status()
        if status:
            print(f"License ID: {status.license_id}")
            print(f"Type: {status.type}")
            print(f"Valid: {status.is_valid}")
            print(f"Expires: {status.valid_until}")
        else:
            print("No license found")

    elif cmd == "deactivate":
        if manager.deactivate():
            print("License deactivated")
        else:
            print("Failed to deactivate")


if __name__ == "__main__":
    main()
