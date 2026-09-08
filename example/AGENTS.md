# AGENTS.md — greet-lib (agent-mesh host law)

This project runs on the agent-mesh protocol. Read `PROTOCOL.md` in the
agent-mesh source for the full constitution — this file adds project law.

## Project law
- Goal: greet-lib is a minimal Node.js library exposing one function,
  `greet(name)`, that returns a friendly one-line greeting. Wave 1 delivers
  the module + a passing test; publishing is a later wave.
- Sensitive: nothing — a toy project. Default rays still apply: never print
  or commit credentials; stay inside this project directory.
- Stack: Node.js, CommonJS, built-in `node:test` only — zero npm
  dependencies. `node --test` must pass before any task closes.
- Hard rules: every claim is BETA unless in the VERIFIED LEDGER; report
  every blocker, never suffer in silence.

## Definition-of-Done: "greet-lib complete"
ALL of: (1) `greet(name)` implemented + unit-tested; (2) verifier passes the
prompt-to-artifact audit; (3) sentinel reports zero C1/C2 for ≥2 cycles.

## Mesh pointers (keep)
- Roles + channels + laws: agent-mesh `PROTOCOL.md` (roles, channels, report
  contract, tier system, sentinel, shell survival law).
- Dispatcher procedure: agent-mesh `PLAYBOOK.md` (task-IDs, heartbeats,
  triage duty, DoD, priorities, economics).
- Session continuity: read `STATE.md` FIRST on spawn; keep it current.
- Verdict register + tier ledger: `AGENT_VERDICTS.md` — check before
  attempting ANY approach; append `<V-NEXT>` rows at task end.
- Friction: report every blocker in your `## FRICTION REPORT`; the
  dispatcher triages same-turn.
- Shell platform: Windows CMD — the quantified trap list lives in
  PROTOCOL §10; keep your counts current.
