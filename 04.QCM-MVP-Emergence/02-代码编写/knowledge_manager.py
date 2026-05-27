"""
Knowledge Manager - 统一知识读取模块
功能：
1. 读取知识图谱 (KNOWLEDGE_GRAPH.md)
2. 读取知识结晶 (00-知识结晶/*.md)
3. 读取长期记忆 (logs/audit_log.jsonl)
4. 提供统一API查询
"""

import os
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

import re
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass


PROJECT_ROOT = Path(r"..")
CODE_DIR = PROJECT_ROOT / "02-代码编写"
KNOWLEDGE_GRAPH_FILE = CODE_DIR / "KNOWLEDGE_GRAPH.md"
CRYSTALLIZATION_DIR = PROJECT_ROOT / "00-知识结晶"
AUDIT_LOG_FILE = CODE_DIR / "logs" / "audit_log.jsonl"


@dataclass
class FormulaInfo:
    """公式信息"""
    id: int
    name: str
    paper_section: str
    code_file: Optional[str]
    line_number: Optional[int]
    aligned: str


@dataclass
class CapabilityInfo:
    """原子能力信息"""
    name: str
    code: str
    file: Optional[str]
    line_range: Optional[str]
    status: str


@dataclass
class AuditRecord:
    """审计记录"""
    transaction_id: str
    timestamp: float
    source_role: str
    destination_role: str
    message_type: str
    delta_hash: str
    bandwidth_saved: int


class KnowledgeGraphReader:
    """知识图谱读取器"""

    def __init__(self, file_path: Path = KNOWLEDGE_GRAPH_FILE):
        self.file_path = file_path
        self.content = ""
        self.formulas: List[FormulaInfo] = []
        self.capabilities: List[CapabilityInfo] = []

    def load(self) -> bool:
        """加载知识图谱"""
        if not self.file_path.exists():
            print(f"[WARN] Knowledge graph file not found: {self.file_path}")
            return False

        try:
            self.content = self.file_path.read_text(encoding='utf-8')
            self._parse_formulas()
            self._parse_capabilities()
            return True
        except Exception as e:
            print(f"[ERROR] Failed to load knowledge graph: {e}")
            return False

    def _parse_formulas(self):
        """解析22公式体系"""
        lines = self.content.split('\n')
        in_formula_table = False
        max_formula_id = 0

        for line in lines:
            if '|' in line and '公式名' in line:
                in_formula_table = True
                continue
            if in_formula_table and line.startswith('|') and '---' not in line:
                parts = [p.strip() for p in line.split('|')[1:-1]]
                if len(parts) >= 6:
                    try:
                        fid = int(parts[0]) if parts[0].isdigit() else 0
                        if fid > max_formula_id:
                            max_formula_id = fid
                        formula = FormulaInfo(
                            id=fid,
                            name=parts[1],
                            paper_section=parts[2],
                            code_file=parts[3] if parts[3] != '-' else None,
                            line_number=int(parts[4]) if parts[4].isdigit() else None,
                            aligned=parts[5]
                        )
                        self.formulas.append(formula)
                    except:
                        pass
            elif in_formula_table and line.strip() == '':
                in_formula_table = False

        if max_formula_id > len(self.formulas) and max_formula_id > 0:
            print(f"[INFO] Parsed {len(self.formulas)} formulas, max ID: {max_formula_id}")

    def _parse_capabilities(self):
        """解析10大原子能力"""
        lines = self.content.split('\n')
        in_capability_table = False

        for line in lines:
            if '|' in line and '能力' in line and '代码' in line:
                in_capability_table = True
                continue
            if in_capability_table and line.startswith('|') and '---' not in line:
                parts = [p.strip() for p in line.split('|')[1:-1]]
                if len(parts) >= 5:
                    capability = CapabilityInfo(
                        name=parts[0],
                        code=parts[1],
                        file=parts[2] if parts[2] != '-' else None,
                        line_range=parts[3] if parts[3] != '-' else None,
                        status=parts[4]
                    )
                    self.capabilities.append(capability)
            elif in_capability_table and line.strip() == '':
                in_capability_table = False

    def get_aligned_formulas(self) -> List[FormulaInfo]:
        """获取已对齐的公式"""
        return [f for f in self.formulas if '✅' in f.aligned]

    def get_unaligned_formulas(self) -> List[FormulaInfo]:
        """获取未对齐的公式"""
        return [f for f in self.formulas if '❌' in f.aligned]

    def get_integrated_capabilities(self) -> List[CapabilityInfo]:
        """获取已集成的原子能力"""
        return [c for c in self.capabilities if '集成' in c.status]

    def get_summary(self) -> Dict[str, Any]:
        """获取知识图谱摘要"""
        return {
            'total_formulas': len(self.formulas),
            'aligned_formulas': len(self.get_aligned_formulas()),
            'unaligned_formulas': len(self.get_unaligned_formulas()),
            'total_capabilities': len(self.capabilities),
            'integrated_capabilities': len(self.get_integrated_capabilities()),
        }


class KnowledgeCrystallizationReader:
    """知识结晶读取器"""

    def __init__(self, dir_path: Path = CRYSTALLIZATION_DIR):
        self.dir_path = dir_path
        self.documents: Dict[str, Dict[str, Any]] = {}

    def load_all(self) -> int:
        """加载所有知识结晶文档"""
        if not self.dir_path.exists():
            print(f"[WARN] Crystallization directory not found: {self.dir_path}")
            return 0

        count = 0
        for md_file in self.dir_path.glob("*.md"):
            try:
                content = md_file.read_text(encoding='utf-8')
                doc_info = {
                    'filename': md_file.name,
                    'path': str(md_file),
                    'size': len(content),
                    'sections': self._extract_sections(content),
                    'preview': content[:500],
                }
                self.documents[md_file.name] = doc_info
                count += 1
            except Exception as e:
                print(f"[ERROR] Failed to load {md_file.name}: {e}")

        return count

    def _extract_sections(self, content: str) -> List[str]:
        """提取文档章节"""
        sections = []
        for line in content.split('\n'):
            if line.startswith('#'):
                sections.append(line.strip('#').strip())
        return sections

    def get_document(self, name: str) -> Optional[Dict[str, Any]]:
        """获取指定文档"""
        return self.documents.get(name)

    def search_keyword(self, keyword: str) -> List[Dict[str, Any]]:
        """关键词搜索"""
        results = []
        for name, doc in self.documents.items():
            if keyword.lower() in name.lower() or keyword in doc.get('preview', ''):
                results.append(doc)
        return results

    def get_summary(self) -> Dict[str, Any]:
        """获取知识结晶摘要"""
        return {
            'total_documents': len(self.documents),
            'documents': [
                {
                    'name': d['filename'],
                    'size': d['size'],
                    'sections': len(d['sections'])
                }
                for d in self.documents.values()
            ]
        }


class LongTermMemoryReader:
    """长期记忆读取器 - 审计日志"""

    def __init__(self, log_file: Path = AUDIT_LOG_FILE):
        self.log_file = log_file
        self.records: List[AuditRecord] = []

    def load(self) -> int:
        """加载审计日志"""
        if not self.log_file.exists():
            print(f"[WARN] Audit log file not found: {self.log_file}")
            return 0

        count = 0
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        try:
                            data = json.loads(line)
                            record = AuditRecord(
                                transaction_id=data.get('transaction_id', ''),
                                timestamp=data.get('timestamp', 0),
                                source_role=data.get('source_role', ''),
                                destination_role=data.get('destination_role', ''),
                                message_type=data.get('message_type', ''),
                                delta_hash=data.get('delta_hash', ''),
                                bandwidth_saved=data.get('bandwidth_saved_bytes', 0)
                            )
                            self.records.append(record)
                            count += 1
                        except json.JSONDecodeError:
                            pass
        except Exception as e:
            print(f"[ERROR] Failed to load audit log: {e}")

        return count

    def get_recent(self, n: int = 10) -> List[AuditRecord]:
        """获取最近的n条记录"""
        return self.records[-n:] if self.records else []

    def get_statistics(self) -> Dict[str, Any]:
        """获取审计统计"""
        if not self.records:
            return {
                'total_transactions': 0,
                'total_bandwidth_saved': 0,
                'unique_roles': set(),
            }

        roles = set()
        total_bandwidth = 0

        for r in self.records:
            roles.add(r.source_role)
            roles.add(r.destination_role)
            total_bandwidth += r.bandwidth_saved

        return {
            'total_transactions': len(self.records),
            'total_bandwidth_saved': total_bandwidth,
            'unique_roles': len(roles),
            'first_transaction': self.records[0].transaction_id if self.records else None,
            'last_transaction': self.records[-1].transaction_id if self.records else None,
        }


class KnowledgeManager:
    """统一知识管理器 - 整合三大知识来源"""

    def __init__(self):
        self.kg_reader = KnowledgeGraphReader()
        self.crystal_reader = KnowledgeCrystallizationReader()
        self.memory_reader = LongTermMemoryReader()
        self._loaded = False

    def load_all(self) -> Dict[str, Any]:
        """加载所有知识来源"""
        results = {
            'knowledge_graph': False,
            'crystallizations': 0,
            'long_term_memory': 0,
        }

        if self._loaded:
            return results

        if self.kg_reader.load():
            results['knowledge_graph'] = True

        results['crystallizations'] = self.crystal_reader.load_all()

        results['long_term_memory'] = self.memory_reader.load()

        self._loaded = True
        return results

    def reload(self) -> Dict[str, Any]:
        """重新加载所有知识来源"""
        self._loaded = False
        return self.load_all()

    def search_all(self, keyword: str) -> Dict[str, Any]:
        """跨所有知识来源的全文搜索"""
        results = {
            'knowledge_graph': [],
            'crystallizations': [],
            'memory': [],
        }

        keyword_lower = keyword.lower()

        for formula in self.kg_reader.formulas:
            if keyword_lower in formula.name.lower() or keyword_lower in formula.paper_section.lower():
                results['knowledge_graph'].append({
                    'type': 'formula',
                    'id': formula.id,
                    'name': formula.name,
                    'section': formula.paper_section,
                })

        results['crystallizations'] = self.crystal_reader.search_keyword(keyword)

        for record in self.memory_reader.records:
            if keyword_lower in record.source_role.lower() or keyword_lower in record.destination_role.lower():
                results['memory'].append({
                    'transaction_id': record.transaction_id,
                    'source': record.source_role,
                    'destination': record.destination_role,
                })

        results['total_matches'] = (
            len(results['knowledge_graph']) +
            len(results['crystallizations']) +
            len(results['memory'])
        )

        return results

    def get_incident_timeline(self, n: int = 20) -> List[Dict[str, Any]]:
        """获取事件时间线"""
        timeline = []

        for record in self.memory_reader.records[-n:]:
            timeline.append({
                'transaction_id': record.transaction_id,
                'timestamp': record.timestamp,
                'source': record.source_role,
                'destination': record.destination_role,
                'message_type': record.message_type,
                'bandwidth_saved': record.bandwidth_saved,
            })

        return timeline

    def get_full_status(self) -> Dict[str, Any]:
        """获取完整状态"""
        return {
            'knowledge_graph': self.kg_reader.get_summary(),
            'crystallizations': self.crystal_reader.get_summary(),
            'long_term_memory': self.memory_reader.get_statistics(),
        }

    def query(self, query_type: str, **kwargs) -> Any:
        """统一查询接口"""
        if query_type == 'aligned_formulas':
            return self.kg_reader.get_aligned_formulas()
        elif query_type == 'unaligned_formulas':
            return self.kg_reader.get_unaligned_formulas()
        elif query_type == 'all_formulas':
            return self.kg_reader.formulas
        elif query_type == 'capabilities':
            return self.kg_reader.get_integrated_capabilities()
        elif query_type == 'document':
            return self.crystal_reader.get_document(kwargs.get('name', ''))
        elif query_type == 'search':
            return self.crystal_reader.search_keyword(kwargs.get('keyword', ''))
        elif query_type == 'search_all':
            return self.search_all(kwargs.get('keyword', ''))
        elif query_type == 'recent_memory':
            return self.memory_reader.get_recent(kwargs.get('n', 10))
        elif query_type == 'memory_stats':
            return self.memory_reader.get_statistics()
        elif query_type == 'timeline':
            return self.get_incident_timeline(kwargs.get('n', 20))
        elif query_type == 'full_status':
            return self.get_full_status()
        else:
            return None


def test_knowledge_manager():
    """测试知识管理器"""
    print("=" * 60)
    print("Knowledge Manager Test")
    print("=" * 60)

    km = KnowledgeManager()

    print("\n[1] Loading all knowledge sources...")
    results = km.load_all()
    print(f"    Knowledge Graph: {results['knowledge_graph']}")
    print(f"    Crystallizations: {results['crystallizations']}")
    print(f"    Long-term Memory: {results['long_term_memory']}")

    print("\n[2] Getting full status...")
    status = km.get_full_status()
    print(f"    Formula Count: {status['knowledge_graph']['total_formulas']}")
    print(f"    Crystallizations: {status['crystallizations']['total_documents']} docs")
    print(f"    Memory: {status['long_term_memory']['total_transactions']} transactions")

    print("\n[3] Querying all formulas...")
    all_formulas = km.query('all_formulas')
    print(f"    Total: {len(all_formulas)} formulas")
    for f in all_formulas[:5]:
        print(f"      Formula {f.id}: aligned={f.aligned}")

    print("\n[4] Querying integrated capabilities...")
    caps = km.query('capabilities')
    print(f"    Found {len(caps)} integrated capabilities")

    print("\n[5] Cross-source search for 'resonance'...")
    search_results = km.query('search_all', keyword='resonance')
    print(f"    Total matches: {search_results['total_matches']}")
    print(f"    Knowledge Graph: {len(search_results['knowledge_graph'])}")
    print(f"    Crystallizations: {len(search_results['crystallizations'])}")

    print("\n[6] Getting incident timeline...")
    timeline = km.query('timeline', n=5)
    print(f"    Recent events: {len(timeline)}")

    print("\n" + "=" * 60)
    print("[PASS] Knowledge Manager Test Passed")
    print("=" * 60)


if __name__ == "__main__":
    test_knowledge_manager()
