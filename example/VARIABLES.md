# VARIABLES.md — the living board

Rule: after EVERY wave the dispatcher updates this board AND shows the user
the rendered tables (SOLVED / OPEN / CHANGES-NEW + economics).

## Wave economics (token spend per agent — measure, don't guess)
| agent | tokens | note |
|-------|--------|------|
| w1-s1-greet (specialist) | 21.4k | implement + test; one clean run |
| w1-v1-audit (verifier) | 9.7k | prompt-to-artifact audit + smoke check |

Wave 1 total ≈ 31k (via agent-mesh `tools/token_report.py`).

## SOLVED (do not re-open; supersede only with new evidence)
| Var | Value | Evidence |
|-----|-------|----------|
| greeting format | `Hello, ${name}!` | V-001 (VERIFIED) — src/greet.js · src/greet.test.js |

## OPEN / IN-PROGRESS
| Var | Variable | Status | Owner | Blocked-by |
|-----|----------|--------|-------|------------|
| publish target | publish greet-lib to npm | queued (w2-s1-publish) | dispatcher | user decision: package name + public/private |

## NEW VARIABLES LOG
- 2026-09-08 + wave 1: greeting format (→ SOLVED); publish target (→ OPEN).
