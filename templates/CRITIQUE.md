# CRITIQUE.md — critic findings

Schema `C-<NNN>` (append-only; dispatcher adjudicates each finding same-turn
and records FIX/QUEUED/WON'T-FIX with reason):

```
## C-<NNN> — <title>
- Target: <rule/doc/proposal/decision attacked>
- Severity: BLOCKER / HIGH / MEDIUM / LOW
- Claim attacked: <verbatim>
- Evidence: <path / command output>
- Proposed fix: <concrete change>
```
Adversarial by charter — including against the dispatcher's own decisions.
A finding without a path/command is a vibe, not a finding.
