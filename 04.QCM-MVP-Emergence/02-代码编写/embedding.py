"""
AI Embedding Module
Uses sentence-transformers for real semantic embeddings
With fallback to random embeddings if library not available
"""

import math
import random
from typing import Optional, List

# Try to import sentence-transformers
try:
    from sentence_transformers import SentenceTransformer
    ST_AVAILABLE = True
except ImportError:
    ST_AVAILABLE = False
    print("[INFO] sentence-transformers not installed, using random embeddings")


class Embedder:
    """Embedding生成器 - 支持真实语义嵌入或模拟嵌入"""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2", device: str = "cpu"):
        """
        初始化嵌入器
        
        Args:
            model_name: sentence-transformers模型名称
            device: 设备 ('cpu' 或 'cuda')
        """
        self.model_name = model_name
        self.device = device
        self.model: Optional[SentenceTransformer] = None
        self.dimension = 384  # default for MiniLM-L6-v2
        
        if ST_AVAILABLE:
            try:
                self.model = SentenceTransformer(model_name, device=device)
                self.dimension = self.model.get_sentence_embedding_dimension()
                print(f"[OK] Loaded model: {model_name}, dimension: {self.dimension}")
            except Exception as e:
                print(f"[WARN] Failed to load model: {e}")
                self.model = None
    
    def encode(self, text: str) -> List[float]:
        """
        将文本编码为向量
        
        Args:
            text: 输入文本
            
        Returns:
            归一化后的向量
        """
        if self.model is not None:
            # 使用真实模型
            embedding = self.model.encode(text, convert_to_numpy=True)
            return self._normalize(embedding.tolist())
        else:
            # 回退到随机嵌入
            return self._random_embedding()
    
    def encode_batch(self, texts: List[str]) -> List[List[float]]:
        """
        批量编码文本
        
        Args:
            texts: 文本列表
            
        Returns:
            向量列表
        """
        if self.model is not None:
            embeddings = self.model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
            return [self._normalize(e.tolist()) for e in embeddings]
        else:
            return [self._random_embedding() for _ in texts]
    
    def _normalize(self, vector: List[float]) -> List[float]:
        """L2归一化"""
        norm = math.sqrt(sum(x ** 2 for x in vector))
        if norm > 0:
            return [x / norm for x in vector]
        return vector
    
    def _random_embedding(self) -> List[float]:
        """生成随机归一化向量"""
        vector = [random.uniform(-1, 1) for _ in range(self.dimension)]
        return self._normalize(vector)
    
    def compute_similarity(self, text1: str, text2: str) -> float:
        """计算两个文本的余弦相似度"""
        v1 = self.encode(text1)
        v2 = self.encode(text2)
        
        dot_product = sum(a * b for a, b in zip(v1, v2))
        return dot_product  # 已归一化
    
    def get_dimension(self) -> int:
        """获取向量维度"""
        return self.dimension


class EmbeddingCache:
    """Embedding缓存 - 避免重复计算"""
    
    def __init__(self, embedder: Embedder):
        self.embedder = embedder
        self.cache: dict[str, List[float]] = {}
    
    def get_or_compute(self, text: str) -> List[float]:
        """获取缓存或计算新的embedding"""
        if text not in self.cache:
            self.cache[text] = self.embedder.encode(text)
        return self.cache[text]
    
    def clear(self):
        """清空缓存"""
        self.cache.clear()
    
    def size(self) -> int:
        """缓存大小"""
        return len(self.cache)


def test_embedder():
    """测试嵌入器功能"""
    embedder = Embedder()
    
    print(f"Dimension: {embedder.get_dimension()}")
    
    # Test single encoding
    text = "This is a test sentence"
    vector = embedder.encode(text)
    assert len(vector) == embedder.get_dimension()
    print(f"[OK] Single encoding: {len(vector)}D")
    
    # Test batch encoding
    texts = ["Hello world", "Another sentence", "Third text"]
    vectors = embedder.encode_batch(texts)
    assert len(vectors) == 3
    print(f"[OK] Batch encoding: {len(vectors)} vectors")
    
    # Test similarity (only if model loaded)
    if ST_AVAILABLE:
        sim = embedder.compute_similarity("Hello world", "Hi there")
        print(f"[OK] Similarity: {sim:.4f}")
    
    # Test cache
    cache = EmbeddingCache(embedder)
    v1 = cache.get_or_compute("test")
    v2 = cache.get_or_compute("test")
    assert v1 == v2
    print(f"[OK] Cache: {cache.size()} entries")
    
    print("[PASS] All embedder tests passed!")


if __name__ == "__main__":
    test_embedder()