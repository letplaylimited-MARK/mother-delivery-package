# Atomic File Inventory Summary

> Generated at: 2026-06-01T02:39:29
> Inventory: `ATOMIC-FILE-INVENTORY.jsonl`
> Scope: excludes `.git`, `__pycache__`, `.pytest_cache`, `node_modules`, `dist`, `build`, `coverage`.

## Totals

| Metric | Value |
|---|---:|
| Files inventoried | 1174 |
| Bytes inventoried | 23970904 |
| Text lines counted | 237635 |
| QCM skill internal files | 43 |

## By Subsystem

| 项 | 数量 |
|---|---:|
| `P00_SUPER_PROMPT` | 80 |
| `P01_GHOST_CHANNEL` | 296 |
| `P02_UNIVERSAL_KB` | 28 |
| `P03_WORKBUDDY_KB` | 153 |
| `P04_QCM` | 148 |
| `P05_QSPECTRUM` | 423 |
| `QCM_SKILL` | 1 |
| `REFERENCE_PROJECT` | 16 |
| `ROOT` | 15 |
| `USER_PACK` | 14 |

## By Kind

| 项 | 数量 |
|---|---:|
| `archive` | 3 |
| `code` | 353 |
| `config` | 11 |
| `data` | 161 |
| `doc` | 607 |
| `other` | 39 |

## By Priority

| 项 | 数量 |
|---|---:|
| `P0` | 45 |
| `P1` | 576 |
| `P2` | 553 |

## Audit State

Every record starts at `inventoried`. Future deep-read batches must promote files to `triaged`, `read`, `understood`, `linked`, `validated`, `crystallized`, or `delivery_bound` with evidence.

## QCM Skill Package

The root `qcm-universal-ai-system-v3.0.skill` archive contains 43 internal files. These are tracked as a package-level capability first; deep extraction should happen only when a QCM batch needs the internal scripts, references, tests, or templates.
