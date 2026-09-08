# tmp/architect/spin_watch.py — PROTOTYPE standalone watchdog for P-002 (architect, 2026-09-08).
# agent-mesh external watchdog
#
# Wraps ANY command with a hard wall-clock kill budget (independent of the
# payload's own --timeout: sync clock-spin blocks in-process timers forever —
# HARNESS_STATUS s19: 13 runs = 13 manual kills; audit: 28 TaskOutput timeouts).
# Kills the whole process TREE via taskkill /T /F, exits 124 on kill (GNU
# timeout convention), passes through payload exit code otherwise.
#
# Usage:  spin_watch.py [--kill-after S] [--name NAME] -- command [args...]
# Default budget: 900s (P-002 law: legit Node runs <=450s observed; 2x margin).
import os, subprocess, sys, time

CREATE_NEW_PROCESS_GROUP = 0x00000200

def main():
    argv = sys.argv[1:]
    kill_after, name = 900, None
    while argv and argv[0].startswith("--") and argv[0] != "--":
        if argv[0] == "--kill-after":
            kill_after = int(argv[1]); argv = argv[2:]
        elif argv[0] == "--name":
            name = argv[1]; argv = argv[2:]
        else:
            sys.stderr.write("unknown option %r\n" % argv[0]); sys.exit(2)
    if not argv or argv[0] != "--" or len(argv) < 2:
        sys.stderr.write("usage: spin_watch.py [--kill-after S] [--name NAME] -- command [args...]\n")
        sys.exit(2)
    cmd = argv[1:]
    if name is None:
        name = "watch_%s_%d" % (os.path.basename(cmd[0]).replace(".", "_"), int(time.time()))

    logdir = os.environ.get("RUN_TASK_LOGDIR", os.getcwd())
    os.makedirs(logdir, exist_ok=True)
    logp = os.path.join(logdir, name + ".log")
    errp = os.path.join(logdir, name + ".err")

    t0 = time.time()
    with open(logp, "wb") as lg, open(errp, "wb") as er:
        proc = subprocess.Popen(cmd, stdout=lg, stderr=er,
                                creationflags=CREATE_NEW_PROCESS_GROUP)
        print("[SPIN_WATCH] pid=%d budget=%ds log=%s" % (proc.pid, kill_after, logp))
        killed = False
        try:
            proc.wait(timeout=kill_after)
        except subprocess.TimeoutExpired:
            killed = True
            subprocess.run(["taskkill", "/PID", str(proc.pid), "/T", "/F"], capture_output=True)
            proc.wait(timeout=30)
    rc = 124 if killed else proc.returncode
    print("[SPIN_WATCH] done in %.1fs exit=%d%s" % (time.time() - t0, rc,
          "  (KILLED — spin/hang suspected; see .err tail)" if killed else ""))
    sys.exit(rc)

if __name__ == "__main__":
    main()
