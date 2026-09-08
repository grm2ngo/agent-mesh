# SETUP.md — install agent-mesh into any project

## What the installer does

`init\mesh-init.cmd <path-to-your-project>` copies the starter set:

```
<your-project>/
├── AGENTS.md            # host law file (EDIT THIS — project name + specifics)
├── DISPATCH.md          # dispatcher playbook copy
├── STATE.md             # session-continuity (keep current)
├── AGENT_FRICTION.md    # friction log (append-only)
├── AGENT_VERDICTS.md    # verdict register + tier system + ledger
├── VARIABLES.md         # living board + wave economics
├── SENTINEL.md          # sentinel cycles (sentinel is sole writer)
├── LESSONS.md           # distilled lessons (curator appends)
└── tools/               # runner, watchdog, tier-check, mojibake, token report
```

Plus `agents/*.md` copied to a place your harness reads agent definitions from
(see step 2).

## Install (3 steps)

1. **Run the installer** (or copy `templates/` + `tools/` manually):
   ```cmd
   init\mesh-init.cmd C:\path\to\your\project
   ```
2. **Load the agent definitions** — copy `agents/*.md` into your harness's
   agent-definitions folder. Examples:
   - ZCode-style: `<project>\.zcode\agents\` (and optionally the user-level folder)
   - Claude-Code-style: your `.claude/agents/` equivalent
   - Any harness: paste each file's body into a custom-role prompt.
3. **Edit `AGENTS.md`**: set the project name, one paragraph of project law
   (what's sensitive, what's the goal, any hard rules), and your shell
   platform (keep/trim PROTOCOL §10's trap list).

## First dispatch (smoke test)

Ask your main agent to:
1. Read `AGENTS.md`, `PLAYBOOK.md`, `STATE.md`.
2. Dispatch one small specialist task WITH the report contract (FRICTION
   REPORT + `<V-NEXT>` verdict rows).
3. Triage the report same-turn per PLAYBOOK §5.
If friction got logged + triaged and a verdict row appeared — the mesh works.

## Going further

- Write your project's Definition-of-Done (PLAYBOOK §6) — this also arms the
  sentinel's exit condition.
- Run the sentinel continuously (background) + re-arm on a timer if your
  harness supports scheduling.
- After your first big wave, run `tools/token_report.py` for the economics
  table, and a friction-audit pass over your agent logs to baseline your
  shell-trap counts.

## Uninstall

Delete the copied files. Nothing else touches your project (no hooks, no
runtime, no dependencies — files and agent defs only).
