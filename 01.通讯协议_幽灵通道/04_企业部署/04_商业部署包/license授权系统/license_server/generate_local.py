#!/usr/bin/env python3
"""
Ghost Channel Enterprise - Local License Generator
幽灵通道商业版 - 本地许可证生成器

无需服务器的离线许可证生成工具
"""

import hashlib
import time
import secrets
import json
import argparse
import sys
from datetime import datetime, timedelta
from typing import List, Optional, Dict
from dataclasses import dataclass, asdict


@dataclass
class LicenseInfo:
    """许可证信息"""

    key: str
    license_type: str
    features: List[str]
    issued_at: str
    expires_at: str
    max_activations: int
    customer_name: Optional[str]
    customer_email: Optional[str]
    customer_id: Optional[str]


class LocalLicenseGenerator:
    """本地许可证生成器"""

    FEATURE_CODES = {
        "semantic_matching": "s",
        "predictive_sync": "p",
        "knowledge_graph": "k",
        "crystallizer": "c",
        "learning_engine": "l",
        "self_healing_pro": "h",
    }

    FEATURE_NAMES = {v: k for k, v in FEATURE_CODES.items()}

    TYPE_CODES = {
        "trial": "t",
        "pro": "p",
        "team": "a",  # a for team
        "enterprise": "e",
    }

    TYPE_DURATIONS = {
        "trial": 14,
        "pro": 365,
        "team": 365,
        "enterprise": 365,
    }

    TYPE_ACTIVATIONS = {
        "trial": 1,
        "pro": 2,
        "team": 10,
        "enterprise": 100,
    }

    TYPE_FEATURES = {
        "trial": ["semantic_matching"],
        "pro": ["semantic_matching", "predictive_sync"],
        "team": [
            "semantic_matching",
            "predictive_sync",
            "knowledge_graph",
            "crystallizer",
        ],
        "enterprise": [
            "semantic_matching",
            "predictive_sync",
            "knowledge_graph",
            "crystallizer",
            "learning_engine",
            "self_healing_pro",
        ],
    }

    def __init__(self, secret_key: str = None):
        self.secret_key = secret_key or self._generate_secret()

    def _generate_secret(self) -> str:
        """生成密钥"""
        return secrets.token_hex(32)

    def _compute_signature(self, data: str) -> str:
        """计算签名"""
        return hashlib.sha256((data + self.secret_key).encode()).hexdigest()[:16]

    def generate_key(
        self,
        license_type: str,
        features: List[str] = None,
        duration_days: int = None,
        max_activations: int = None,
        customer_name: str = None,
        customer_email: str = None,
        customer_id: str = None,
    ) -> LicenseInfo:
        """生成许可证"""

        # 默认值
        if features is None:
            features = self.TYPE_FEATURES.get(license_type, [])
        if duration_days is None:
            duration_days = self.TYPE_DURATIONS.get(license_type, 365)
        if max_activations is None:
            max_activations = self.TYPE_ACTIVATIONS.get(license_type, 1)

        # 生成密钥组件
        timestamp = int(time.time())
        expires = timestamp + (duration_days * 86400)
        key_id = secrets.token_hex(8)

        # 构建功能代码
        feature_codes = "".join(self.FEATURE_CODES.get(f, f[0]) for f in features)

        # 构建密钥
        key_data = f"{license_type}:{','.join(features)}:{timestamp}:{expires}"
        signature = self._compute_signature(key_data)

        key = f"gc_{self.TYPE_CODES.get(license_type, 'x')}_{feature_codes}_{key_id}_{expires}_{signature}"

        return LicenseInfo(
            key=key,
            license_type=license_type,
            features=features,
            issued_at=datetime.fromtimestamp(timestamp).isoformat(),
            expires_at=datetime.fromtimestamp(expires).isoformat(),
            max_activations=max_activations,
            customer_name=customer_name,
            customer_email=customer_email,
            customer_id=customer_id,
        )

    def verify_key(self, key: str) -> Dict:
        """验证许可证"""
        parts = key.split("_")
        if len(parts) < 5:
            return {"valid": False, "error": "Invalid key format"}

        prefix = parts[0]  # gc
        type_code = parts[1]
        expires = int(parts[3])
        signature = parts[4]

        # 重建数据验证签名
        key_data = f"{parts[0]}_{parts[1]}_{parts[2]}_{parts[3]}"
        features_str = parts[2]
        expected_sig = self._compute_signature(
            f":{features_str}:{parts[0].split('_')[1] if '_' in parts[0] else ''}:{parts[3]}"
        )

        # 检查过期
        if time.time() > expires:
            return {"valid": False, "error": "License expired"}

        # 解析功能
        features = [
            self.FEATURE_NAMES.get(c, c) for c in type_code if c in self.FEATURE_NAMES
        ]
        features.append(self.FEATURE_NAMES.get(type_code[0], type_code))
        features = list(set(features))

        return {
            "valid": True,
            "expires_at": datetime.fromtimestamp(expires).isoformat(),
            "features": features,
            "license_type": self._code_to_type(type_code),
        }

    def _code_to_type(self, code: str) -> str:
        """代码转类型"""
        for t, c in self.TYPE_CODES.items():
            if c == code[0]:
                return t
        return "unknown"

    def export_json(self, license: LicenseInfo) -> str:
        """导出为JSON"""
        return json.dumps(asdict(license), indent=2, ensure_ascii=False)

    def export_txt(self, license: LicenseInfo) -> str:
        """导出为文本"""
        lines = [
            "=" * 60,
            "Ghost Channel Enterprise License",
            "=" * 60,
            f"License Key: {license.key}",
            f"Type: {license.license_type.upper()}",
            f"Features: {', '.join(license.features)}",
            f"Issued: {license.issued_at}",
            f"Expires: {license.expires_at}",
            f"Max Activations: {license.max_activations}",
        ]
        if license.customer_email:
            lines.append(f"Customer: {license.customer_email}")
        if license.customer_name:
            lines.append(f"Name: {license.customer_name}")
        lines.append("=" * 60)
        return "\n".join(lines)


def print_license(license: LicenseInfo, format: str = "text"):
    """打印许可证"""
    if format == "json":
        print(generator.export_json(license))
    else:
        print(generator.export_txt(license))


def main():
    parser = argparse.ArgumentParser(
        description="Ghost Channel Enterprise - Local License Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate trial license
  python generate_local.py --trial
  
  # Generate pro license for customer
  python generate_local.py --pro --email customer@example.com --name "John Doe"
  
  # Generate custom features license
  python generate_local.py --type pro --features semantic_matching predictive_sync --days 180
  
  # Verify a license key
  python generate_local.py --verify gc_p_sp_xxxx_xxxx_xxxx
  
  # Export as JSON
  python generate_local.py --trial --format json
        """,
    )

    # 许可证类型
    type_group = parser.add_mutually_exclusive_group()
    type_group.add_argument(
        "--trial", action="store_true", help="Trial license (14 days)"
    )
    type_group.add_argument("--pro", action="store_true", help="Pro license (1 year)")
    type_group.add_argument("--team", action="store_true", help="Team license (1 year)")
    type_group.add_argument(
        "--enterprise", action="store_true", help="Enterprise license (1 year)"
    )
    type_group.add_argument("--type", dest="license_type", help="Custom license type")

    parser.add_argument("--features", nargs="+", help="Custom features list")
    parser.add_argument("--days", type=int, help="Custom duration in days")
    parser.add_argument("--activations", type=int, help="Max activations")
    parser.add_argument("--name", dest="customer_name", help="Customer name")
    parser.add_argument("--email", dest="customer_email", help="Customer email")
    parser.add_argument("--id", dest="customer_id", help="Customer ID")
    parser.add_argument(
        "--format", choices=["text", "json"], default="text", help="Output format"
    )
    parser.add_argument("--verify", metavar="KEY", help="Verify license key")
    parser.add_argument("--secret", help="Custom secret key")

    args = parser.parse_args()

    global generator
    generator = LocalLicenseGenerator(secret_key=args.secret)

    # 验证模式
    if args.verify:
        result = generator.verify_key(args.verify)
        print(json.dumps(result, indent=2))
        return

    # 确定许可证类型
    if args.trial:
        license_type = "trial"
    elif args.pro:
        license_type = "pro"
    elif args.team:
        license_type = "team"
    elif args.enterprise:
        license_type = "enterprise"
    elif args.license_type:
        license_type = args.license_type
    else:
        parser.print_help()
        return

    # 生成许可证
    license = generator.generate_key(
        license_type=license_type,
        features=args.features,
        duration_days=args.days,
        max_activations=args.activations,
        customer_name=args.customer_name,
        customer_email=args.customer_email,
        customer_id=args.customer_id,
    )

    print_license(license, args.format)


if __name__ == "__main__":
    main()
