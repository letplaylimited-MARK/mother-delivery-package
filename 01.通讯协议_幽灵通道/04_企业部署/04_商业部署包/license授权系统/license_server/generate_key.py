#!/usr/bin/env python3
"""
Ghost Channel Enterprise - License Key Generator
幽灵通道商业版 - 许可证密钥生成器
"""

import argparse
import hashlib
import sys
import time
import secrets
from datetime import datetime, timedelta

SERVER_URL = "http://localhost:8001"


def generate_trial_key() -> dict:
    """生成试用密钥"""
    return {
        "license_type": "trial",
        "features": ["semantic_matching"],
        "duration_days": 14,
        "max_activations": 1,
    }


def generate_pro_key() -> dict:
    """生成Pro密钥"""
    return {
        "license_type": "pro",
        "features": [
            "semantic_matching",
            "predictive_sync",
        ],
        "duration_days": 365,
        "max_activations": 2,
    }


def generate_team_key() -> dict:
    """生成Team密钥"""
    return {
        "license_type": "team",
        "features": [
            "semantic_matching",
            "predictive_sync",
            "knowledge_graph",
            "crystallizer",
        ],
        "duration_days": 365,
        "max_activations": 10,
    }


def generate_enterprise_key() -> dict:
    """生成Enterprise密钥"""
    return {
        "license_type": "enterprise",
        "features": [
            "semantic_matching",
            "predictive_sync",
            "knowledge_graph",
            "crystallizer",
            "learning_engine",
            "self_healing_pro",
        ],
        "duration_days": 365,
        "max_activations": 100,
    }


def generate_custom_key(
    features: list,
    duration_days: int,
    max_activations: int,
) -> dict:
    """生成自定义密钥"""
    return {
        "license_type": "custom",
        "features": features,
        "duration_days": duration_days,
        "max_activations": max_activations,
    }


def print_license_info(license_key: str, response: dict):
    """打印许可证信息"""
    print("\n" + "=" * 60)
    print("License Generated Successfully!")
    print("=" * 60)
    print(f"License Key: {license_key}")
    print(f"Expires: {response.get('expires_at', 'N/A')}")
    print(f"Features: {', '.join(response.get('features', []))}")
    print("=" * 60)
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Ghost Channel Enterprise License Key Generator"
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--trial", action="store_true", help="Generate trial license")
    group.add_argument("--pro", action="store_true", help="Generate Pro license")
    group.add_argument("--team", action="store_true", help="Generate Team license")
    group.add_argument(
        "--enterprise", action="store_true", help="Generate Enterprise license"
    )
    group.add_argument("--custom", nargs="+", help="Custom features")

    parser.add_argument(
        "--days",
        type=int,
        default=None,
        help="License duration in days (default: varies by type)",
    )
    parser.add_argument(
        "--activations",
        type=int,
        default=None,
        help="Maximum activations (default: varies by type)",
    )
    parser.add_argument(
        "--email",
        type=str,
        default=None,
        help="Customer email",
    )
    parser.add_argument(
        "--customer-id",
        type=str,
        default=None,
        help="Customer ID",
    )
    parser.add_argument(
        "--server",
        type=str,
        default=SERVER_URL,
        help="License server URL",
    )
    parser.add_argument(
        "--offline",
        action="store_true",
        help="Generate offline key (without server)",
    )

    args = parser.parse_args()

    if args.trial:
        config = generate_trial_key()
    elif args.pro:
        config = generate_pro_key()
    elif args.team:
        config = generate_team_key()
    elif args.enterprise:
        config = generate_enterprise_key()
    elif args.custom:
        config = generate_custom_key(
            features=args.custom,
            duration_days=args.days or 365,
            max_activations=args.activations or 1,
        )
    else:
        config = {}

    if args.days:
        config["duration_days"] = args.days
    if args.activations:
        config["max_activations"] = args.activations

    config["customer_email"] = args.email
    config["customer_id"] = args.customer_id

    if args.offline:
        offline_key = generate_offline_key(config)
        print_license_info(
            offline_key,
            {
                "expires_at": datetime.fromtimestamp(
                    time.time() + config["duration_days"] * 86400
                ).isoformat(),
                "features": config["features"],
            },
        )
        return

    try:
        import httpx

        response = httpx.post(
            f"{args.server}/license/generate",
            json=config,
            timeout=10,
        )

        if response.status_code == 200:
            data = response.json()
            print_license_info(data["license_key"], data)
        else:
            print(f"Error: {response.status_code} - {response.text}")
            sys.exit(1)

    except ImportError:
        print("Error: httpx required for server communication")
        print("Install with: pip install httpx")
        sys.exit(1)
    except Exception as e:
        print(f"Error connecting to server: {e}")
        print("\nUse --offline to generate keys without server connection")
        sys.exit(1)


def generate_offline_key(config: dict) -> str:
    """生成离线密钥"""
    key_id = secrets.token_hex(8)
    timestamp = int(time.time())
    duration = config.get("duration_days", 365)
    expires = timestamp + (duration * 86400)

    license_type = config.get("license_type", "custom")
    features = config.get("features", [])

    key_data = f"{license_type}:{','.join(features)}:{timestamp}:{expires}"
    key_hash = hashlib.sha256(key_data.encode()).hexdigest()[:16]

    key = f"gc_ent_{license_type[0]}{''.join(f[0] for f in features)}_{key_id}_{expires}_{key_hash}"

    return key


if __name__ == "__main__":
    main()
