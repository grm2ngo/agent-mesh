# agent-mesh

**A file-based multi-agent orchestration protocol for AI coding assistants.**
Turn any agent harness that supports subagents + file tools into a self-verifying,
self-correcting, knowledge-accumulating workforce.

```
                        ┌─────────────────────────────┐
                        │        DISPATCHER           │  (your main agent —
                        │  assign · triage · relay     │   the hub & approver)
                        └──────┬──────────────┬───────┘
              propose ─────────┤              ├───────── critique
                  ┌────────────▼───┐   ┌──────▼─────────┐
                  │   ARCHITECT    │   │     CRITIC     │   propose →
                  │ decision-ready │◄──┤  attacks plans  │   critique → approve
                  │   proposals    │   │  with evidence  │
                  └────────────────┘   └────────────────┘
        ┌──────────┐ ┌───────────┐ ┌──────────┐ ┌────────────┐
        │ SPECIAL- │ │  CURATOR  │ │ VERIFIER │ │  SENTINEL  │
        │ ISTS     │ │  (memory) │ │(gatekeep)│ │ (isolated  │
        │ any trade│ │ lessons,  │ │ prompt↔  │ │  watcher,  │
        │          │ │ verdicts  │ │ artifact │ │ conflicts) │
        └──────────┘ └───────────┘ └──────────┘ └────────────┘
              FILES ARE THE BUS — every agent reads/writes the same
              small set of canonical markdown files (see PROTOCOL.md)
```

## Why

A single LLM agent forgets, repeats dead ends, trusts stale docs, and ships
plausible-but-wrong claims. agent-mesh fixes the four failure classes with
four mechanisms:

| Failure class | Mechanism |
|---------------|-----------|
| Repeating dead ends | **Verdict register** (CONFIRMED / REFUTED / DO-NOT-RETRY) — check before attempting, append after every task |
| Silent knowledge rot | **Tier system** — every claim is BETA by default; VERIFIED requires multi-system reproduction + adversarial review + a ledger row |
| Unreported friction | **Mandatory FRICTION REPORT** on every subagent report + same-turn triage by the dispatcher (FIX-now / LESSON / DEFER — nothing falls through) |
| Doc/claim drift | **Isolated sentinel** continuously cross-checks all canonical files for contradictions, silent mutations, orphan refs, law violations, duplication |

Plus: adversarial review by design (architect proposes, critic attacks, dispatcher
approves), heartbeats + continuation briefs for long work, token economics per wave,
and a session-continuity state file so a dead session resumes without archaeology.

## Quickstart

```cmd
git clone https://github.com/grm2ngo/agent-mesh
cd agent-mesh
init\mesh-init.cmd C:\path\to\your\project
```

Then in your project (see `SETUP.md` for details):
1. Edit the generated `AGENTS.md` header (project name + any project-specific law).
2. Copy `agents/*.md` into your harness's agent-definitions folder.
3. Start dispatching per `PLAYBOOK.md` — the loop takes care of itself.

## What you get

| File | Role |
|------|------|
| `PROTOCOL.md` | The constitution: roles, channels, laws, tier system, sentinel classes |
| `PLAYBOOK.md` | Dispatcher procedure: dispatch checklist, templates, DoD, priorities, economics |
| `SETUP.md` | Install into any project (3 steps) |
| `agents/` | Six generic agent definitions (architect, critic, sentinel, friction-auditor, curator, verifier) |
| `templates/` | Starter canonical files your project will live in (STATE / FRICTION / VERDICTS / VARIABLES / SENTINEL / LESSONS / AGENTS) |
| `tools/` | Utilities: task runner, watchdog, tier checker, mojibake repair, token report |
| `docs/LESSONS.md` | Field-tested, project-agnostic lessons |

## Requirements

- An agent harness with: subagents (background-able), file read/write tools, a
  message-passing path to the main agent (or use files only).
- Tested on Windows/CMD (the shell survival law in PROTOCOL.md includes a
  quantified CMD trap list) — the protocol itself is platform-neutral; port the
  shell law to your shell.

## License

MIT — see `LICENSE`. No project-specific data ships in this repo (templates only).
