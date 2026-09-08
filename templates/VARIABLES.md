# VARIABLES.md — the living board

Rule: after EVERY wave the dispatcher updates this board AND shows the user
the rendered tables (SOLVED / OPEN / CHANGES-NEW + economics + mesh health).

## Mesh health (4 metrics, every wave)
| Metric | Value | Target |
|--------|-------|--------|
| Tier-gate (`tools/check_tiers.py`) | <ledger ids · unmapped [VERIFIED] tags> | 0 unmapped |
| Sentinel | <cycles live · unresolved C1/C2> | ≥2 consecutive clean cycles |
| Heartbeats | <staleness of running agents> | < 2× cadence |
| DoD progress | <n/5> | all |

## Wave economics (token spend per agent — measure, don't guess)

## Wave economics (token spend per agent — measure, don't guess)
| agent | tokens | note |
|-------|--------|------|

## SOLVED (do not re-open; supersede only with new evidence)
| Var | Value | Evidence |
|-----|-------|----------|

## OPEN / IN-PROGRESS
| Var | Variable | Status | Owner | Blocked-by |
|-----|----------|--------|-------|------------|

## NEW VARIABLES LOG
- <date + wave>: <newly discovered variables>
