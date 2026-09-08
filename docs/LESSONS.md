# LESSONS.md — distilled lessons

Each lesson = an action principle, not a scar. The curator appends when a
pattern repeats ≥2 times (or once, if it cost ≥1 full session). Seed set —
field-tested, project-agnostic:

## 1. THE BIGGEST WALL IS OFTEN YOUR OWN INSTRUMENTATION
Profile before diagnosing; a second clock (heartbeat + external watchdog)
on every long run — in-process timeouts cannot fire when the loop is stuck.

## 2. WALL-OR-DONE — CHECK "IS IT JUST FINISHED?" BEFORE DEBUGGING A STALL
Verify terminal conditions first (last op = clear+return? pending timers =
0?). What looks like a stall may be normal completion with a missing
environment piece. Cheap instrumentation beats expensive speculation.

## 3. FAITHFUL MEANS FAITHFUL TO FAILURES TOO
Environments must fail exactly where the real system fails — swallowing
errors and resolving names "helpfully" creates phantom progress.

## 4. PROVE MARKERS BEFORE BUILDING TIMELINES ON THEM
Every marker must be demonstrated by experiment (send X → observe X) before
any genealogy is built on it.

## 5. ADVERSARIAL REVIEW > N AGREEING
Prosecutor + engineer + skeptic with MANDATORY checks beats consensus.
Briefs must be self-contained; artifacts written early so dead agents
still deliver.

## 6. CHEAP FALSIFICATION FIRST
Rank hypotheses by info-gain/cost; kill the cheap ones before spending.

## 7. KNOW YOUR MEASUREMENT TOOL'S CEILING
Start every measurement plan with "what can this tool NOT give?" — then
pick the right tool class per value type.

## 8. RUNTIME-FIRST, STATIC-SECOND ON CHANGING TARGETS
Derivation methods that work on one generation of a rotating target may die
on the next; record where every constant sits on the
STABLE ↔ PER-VERSION ↔ PER-INSTANCE axis and reuse at the correct level.

## 9. SHARED NAMESPACES NEED A SINGLE WRITER
Concurrent appenders to one register collide; propose-with-placeholder +
central assignment ends the class.

## 10. OBSERVABILITY CADENCE ATTACHES TO COMPUTE
Heartbeat after every RUN, not every analysis. Commit a live directory only
after its completion event; stage explicit paths, never blanket adds.

## 11. HUB + FILES AS THE BUS KEEPS AGENTS REPLACABLE
Broadcast changes immediately; harvest artifacts from dead agents; a new
session resumes from the state file without archaeology.
