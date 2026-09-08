# tmp/architect/_run_task.py — PROTOTYPE backend for proposal P-001/P-002 (architect, 2026-09-08).
# agent-mesh task runner core.
#
# Standard task runner backend for Windows CMD:
#   - set env vars, spawn payload, capture .log/.err
#   - kill-after watchdog (taskkill /T /F on the spawn tree) -> exit 124
#   - exit-code MAP: classify benign exit-1 (findstr/dir no-match, harness
#     "NO round-1 XHR" V-022) vs real errors; never trust exit code alone
#   - tail summary printed to caller (default 30 lines)
#
# Contract (called via run_task.cmd shim):
#   _run_task.py NAME [ENV=VAL ...] -- <command> [args...]
# Options via env (not flags, to keep argv contract trivial):
#   RUN_TASK_LOGDIR      dir for NAME.log/NAME.err (default: cwd)
#   RUN_TASK_KILL_AFTER  seconds; default 900 (P-002 budget: 2x ~450s worst
#                        legit rehearsal; override for long runs)
#   RUN_TASK_TAIL        tail lines shown (default 30)
#   RUN_TASK_BENIGN_RE   extra regex; match in tail => benign exit-1
import os, re, subprocess, sys, time

CREATE_NEW_PROCESS_GROUP = 0x00000200

def parse(argv):
    if len(argv) < 3:
        sys.stderr.write("usage: _run_task.py NAME [ENV=VAL ...] -- <command> [args...]\n")
        sys.exit(2)
    name = argv[0]
    env_over = {}
    i = 1
    while i < len(argv) and argv[i] != "--":
        if "=" in argv[i]:
            k, v = argv[i].split("=", 1)
            env_over[k] = v
        else:
            sys.stderr.write("bad env pair (expected VAR=VAL or --): %r\n" % argv[i])
            sys.exit(2)
        i += 1
    if i >= len(argv):
        sys.stderr.write("missing '--' before command\n")
        sys.exit(2)
    return name, env_over, argv[i + 1:]

def tail(path, n):
    try:
        with open(path, "rb") as f:
            data = f.read()
    except OSError:
        return []
    lines = data.decode("utf-8", errors="replace").splitlines()
    return lines[-n:]

def classify(rc, log_tail, err_tail, cmd):
    """Map (rc, output) -> verdict string. The 189-failure class dies here."""
    blob = "\n".join(log_tail + err_tail)
    joined = " ".join(cmd).lower()
    benign_re = os.environ.get("RUN_TASK_BENIGN_RE", "")
    if rc == 0:
        return "OK"
    if rc == 124:
        return "TIMEOUT-KILLED (watchdog fired; raise RUN_TASK_KILL_AFTER if this run is legitimately longer)"
    if rc == 1:
        # (a) no-match tools: findstr/dir/where exit 1 on NO MATCH, not failure
        if any(t in joined for t in ("findstr", "dir ", "dir/", "where ")) and \
           not any(m in blob for m in ("Traceback", "SyntaxError", "ReferenceError",
                                        "AssertionError", "FATAL", "ENOENT")):
            return "BENIGN-NO-MATCH (findstr/dir exit 1 on zero hits — not a failure; V-022 class)"
        # (b) harness known-benign exit-1 (offline 0-POST shape)
        if "NO round-1 XHR" in blob or "0-POST" in blob:
            return "BENIGN-HARNESS (offline no-XHR exit-1 shape; V-022)"
        # (c) caller-supplied extra pattern
        if benign_re and re.search(benign_re, blob):
            return "BENIGN-CUSTOM (RUN_TASK_BENIGN_RE matched)"
    if "SyntaxError" in blob:
        return "PAYLOAD-SYNTAX-ERROR (write a script file — never node -e/python -c multiline; V-019)"
    return "ERROR (real exit %d — inspect full log)" % rc

def main():
    name, env_over, cmd = parse(sys.argv[1:])
    logdir = os.environ.get("RUN_TASK_LOGDIR", os.getcwd())
    os.makedirs(logdir, exist_ok=True)
    logp = os.path.join(logdir, name + ".log")
    errp = os.path.join(logdir, name + ".err")
    kill_after = int(os.environ.get("RUN_TASK_KILL_AFTER", "900"))
    tailn = int(os.environ.get("RUN_TASK_TAIL", "30"))

    env = dict(os.environ)
    env.update(env_over)

    t0 = time.time()
    with open(logp, "wb") as lg, open(errp, "wb") as er:
        proc = subprocess.Popen(cmd, stdout=lg, stderr=er, env=env,
                                creationflags=CREATE_NEW_PROCESS_GROUP,
                                shell=False)
        timed_out = False
        try:
            proc.wait(timeout=kill_after)
        except subprocess.TimeoutExpired:
            timed_out = True
            subprocess.run(["taskkill", "/PID", str(proc.pid), "/T", "/F"],
                           capture_output=True)
            proc.wait(timeout=30)
    rc = 124 if timed_out else proc.returncode
    dt = time.time() - t0

    lt, et = tail(logp, tailn), tail(errp, tailn)
    verdict = classify(rc, lt, et, cmd)

    print("=" * 60)
    print("[RUN_TASK] task=%s  exit=%d  wall=%.1fs" % (name, rc, dt))
    print("[RUN_TASK] verdict: %s" % verdict)
    print("[RUN_TASK] log: %s" % logp)
    print("[RUN_TASK] err: %s" % errp)
    if verdict.startswith(("ERROR", "PAYLOAD")) and not lt and not et:
        print("[RUN_TASK] *** EMPTY OUTPUT + NONZERO EXIT — possible swallowed "
              "stdout (V-019 class). Do not retry blindly; inspect files. ***")
    if lt:
        print("--- tail %s.log (last %d) ---" % (name, len(lt)))
        for line in lt:
            print("  " + line)
    if et:
        print("--- tail %s.err (last %d) ---" % (name, len(et)))
        for line in et:
            print("  " + line)
    print("=" * 60)
    sys.exit(rc)

if __name__ == "__main__":
    main()
