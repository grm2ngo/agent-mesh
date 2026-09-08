# PROPOSALS.md — architect proposals

Schema `P-<NNN>` (append-only; dispatcher adjudicates; approved items get a
`→ APPROVED <date>` line and their law text lands in the canonical files):

```
## P-<NNN> — <title>
- Problem: <description + evidence path>
- Options: A) … B) … C) … (trade-offs each)
- Cost: <estimate>
- Migration: <steps>
- Risks: <list>
- RECOMMENDATION: <option + why>
- LAW TEXT (ready to paste): <verbatim block>
```
Order by risk-reduction per cost. Cross-check AGENT_VERDICTS.md first — never
re-propose refuted or do-not-retry items.
