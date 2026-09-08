# PLAYBOOK.md — dispatcher procedure

How the dispatcher (main agent) briefs, monitors and closes subagent work.
Companion to PROTOCOL.md (law). Keep this file next to AGENTS.md in the host
project.

## 1. Task-ID convention

Format `<wave>-<seq>-<slug>` (e.g. `w3-g1-cdp`, `w3-t1-translate`), assigned
at spawn; respawns keep the id with `-r2`, `-r3`. The id appears in: artifact
dir names, sandbox folders, commit messages (`task <id>`), verdict/friction
rows, STATUS.md heartbeats.

## 2. Every dispatch carries (checklist)

1. Task-ID + role + a SELF-CONTAINED mission (assume the agent has only the
   canonical files as prior knowledge).
2. Time budget (default 60 min; live missions state attempt caps + auto-stop rays).
3. File-ownership boundaries (what it may WRITE; everything else read-only).
4. Safety rays (what must never be sent/touched/printed).
5. Output contract: artifacts to disk EARLY + final message + mandatory
   `## FRICTION REPORT` + verdict rows as `<V-NEXT>` placeholders.
6. PREFLIGHT DO-NOT-RETRY: before dispatching, the dispatcher greps the verdict
   register for DO-NOT-RETRY/REFUTED rows relevant to the task and pastes them
   INTO the brief — the register only saves lives if the agent sees the dead ends.
7. Token budget guidance: state a ceiling per task type; read large files with
   offset/limit; never re-read what's in context (note key facts in STATUS.md).
8. Tier rule: single-run results are BETA; claiming VERIFIED requires citing
   ≥2 independent evidence paths.
9. Reminders: immediate-broadcast duty; info-requests go through the dispatcher.

## 3. Heartbeat & monitoring

Monitor `<artifact-dir>/STATUS.md` (cheap), never transcripts. Cadence ~10 min,
one line per RUN: `HH:MM | done: X | next: Y | blockers: Z`. Nudge once when a
beat is missed by 2× cadence; a silent agent with artifacts still moving is
working — check the directory mtimes first.

## 4. Brief templates (fill per role)

- **specialist/code**: files owned → offline tests that must PASS → commit
  scope (task id in message) → no-push ray.
- **specialist/live-measurement**: tooling inventory FIRST → measurement plan
  → rays (what must never be sent) → artifact contract → window length.
  DEFAULTS TO A CONTINUATION CHAIN: each run ends with a STATUS.md handoff;
  respawn from it; never restart from scratch while a handoff exists.
- **architect**: `PROPOSALS.md` `P-<NNN>` contract (problem + evidence path ·
  options A/B/C + trade-offs · cost · migration · risks · RECOMMENDATION ·
  ready-to-paste law text). Ordered by risk-reduction per cost. Cross-check
  the verdict register first — never re-propose refuted items.
- **critic**: `CRITIQUE.md` `C-<NNN>` contract (target · severity
  BLOCKER/HIGH/MEDIUM/LOW · claim attacked · evidence · proposed fix).
  Adversarial by charter, including against the dispatcher.
- **curator**: files owned → heading-preservation warning (insert content
  BEFORE the next heading — the "heading-eating" edit bug) → evidence-faithful
  only, never invents.
- **verifier**: prompt-to-artifact checklist; proxy signals don't count.
- **sentinel**: run per PROTOCOL §6 until the DoD exit condition.

## 5. Triage duty (every report, same turn)

1. Verify claimed outcomes against artifacts (spot-check, don't rubber-stamp).
2. Classify every FRICTION item → FIX-now / LESSON / DEFER; record in
   `AGENT_FRICTION.md`.
3. Assign verdict IDs to `<V-NEXT>` proposals; reconcile blocks into the
   register; evaluate tier upgrades/demotions against PROTOCOL §5.
4. Update `VARIABLES.md` + show the user the board (tables only) with a
   wave-economics row (token spend via `tools/token_report.py`).
5. Broadcast important news (P0 relayed now; P1 batched).
6. Update `STATE.md`.

## 6. Definition-of-Done (write one per project)

A DoD is a short, checkable list. Pattern:

```markdown
## Definition-of-Done: "<project> complete"
ALL of:
1. <core capability> demonstrated end-to-end under the project's quality bar;
2. <integration surface> wired and offline-tested;
3. verifier passes the prompt-to-artifact audit;
4. sentinel reports zero C1/C2 conflicts for ≥2 consecutive cycles;
5. <robustness condition> (rotation/regression survival) demonstrated.
```

Until ALL hold, the project is NOT complete — watchers stay armed. Also write
a SYSTEM DoD for the mesh itself (full propose→critique→approve cycle done ·
sentinel clean · tooling landed · docs tier-compliant · measured error-class
reduction vs baseline).

## 7. Backup / retention minimums

- Off-device backup of canonical files (any sync drive); run a RESTORE DRILL
  (extract + byte-compare) to make the mitigation real; re-drill on a
  different day to promote it to VERIFIED.
- Commit only after completion notifications; keep large artifacts out of
  git if the remote rejects them; a local-only repo needs the drill even more.
