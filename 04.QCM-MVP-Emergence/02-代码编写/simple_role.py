"""
QCM Simple Role - 角色定义
Version: 4.0 (2026-04-27)
Config: 语义模型 + 论文权重 + 固定描述

Features:
- RoleFactory: 8角色支持  
- BaseRole: 可扩展接口
- SemanticEmbedder: 技能词向量方法(与论文对齐)
"""
import random
import math
from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class RoleConfig:
    """角色系统配置"""
    DEFAULT_SEED: int = 42
    DEFAULT_DIM: int = 32
    BASE_INTERACTION: float = 5.0  # 论文标准 F_0=5
    USE_SEMANTIC: bool = True  # 使用语义embedding


ROLE_CONFIG = RoleConfig()


class SemanticEmbedder:
    """语义embedder - 技能词向量方法"""
    
    VOCABULARY = {
        "沟通": 1.0, "协调": 0.8, "合作": 0.7, "交流": 0.6,
        "文档": 0.8, "整理": 0.9, "总结": 0.9, "记录": 0.7,
        "分析": 1.0, "研究": 0.9, "创新": 0.8, "探索": 0.7,
        "数据": 0.8, "模式": 0.7, "假设": 0.6, "测试": 0.6,
        "任务": 0.9, "分配": 0.8, "进度": 0.9, "资源": 0.7,
        "计划": 0.9, "预测": 0.8, "风险": 0.7, "战略": 0.8,
        "评估": 0.9, "评审": 0.8, "反馈": 0.8, "决策": 0.9,
        "质量": 0.8, "标准": 0.7, "审查": 0.7, "判断": 0.6,
        "执行": 1.0, "实施": 0.8, "实现": 0.7, "优化": 0.9,
        "监控": 0.9, "跟踪": 0.7, "交付": 0.8, "完成": 0.7,
        "综合": 0.9, "归纳": 0.8, "演绎": 0.7, "创作": 0.9,
        "整合": 0.7, "框架": 0.6, "系统": 0.6, "方案": 0.7,
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
    
    _instance = None
    _embeddings = {}
    
    @classmethod
    def get_embedding(cls, role_name: str) -> List[float]:
        """Get pre-computed semantic embedding for role"""
        if role_name not in cls._embeddings:
            cls._compute_embedding(role_name)
        return cls._embeddings.get(role_name, [0.0] * 32)
    
    @classmethod
    def _compute_embedding(cls, role_name: str):
        """Compute embedding from keywords"""
        template = cls.ROLE_TEMPLATES.get(role_name)
        if not template:
            cls._embeddings[role_name] = [0.0] * 32
            return
            
        keywords = template.get("keywords", [])
        dim = 32
        vec = [0.0] * dim
        
        for i, (word, weight) in enumerate(cls.VOCABULARY.items()):
            for kw in keywords:
                if kw in word or word in kw:
                    vec[i % dim] += weight
        
        norm = math.sqrt(sum(x**2 for x in vec))
        if norm > 0:
            vec = [x / norm for x in vec]
        cls._embeddings[role_name] = vec
    
    @classmethod
    def get_similarity(cls, role_a: str, role_b: str) -> float:
        """Get cosine similarity between two roles"""
        emb_a = cls.get_embedding(role_a)
        emb_b = cls.get_embedding(role_b)
        
        dot = sum(a * b for a, b in zip(emb_a, emb_b))
        return dot


class BaseRole(ABC):
    @abstractmethod
    def get_state(self) -> Dict[str, Any]:
        pass
    @abstractmethod
    def get_embedding(self) -> List[float]:
        pass
    @abstractmethod
    def update_embedding(self, other: List[float], strength: float):
        pass


class SimpleRole(BaseRole):
    """简单角色实体 - 使用语义embedding"""
    
    def __init__(
        self,
        name: str,
        skills: List[str],
        expertise_distribution: Dict[str, float] = None,
        seed: Optional[int] = None,
        initial_embedding: Optional[List[float]] = None,
        role_type: str = "general",
    ):
        self.name = name
        self.skills = skills
        self.expertise_distribution = expertise_distribution or self._default_distribution()
        self.role_type = role_type
        
        if initial_embedding is not None:
            self.embedding = initial_embedding
        elif ROLE_CONFIG.USE_SEMANTIC and name in SemanticEmbedder.ROLE_TEMPLATES:
            self.embedding = SemanticEmbedder.get_embedding(name)
        else:
            self.embedding = self._generate_embedding(seed)
        
        self.memory: List[Dict[str, Any]] = []
        self.interaction_count = 0
    
    def _default_distribution(self) -> Dict[str, float]:
        total = len(self.skills)
        return {skill: 1.0 / total for skill in self.skills}
    
    def _generate_embedding(self, seed: Optional[int] = None) -> List[float]:
        """Generate role embedding - different seeds produce different embeddings"""
        dim = ROLE_CONFIG.DEFAULT_DIM
        if seed is not None:
            # Use provided seed for deterministic but different embeddings
            rng = random.Random(seed)
        else:
            # True random for testing
            rng = random.Random()
        vec = [rng.uniform(-1, 1) for _ in range(dim)]
        norm = math.sqrt(sum(x**2 for x in vec))
        return [x / norm for x in vec] if norm > 0 else vec
    
    def get_state(self) -> Dict[str, Any]:
        return {"name": self.name, "skills": self.skills, "role_type": self.role_type,
                "embedding": self.embedding, "memory_size": len(self.memory),
                "interaction_count": self.interaction_count}
    
    def get_embedding(self) -> List[float]:
        return self.embedding
    
    def update_embedding(self, other_embedding: List[float], strength: float = 0.1):
        for i in range(len(self.embedding)):
            diff = other_embedding[i] - self.embedding[i]
            adjustment = diff * strength * (1 + 0.1 * self.interaction_count)
            self.embedding[i] += adjustment
        norm = math.sqrt(sum(x**2 for x in self.embedding))
        if norm > 0:
            self.embedding = [x / norm for x in self.embedding]
    
    def add_memory(self, event):
        self.memory.append(event)
        self.interaction_count += 1
    
    def converge_expertise(self, other_distribution: Dict[str, float], strength: float = 0.10):
        """
        Converge expertise distribution toward another role.
        This reduces E_divergence over time.
        """
        all_keys = set(self.expertise_distribution.keys()) | set(other_distribution.keys())
        
        new_dist = {}
        for key in all_keys:
            p_self = self.expertise_distribution.get(key, 0.0)
            p_other = other_distribution.get(key, 0.0)
            new_dist[key] = p_self + strength * (p_other - p_self)
        
        total = sum(new_dist.values())
        if total > 0:
            new_dist = {k: v/total for k, v in new_dist.items()}
        
        self.expertise_distribution = new_dist
    
    def decrease_divergence(self, factor: float = 0.05):
        """Deprecated: Use converge_expertise instead"""
        pass


class RoleFactory:
    """角色工厂"""
    ROLE_TEMPLATES = {
        "Secretary": {"skills": ["整理", "总结", "协调", "沟通"], "expertise": {"沟通": 0.25, "整理": 0.25, "总结": 0.25, "协调": 0.25}},
        "Researcher": {"skills": ["分析", "研究", "创新", "沟通"], "expertise": {"分析": 0.25, "研究": 0.25, "创新": 0.25, "沟通": 0.25}},
        "Coordinator": {"skills": ["任务分配", "进度跟踪", "资源协调", "沟通"], "expertise": {"任务分配": 0.25, "进度跟踪": 0.25, "资源协调": 0.25, "沟通": 0.25}},
        "Evaluator": {"skills": ["评估", "评审", "反馈", "决策"], "expertise": {"评估": 0.25, "评审": 0.25, "反馈": 0.25, "决策": 0.25}},
        "Synthesizer": {"skills": ["综合", "归纳", "演绎", "创作"], "expertise": {"综合": 0.25, "归纳": 0.25, "演绎": 0.25, "创作": 0.25}},
        "Planner": {"skills": ["计划", "预测", "风险管理", "战略"], "expertise": {"计划": 0.25, "预测": 0.25, "风险管理": 0.25, "战略": 0.25}},
        "Executor": {"skills": ["执行", "监控", "优化", "交付"], "expertise": {"执行": 0.25, "监控": 0.25, "优化": 0.25, "交付": 0.25}},
        "Monitor": {"skills": ["监控", "告警", "日志", "报表"], "expertise": {"监控": 0.25, "告警": 0.25, "日志": 0.25, "报表": 0.25}},
    }
    @classmethod
    def create_role(cls, role_type: str, seed: int = None, custom_skills=None):
        t = cls.ROLE_TEMPLATES.get(role_type)
        if not t: raise ValueError(f"Unknown: {role_type}")
        role = SimpleRole(name=role_type, skills=custom_skills or t["skills"],
                          expertise_distribution=t["expertise"].copy(), seed=seed, role_type=role_type)
        role.interaction_count = 15  # More initial interactions
        return role
    @classmethod
    def get_available_roles(cls): return list(cls.ROLE_TEMPLATES.keys())
    @classmethod
    def create_role_set(cls, role_types, base_seed=None):
        return [cls.create_role(rt, seed=(base_seed+i) if base_seed else None) for i,rt in enumerate(role_types)]


def create_demo_roles(seed=ROLE_CONFIG.DEFAULT_SEED):
    """创建演示角色"""
    secretary = SimpleRole(name="Secretary", skills=["整理", "总结", "协调", "沟通"],
                          expertise_distribution={"沟通": 0.25, "整理": 0.25, "总结": 0.25, "协调": 0.25},
                          seed=seed, role_type="Secretary")
    researcher = SimpleRole(name="Researcher", skills=["分析", "研究", "创新", "沟通"],
                         expertise_distribution={"分析": 0.25, "研究": 0.25, "创新": 0.25, "沟通": 0.25},
                         seed=seed + 1, role_type="Researcher")
    
    # More initial interactions to boost I_freq
    secretary.interaction_count = 15
    researcher.interaction_count = 15
    
    return secretary, researcher


def create_8_roles(seed=ROLE_CONFIG.DEFAULT_SEED):
    return RoleFactory.create_role_set(RoleFactory.get_available_roles(), base_seed=seed)


if __name__ == "__main__":
    r1, r2 = create_demo_roles()
    print(f"Role1: {r1.name}, {r1.skills}")
    print(f"Role2: {r2.name}, {r2.skills}")
    print(f"Embed Dim: {len(r1.embedding)}")
    print(f"\n8 Roles:")
    for r in create_8_roles(): print(f"  {r.name}: {r.skills}")
    print(f"\n✅ Role System v3.2 - Fixed seed={ROLE_CONFIG.DEFAULT_SEED}")