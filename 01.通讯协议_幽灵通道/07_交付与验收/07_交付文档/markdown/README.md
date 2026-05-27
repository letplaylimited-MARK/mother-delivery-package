# Ghost Hub 协议文档

**版本**: 1.0.0 | **状态**: 稳定 | **更新时间**: 2026-04-15

---

## 目录

- [安装指南](./INSTALL.md)
- [快速开始](../../docs/QUICK_START.md)
- [使用指南](../../docs/USER_GUIDE.md)
- [用户场景](../../docs/SCENARIOS.md)
- [API参考](../openapi/ghost-hub-api.yaml)
- [故障排查](../html/troubleshooting.html)
- [术语表](../html/glossary.html)

---

## 项目概述

Ghost Hub 是一个高性能实时消息传输协议，设计用于处理大规模并发消息流。

### 核心能力

| 指标 | 数值 |
|------|------|
| P99 延迟 | < 10ms |
| 吞吐量 | > 10,000 msg/s |
| 缓存命中率 | > 99% |
| 带宽降低 | 99.5% |

### 支持的功能

- **三种频道模式**: 广播、多播、单播
- **消息压缩**: Zstd/Gzip/LZ4
- **游标分页**: 双向遍历
- **保留策略**: 数量限制 + TTL

---

## 快速链接

### 开发者资源

- [Python SDK](../../../03_SDK与集成/04_SDK工程包/ghost-channel-sdk/python/)
- [TypeScript SDK](../../../03_SDK与集成/04_SDK工程包/ghost-channel-sdk/typescript/)
- [JSON Schema](../../../03_SDK与集成/04_SDK工程包/ghost-channel-sdk/schemas/)

### 部署

- [Docker Compose 配置](../../../docker-compose.yml)
- [安装指南](./INSTALL.md)

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-04-15 | 初始稳定版本 |

---

*本文档由 Ghost Hub Protocol Team 维护*
