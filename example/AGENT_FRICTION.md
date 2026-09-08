# AGENT_FRICTION.md — friction log (append-only)

Agents append raw entries under their own heading; the dispatcher writes the
triage lines (`→ FIXED <how>` / `→ LESSON <id>` / `→ DEFER <reason>`) same-turn.

## [w1-s1-greet] 2026-09-08 14:12 — BLOCKER
- Friction: smoke-checking greet() inline with multi-line
  `node -e "const {greet}=require('./src/greet.js'); console.log(greet('A'))"`
  under CMD printed NOTHING and exited 0 — stdout silently swallowed.
- Workaround used: wrote the check to `tmp/smoke.js` and ran it as a file
  (`node tmp\smoke.js`) — output appeared on first try.
- Suggestion: ban multi-line `node -e` / `python -c` for checks; script files only.

→ LESSON: textbook PROTOCOL §10 trap 1 — dispatcher re-briefed the agent;
  no new rule needed, field count for this trap updated to 3.

## [w1-v1-audit] 2026-09-08 15:03 — SLOW
- Friction: two edit attempts on src/greet.js failed with anchor-not-found —
  I anchored on the file as read at 14:40, but w1-s1-greet had landed its
  input-validation edit in between (my copy of the file was stale).
- Workaround used: re-read the CURRENT file, re-anchored on a line that
  exists now; edit landed first try.
- Suggestion: always re-read a file immediately before editing it.

→ FIXED: verifier self-recovered; dispatcher added "re-read before re-anchor"
  to the standing dispatch reminders (PROTOCOL §10 rule 6, anti-stale).
