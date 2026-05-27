"""
Ghost Hub SQLite 持久化层

提供完整的数据持久化能力：
- 意图历史
- 设备状态
- Agent协作记录
- 用户偏好
- 工作流执行记录
"""

import sqlite3
import json
import time
import uuid
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime
from contextlib import contextmanager


@dataclass
class Schema:
    """数据库Schema定义"""

    CREATE_TABLES = """
    -- 意图历史表
    CREATE TABLE IF NOT EXISTS intent_history (
        id TEXT PRIMARY KEY,
        intent_text TEXT NOT NULL,
        template_id TEXT,
        template_name TEXT,
        similarity REAL,
        confidence REAL,
        workflow_id TEXT,
        status TEXT,
        execution_time REAL,
        tasks_count INTEGER,
        errors TEXT,
        created_at REAL DEFAULT (strftime('%s', 'now'))
    );
    
    -- 设备状态表
    CREATE TABLE IF NOT EXISTS device_state (
        id TEXT PRIMARY KEY,
        device_id TEXT NOT NULL,
        device_name TEXT,
        device_type TEXT,
        command TEXT,
        params TEXT,
        success INTEGER,
        new_state TEXT,
        error TEXT,
        created_at REAL DEFAULT (strftime('%s', 'now'))
    );
    
    -- Agent活动表
    CREATE TABLE IF NOT EXISTS agent_activity (
        id TEXT PRIMARY KEY,
        agent_id TEXT NOT NULL,
        agent_name TEXT,
        action TEXT,
        intent TEXT,
        success INTEGER,
        result_summary TEXT,
        execution_time REAL,
        created_at REAL DEFAULT (strftime('%s', 'now'))
    );
    
    -- 工作流执行表
    CREATE TABLE IF NOT EXISTS workflow_execution (
        id TEXT PRIMARY KEY,
        workflow_id TEXT NOT NULL,
        intent_text TEXT,
        template_id TEXT,
        template_name TEXT,
        status TEXT,
        steps_count INTEGER,
        completed_steps INTEGER,
        failed_steps INTEGER,
        execution_time REAL,
        results TEXT,
        errors TEXT,
        created_at REAL DEFAULT (strftime('%s', 'now'))
    );
    
    -- 用户偏好表
    CREATE TABLE IF NOT EXISTS user_preferences (
        key TEXT PRIMARY KEY,
        value TEXT,
        updated_at REAL DEFAULT (strftime('%s', 'now'))
    );
    
    -- 知识模板表
    CREATE TABLE IF NOT EXISTS knowledge_templates (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        domain TEXT,
        description TEXT,
        keywords TEXT,
        intent_patterns TEXT,
        task_count INTEGER,
        usage_count INTEGER DEFAULT 0,
        success_rate REAL DEFAULT 1.0,
        created_at REAL DEFAULT (strftime('%s', 'now')),
        updated_at REAL DEFAULT (strftime('%s', 'now'))
    );
    
    -- 域关键词表
    CREATE TABLE IF NOT EXISTS domain_keywords (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        domain TEXT NOT NULL,
        keyword TEXT NOT NULL,
        weight REAL DEFAULT 1.0,
        UNIQUE(domain, keyword)
    );
    
    -- 索引
    CREATE INDEX IF NOT EXISTS idx_intent_template ON intent_history(template_id);
    CREATE INDEX IF NOT EXISTS idx_intent_created ON intent_history(created_at);
    CREATE INDEX IF NOT EXISTS idx_device_created ON device_state(created_at);
    CREATE INDEX IF NOT EXISTS idx_agent_created ON agent_activity(created_at);
    CREATE INDEX IF NOT EXISTS idx_workflow_created ON workflow_execution(created_at);
    CREATE INDEX IF NOT EXISTS idx_domain ON domain_keywords(domain);
    """


class GhostHubDatabase:
    """
    Ghost Hub SQLite数据库

    提供完整的持久化能力
    """

    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            db_path = str(Path.home() / ".ghost_hub" / "ghost_hub.db")

        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        self._conn: Optional[sqlite3.Connection] = None
        self._init_db()

    def _init_db(self):
        """初始化数据库"""
        self._conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
        self._conn.row_factory = sqlite3.Row

        # 启用外键
        self._conn.execute("PRAGMA foreign_keys = ON")

        # 创建表
        self._conn.executescript(Schema.CREATE_TABLES)
        self._conn.commit()

    @contextmanager
    def get_cursor(self):
        """获取数据库游标"""
        cursor = self._conn.cursor()
        try:
            yield cursor
            self._conn.commit()
        except Exception as e:
            self._conn.rollback()
            raise e
        finally:
            cursor.close()

    def close(self):
        """关闭数据库"""
        if self._conn:
            self._conn.close()

    # === 意图历史 ===

    def record_intent(
        self,
        intent_text: str,
        template_id: Optional[str],
        template_name: Optional[str],
        similarity: float,
        confidence: float,
        workflow_id: str,
        status: str,
        execution_time: float,
        tasks_count: int,
        errors: List[str],
    ) -> str:
        """记录意图执行"""
        record_id = f"ir_{uuid.uuid4().hex[:8]}"

        with self.get_cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO intent_history 
                (id, intent_text, template_id, template_name, similarity, 
                 confidence, workflow_id, status, execution_time, tasks_count, errors)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    record_id,
                    intent_text,
                    template_id,
                    template_name,
                    similarity,
                    confidence,
                    workflow_id,
                    status,
                    execution_time,
                    tasks_count,
                    json.dumps(errors, ensure_ascii=False),
                ),
            )

        return record_id

    def get_intent_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """获取意图历史"""
        with self.get_cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM intent_history
                ORDER BY created_at DESC
                LIMIT ?
            """,
                (limit,),
            )

            return [dict(row) for row in cursor.fetchall()]

    def get_intent_stats(self) -> Dict[str, Any]:
        """获取意图统计"""
        with self.get_cursor() as cursor:
            cursor.execute("""
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed,
                    SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) as failed,
                    AVG(execution_time) as avg_time
                FROM intent_history
            """)

            row = cursor.fetchone()
            return {
                "total": row["total"] or 0,
                "completed": row["completed"] or 0,
                "failed": row["failed"] or 0,
                "avg_execution_time": row["avg_time"] or 0,
            }

    # === 设备状态 ===

    def record_device_command(
        self,
        device_id: str,
        device_name: str,
        device_type: str,
        command: str,
        params: Dict,
        success: bool,
        new_state: Dict,
        error: Optional[str],
    ) -> str:
        """记录设备命令"""
        record_id = f"dr_{uuid.uuid4().hex[:8]}"

        with self.get_cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO device_state
                (id, device_id, device_name, device_type, command, params,
                 success, new_state, error)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    record_id,
                    device_id,
                    device_name,
                    device_type,
                    command,
                    json.dumps(params),
                    1 if success else 0,
                    json.dumps(new_state),
                    error,
                ),
            )

        return record_id

    def get_device_history(
        self, device_id: Optional[str] = None, limit: int = 100
    ) -> List[Dict[str, Any]]:
        """获取设备历史"""
        with self.get_cursor() as cursor:
            if device_id:
                cursor.execute(
                    """
                    SELECT * FROM device_state
                    WHERE device_id = ?
                    ORDER BY created_at DESC
                    LIMIT ?
                """,
                    (device_id, limit),
                )
            else:
                cursor.execute(
                    """
                    SELECT * FROM device_state
                    ORDER BY created_at DESC
                    LIMIT ?
                """,
                    (limit,),
                )

            return [dict(row) for row in cursor.fetchall()]

    # === Agent活动 ===

    def record_agent_activity(
        self,
        agent_id: str,
        agent_name: str,
        action: str,
        intent: str,
        success: bool,
        result_summary: str,
        execution_time: float,
    ) -> str:
        """记录Agent活动"""
        record_id = f"ar_{uuid.uuid4().hex[:8]}"

        with self.get_cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO agent_activity
                (id, agent_id, agent_name, action, intent, success,
                 result_summary, execution_time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    record_id,
                    agent_id,
                    agent_name,
                    action,
                    intent,
                    1 if success else 0,
                    result_summary,
                    execution_time,
                ),
            )

        return record_id

    def get_agent_stats(self) -> Dict[str, Any]:
        """获取Agent统计"""
        with self.get_cursor() as cursor:
            cursor.execute("""
                SELECT 
                    agent_id,
                    agent_name,
                    COUNT(*) as total,
                    SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as success
                FROM agent_activity
                GROUP BY agent_id
            """)

            return [dict(row) for row in cursor.fetchall()]

    # === 工作流执行 ===

    def record_workflow(
        self,
        workflow_id: str,
        intent_text: str,
        template_id: Optional[str],
        template_name: Optional[str],
        status: str,
        steps_count: int,
        completed_steps: int,
        failed_steps: int,
        execution_time: float,
        results: Dict,
        errors: List[str],
    ) -> str:
        """记录工作流执行"""
        record_id = f"wf_{uuid.uuid4().hex[:8]}"

        with self.get_cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO workflow_execution
                (id, workflow_id, intent_text, template_id, template_name,
                 status, steps_count, completed_steps, failed_steps,
                 execution_time, results, errors)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    record_id,
                    workflow_id,
                    intent_text,
                    template_id,
                    template_name,
                    status,
                    steps_count,
                    completed_steps,
                    failed_steps,
                    execution_time,
                    json.dumps(results),
                    json.dumps(errors),
                ),
            )

        return record_id

    def get_workflow_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """获取工作流历史"""
        with self.get_cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM workflow_execution
                ORDER BY created_at DESC
                LIMIT ?
            """,
                (limit,),
            )

            return [dict(row) for row in cursor.fetchall()]

    # === 用户偏好 ===

    def set_preference(self, key: str, value: Any) -> bool:
        """设置用户偏好"""
        with self.get_cursor() as cursor:
            cursor.execute(
                """
                INSERT OR REPLACE INTO user_preferences (key, value, updated_at)
                VALUES (?, ?, strftime('%s', 'now'))
            """,
                (key, json.dumps(value)),
            )

        return True

    def get_preference(self, key: str, default: Any = None) -> Any:
        """获取用户偏好"""
        with self.get_cursor() as cursor:
            cursor.execute(
                """
                SELECT value FROM user_preferences WHERE key = ?
            """,
                (key,),
            )

            row = cursor.fetchone()
            if row:
                return json.loads(row["value"])
            return default

    # === 知识模板 ===

    def save_template(
        self,
        template_id: str,
        name: str,
        domain: str,
        description: str,
        keywords: List[str],
        intent_patterns: List[str],
        task_count: int,
    ) -> bool:
        """保存模板"""
        with self.get_cursor() as cursor:
            cursor.execute(
                """
                INSERT OR REPLACE INTO knowledge_templates
                (id, name, domain, description, keywords, intent_patterns,
                 task_count, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, strftime('%s', 'now'))
            """,
                (
                    template_id,
                    name,
                    domain,
                    description,
                    json.dumps(keywords),
                    json.dumps(intent_patterns),
                    task_count,
                ),
            )

        return True

    def update_template_stats(self, template_id: str, success: bool) -> bool:
        """更新模板统计"""
        with self.get_cursor() as cursor:
            cursor.execute(
                """
                UPDATE knowledge_templates
                SET usage_count = usage_count + 1,
                    success_rate = (success_rate * usage_count + ?) / (usage_count + 1),
                    updated_at = strftime('%s', 'now')
                WHERE id = ?
            """,
                (1 if success else 0, template_id),
            )

        return True

    def get_templates(self, domain: Optional[str] = None) -> List[Dict[str, Any]]:
        """获取模板列表"""
        with self.get_cursor() as cursor:
            if domain:
                cursor.execute(
                    """
                    SELECT * FROM knowledge_templates
                    WHERE domain = ?
                    ORDER BY usage_count DESC
                """,
                    (domain,),
                )
            else:
                cursor.execute("""
                    SELECT * FROM knowledge_templates
                    ORDER BY usage_count DESC
                """)

            return [dict(row) for row in cursor.fetchall()]

    # === 域关键词 ===

    def add_domain_keyword(self, domain: str, keyword: str, weight: float = 1.0) -> bool:
        """添加域关键词"""
        with self.get_cursor() as cursor:
            cursor.execute(
                """
                INSERT OR IGNORE INTO domain_keywords (domain, keyword, weight)
                VALUES (?, ?, ?)
            """,
                (domain, keyword, weight),
            )

        return True

    def get_domain_keywords(self, domain: str) -> List[str]:
        """获取域关键词"""
        with self.get_cursor() as cursor:
            cursor.execute(
                """
                SELECT keyword FROM domain_keywords
                WHERE domain = ?
            """,
                (domain,),
            )

            return [row["keyword"] for row in cursor.fetchall()]

    # === 统计和报告 ===

    def get_full_stats(self) -> Dict[str, Any]:
        """获取完整统计"""
        return {
            "intents": self.get_intent_stats(),
            "devices": {
                "total_commands": self.get_cursor()
                .execute("SELECT COUNT(*) FROM device_state")
                .fetchone()[0]
                or 0
            },
            "agents": self.get_agent_stats(),
            "workflows": {
                "total": self.get_cursor()
                .execute("SELECT COUNT(*) FROM workflow_execution")
                .fetchone()[0]
                or 0
            },
            "templates": {
                "total": self.get_cursor()
                .execute("SELECT COUNT(*) FROM knowledge_templates")
                .fetchone()[0]
                or 0
            },
        }

    def export_data(self) -> Dict[str, Any]:
        """导出所有数据"""
        return {
            "intents": self.get_intent_history(1000),
            "devices": self.get_device_history(None, 1000),
            "agents": self.get_agent_stats(),
            "workflows": self.get_workflow_history(1000),
            "templates": self.get_templates(),
            "exported_at": datetime.now().isoformat(),
        }


# 全局单例
_global_db: Optional[GhostHubDatabase] = None


def get_database() -> GhostHubDatabase:
    """获取全局数据库实例"""
    global _global_db
    if _global_db is None:
        _global_db = GhostHubDatabase()
    return _global_db


if __name__ == "__main__":
    print("=" * 60)
    print("Ghost Hub SQLite 持久化测试")
    print("=" * 60)

    db = GhostHubDatabase()

    # 测试记录意图
    print("\n[记录意图]")
    db.record_intent(
        intent_text="打开客厅灯",
        template_id="tpl_iot_smart_home",
        template_name="智能家居控制",
        similarity=0.85,
        confidence=0.9,
        workflow_id="wf_001",
        status="completed",
        execution_time=0.5,
        tasks_count=4,
        errors=[],
    )
    print("  Intent recorded: OK")

    # 测试记录设备命令
    print("\n[记录设备命令]")
    db.record_device_command(
        device_id="dev_001",
        device_name="客厅灯",
        device_type="light",
        command="turn_on",
        params={"brightness": 80},
        success=True,
        new_state={"status": "on", "brightness": 80},
        error=None,
    )
    print("  Device command recorded: OK")

    # 测试记录Agent活动
    print("\n[记录Agent活动]")
    db.record_agent_activity(
        agent_id="data_agent",
        agent_name="数据分析Agent",
        action="analyze",
        intent="分析销售数据",
        success=True,
        result_summary="分析完成，找到3个关键指标",
        execution_time=2.5,
    )
    print("  Agent activity recorded: OK")

    # 测试保存模板
    print("\n[保存模板]")
    db.save_template(
        template_id="tpl_test",
        name="测试模板",
        domain="test",
        description="用于测试的模板",
        keywords=["测试", "示例"],
        intent_patterns=["测试"],
        task_count=3,
    )
    print("  Template saved: OK")

    # 测试获取统计
    print("\n[获取统计]")
    stats = db.get_full_stats()
    print(f"  Intents: {stats['intents']['total']}")
    print(f"  Templates: {stats['templates']['total']}")
    print(
        f"  Success rate: {stats['intents']['completed'] / max(stats['intents']['total'], 1) * 100:.1f}%"
    )

    # 测试域关键词
    print("\n[域关键词]")
    db.add_domain_keyword("iot", "灯")
    db.add_domain_keyword("iot", "空调")
    keywords = db.get_domain_keywords("iot")
    print(f"  IoT keywords: {keywords}")

    # 导出数据
    print("\n[导出数据]")
    data = db.export_data()
    print(f"  Exported {len(data['intents'])} intents")
    print(f"  Exported {len(data['devices'])} device records")

    db.close()
    print("\n  Database closed: OK")

    print("\n" + "=" * 60)
    print("  All tests passed!")
    print("=" * 60)
