"""
QCM Resonance Calculator - R value calculation
Version: 6.0 (2026-04-28)
Weights: v6.0 emergence (0.35/0.40/0.25) + E penalty removed
Ref: 22_FORMULA_MATRIX_ANALYSIS.md, Line 429

NOTE: Constants sourced from qcm/config.py DEFAULT_CONFIG["paper_params"]["calculator"].
      Cannot use lazy import here due to circular dependency (qcm.core → calculator → qcm.config).
"""
import math
from typing import List, Dict
from simple_role import SimpleRole, ROLE_CONFIG
from semantic_embedder import SemanticEmbedder


class ResonanceCalculator:
    """Resonance calculator - R value core"""

    # Paper-calibrated constants (source: qcm/config.py paper_params.calculator)
    W_K = 0.35  # v6.0 calibrated weight
    W_C = 0.40  # v6.0 calibrated weight
    W_I = 0.25  # v6.0 calibrated weight
    W_E = 0.00  # v6.0: E penalty removed (kept param for back-compat)

    F_0 = 5  # Paper half-saturation constant

    # Hybrid mode config
    TRANSITION_START = 10  # Round to start transition
    TRANSITION_END = 30   # Round when fully embedding-based
    
    _semantic_embedder = None
    
    @classmethod
    def _get_embedder(cls):
        if cls._semantic_embedder is None:
            cls._semantic_embedder = SemanticEmbedder()
        return cls._semantic_embedder
    
    @classmethod
    def _compute_alpha(cls, round_count: int) -> float:
        """Compute blending factor alpha for hybrid mode"""
        if round_count <= cls.TRANSITION_START:
            return 0.0  # Pure semantic
        elif round_count >= cls.TRANSITION_END:
            return 1.0  # Pure embedding
        else:
            # Linear interpolation
            return (round_count - cls.TRANSITION_START) / (cls.TRANSITION_END - cls.TRANSITION_START)

    def __init__(self):
        self.history: List[float] = []

    def cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity (Formula 2)"""
        if len(vec1) != len(vec2):
            return 0.0

        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = math.sqrt(sum(x**2 for x in vec1))
        norm2 = math.sqrt(sum(x**2 for x in vec2))

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot_product / (norm1 * norm2)

    def jaccard_complement(self, set1: set, set2: set) -> float:
        """Calculate Jaccard complement (Formula 3)"""
        if not set1 and not set2:
            return 0.0

        intersection = len(set1 & set2)
        union = len(set1 | set2)

        if union == 0:
            return 0.0

        return 1.0 - (intersection / union)

    def interaction_frequency(
        self, entity_a: SimpleRole, entity_b: SimpleRole, base: float = None
    ) -> float:
        """
        Calculate interaction frequency (Formula 4)

        I = F / (F + F_0) * e^(-λΔt)
        Using: F_0 = 5 (paper constant)
        """
        if base is None:
            base = self.F_0
            
        f_a = entity_a.interaction_count
        f_b = entity_b.interaction_count
        f_ij = min(f_a, f_b)

        return f_ij / (f_ij + base)

    def kl_divergence(self, dist1: Dict[str, float], dist2: Dict[str, float]) -> float:
        """
        Calculate KL divergence (Formula 5)

        E_div = D_KL(P || Q) + D_KL(Q || P)
        """
        all_keys = set(dist1.keys()) | set(dist2.keys())

        d1_sum = sum(dist1.values()) or 1.0
        d2_sum = sum(dist2.values()) or 1.0

        kl_1_2 = 0.0
        kl_2_1 = 0.0

        for key in all_keys:
            p = dist1.get(key, 0.0) / d1_sum
            q = dist2.get(key, 0.0) / d2_sum

            p = max(p, 1e-10)
            q = max(q, 1e-10)

            kl_1_2 += p * math.log(p / q)
            kl_2_1 += q * math.log(q / p)

        return kl_1_2 + kl_2_1

    def calculate_R(self, entity_a: SimpleRole, entity_b: SimpleRole, round_count: int = 0) -> float:
        """
        Calculate knowledge resonance value (Formula 1 core)

        R = w1*K_sim + w2*C_comp + w3*I_freq - w4*E_divergence
        
        Hybrid mode: K = semantic_K * (1-alpha) + embedding_K * alpha
        """
        # K_sim: hybrid semantic + embedding similarity
        if ROLE_CONFIG.USE_SEMANTIC:
            embedder = self._get_embedder()
            
            # Semantic K (fixed)
            k_semantic = embedder.get_combined_similarity(entity_a.name, entity_b.name)
            k_semantic = max(0, k_semantic)
            
            # Embedding K (dynamic)
            k_embedding = self.cosine_similarity(entity_a.embedding, entity_b.embedding)
            k_embedding = (k_embedding + 1) / 2  # normalize to [0,1]
            
            # Blend based on round
            alpha = self._compute_alpha(round_count)
            k_sim = k_semantic * (1 - alpha) + k_embedding * alpha
        else:
            k_sim = self.cosine_similarity(entity_a.embedding, entity_b.embedding)
            k_sim = (k_sim + 1) / 2  # normalize to [0,1]

        # C_comp: complementarity (Jaccard)
        c_comp = self.jaccard_complement(set(entity_a.skills), set(entity_b.skills))

        # I_freq: interaction frequency
        i_freq = self.interaction_frequency(entity_a, entity_b)

        # E_divergence: divergence (KL)
        e_div = self.kl_divergence(
            entity_a.expertise_distribution, entity_b.expertise_distribution
        )
        e_div = min(e_div, 1.0)  # clamp to [0,1]

        # Formula 1: R = w1*K + w2*C + w3*I - w4*E
        R = self.W_K * k_sim + self.W_C * c_comp + self.W_I * i_freq - self.W_E * e_div

        # clamp to [0,1]
        R = max(0.0, min(1.0, R))

        self.history.append(R)

        return R

    def get_components(
        self, entity_a: SimpleRole, entity_b: SimpleRole, round_count: int = 0
    ) -> Dict[str, float]:
        """获取R值的各个分量（用于调试）"""
        if ROLE_CONFIG.USE_SEMANTIC:
            embedder = self._get_embedder()
            
            # Semantic K
            k_semantic = embedder.get_combined_similarity(entity_a.name, entity_b.name)
            k_semantic = max(0, k_semantic)
            cos_sim = embedder.get_role_pair_similarity(entity_a.name, entity_b.name)
            skill_comp = embedder.get_skill_overlap(entity_a.name, entity_b.name)
            
            # Embedding K
            k_embedding = self.cosine_similarity(entity_a.embedding, entity_b.embedding)
            k_embedding = (k_embedding + 1) / 2
            
            # Hybrid K
            alpha = self._compute_alpha(round_count)
            k_sim = k_semantic * (1 - alpha) + k_embedding * alpha
        else:
            k_sim = self.cosine_similarity(entity_a.embedding, entity_b.embedding)
            k_sim = (k_sim + 1) / 2
            cos_sim = k_sim
            skill_comp = k_sim
            alpha = 0.0

        c_comp = self.jaccard_complement(set(entity_a.skills), set(entity_b.skills))

        i_freq = self.interaction_frequency(entity_a, entity_b)

        e_div = self.kl_divergence(
            entity_a.expertise_distribution, entity_b.expertise_distribution
        )
        e_div = min(e_div, 1.0)

        return {
            "K_sim": round(k_sim, 4),
            "k_semantic": round(k_semantic, 4) if ROLE_CONFIG.USE_SEMANTIC else round(k_sim, 4),
            "k_embedding": round(k_embedding, 4) if ROLE_CONFIG.USE_SEMANTIC else round(k_sim, 4),
            "alpha": round(alpha, 4) if ROLE_CONFIG.USE_SEMANTIC else 0.0,
            "cos_sim": round(cos_sim, 4),
            "skill_comp": round(skill_comp, 4),
            "C_comp": round(c_comp, 4),
            "I_freq": round(i_freq, 4),
            "E_div": round(e_div, 4),
            "R": round(
                self.W_K * k_sim
                + self.W_C * c_comp
                + self.W_I * i_freq
                - self.W_E * e_div,
                4,
            ),
        }


def test_calculator():
    """测试共鸣计算器"""
    from simple_role import create_demo_roles

    role1, role2 = create_demo_roles()

    calc = ResonanceCalculator()

    # 初始R值
    R = calc.calculate_R(role1, role2)
    print(f"初始R值: {R:.4f}")

    # 分量分解
    components = calc.get_components(role1, role2)
    print(f"分量: {components}")

    # 模拟交互后更新
    role1.add_memory({"type": "sync", "from": role2.name})
    role2.add_memory({"type": "sync", "from": role1.name})

    R2 = calc.calculate_R(role1, role2)
    print(f"交互后R值: {R2:.4f}")

    return R, R2


if __name__ == "__main__":
    r1, r2 = test_calculator()
    print(f"✅ 共鸣计算器测试通过")
