# AGENT_FRICTION.md — friction log (append-only)

Protocol: every subagent reports EVERY blocker in its `## FRICTION REPORT`;
the dispatcher triages each item SAME-TURN (FIX-now / LESSON / DEFER) and
records the status here. Agents append their raw entries under their own
heading; the dispatcher writes the triage blocks.

Entry format (agents):
```
## [<TASK-ID>] <date time> — <severity: BLOCKER / SLOW / LIGHT>
- Friction: <exact description + failing command verbatim + file involved>
- Workaround used: <if any>
- Suggestion: <what you need fixed>
```
Triage status is written by the dispatcher: `→ FIXED <how>` / `→ LESSON <id>`
/ `→ DEFER <reason>`.
