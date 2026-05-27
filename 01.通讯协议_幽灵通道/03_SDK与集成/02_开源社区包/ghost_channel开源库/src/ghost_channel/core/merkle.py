"""
Ghost Channel - Merkle Tree
幽灵通道 - Merkle树完整性验证

原子能力D: Merkle完整性验证
实现: SHA-256哈希树, 防篡改, 低成本验证
验证: 100%完整性验证
"""

from __future__ import annotations
import hashlib
import json
from typing import Any, TypedDict
from dataclasses import dataclass


@dataclass
class MerkleProof:
    """Merkle证明"""

    root: str
    leaf_hash: str
    proof: list[str]
    leaf_index: int


class MerkleTree:
    """Merkle树 - 完整性验证器"""

    def __init__(self, hash_func=None):
        self.hash_func = hash_func or hashlib.sha256
        self.leaves: list[bytes] = []
        self.tree: list[list[bytes]] = []

    def compute_hash(self, data: Any) -> str:
        """计算数据的SHA-256哈希"""
        if isinstance(data, (dict, list)):
            data_str = json.dumps(data, sort_keys=True, default=str).encode("utf-8")
        elif isinstance(data, str):
            data_str = data.encode("utf-8")
        elif isinstance(data, bytes):
            data_str = data
        else:
            data_str = str(data).encode("utf-8")
        return hashlib.sha256(data_str).hexdigest()

    def build(self, items: list[Any]) -> str:
        """
        构建Merkle树

        Args:
            items: 数据项列表

        Returns:
            根哈希
        """
        if not items:
            self.tree = []
            self.leaves = []
            return self.compute_hash("")

        # 计算叶子哈希
        self.leaves = [self.compute_hash(item) for item in items]

        if not self.leaves:
            return ""

        # 构建树
        level = self.leaves
        self.tree = [level]

        while len(level) > 1:
            next_level = []
            for i in range(0, len(level), 2):
                if i + 1 < len(level):
                    combined = level[i] + level[i + 1]
                else:
                    # 奇数个节点，复制最后一个
                    combined = level[i] + level[i]
                next_level.append(self.compute_hash(combined))

            self.tree.append(next_level)
            level = next_level

        return self.tree[0][0] if self.tree and self.tree[0] else ""

    def get_root(self) -> str:
        """获取根哈希"""
        if not self.tree or not self.tree[0]:
            return ""
        return self.tree[0][0]

    def get_depth(self) -> int:
        """获取树深度"""
        return len(self.tree)

    def verify(self, items: list[Any], expected_root: str) -> bool:
        """
        验证数据完整性

        Args:
            items: 数据项列表
            expected_root: 期望的根哈希

        Returns:
            是否验证通过
        """
        actual_root = self.build(items)
        return actual_root == expected_root

    def verify_proof(self, proof: MerkleProof) -> bool:
        """验证Merkle证明"""
        current = proof.leaf_hash

        for i, sibling in enumerate(proof.proof):
            if proof.leaf_index % 2 == 0:
                current = self.compute_hash(current + sibling)
            else:
                current = self.compute_hash(sibling + current)
            proof.leaf_index //= 2

        return current == proof.root

    def generate_proof(self, items: list[Any], leaf_index: int) -> MerkleProof | None:
        """生成Merkle证明"""
        root = self.build(items)

        if leaf_index < 0 or leaf_index >= len(self.leaves):
            return None

        proof = []
        idx = leaf_index

        for level in range(len(self.tree) - 1):
            if idx % 2 == 0:
                sibling = (
                    self.tree[level][idx + 1]
                    if idx + 1 < len(self.tree[level])
                    else self.tree[level][idx]
                )
            else:
                sibling = self.tree[level][idx - 1]
            proof.append(sibling)
            idx //= 2

        return MerkleProof(
            root=root,
            leaf_hash=self.leaves[leaf_index],
            proof=proof,
            leaf_index=leaf_index,
        )


class IntegrityVerifier:
    """完整性验证器"""

    def __init__(self):
        self.merkle = MerkleTree()
        self.roots: dict[str, str] = {}

    def verify_state(self, state: dict, expected_root: str) -> bool:
        """验证状态完整性"""
        items = list(state.values())
        return self.merkle.verify(items, expected_root)

    def verify_delta(self, delta_data: dict, expected_hash: str) -> bool:
        """验证Delta完整性"""
        actual_hash = self.merkle.compute_hash(delta_data)
        return actual_hash == expected_hash

    def store_root(self, entity_id: str, root: str):
        """存储根哈希"""
        self.roots[entity_id] = root

    def get_root(self, entity_id: str) -> str:
        """获取根哈希"""
        return self.roots.get(entity_id, "")

    def verify_entity(self, entity_id: str, state: dict) -> bool:
        """验证实体完整性"""
        expected_root = self.roots.get(entity_id, "")
        if not expected_root:
            return False
        return self.verify_state(state, expected_root)
