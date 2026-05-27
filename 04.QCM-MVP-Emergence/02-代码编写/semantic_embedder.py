"""
Semantic Embedder - Skill-Based Version
Version: 3.0 (2026-04-27)
Uses skill keyword vectors and TF-IDF-like approach
"""
import math
import re
from typing import List, Dict, Set
from collections import Counter

class SemanticEmbedder:
    """
    Semantic embedder using skill-based approach:
    1. Extract skill keywords from role descriptions
    2. Create skill vectors
    3. Use Jaccard + word overlap for similarity
    This aligns with paper's F2-F3 design
    """
    
    # Extended skill vocabulary with more details
    VOCABULARY = {
        # Communication
        "沟通": 1.0, "协调": 0.8, "合作": 0.7, "交流": 0.6,
        "文档": 0.8, "整理": 0.9, "总结": 0.9, "记录": 0.7,
        
        # Analysis
        "分析": 1.0, "研究": 0.9, "创新": 0.8, "探索": 0.7,
        "数据": 0.8, "模式": 0.7, "假设": 0.6, "测试": 0.6,
        
        # Management
        "任务": 0.9, "分配": 0.8, "进度": 0.9, "资源": 0.7,
        "计划": 0.9, "预测": 0.8, "风险": 0.7, "战略": 0.8,
        
        # Quality
        "评估": 0.9, "评审": 0.8, "反馈": 0.8, "决策": 0.9,
        "质量": 0.8, "标准": 0.7, "审查": 0.7, "判断": 0.6,
        
        # Execution
        "执行": 1.0, "实施": 0.8, "实现": 0.7, "优化": 0.9,
        "监控": 0.9, "跟踪": 0.7, "交付": 0.8, "完成": 0.7,
        
        # Integration
        "综合": 0.9, "归纳": 0.8, "演绎": 0.7, "创作": 0.9,
        "整合": 0.7, "框架": 0.6, "系统": 0.6, "方案": 0.7,
        
        # Monitoring
        "日志": 0.9, "报表": 0.8, "告警": 0.9, "监控": 1.0,
        "健康": 0.7, "状态": 0.6, "性能": 0.7, "追踪": 0.7,
    }
    
    ROLE_TEMPLATES = {
        "Secretary": {
            "keywords": ["文档", "整理", "总结", "协调", "沟通", "会议", "日程", "记录", "沟通"],
            "skills": ["整理", "总结", "协调", "沟通"]
        },
        "Researcher": {
            "keywords": ["分析", "研究", "创新", "探索", "假设", "数据", "测试", "模式", "沟通"],
            "skills": ["分析", "研究", "创新", "沟通"]
        },
        "Coordinator": {
            "keywords": ["任务", "分配", "进度", "资源", "协调", "时间线", "项目"],
            "skills": ["任务分配", "进度跟踪", "资源协调", "沟通"]
        },
        "Evaluator": {
            "keywords": ["评估", "评审", "质量", "标准", "反馈", "决策", "判断"],
            "skills": ["评估", "评审", "反馈", "决策"]
        },
        "Synthesizer": {
            "keywords": ["综合", "归纳", "整合", "框架", "方案", "创作", "融合"],
            "skills": ["综合", "归纳", "演绎", "创作"]
        },
        "Planner": {
            "keywords": ["计划", "预测", "风险", "战略", "目标", "长期", "规划"],
            "skills": ["计划", "预测", "风险管理", "战略"]
        },
        "Executor": {
            "keywords": ["执行", "实施", "优化", "监控", "交付", "完成", "性能"],
            "skills": ["执行", "监控", "优化", "交付"]
        },
        "Monitor": {
            "keywords": ["监控", "日志", "告警", "报表", "健康", "状态", "追踪"],
            "skills": ["监控", "告警", "日志", "报表"]
        }
    }
    
    def __init__(self):
        self.method = "skill_based"
        self.dimension = len(self.VOCABULARY)
        self.embeddings_cache: Dict[str, List[float]] = {}
        
        # Pre-compute embeddings
        self._precompute_embeddings()
    
    def _keyword_to_vector(self, keywords: List[str]) -> List[float]:
        """Convert keywords to weighted vector"""
        vec = [0.0] * self.dimension
        
        for i, (word, weight) in enumerate(self.VOCABULARY.items()):
            for kw in keywords:
                if kw in word or word in kw:
                    vec[i] = weight
        
        # Normalize
        norm = math.sqrt(sum(x**2 for x in vec))
        if norm > 0:
            vec = [x / norm for x in vec]
        
        return vec
    
    def _precompute_embeddings(self):
        """Pre-compute embeddings for all roles"""
        for role_name, template in self.ROLE_TEMPLATES.items():
            keywords = template["keywords"]
            embedding = self._keyword_to_vector(keywords)
            self.embeddings_cache[role_name] = embedding
    
    def encode(self, text: str) -> List[float]:
        """Encode text based on keyword matching"""
        keywords = []
        for word in self.VOCABULARY.keys():
            if word in text:
                keywords.append(word)
        return self._keyword_to_vector(keywords)
    
    def encode_role(self, role_name: str) -> List[float]:
        """Get pre-computed role embedding"""
        return self.embeddings_cache.get(role_name, self._keyword_to_vector([]))
    
    def get_role_pair_similarity(self, role_a: str, role_b: str) -> float:
        """Get cosine similarity between two roles"""
        emb_a = self.encode_role(role_a)
        emb_b = self.encode_role(role_b)
        
        # Cosine similarity
        dot = sum(a * b for a, b in zip(emb_a, emb_b))
        
        return dot
    
    def get_all_role_similarities(self) -> Dict[str, float]:
        """Get similarities for all role pairs"""
        roles = list(self.ROLE_TEMPLATES.keys())
        results = {}
        
        for i, role_a in enumerate(roles):
            for role_b in roles[i+1:]:
                key = f"{role_a}-{role_b}"
                sim = self.get_role_pair_similarity(role_a, role_b)
                results[key] = sim
                
        return results
    
    def get_skill_overlap(self, role_a: str, role_b: str) -> float:
        """Get skill overlap (Jaccard-style)"""
        skills_a = set(self.ROLE_TEMPLATES[role_a]["skills"])
        skills_b = set(self.ROLE_TEMPLATES[role_b]["skills"])
        
        intersection = len(skills_a & skills_b)
        union = len(skills_a | skills_b)
        
        return 1.0 - (intersection / union) if union > 0 else 0.0
    
    def get_combined_similarity(self, role_a: str, role_b: str) -> float:
        """Combine cosine similarity with skill complementarity"""
        cos_sim = self.get_role_pair_similarity(role_a, role_b)
        skill_comp = self.get_skill_overlap(role_a, role_b)
        
        # Weighted combination: 40% semantic + 60% skill complementarity
        return 0.4 * cos_sim + 0.6 * skill_comp


def test_semantic_embedder():
    """Test the semantic embedder"""
    print("=" * 60)
    print("Semantic Embedder Test (Skill-Based)")
    print("=" * 60)
    
    embedder = SemanticEmbedder()
    
    print(f"\n[OK] Method: {embedder.method}")
    print(f"[OK] Dimension: {embedder.dimension}")
    print(f"[OK] Vocabulary: {len(embedder.VOCABULARY)}")
    
    print("\n--- Cosine Similarity ---")
    similarities = embedder.get_all_role_similarities()
    
    for pair, sim in sorted(similarities.items()):
        print(f"  {pair}: {sim:.4f}")
    
    print("\n--- Combined Similarity (with Skill Complementarity) ---")
    
    key_pairs = [
        ("Secretary", "Researcher"),
        ("Secretary", "Coordinator"),
        ("Researcher", "Evaluator"),
        ("Coordinator", "Executor"),
    ]
    
    results = []
    for role_a, role_b in key_pairs:
        cos_sim = embedder.get_role_pair_similarity(role_a, role_b)
        skill_comp = embedder.get_skill_overlap(role_a, role_b)
        combined = embedder.get_combined_similarity(role_a, role_b)
        
        in_range = 0.3 <= combined <= 0.6 or combined > 0.7
        status = "OK" if in_range else "CHECK"
        
        print(f"  {role_a}-{role_b}: cos={cos_sim:.3f}, skill_c={skill_comp:.3f}, combined={combined:.3f} [{status}]")
        
        results.append((role_a, role_b, combined))
    
    print("\n--- Summary ---")
    for role_a, role_b, combined in results:
        print(f"  {role_a}-{role_b}: {combined:.4f}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    test_semantic_embedder()