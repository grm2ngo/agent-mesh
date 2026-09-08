# AGENT_VERDICTS.md — verdict register + tier system

Check BEFORE attempting any approach; append at task end. Never delete rows —
supersede in-row with `SUPERSEDED-BY <id>`.

Schema per row: `| ID | Verdict | Claim | Evidence / Source | Notes |`
Verdicts: `CONFIRMED-TRUE` · `REFUTED` · `DO-NOT-RETRY` · `UNVERIFIED-INFER`
ID allocation: agents propose rows with `<V-NEXT>` in a tagged block; the
dispatcher assigns final IDs at triage. Next free ID: V-004.

## TIER SYSTEM — BETA vs VERIFIED
Everything is BETA by default — including CONFIRMED-TRUE rows — unless listed
in the VERIFIED LEDGER below. Promotion bar: agent-mesh PROTOCOL.md §5
(≥2 independent instances · matching results · evidence paths on disk ·
survived adversarial review · rotation-relevant).

### VERIFIED LEDGER
| ID | Why it meets the bar |
|----|----------------------|
| V-001 | Two independent methods, two evidence paths: (1) unit-test run `node --test` green (`src/greet.test.js`); (2) verifier's separate smoke run against `src/greet.js` printed the exact expected string. Results match; verifier (adversarial pass) had a shot — no open findings. |

## GREETING-LIB verdicts
| ID | Verdict | Claim | Evidence / Source | Notes |
|----|---------|-------|-------------------|-------|
| V-001 | CONFIRMED-TRUE | `greet(name)` returns exactly `Hello, ${name}!` | src/greet.js · src/greet.test.js | VERIFIED — see ledger above |
| V-002 | DO-NOT-RETRY | Multi-line `node -e` one-liners as smoke checks under CMD — stdout silently swallowed | AGENT_FRICTION.md [w1-s1-greet] | Script files only (PROTOCOL §10-1) |
| V-003 | CONFIRMED-TRUE | `node --test` covers this project with zero npm dependencies | src/greet.test.js (green run, wave 1) | BETA — one environment only |
