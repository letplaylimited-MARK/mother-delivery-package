# QCM-MVP 启动检查清单

**Version**: 2.0
**Last Updated**: 2026-04-26

---

## 每次启动必须执行

### Step 1: 阅读CHANGELOG.md (2分钟)
- [ ] 读取最新版本记录
- [ ] 确认当前版本号
- [ ] 确认上次修改内容

### Step 2: 阅读KNOWLEDGE_GRAPH.md (2分钟)
- [ ] 确认知识图谱版本
- [ ] 确认当前系统状态

### Step 3: 检查知识结晶 (1分钟)
- [ ] 确认最新日期的知识结晶
- [ ] 确认与CHANGELOG对齐

### Step 4: 检查长期记忆 (1分钟)
- [ ] 查询QCM-Reconstruction entity
- [ ] 确认与文档状态一致

### Step 5: 运行验证 (3分钟)
- [ ] python main.py
- [ ] 确认涌现触发结果

---

## 核心追踪文件

| 文件 | 用途 | 更新频率 |
|------|------|----------|
| CHANGELOG.md | 变更追踪 | 每次修改 |
| KNOWLEDGE_GRAPH.md | 系统状态 | 每次修改 |
| 00-知识结晶/*.md | 深度思考 | 重要问题 |
| 长期记忆 | 快速状态 | 每次修改 |

---

## 版本对应

| CHANGELOG | KNOWLEDGE | 状态 |
|-----------|-----------|------|
| v2.0 | v4.0 | 已是最新 |
| v1.5 | v3.0 | 旧版本 |
| v1.0 | v2.0 | 旧版本 |

---

## 快速验证命令

```bash
# 1. 确认版本
cat CHANGELOG.md | Select-String "Version"

# 2. 验证系统
python main.py

# 3. 确认涌现
# 应该看到: Round XX: R = 0.XXXX -> 涌现
```