"""
Ghost Hub 持久化存储

支持多种存储后端：
- SQLite: 轻量级本地存储
- JSON: 文件系统存储
- 可扩展: 支持更多后端
"""

import json
import sqlite3
import threading
import time
from pathlib import Path
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, asdict
from abc import ABC, abstractmethod
from datetime import datetime
from contextlib import contextmanager
import logging

logger = logging.getLogger(__name__)


class StorageBackend(ABC):
    """存储后端抽象基类"""

    @abstractmethod
    def save(self, key: str, data: Dict[str, Any]) -> bool:
        pass

    @abstractmethod
    def load(self, key: str) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def delete(self, key: str) -> bool:
        pass

    @abstractmethod
    def list_keys(self, pattern: str = "*") -> List[str]:
        pass

    @abstractmethod
    def exists(self, key: str) -> bool:
        pass

    @abstractmethod
    def get_stats(self) -> Dict[str, Any]:
        pass


class JSONStorage(StorageBackend):
    """
    JSON文件存储

    每个记录存储为一个JSON文件

    优点: 简单、易于调试、跨平台
    缺点: 性能一般、不支持并发写入
    """

    def __init__(self, storage_path: str):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    def _get_file_path(self, key: str) -> Path:
        # 安全的文件名
        safe_key = key.replace("/", "_").replace("\\", "_")
        return self.storage_path / f"{safe_key}.json"

    def save(self, key: str, data: Dict[str, Any]) -> bool:
        try:
            with self._lock:
                file_path = self._get_file_path(key)

                # 添加元数据
                record = {
                    "key": key,
                    "data": data,
                    "created_at": getattr(data, "_created_at", None) or datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat(),
                }

                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(record, f, ensure_ascii=False, indent=2)

                return True
        except Exception as e:
            logger.error(f"JSON存储保存失败 [{key}]: {e}")
            return False

    def load(self, key: str) -> Optional[Dict[str, Any]]:
        try:
            file_path = self._get_file_path(key)
            if not file_path.exists():
                return None

            with open(file_path, "r", encoding="utf-8") as f:
                record = json.load(f)

            return record.get("data")
        except Exception as e:
            logger.error(f"JSON存储加载失败 [{key}]: {e}")
            return None

    def delete(self, key: str) -> bool:
        try:
            file_path = self._get_file_path(key)
            if file_path.exists():
                file_path.unlink()
                return True
            return False
        except Exception as e:
            logger.error(f"JSON存储删除失败 [{key}]: {e}")
            return False

    def list_keys(self, pattern: str = "*") -> List[str]:
        try:
            # 简单的通配符支持
            keys = []
            for file_path in self.storage_path.glob("*.json"):
                key = file_path.stem
                if pattern == "*" or pattern.replace("*", "") in key:
                    keys.append(key)
            return keys
        except Exception as e:
            logger.error(f"JSON存储列表失败: {e}")
            return []

    def exists(self, key: str) -> bool:
        return self._get_file_path(key).exists()

    def get_stats(self) -> Dict[str, Any]:
        try:
            files = list(self.storage_path.glob("*.json"))
            total_size = sum(f.stat().st_size for f in files)

            return {
                "backend": "json",
                "path": str(self.storage_path),
                "record_count": len(files),
                "total_size_bytes": total_size,
                "total_size_kb": round(total_size / 1024, 2),
            }
        except Exception as e:
            logger.error(f"JSON存储统计失败: {e}")
            return {}


class SQLiteStorage(StorageBackend):
    """
    SQLite数据库存储

    优点: 高性能、支持并发、支持SQL查询
    缺点: 跨平台兼容性稍差
    """

    def __init__(self, db_path: str, table_name: str = "ghost_hub_data"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.table_name = table_name
        self._local = threading.local()
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        if not hasattr(self._local, "connection"):
            self._local.connection = sqlite3.connect(str(self.db_path), check_same_thread=False)
            self._local.connection.row_factory = sqlite3.Row
        return self._local.connection

    @contextmanager
    def _transaction(self):
        conn = self._get_connection()
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise

    def _init_db(self):
        """初始化数据库表"""
        import re

        if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", self.table_name):
            raise ValueError(f"Invalid table name: {self.table_name}")

        with self._transaction() as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS `{self.table_name}` (
                    key TEXT PRIMARY KEY,
                    data TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)
            cursor.execute(f"""
                CREATE INDEX IF NOT EXISTS idx_updated_at 
                ON `{self.table_name}`(updated_at)
            """)

    def save(self, key: str, data: Dict[str, Any]) -> bool:
        try:
            with self._transaction() as conn:
                cursor = conn.cursor()

                # 检查是否存在
                cursor.execute(f"SELECT created_at FROM {self.table_name} WHERE key = ?", (key,))
                row = cursor.fetchone()

                now = datetime.now().isoformat()
                data_json = json.dumps(data, ensure_ascii=False)

                if row:
                    # 更新
                    cursor.execute(
                        f"UPDATE {self.table_name} SET data = ?, updated_at = ? WHERE key = ?",
                        (data_json, now, key),
                    )
                else:
                    # 插入
                    cursor.execute(
                        f"INSERT INTO {self.table_name} (key, data, created_at, updated_at) VALUES (?, ?, ?, ?)",
                        (key, data_json, now, now),
                    )

                return True
        except Exception as e:
            logger.error(f"SQLite存储保存失败 [{key}]: {e}")
            return False

    def load(self, key: str) -> Optional[Dict[str, Any]]:
        try:
            cursor = self._get_connection().cursor()
            cursor.execute(f"SELECT data FROM {self.table_name} WHERE key = ?", (key,))
            row = cursor.fetchone()

            if row:
                return json.loads(row["data"])
            return None
        except Exception as e:
            logger.error(f"SQLite存储加载失败 [{key}]: {e}")
            return None

    def delete(self, key: str) -> bool:
        try:
            with self._transaction() as conn:
                cursor = conn.cursor()
                cursor.execute(f"DELETE FROM {self.table_name} WHERE key = ?", (key,))
                return cursor.rowcount > 0
        except Exception as e:
            logger.error(f"SQLite存储删除失败 [{key}]: {e}")
            return False

    def list_keys(self, pattern: str = "*") -> List[str]:
        try:
            cursor = self._get_connection().cursor()

            if pattern == "*":
                cursor.execute(f"SELECT key FROM {self.table_name}")
            else:
                # SQL LIKE查询
                like_pattern = pattern.replace("*", "%")
                cursor.execute(
                    f"SELECT key FROM {self.table_name} WHERE key LIKE ?", (like_pattern,)
                )

            return [row["key"] for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"SQLite存储列表失败: {e}")
            return []

    def exists(self, key: str) -> bool:
        try:
            cursor = self._get_connection().cursor()
            cursor.execute(f"SELECT 1 FROM {self.table_name} WHERE key = ?", (key,))
            return cursor.fetchone() is not None
        except Exception as e:
            return False

    def query(self, sql: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """执行SQL查询"""
        try:
            cursor = self._get_connection().cursor()
            cursor.execute(sql, params)

            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"SQLite查询失败: {e}")
            return []

    def get_stats(self) -> Dict[str, Any]:
        try:
            cursor = self._get_connection().cursor()

            cursor.execute(f"SELECT COUNT(*) as count FROM {self.table_name}")
            count = cursor.fetchone()["count"]

            cursor.execute(f"SELECT SUM(LENGTH(data)) as size FROM {self.table_name}")
            size = cursor.fetchone()["size"] or 0

            cursor.execute(f"SELECT MAX(updated_at) as last_update FROM {self.table_name}")
            last_update = cursor.fetchone()["last_update"]

            return {
                "backend": "sqlite",
                "db_path": str(self.db_path),
                "table": self.table_name,
                "record_count": count,
                "total_size_bytes": size,
                "total_size_kb": round(size / 1024, 2),
                "last_update": last_update,
            }
        except Exception as e:
            logger.error(f"SQLite存储统计失败: {e}")
            return {}


class DataStore:
    """
    Ghost Hub 数据存储

    统一的数据存储接口，支持多种后端

    使用示例:
        store = DataStore(backend="sqlite")
        store.save("intent_001", {"text": "打开灯", "result": "success"})
        data = store.load("intent_001")
    """

    def __init__(self, backend: str = "json", **kwargs):
        """
        初始化数据存储

        Args:
            backend: 存储后端 ("json" 或 "sqlite")
            **kwargs: 后端特定配置
        """
        self.backend_name = backend
        self._lock = threading.Lock()

        if backend == "sqlite":
            db_path = kwargs.get("db_path", "~/.ghost_hub/store.db")
            table_name = kwargs.get("table_name", "ghost_hub_data")
            self.backend = SQLiteStorage(str(Path(db_path).expanduser()), table_name)
        else:
            storage_path = kwargs.get("storage_path", "~/.ghost_hub/data")
            self.backend = JSONStorage(str(Path(storage_path).expanduser()))

        # 版本控制 - 受锁保护
        self._versions: Dict[str, List[Dict[str, Any]]] = {}
        self._max_versions = kwargs.get("max_versions", 10)

    def save(self, key: str, data: Dict[str, Any], versioned: bool = True) -> bool:
        """
        保存数据

        Args:
            key: 数据键
            data: 数据内容
            versioned: 是否保存版本历史

        Returns:
            是否保存成功
        """
        with self._lock:
            # 保存版本
            if versioned and self.backend.exists(key):
                old_data = self.backend.load(key)
                if old_data:
                    if key not in self._versions:
                        self._versions[key] = []
                    self._versions[key].append(
                        {"data": old_data, "timestamp": datetime.now().isoformat()}
                    )
                    if len(self._versions[key]) > self._max_versions:
                        self._versions[key] = self._versions[key][-self._max_versions :]

            return self.backend.save(key, data)

    def load(self, key: str) -> Optional[Dict[str, Any]]:
        """加载数据"""
        return self.backend.load(key)

    def delete(self, key: str) -> bool:
        """删除数据"""
        with self._lock:
            if key in self._versions:
                del self._versions[key]
            return self.backend.delete(key)

    def list_keys(self, pattern: str = "*") -> List[str]:
        """列出所有键"""
        return self.backend.list_keys(pattern)

    def exists(self, key: str) -> bool:
        """检查键是否存在"""
        return self.backend.exists(key)

    def get_versions(self, key: str) -> List[Dict[str, Any]]:
        """获取版本历史"""
        with self._lock:
            return self._versions.get(key, []).copy()

    def restore_version(self, key: str, version_index: int = -1) -> bool:
        """恢复历史版本"""
        with self._lock:
            versions = self._versions.get(key, [])
            if not versions or abs(version_index) >= len(versions):
                return False

            old_data = versions[version_index]["data"]
            return self.backend.save(key, old_data)

    def get_stats(self) -> Dict[str, Any]:
        """获取存储统计"""
        with self._lock:
            stats = self.backend.get_stats()
            stats["versions_tracked"] = len(self._versions)
            return stats

    def save_batch(self, items: Dict[str, Dict[str, Any]]) -> int:
        """批量保存"""
        count = 0
        for key, data in items.items():
            if self.save(key, data):
                count += 1
        return count

    def load_batch(self, keys: List[str]) -> Dict[str, Optional[Dict[str, Any]]]:
        """批量加载"""
        return {key: self.load(key) for key in keys}

    def clear(self) -> int:
        """清空所有数据"""
        keys = self.list_keys()
        count = 0
        for key in keys:
            if self.delete(key):
                count += 1
        self._versions.clear()
        return count


# === 全局数据存储实例 ===

_global_store: Optional[DataStore] = None


def get_datastore(backend: str = None) -> DataStore:
    """获取全局数据存储实例"""
    global _global_store

    if _global_store is None:
        if backend is None:
            # 优先使用SQLite
            backend = "sqlite"

        storage_dir = Path.home() / ".ghost_hub"
        storage_dir.mkdir(parents=True, exist_ok=True)

        _global_store = DataStore(
            backend=backend,
            storage_path=str(storage_dir / "data"),
            db_path=str(storage_dir / "store.db"),
        )

    return _global_store


# === 快捷函数 ===


def save_intent_record(record: Dict[str, Any]) -> bool:
    """保存意图记录"""
    record_id = record.get("id", f"intent_{time.time()}")
    store = get_datastore()
    return store.save(f"intent:{record_id}", record)


def load_intent_records(limit: int = 100) -> List[Dict[str, Any]]:
    """加载意图记录"""
    store = get_datastore()
    keys = store.list_keys("intent:*")
    keys = keys[-limit:]

    records = []
    for key in keys:
        data = store.load(key)
        if data:
            records.append(data)

    return records


def save_device_state(device_id: str, state: Dict[str, Any]) -> bool:
    """保存设备状态"""
    store = get_datastore()
    return store.save(f"device:{device_id}", state)


def load_device_states() -> Dict[str, Dict[str, Any]]:
    """加载所有设备状态"""
    store = get_datastore()
    keys = store.list_keys("device:*")

    states = {}
    for key in keys:
        device_id = key.replace("device:", "")
        state = store.load(key)
        if state:
            states[device_id] = state

    return states
