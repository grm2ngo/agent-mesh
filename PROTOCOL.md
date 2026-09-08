# PROTOCOL.md — the agent-mesh constitution

This file defines the operating law for a multi-agent workforce on top of any
harness that supports subagents + file tools. Host projects adopt it by keeping
a project-local `AGENTS.md` (see `templates/AGENTS.md`) that includes this
protocol and adds project-specific law.

---

## 1. ROLES

| Role | Count | Charter |
|------|-------|---------|
| **dispatcher** | 1 (your main agent) | Assigns work, triages every report SAME-TURN, is the sole ID-assigner and law-approver, relays information between members (info-broker) |
| **specialists** | any | The trades: coding, research, measurement, reverse-engineering, ops — whatever the project needs. Briefed per-dispatch (PLAYBOOK.md) |
| **architect** | 1 | Turns observed problems into decision-ready proposals (options + trade-offs + ready-to-paste law text). Never lands changes itself |
| **critic** | 1 | Adversarial reviewer: attacks proposals, rules, docs and EVEN dispatcher decisions, with evidence. No rubber-stamping |
| **curator** | 1 | Memory keeper: merges reports into canonical files, distills repeated patterns into lessons. Organizes, never invents |
| **verifier** | on demand | Acceptance gate: prompt-to-artifact checklists; proxy signals (green tests ≠ done if tests don't cover the ask) don't count |
| **friction-auditor** | on demand | Mines agent-session logs for recurring error clusters; quantifies; proposes FIX/LESSON/DEFER |
| **sentinel** | 1, always-on | ISOLATED consistency watcher over all canonical files (see §6). No collaboration, no broadcasts in or out |

## 2. CHANNELS — FILES ARE THE BUS

A small, fixed set of markdown files at the host project root is the ONLY
inter-agent communication medium besides dispatcher relays:

| File | Content |
|------|---------|
| `STATE.md` | Session-continuity heartbeat: running agents, queue, key decisions. A dispatcher reads it FIRST on spawn and keeps it current |
| `AGENT_FRICTION.md` | Friction log: every blocker any agent hit + dispatcher triage status (FIX-now / LESSON / DEFER). Appends only |
| `AGENT_VERDICTS.md` | Verdict register: CONFIRMED-TRUE / REFUTED / DO-NOT-RETRY / UNVERIFIED-INFER + evidence path, plus the TIER SYSTEM header and VERIFIED LEDGER (§5) |
| `VARIABLES.md` | The living board: SOLVED / OPEN variables, owners, blockers + wave economics (token spend) |
| `LESSONS.md` | Distilled, project-agnostic-within-project lessons. Curator appends when a pattern repeats ≥2 times |
| `SENTINEL.md` | The sentinel's cycle reports + claim registry (sentinel is the only writer) |
| `MAP.md` *(optional)* | One-file atlas of a complex domain: paths, vocabulary, mechanisms, milestones, do-not-trust list |

**Canonical-copy rule:** each concern has exactly ONE canonical file; copies
elsewhere are archives and must carry an `ARCHIVED` banner pointing at the
canonical location.

## 3. THE REPORT CONTRACT

Every subagent final report ends with a mandatory block:

```markdown
## FRICTION REPORT
<every blocker hit, in maximal detail: exact failing command/error, file+line,
attempt number, workaround used, suggested fix — or NONE>
```

- A report missing the block gets sent back by the dispatcher.
- The dispatcher triages EVERY item **in the same turn** it receives the report:
  classifies FIX-now / LESSON / DEFER and records the status in
  `AGENT_FRICTION.md`. No friction item is ever left unclassified.
- At task end agents ALSO append verdict rows to `AGENT_VERDICTS.md` —
  successors must not retry what already died there.

### Verdict register rules
- Schema: `| ID | Verdict | Claim | Evidence / Source | Notes |`
- **ID allocation is single-writer**: agents PROPOSE rows using `<V-NEXT>`
  placeholder markers inside a tagged block (e.g. `### V-<TASK>-BLOCK`);
  the DISPATCHER assigns final IDs at triage. (Shared mutable namespaces
  need a single writer — learned the hard way, 4 collisions.)
- Never delete rows; supersede in-row with `SUPERSEDED-BY <id>`.

## 4. COMMUNICATION LAW

- **Immediate-broadcast duty**: an agent discovering load-bearing information
  MID-TASK (model flip, blocker broken, standing file moved, law changed)
  messages the dispatcher IMMEDIATELY — never holds it for the final report.
- **Info-broker**: an agent needing information owned by another agent asks
  the DISPATCHER, who checks the canonical files first, then relays the
  request; the owner answers in its next message (no session end needed).
- **Broadcast priorities**: **P0 (interrupt)** — model flips, wall breaks,
  auth changes, canonical moves, stop orders → relayed immediately;
  **P1 (FYI)** — verdicts, commits, queue changes → batched naturally.
- **Multi-dispatcher coexistence**: if several main sessions run on the same
  project, coordinate ONLY through the canonical files; every insertion
  follows this protocol (tagged, English/working-language, no clobbering).

## 5. TIER SYSTEM — BETA vs VERIFIED

Every claim, constant, tool, model and hypothesis is **BETA by default** —
including CONFIRMED-TRUE rows — unless listed in the VERIFIED LEDGER.

**Promotion to VERIFIED requires ALL of:**
1. ≥2 INDEPENDENT verification instances — different systems / methods /
   build-generations / environments (re-running the same script on the same
   input does NOT count);
2. results MATCH within stated tolerance, no unresolved contradiction
   anywhere in the register or critique file;
3. evidence paths exist on disk and are cited in the row;
4. survived adversarial review (critic or verifier had a shot; no open
   finding against it);
5. rotation-relevant facts held across ≥1 rotation cycle, or their bound is
   documented.

**Demotion:** any failed reproduction or contradiction → immediate demote to
BETA + SUPERSEDED handling. The dispatcher executes demotions; when the critic
contests a grant, the grant is demoted to BETA-pending-repair until reconciled.

**Grandfather clause:** pre-adoption content is provisionally BETA;
retroactive markers are not required until the re-tag pass completes (set a
deadline; keep a worklist).

**Scope clause:** for claims observable only on one machine (shell/tool
behavior), the multi-system bar counts CROSS-SESSION independence.

Canonical docs must not rest load-bearing claims on unmarked BETA evidence.
A mechanical checker lives in `tools/check_tiers.py`.

## 6. SENTINEL — THE ISOLATED WATCHER

One sentinel agent runs continuously in the background until the project's
Definition-of-Done (PLAYBOOK.md §DoD) is met:
- reads ONLY the canonical files; writes ONLY `SENTINEL.md` + its scratch;
- never messages anyone; ignores everything except a direct STOP;
- each cycle: mtime-diff the canonical set against its claim registry,
  re-scan changed files, and report classes:
  **C1** contradiction · **C2** silent mutation (claim changed with no
  SUPERSEDED marker) · **C3** orphan reference · **C4** law violation ·
  **C5** idea duplication · **C6** tier violation (VERIFIED tag not in ledger).
- resolutions are recorded by the dispatcher citing the sentinel finding id.

## 7. EXECUTION LAW

- **Timebox**: every dispatch carries an explicit time budget.
- **Heartbeat**: long-running agents maintain `<artifact-dir>/STATUS.md` —
  one line per RUN (~10 min cadence), format `HH:MM | done: X | next: Y |
  blockers: Z`. Beats attach to compute milestones, not thinking milestones.
- **Dead-agent delivery**: artifacts are written to disk EARLY and often; a
  dead agent's work still ships.
- **Respawn-on-death**: the dispatcher respawns with a continuation brief
  built from STATUS.md + artifacts; task-id keeps an `-rN` suffix.
- **Continuation-brief default**: live/long work runs as a chain of
  continuation sessions; never restart from scratch while a handoff exists.
- **Concurrency cap**: ≤8 concurrent agents; excess work queues.
- **Edit-locks**: during translation/large-edit waves the dispatcher records
  owner + ETA per file in `STATE.md`.
- **Git discipline**: commit a live agent's directory only AFTER its
  completion notification; stage explicit finished subpaths, never
  `git add -A` over live directories.

## 8. SANDBOX & PROMOTION OF CODE

Experimental code lives in `<project>/sandbox/<task-id>/` (scratch +
`VALIDATION.md`); main code NEVER imports from sandbox. Promotion = offline
tests PASS + verifier approval + a row in `sandbox/PROMOTIONS.md`. Knowledge
tiers (§5) and code tiers are the same system.

## 9. LANGUAGE

All inter-agent work products (reports, canonical files, code comments,
commit messages) use one working language (default: English). The user-facing
channel may differ. Legacy content stays as-is; new sections follow the law.

## 10. SHELL SURVIVAL LAW (reference implementation: Windows CMD)

Know your shell's traps and keep a QUANTIFIED list (counts, not vibes).
The CMD reference set — each rule earned by repeated, counted failures:

1. Multi-line `python -c` / `node -e` swallow stdout / fail silently →
   always script files; prefer a task runner (`tools/run_task.cmd`).
2. PowerShell `$var` does not survive inline in CMD → write `.ps1` files.
3. Exit codes change meaning across cmd/redirect layers; `%errorlevel%`
   expands at PARSE time → check in a separate call.
4. Absolute paths for artifacts; know your tool's path-joining quirks
   (e.g. a `--out` that prepends a fixed segment and silently doubles it).
5. `.bak` before any blanket edit of unversioned files.
6. Anti-stale: read the CURRENT file before citing it; overturned claims
   carry `SUPERSEDED-BY`.
7. POSIX commands do not exist in CMD (`ls/cat/grep/head/wc/sed/awk`) →
   `dir /b`, `type`, `findstr`, or script files.
8. `timeout /t` fails in non-interactive shells → poll logs/files.
9. Edit-tool anchors: byte-check encoding before anchoring on rendered text;
   console rendering of UTF-8 lies.
10. Never chain `&` after a parenthesized `if/else` — the chain binds into
    the else-branch and the remaining checks silently never run.
11. `Get-Process` has no CommandLine property (use CIM); redirect-handle glue
    (`0>`/`1>`) eats digits in echo lines.

Port this list to your shell; keep the counts.
