# Atomic File Inventory Summary

> Generated at: 2026-06-01T00:21:00
> Inventory: `ATOMIC-FILE-INVENTORY.jsonl`
> Scope: excludes `.git`, `__pycache__`, `.pytest_cache`, `node_modules`, `dist`, `build`, `coverage`.

## Totals

| Metric | Value |
|---|---:|
| Files inventoried | 1155 |
| Bytes inventoried | 20573478 |
| Text lines counted | 236513 |
| QCM skill internal files | 43 |

## By Subsystem

| 项 | 数量 |
|---|---:|
| `P00_SUPER_PROMPT` | 79 |
| `P01_GHOST_CHANNEL` | 296 |
| `P02_UNIVERSAL_KB` | 28 |
| `P03_WORKBUDDY_KB` | 153 |
| `P04_QCM` | 148 |
| `P05_QSPECTRUM` | 423 |
| `QCM_SKILL` | 1 |
| `ROOT` | 13 |
| `USER_PACK` | 14 |

## By Kind

| 项 | 数量 |
|---|---:|
| `archive` | 3 |
| `code` | 347 |
| `config` | 11 |
| `data` | 160 |
| `doc` | 595 |
| `other` | 39 |

## By Priority

| 项 | 数量 |
|---|---:|
| `P0` | 42 |
| `P1` | 569 |
| `P2` | 544 |

## Audit State

Every record starts at `inventoried`. Future deep-read batches must promote files to `triaged`, `read`, `understood`, `linked`, `validated`, `crystallized`, or `delivery_bound` with evidence.

## QCM Skill Package

The root `qcm-universal-ai-system-v3.0.skill` archive contains 43 internal files. These are tracked as a package-level capability first; deep extraction should happen only when a QCM batch needs the internal scripts, references, tests, or templates.
