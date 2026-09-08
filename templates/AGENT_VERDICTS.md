# AGENT_VERDICTS.md — verdict register + tier system

Check BEFORE attempting any approach; append at task end. Never delete rows —
supersede in-row with `SUPERSEDED-BY <id>`.

Schema per row: `| ID | Verdict | Claim | Evidence / Source | Notes |`
Verdicts: `CONFIRMED-TRUE` · `REFUTED` · `DO-NOT-RETRY` · `UNVERIFIED-INFER`

ID allocation (single-writer): agents PROPOSE rows with `<V-NEXT>` markers
inside a tagged block (`### V-<TASK>-BLOCK`); the DISPATCHER assigns final
IDs at triage. Next free ID: V-001.

## TIER SYSTEM — BETA vs VERIFIED
Everything is BETA by default — including CONFIRMED-TRUE rows — unless listed
in the VERIFIED LEDGER below. Promotion bar, demotion process, grandfather
and scope clauses: agent-mesh PROTOCOL.md §5 (copy the five criteria here if
you want the register self-contained).

### VERIFIED LEDGER
| ID | Why it meets the bar |
|----|----------------------|

## <DOMAIN> verdicts
| ID | Verdict | Claim | Evidence / Source | Notes |
|----|---------|-------|-------------------|-------|
