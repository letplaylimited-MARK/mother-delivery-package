# QCM-MVP 第一轮R值稳定性分析

**分析日期**: 2026-04-27
**状态**: 根因已确定

---

## 一、问题分析

### 1.1 观察到的现象

| 运行 | Round 1 R值 |
|------|-------------|
| 第1次 | 0.6798 |
| 第2次 | 0.6414 |
| 第3次 | 0.6916 |
| ... | 随机变化 |

### 1.2 根因分析

**问题**: `simple_role.py` 第37行使用随机embedding

```python
# simple_role.py:34-39
def _generate_embedding(self) -> List[float]:
    dim = 32
    vec = [random.uniform(-1, 1) for _ in range(dim)]  # 随机生成
    norm = math.sqrt(sum(x**2 for x in vec))
    return [x / norm for x in vec]
```

**影响**:
1. 每次运行生成不同的随机向量
2. 两个角色的初始余弦相似度(K_sim)随机变化
3. 导致第一轮R值不固定

---

## 二、解决方案

### 方案A: 固定种子(推荐)

在角色创建前设置随机种子，确保可复现:

```python
# main.py 或 simple_role.py
import random

# 在系统初始化时设置种子
random.seed(42)  # 固定种子

# 之后创建的embedding将保持一致
```

### 方案B: 固定初始embedding

使用固定的初始向量:

```python
# simple_role.py
FIXED_EMBEDDING = [0.5] * 32  # 固定向量

def _generate_embedding(self) -> List[float]:
    # 返回固定向量而非随机
    return FIXED_EMBEDDING.copy()
```

### 方案C: 确定性embedding

基于角色属性生成deterministic embedding:

```python
def _generate_embedding(self) -> List[float]:
    # 基于name和skills生成确定性向量
    seed_str = f"{self.name}:{','.join(self.skills)}"
    # 使用hash生成确定性随机数
    random.seed(hash(seed_str))
    vec = [random.uniform(-1, 1) for _ in range(32)]
    ...
```

---

## 三、推荐修复(方案A)

### 3.1 修改 simple_role.py

```python
# simple_role.py 开头添加
import random

# 可配置种子
DEFAULT_SEED = 42

def _generate_embedding(self) -> List[float]:
    dim = 32
    # 使用确定性种子
    random.seed(DEFAULT_SEED + hash(self.name) % 1000)
    vec = [random.uniform(-1, 1) for _ in range(dim)]
    norm = math.sqrt(sum(x**2 for x in vec))
    return [x / norm for x in vec]
```

### 3.2 修改 main.py

在系统初始化时设置种子:

```python
class QCMSystem:
    def __init__(self, seed: int = 42):
        # 设置随机种子确保可复现
        random.seed(seed)
        
        self.role_a, self.role_b = create_demo_roles()
        ...
```

---

## 四、修复后预期结果

### 4.1 确定性R值

| 运行 | Round 1 R值 |
|------|-------------|
| 固定种子 | 0.68xx (固定) |
| 固定种子 | 0.68xx (相同) |

### 4.2 稳定性验证

```bash
python main.py
# 多次运行，Round 1应保持一致
```

---

## 五、长期记忆更新

### 5.1 需要更新

- KNOWLEDGE_GRAPH.md - 添加随机种子说明
- CHANGELOG.md - 记录v2.1修复
- 长期记忆 - 更新entity

### 5.2 执行

```python
# 步骤1: 修改simple_role.py添加种子
# 步骤2: 修改main.py传入种子
# 步骤3: 运行测试确认Round 1一致
# 步骤4: 更新知识图谱
# 步骤5: 更新CHANGELOG.md
# 步骤6: 更新长期记忆
```

---

*更新日期: 2026-04-27*