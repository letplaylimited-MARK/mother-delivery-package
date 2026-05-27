"""
Ghost Hub 知识层 - 意图模板知识图谱

将意图模板与知识图谱关联，支持：
- 意图相似度推理
- 模板推荐
- 领域知识关联
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Set
from collections import defaultdict


class IntentKnowledgeGraph:
    """
    Ghost Hub 意图知识图谱

    管理意图模板的语义关系，支持意图推理和推荐

    使用示例:
        kg = IntentKnowledgeGraph()
        kg.add_template_domain("iot", ["灯", "空调", "控制"])
        similar = kg.find_similar_intents("打开客厅灯")
    """

    def __init__(self, storage_path: Optional[str] = None):
        if storage_path is None:
            storage_path = Path.home() / ".ghost_hub" / "knowledge" / "intent_graph.json"

        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)

        # 节点: template_id -> template_info
        self.templates: Dict[str, Dict[str, Any]] = {}

        # 边: relation_type -> [(source, target, weight)]
        self.relations: Dict[str, List[tuple]] = defaultdict(list)

        # 域: domain -> keywords
        self.domains: Dict[str, Set[str]] = defaultdict(set)

        # 加载
        self._load()

        # 初始化默认域
        if not self.domains:
            self._init_default_domains()

    def _init_default_domains(self):
        """初始化默认域"""
        domain_keywords = {
            "iot": {"灯", "空调", "控制", "打开", "关闭", "调节", "温度", "智能", "家居", "设备"},
            "hr": {"招聘", "面试", "简历", "人才", "员工", "绩效", "评估"},
            "finance": {"成本", "财务", "预算", "报销", "支出", "收入", "报表"},
            "ops": {"工单", "客服", "支持", "故障", "问题", "运维", "监控"},
            "data": {"分析", "统计", "数据", "报表", "可视化", "图表"},
            "code": {"代码", "开发", "编程", "实现", "重构", "测试"},
            "general": set(),
        }

        for domain, keywords in domain_keywords.items():
            self.domains[domain] = keywords

    def _load(self):
        """加载数据"""
        if not self.storage_path.exists():
            return

        try:
            with open(self.storage_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.templates = data.get("templates", {})
            self.relations = defaultdict(list, data.get("relations", {}))
            self.domains = defaultdict(set, {k: set(v) for k, v in data.get("domains", {}).items()})
        except:
            pass

    def _save(self):
        """保存数据"""
        data = {
            "templates": self.templates,
            "relations": dict(self.relations),
            "domains": {k: list(v) for k, v in self.domains.items()},
            "updated_at": str(
                Path(self.storage_path).stat().st_mtime if self.storage_path.exists() else ""
            ),
        }

        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def register_template(self, template_id: str, template_info: Dict[str, Any]):
        """注册意图模板"""
        self.templates[template_id] = {
            "id": template_id,
            "name": template_info.get("name", ""),
            "domain": template_info.get("domain", "general"),
            "description": template_info.get("description", ""),
            "keywords": list(set(template_info.get("keywords", []))),  # 转为list
            "intent_patterns": template_info.get("intent_patterns", []),
            "task_count": template_info.get("task_count", 0),
            "usage_count": 0,
            "success_rate": 1.0,
        }
        self._save()

    def update_template_stats(self, template_id: str, success: bool):
        """更新模板统计"""
        if template_id not in self.templates:
            return

        t = self.templates[template_id]
        total = t["usage_count"] + 1
        successes = t["success_rate"] * t["usage_count"] + (1 if success else 0)
        t["usage_count"] = total
        t["success_rate"] = successes / total

        self._save()

    def add_relation(self, source_id: str, target_id: str, relation_type: str, weight: float = 1.0):
        """添加模板关系"""
        if source_id not in self.templates or target_id not in self.templates:
            return

        self.relations[relation_type].append((source_id, target_id, weight))
        self._save()

    def add_domain_keyword(self, domain: str, keyword: str):
        """添加域关键词"""
        self.domains[domain].add(keyword)
        self._save()

    def detect_domain(self, text: str) -> Dict[str, float]:
        """检测文本所属域"""
        text_lower = text.lower()
        scores = {}

        for domain, keywords in self.domains.items():
            if not keywords:
                continue
            matches = sum(1 for kw in keywords if kw in text_lower)
            if matches > 0:
                scores[domain] = matches / len(keywords)

        return scores

    def find_similar_templates(self, text: str, limit: int = 5) -> List[Dict[str, Any]]:
        """查找相似模板"""
        text_lower = text.lower()
        text_words = set(text_lower.split())

        scored = []

        for template_id, template in self.templates.items():
            score = 0.0

            # 名称匹配
            name_words = set(template["name"].lower().split())
            overlap = len(text_words & name_words)
            score += overlap * 0.4

            # 描述匹配
            desc_words = set(template["description"].lower().split())
            overlap = len(text_words & desc_words)
            score += overlap * 0.2

            # 关键词匹配
            keyword_overlap = len(text_words & set(template["keywords"]))
            score += keyword_overlap * 0.3

            # 模式匹配
            for pattern in template["intent_patterns"]:
                if pattern.lower() in text_lower:
                    score += 0.5

            # 域匹配加权
            domain_scores = self.detect_domain(text)
            if template["domain"] in domain_scores:
                score += domain_scores[template["domain"]] * 0.3

            if score > 0:
                scored.append(
                    {
                        "template_id": template_id,
                        "name": template["name"],
                        "domain": template["domain"],
                        "score": score,
                        "usage_count": template["usage_count"],
                        "success_rate": template["success_rate"],
                    }
                )

        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:limit]

    def find_related_templates(self, template_id: str, depth: int = 1) -> List[Dict[str, Any]]:
        """查找关联模板"""
        if template_id not in self.templates:
            return []

        related = []
        visited = {template_id}
        current_level = [template_id]

        for _ in range(depth):
            next_level = []

            for current in current_level:
                for rel_type, edges in self.relations.items():
                    for source, target, weight in edges:
                        if source == current and target not in visited:
                            related.append(
                                {
                                    "template_id": target,
                                    "relation_type": rel_type,
                                    "weight": weight,
                                    "name": self.templates.get(target, {}).get("name", ""),
                                }
                            )
                            visited.add(target)
                            next_level.append(target)
                        elif target == current and source not in visited:
                            related.append(
                                {
                                    "template_id": source,
                                    "relation_type": rel_type,
                                    "weight": weight,
                                    "name": self.templates.get(source, {}).get("name", ""),
                                }
                            )
                            visited.add(source)
                            next_level.append(source)

            current_level = next_level

        return related

    def get_domain_templates(self, domain: str) -> List[Dict[str, Any]]:
        """获取域内所有模板"""
        return [
            {
                "template_id": tid,
                "name": t["name"],
                "description": t["description"],
                "usage_count": t["usage_count"],
                "success_rate": t["success_rate"],
            }
            for tid, t in self.templates.items()
            if t["domain"] == domain
        ]

    def suggest_template(self, text: str) -> Optional[Dict[str, Any]]:
        """推荐最佳模板"""
        similar = self.find_similar_templates(text, limit=3)

        if not similar:
            return None

        # 综合评分: 相似度 * 成功率 * 使用次数
        best = None
        best_score = -1

        for t in similar:
            score = t["score"] * (0.5 + 0.5 * t["success_rate"]) * (0.5 + 0.1 * t["usage_count"])
            if score > best_score:
                best_score = score
                best = t

        return best

    def extract_keywords(self, text: str) -> List[str]:
        """提取关键词"""
        stopwords = {
            "的",
            "了",
            "在",
            "是",
            "我",
            "有",
            "和",
            "就",
            "不",
            "人",
            "都",
            "一",
            "个",
            "上",
            "也",
            "很",
            "到",
            "说",
            "要",
            "去",
            "你",
            "会",
            "着",
            "没",
            "看",
            "好",
            "自",
            "己",
            "这",
            "那",
        }

        words = text.lower().split()
        keywords = [w for w in words if w not in stopwords and len(w) >= 2]

        return list(set(keywords))

    def learn_from_intent(self, intent_text: str, matched_template_id: Optional[str]):
        """从意图中学习"""
        keywords = self.extract_keywords(intent_text)

        # 更新域关键词
        domain_scores = self.detect_domain(intent_text)
        if domain_scores:
            dominant_domain = max(domain_scores, key=domain_scores.get)
            for kw in keywords:
                self.add_domain_keyword(dominant_domain, kw)

        # 如果有匹配的模板，增加其使用统计
        if matched_template_id:
            self.update_template_stats(matched_template_id, success=True)

            # 关联相似的关键词
            template = self.templates.get(matched_template_id, {})
            kw_list = template.get("keywords", [])
            for kw in keywords:
                if kw not in kw_list:
                    kw_list.append(kw)
            template["keywords"] = kw_list

    def get_stats(self) -> Dict[str, Any]:
        """获取统计"""
        domain_counts = defaultdict(int)
        for t in self.templates.values():
            domain_counts[t["domain"]] += 1

        return {
            "total_templates": len(self.templates),
            "total_relations": sum(len(r) for r in self.relations.values()),
            "domain_counts": dict(domain_counts),
            "domains": list(self.domains.keys()),
            "relation_types": list(self.relations.keys()),
        }


# 全局单例
_global_intent_kg: Optional[IntentKnowledgeGraph] = None


def get_intent_kg() -> IntentKnowledgeGraph:
    """获取全局意图知识图谱"""
    global _global_intent_kg
    if _global_intent_kg is None:
        _global_intent_kg = IntentKnowledgeGraph()
    return _global_intent_kg
