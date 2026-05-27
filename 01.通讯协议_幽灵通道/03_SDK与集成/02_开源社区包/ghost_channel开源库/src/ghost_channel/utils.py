"""
Ghost Channel - Performance Optimizer
幽灵通道 - 性能优化模块

功能:
- 缓存管理 (LRU, TTL)
- 连接池
- 批处理
- 资源池
"""

from __future__ import annotations
import time
import asyncio
from typing import Any, Optional, Callable
from dataclasses import dataclass, field
from collections import OrderedDict, deque
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


@dataclass
class CacheEntry:
    """缓存条目"""

    key: str
    value: Any
    created_at: float = field(default_factory=time.time)
    access_count: int = 0
    last_accessed: float = field(default_factory=time.time)
    ttl: float = 0  # 存活时间, 0=永生


class LRUCache:
    """LRU缓存"""

    def __init__(self, max_size: int = 1000, default_ttl: float = 3600):
        self.max_size = max_size
        self.default_ttl = default_ttl
        self.cache: OrderedDict[str, CacheEntry] = OrderedDict()
        self.hits = 0
        self.misses = 0

    def get(self, key: str, default: Any = None) -> Any:
        """获取缓存"""
        entry = self.cache.get(key)

        if entry is None:
            self.misses += 1
            return default

        # 检查过期
        if entry.ttl > 0 and time.time() - entry.created_at > entry.ttl:
            del self.cache[key]
            self.misses += 1
            return default

        # 更新访问
        entry.access_count += 1
        entry.last_accessed = time.time()
        self.cache.move_to_end(key)

        self.hits += 1
        return entry.value

    def set(self, key: str, value: Any, ttl: float = None):
        """设置缓存"""
        # 驱逐最旧的
        if len(self.cache) >= self.max_size and key not in self.cache:
            self.cache.popitem(last=False)

        self.cache[key] = CacheEntry(
            key=key,
            value=value,
            ttl=ttl or self.default_ttl,
        )

    def delete(self, key: str) -> bool:
        """删除缓存"""
        if key in self.cache:
            del self.cache[key]
            return True
        return False

    def clear(self):
        """清空缓存"""
        self.cache.clear()
        self.hits = 0
        self.misses = 0

    def get_stats(self) -> dict:
        """统计"""
        total = self.hits + self.misses
        hit_rate = self.hits / total if total > 0 else 0
        return {
            "size": len(self.cache),
            "max_size": self.max_size,
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": hit_rate,
        }


class ConnectionPool:
    """连接池"""

    def __init__(
        self,
        factory: Callable,
        max_size: int = 10,
        min_size: int = 2,
        timeout: float = 30.0,
    ):
        self.factory = factory
        self.max_size = max_size
        self.timeout = timeout

        self.pool: deque = deque(maxlen=max_size)
        self.in_use: set = set()
        self.lock = asyncio.Lock()

        # 预热
        for _ in range(min_size):
            conn = factory()
            self.pool.append(conn)

    async def acquire(self) -> Any:
        """获取连接"""
        async with self.lock:
            if self.pool:
                conn = self.pool.popleft()
                self.in_use.add(conn)
                return conn

            # 创建新连接
            if len(self.in_use) < self.max_size:
                conn = self.factory()
                self.in_use.add(conn)
                return conn

        # 等待释放
        raise TimeoutError("Connection pool exhausted")

    async def release(self, conn: Any):
        """释放连接"""
        async with self.lock:
            if conn in self.in_use:
                self.in_use.remove(conn)
                if len(self.pool) < self.max_size:
                    self.pool.append(conn)

    async def close_all(self):
        """关闭所有连接"""
        async with self.lock:
            for conn in list(self.pool) + list(self.in_use):
                if hasattr(conn, "close"):
                    conn.close()
            self.pool.clear()
            self.in_use.clear()


class BatchProcessor:
    """批处理器"""

    def __init__(self, batch_size: int = 32, timeout: float = 1.0):
        self.batch_size = batch_size
        self.timeout = timeout
        self.queue: list = []
        self.lock = asyncio.Lock()
        self.processing = False

    async def add(self, item: Any) -> asyncio.Future:
        """添加项目"""
        future = asyncio.get_running_loop().create_future()

        async with self.lock:
            self.queue.append(item)

            # 达到批次大小，处理
            if len(self.queue) >= self.batch_size:
                asyncio.create_task(self._process_batch())

            # 超时处理
            elif not self.processing:
                asyncio.create_task(self._process_timeout())

        return future

    async def _process_batch(self):
        """处理批次"""
        async with self.lock:
            if self.processing or not self.queue:
                return

            self.processing = True
            batch = self.queue[: self.batch_size]
            self.queue = self.queue[self.batch_size :]

        # 处理
        # ...

        self.processing = False

    async def _process_timeout(self):
        """超时处理"""
        await asyncio.sleep(self.timeout)
        async with self.lock:
            if self.queue and not self.processing:
                self.processing = True
                batch = self.queue
                self.queue = []
                # 处理
                self.processing = False


class ResourcePool:
    """资源池"""

    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.process_executor = ProcessPoolExecutor(max_workers=2)

    def submit(self, fn: Callable, *args, **kwargs):
        """提交任务"""
        return self.executor.submit(fn, *args, **kwargs)

    def map(self, fn: Callable, iterable):
        """批量映射"""
        return self.executor.map(fn, iterable)

    def process(self, fn: Callable, *args, **kwargs):
        """进程池执行"""
        return self.process_executor.submit(fn, *args, **kwargs)

    def shutdown(self, wait: bool = True):
        """关闭"""
        self.executor.shutdown(wait=wait)
        self.process_executor.shutdown(wait=wait)


class RateLimiter:
    """速率限制器"""

    def __init__(self, rate: float, burst: int = 1):
        self.rate = rate  # 每秒令牌数
        self.burst = burst
        self.tokens = burst
        self.last_update = time.time()
        self.lock = asyncio.Lock()

    async def acquire(self, tokens: int = 1) -> bool:
        """获取令牌"""
        async with self.lock:
            now = time.time()
            # 补充令牌
            self.tokens = min(
                self.burst, self.tokens + (now - self.last_update) * self.rate
            )
            self.last_update = now

            if self.tokens >= tokens:
                self.tokens -= tokens
                return True

            return False

    def wait_time(self, tokens: int = 1) -> float:
        """等待时间"""
        if self.tokens >= tokens:
            return 0
        return (tokens - self.tokens) / self.rate


class PerformanceMonitor:
    """性能监控"""

    def __init__(self):
        self.metrics: dict = {}
        self.start_time = time.time()

    def record(self, name: str, value: float):
        """记录指标"""
        if name not in self.metrics:
            self.metrics[name] = []
        self.metrics[name].append(
            {
                "value": value,
                "timestamp": time.time(),
            }
        )

    def get_stats(self, name: str) -> dict:
        """获取统计"""
        values = [m["value"] for m in self.metrics.get(name, [])]

        if not values:
            return {}

        return {
            "count": len(values),
            "sum": sum(values),
            "avg": sum(values) / len(values),
            "min": min(values),
            "max": max(values),
        }

    def get_all_stats(self) -> dict:
        """获取所有统计"""
        return {
            "uptime": time.time() - self.start_time,
            **{name: self.get_stats(name) for name in self.metrics},
        }

    def reset(self):
        """重置"""
        self.metrics.clear()
        self.start_time = time.time()
