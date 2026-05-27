"""
意图银行组件 - 自包含实现
意图解析、模板匹配、任务分解
"""

import re
import json
import math
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple, Set
from dataclasses import dataclass, field
from collections import Counter


@dataclass
class IntentVector:
    """意图向量"""

    urgency: float = 0.5
    complexity: float = 0.5
    autonomy: float = 0.5
    cooperation: float = 0.5
    risk_tolerance: float = 0.5
    domain: str = "general"

    def to_array(self) -> List[float]:
        return [
            self.urgency,
            self.complexity,
            self.autonomy,
            self.cooperation,
            self.risk_tolerance,
        ]

    def cosine_similarity(self, other: "IntentVector") -> float:
        a = self.to_array()
        b = other.to_array()
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = sum(x * x for x in a) ** 0.5
        norm_b = sum(x * x for x in b) ** 0.5
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)


@dataclass
class Task:
    """原子任务"""

    id: str
    name: str
    description: str
    sequence: int
    dependencies: List[str] = field(default_factory=list)
    estimated_time: str = ""
    tools: List[str] = field(default_factory=list)


@dataclass
class Template:
    """意图模板"""

    id: str
    name: str
    domain: str
    description: str
    intent_patterns: List[str]
    intent_vector: IntentVector
    tasks: List[Task]
    business_metrics: Dict[str, str] = field(default_factory=dict)
    roi_estimate: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class IntentMatch:
    """意图匹配结果"""

    template: Template
    similarity: float
    confidence: float
    matched_patterns: List[str]


@dataclass
class MatchResult:
    """匹配结果集"""

    matches: List[IntentMatch]
    top_match: Optional[IntentMatch] = None

    @property
    def has_match(self) -> bool:
        return self.top_match is not None and self.top_match.similarity >= 0.3


@dataclass
class MultiIntentResult:
    """多意图解析结果"""

    intents: List[str]
    templates: List[Template]
    execution_order: List[str]


@dataclass
class TaskNode:
    """任务依赖图节点"""

    task: Task
    level: int
    parents: List[str] = field(default_factory=list)
    children: List[str] = field(default_factory=list)


@dataclass
class TaskGraph:
    """任务依赖图"""

    nodes: Dict[str, TaskNode]
    execution_order: List[List[str]]
    total_estimated_time: str


class SemanticSimilarity:
    """语义相似度计算器 (TF-IDF)"""

    def __init__(self):
        self._stopwords = set(
            [
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
                "一个",
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
                "没有",
                "看",
                "好",
                "自己",
                "这",
                "那",
                "么",
            ]
        )

    def tokenize(self, text: str) -> List[str]:
        tokens = re.findall(r"[\w]+", text.lower())
        return [t for t in tokens if t not in self._stopwords and len(t) > 1]

    def calculate_tfidf(self, documents: List[str]) -> List[Dict[str, float]]:
        doc_tokens = [self.tokenize(d) for d in documents]
        doc_count = len(documents)

        idf = {}
        all_tokens = set()
        for tokens in doc_tokens:
            all_tokens.update(tokens)
            for token in set(tokens):
                idf[token] = idf.get(token, 0) + 1

        for token in idf:
            idf[token] = math.log(doc_count / (idf[token] + 1))

        tfidf_vectors = []
        for tokens in doc_tokens:
            tf = Counter(tokens)
            tfidf = {}
            for token in set(tokens):
                tfidf[token] = tf[token] / len(tokens) * idf.get(token, 0)
            tfidf_vectors.append(tfidf)

        return tfidf_vectors

    def cosine_similarity(self, vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
        common_keys = set(vec1.keys()) & set(vec2.keys())
        if not common_keys:
            return 0.0

        dot = sum(vec1[k] * vec2[k] for k in common_keys)
        norm1 = math.sqrt(sum(v * v for v in vec1.values()))
        norm2 = math.sqrt(sum(v * v for v in vec2.values()))

        if norm1 == 0 or norm2 == 0:
            return 0.0
        return dot / (norm1 * norm2)

    def similarity(self, text1: str, text2: str) -> float:
        tfidf = self.calculate_tfidf([text1, text2])
        return self.cosine_similarity(tfidf[0], tfidf[1])


class IntentParser:
    """意图解析器"""

    def __init__(self):
        self.domain_keywords = {
            "hr": ["招聘", "面试", "简历", "人才", "员工", "hr", "recruit", "interview"],
            "iot": ["灯", "空调", "控制", "家居", "设备", "iot", "home", "smart"],
            "finance": ["成本", "财务", "预算", "费用", "报销", "finance", "cost", "budget"],
            "ops": ["工单", "客服", "支持", "故障", "问题", "ops", "ticket", "support"],
            "federation": ["协作", "团队", "多agent", "分布式", "合作", "collab", "multi"],
        }
        self.intent_separators = ["并且", "同时", "还有", "和", "以及", "also", "and", ","]

    def parse(self, text: str) -> Tuple[str, float, IntentVector]:
        domain = self._detect_domain(text)
        confidence = self._calculate_confidence(text, domain)
        vector = self._create_intent_vector(text, domain)
        return domain, confidence, vector

    def separate_intents(self, text: str) -> List[str]:
        """分离多意图"""
        for sep in self.intent_separators:
            if sep in text:
                parts = text.split(sep)
                return [p.strip() for p in parts if p.strip()]
        return [text.strip()]

    def _detect_domain(self, text: str) -> str:
        text_lower = text.lower()
        scores: Dict[str, int] = {}

        for domain, keywords in self.domain_keywords.items():
            scores[domain] = sum(1 for kw in keywords if kw.lower() in text_lower)

        if scores:
            best_domain = max(scores, key=scores.get)
            if scores[best_domain] > 0:
                return best_domain
        return "general"

    def _calculate_confidence(self, text: str, domain: str) -> float:
        keywords = self.domain_keywords.get(domain, [])
        matches = sum(1 for kw in keywords if kw.lower() in text.lower())
        return min(0.9, 0.3 + matches * 0.15)

    def _create_intent_vector(self, text: str, domain: str) -> IntentVector:
        urgency = 0.5
        if any(w in text for w in ["紧急", "立即", "马上", "急"]):
            urgency = 0.8
        elif any(w in text for w in ["稍后", "不急", "以后", "未来"]):
            urgency = 0.3

        complexity = 0.5
        if any(w in text for w in ["优化", "分析", "复杂", "全面"]):
            complexity = 0.7
        elif any(w in text for w in ["简单", "快速", "只要"]):
            complexity = 0.3

        autonomy = 0.6
        if any(w in text for w in ["自动", "帮我", "执行"]):
            autonomy = 0.8

        cooperation = 0.5
        if any(w in text for w in ["协作", "团队", "多个"]):
            cooperation = 0.8

        risk = 0.4
        if any(w in text for w in ["保守", "安全", "稳妥"]):
            risk = 0.2
        elif any(w in text for w in ["激进", "大胆", "风险"]):
            risk = 0.7

        return IntentVector(urgency, complexity, autonomy, cooperation, risk, domain)


class IntentMatcher:
    """意图匹配器"""

    def __init__(self, threshold: float = 0.3):
        self.threshold = threshold
        self.parser = IntentParser()
        self.semantic = SemanticSimilarity()

    def match(self, text: str, templates: List[Template]) -> MatchResult:
        if not templates:
            return MatchResult(matches=[])

        domain, confidence, intent_vector = self.parser.parse(text)
        matches: List[IntentMatch] = []

        for template in templates:
            sim_score = self._calculate_similarity(text, template)
            vec_score = intent_vector.cosine_similarity(template.intent_vector)

            pattern_score = 0.0
            matched = []
            for pattern in template.intent_patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    pattern_score = 1.0
                    matched.append(pattern)

            semantic_score = self.semantic.similarity(text, template.description)

            final_similarity = (
                sim_score * 0.25 + vec_score * 0.25 + pattern_score * 0.25 + semantic_score * 0.25
            )

            if final_similarity >= self.threshold:
                match = IntentMatch(
                    template=template,
                    similarity=final_similarity,
                    confidence=confidence,
                    matched_patterns=matched,
                )
                matches.append(match)

        matches.sort(key=lambda x: x.similarity, reverse=True)
        top = matches[0] if matches else None

        return MatchResult(matches=matches, top_match=top)

    def _calculate_similarity(self, text: str, template: Template) -> float:
        text_lower = text.lower()
        name_lower = template.name.lower()
        desc_lower = template.description.lower()

        common_chars = set(text_lower) & set(name_lower + desc_lower)
        if not common_chars:
            return 0.0

        return len(common_chars) / max(len(set(text_lower)), 1) * 0.5


class TaskGraphBuilder:
    """任务依赖图构建器"""

    def __init__(self):
        pass

    def build(self, tasks: List[Task]) -> TaskGraph:
        nodes: Dict[str, TaskNode] = {}
        task_map = {t.id: t for t in tasks}

        for task in tasks:
            node = TaskNode(
                task=task,
                level=0,
                parents=list(task.dependencies),
                children=[],
            )
            nodes[task.id] = node

        for task_id, node in nodes.items():
            for dep_id in node.parents:
                if dep_id in nodes:
                    nodes[dep_id].children.append(task_id)

        for node in nodes.values():
            node.level = self._calculate_level(node, nodes)

        execution_order = self._get_topological_order(nodes)

        return TaskGraph(
            nodes=nodes,
            execution_order=execution_order,
            total_estimated_time=self._estimate_total_time(tasks),
        )

    def _calculate_level(self, node: TaskNode, nodes: Dict[str, TaskNode]) -> int:
        if not node.parents:
            return 0
        return max((nodes[p].level for p in node.parents if p in nodes), default=0) + 1

    def _get_topological_order(self, nodes: Dict[str, TaskNode]) -> List[List[str]]:
        levels: Dict[int, List[str]] = {}
        for task_id, node in nodes.items():
            if node.level not in levels:
                levels[node.level] = []
            levels[node.level].append(task_id)

        result = []
        for level in sorted(levels.keys()):
            result.append(levels[level])
        return result

    def _estimate_total_time(self, tasks: List[Task]) -> str:
        return f"{len(tasks)} 个任务"


class TemplateLoader:
    """模板加载器"""

    def __init__(self, templates_dir: Optional[Path] = None):
        if templates_dir is None:
            templates_dir = Path(__file__).parent.parent / "templates"
        self.templates_dir = templates_dir

    def load_all(self) -> List[Template]:
        templates = []

        if not self.templates_dir.exists():
            return self._get_builtin_templates()

        for json_file in self.templates_dir.glob("*.json"):
            if json_file.name == "index.json":
                continue
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                template = self._parse_template(data)
                templates.append(template)
            except Exception:
                continue

        if not templates:
            return self._get_builtin_templates()

        return templates

    def _parse_template(self, data: Dict) -> Template:
        if not data.get("id"):
            raise ValueError("Template missing required field: 'id'")
        if not data.get("name"):
            raise ValueError("Template missing required field: 'name'")

        vector_data = data.get("intent_vector", {})
        intent_vector = IntentVector(
            urgency=vector_data.get("urgency", 0.5),
            complexity=vector_data.get("complexity", 0.5),
            autonomy=vector_data.get("autonomy", 0.5),
            cooperation=vector_data.get("cooperation", 0.5),
            risk_tolerance=vector_data.get("risk_tolerance", 0.5),
            domain=data.get("domain", "general"),
        )

        tasks = []
        for t in data.get("tasks", []):
            if not t.get("id") or not t.get("name"):
                continue
            tasks.append(
                Task(
                    id=t["id"],
                    name=t["name"],
                    description=t.get("description", ""),
                    sequence=t.get("sequence", 1),
                    dependencies=t.get("dependencies", []),
                    estimated_time=t.get("estimated_time", ""),
                    tools=t.get("tools", []),
                )
            )

        return Template(
            id=data["id"],
            name=data["name"],
            domain=data.get("domain", "general"),
            description=data.get("description", ""),
            intent_patterns=data.get("intent_pattern", "").split("|")
            if isinstance(data.get("intent_pattern"), str)
            else data.get("intent_patterns", []),
            intent_vector=intent_vector,
            tasks=tasks,
            business_metrics=data.get("business_metrics", {}),
            roi_estimate=data.get("roi_estimate", {}),
            tags=data.get("tags", []),
        )

    def _get_builtin_templates(self) -> List[Template]:
        return [
            Template(
                id="tpl_hr_default",
                name="HR面试流程优化",
                domain="hr",
                description="优化招聘面试流程",
                intent_patterns=["面试", "招聘", "简历", "hr"],
                intent_vector=IntentVector(0.5, 0.6, 0.6, 0.7, 0.3, "hr"),
                tasks=[
                    Task("t1", "简历解析", "解析简历", 1),
                    Task("t2", "匹配度分析", "分析匹配度", 2, ["t1"]),
                    Task("t3", "问题生成", "生成面试问题", 3, ["t2"]),
                ],
            ),
            Template(
                id="tpl_iot_default",
                name="智能家居控制",
                domain="iot",
                description="控制智能设备",
                intent_patterns=["灯", "空调", "控制", "打开", "关闭"],
                intent_vector=IntentVector(0.6, 0.2, 0.9, 0.1, 0.4, "iot"),
                tasks=[
                    Task("t1", "意图解析", "解析指令", 1),
                    Task("t2", "设备匹配", "匹配设备", 2, ["t1"]),
                    Task("t3", "指令下发", "下发命令", 3, ["t2"]),
                ],
            ),
        ]


class IntentionBankComponent:
    """意图银行组件"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.threshold = self.config.get("match_threshold", 0.3)
        self.max_results = self.config.get("max_results", 5)

        templates_dir = self.config.get("templates_dir")
        self._loader = TemplateLoader(Path(templates_dir) if templates_dir else None)
        self._matcher = IntentMatcher(threshold=self.threshold)
        self._graph_builder = TaskGraphBuilder()

        self._templates: List[Template] = []
        self._load_templates()

    def _load_templates(self):
        self._templates = self._loader.load_all()

    def match_intent(self, text: str) -> MatchResult:
        """匹配意图"""
        return self._matcher.match(text, self._templates)

    def match_multi_intent(self, text: str) -> MultiIntentResult:
        """多意图解析"""
        intents = self._matcher.parser.separate_intents(text)
        templates = []
        execution_order = []

        for intent in intents:
            result = self._matcher.match(intent, self._templates)
            if result.has_match:
                templates.append(result.top_match.template)
                execution_order.append(result.top_match.template.id)

        return MultiIntentResult(
            intents=intents,
            templates=templates,
            execution_order=execution_order,
        )

    def build_task_graph(self, template: Template) -> TaskGraph:
        """构建任务依赖图"""
        return self._graph_builder.build(template.tasks)

    def get_template(self, template_id: str) -> Optional[Template]:
        """获取模板"""
        for tpl in self._templates:
            if tpl.id == template_id:
                return tpl
        return None

    def list_templates(self, domain: Optional[str] = None) -> List[Template]:
        """列出模板"""
        if domain:
            return [t for t in self._templates if t.domain == domain]
        return self._templates

    def decompose_task(self, template: Template) -> List[Task]:
        """任务分解"""
        return sorted(template.tasks, key=lambda x: x.sequence)

    def get_stats(self) -> Dict[str, Any]:
        """获取统计"""
        return {
            "enabled": True,
            "templates_loaded": len(self._templates),
            "domains": list(set(t.domain for t in self._templates)),
            "match_threshold": self.threshold,
        }
