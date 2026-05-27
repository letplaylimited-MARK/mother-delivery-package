# 幽灵通道 Ghost Channel v1.0

**Q-SpecTrum 超极智脑对外通讯协议层**

Ghost Channel 是 Q-SpecTrum 智脑的标准通讯协议，提供安全、去中心化、多代理（multi-agent）的沟通基础设施。

## Key Facts
- **3 SDKs**: ghost_channel (protocol) → ghost_channel_sdk (lightweight) → ghost_hub_sdk (enterprise)
- **162/162 tests passing** | **299 files** SHA256 verified | MIT License v1.0.0
- See `00_总览/PROJECT_HANDOFF.md` for full handoff documentation

## What's Included

- **Protocol**: Decentralized multi-agent communication, causal broadcast, vector clock, Merkle Tree integrity
- **SDKs**: Python (enterprise / open-source / lightweight) + TypeScript
- **Deployment**: Docker, K8s, license system, monitoring
- **Templates**: Industry scenario templates (in GhostHub_SDK/templates/)

## Quick Start

```bash
# Enterprise SDK
cd 03_SDK与集成/03_企业SDK包/GhostHub_SDK
pip install -e .[all]
python demos/demo_all.py
```

详细指引 → 见 `INDEX.md`
