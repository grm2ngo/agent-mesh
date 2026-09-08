# tmp/architect/token_report.py — PROTOTYPE mechanism for P-011 (architect, 2026-09-08).
# agent-mesh token economics report
#
# Post-hoc token + context-hygiene measurement from ZCode rollout transcripts.
# Schema per V-029: each JSONL line is a FULL-HISTORY snapshot of one API call —
# parse ONLY the last line per file, dedupe tool_use by id. This script NEVER
# prints transcript CONTENT — only numbers, file paths of Read calls, and masked
# shapes (credentials-safe by construction).
#
# Outputs per session: path, size, token fields found (whatever usage keys exist),
# Read-call counts (total + top re-read files), Bash-call count. Plus a corpus
# summary (median/p75/max tokens) for ceiling calibration (DISPATCH item 7).
#
# Usage: token_report.py [--rollout DIR] [--limit N]
import os, re, sys, io, json, statistics

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROLLOUT = r"C:\Users\me\.zcode\cli\rollout"
TAIL_BYTES = 4 * 1024 * 1024  # last line can be huge; read a 4MB tail

def last_line(path):
    with open(path, "rb") as f:
        f.seek(0, os.SEEK_END)
        size = f.tell()
        f.seek(max(0, size - TAIL_BYTES))
        chunk = f.read()
    lines = [ln for ln in chunk.split(b"\n") if ln.strip()]
    return lines[-1] if lines else None

def find_usage(obj, out, depth=0):
    """Recursively collect keys that look like token usage."""
    if depth > 8 or isinstance(obj, (str, int, float, bool)) or obj is None:
        return
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, int) and re.search(r"token", k, re.I) and v > 0:
                out[k] = max(out.get(k, 0), v)
            else:
                find_usage(v, out, depth + 1)
    elif isinstance(obj, list):
        for v in obj[-50:]:
            find_usage(v, out, depth + 1)

def collect_reads(obj, reads, seen, bash):
    if isinstance(obj, dict):
        if obj.get("type") == "tool_use" or ("name" in obj and "input" in obj):
            tid = obj.get("id")
            if tid and tid not in seen:
                seen.add(tid)
                name = obj.get("name", "")
                if name == "Read":
                    fp = obj.get("input", {}).get("file_path", "?")
                    reads[fp] = reads.get(fp, 0) + 1
                elif name == "Bash":
                    bash[0] += 1
                elif name.startswith("mcp__") is False and name in ("Edit", "Write", "Grep"):
                    pass
        for v in obj.values():
            collect_reads(v, reads, seen, bash)
    elif isinstance(obj, list):
        for v in obj:
            collect_reads(v, reads, seen, bash)

def main():
    limit = int(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else 0
    files = sorted(f for f in os.listdir(ROLLOUT) if f.endswith(".jsonl"))
    if limit:
        files = files[-limit:]
    rows = []
    for fn in files:
        p = os.path.join(ROLLOUT, fn)
        try:
            raw = last_line(p)
            obj = json.loads(raw) if raw else {}
        except (json.JSONDecodeError, OSError) as e:
            rows.append((fn, os.path.getsize(p), {"ERROR": str(e)[:40]}, {}, 0))
            continue
        usage, reads, seen, bash = {}, {}, set(), [0]
        find_usage(obj, usage)
        collect_reads(obj, reads, seen, bash)
        rows.append((fn, os.path.getsize(p), usage, reads, bash[0]))
    print("%-58s %10s %8s  %s" % ("session-file", "MB", "bash", "token-fields (max per key)"))
    tok_totals = []
    for fn, size, usage, reads, bash in rows:
        core = {k: v for k, v in usage.items() if re.search(r"input|output|total|cache_read", k, re.I)}
        tot = sum(v for k, v in core.items() if re.search(r"input|output|total", k, re.I) and "cache" not in k.lower())
        tok_totals.append(tot)
        top = sorted(reads.items(), key=lambda kv: -kv[1])[:3]
        top_s = "; ".join("%s x%d" % (os.path.basename(k), v) for k, v in top)
        print("%-58s %10.1f %8d  %s" % (fn[:58], size / 1e6, bash, core if core else usage))
        if top_s:
            print("    top-reads: %s" % top_s[:150])
    if tok_totals:
        print("\ncorpus: n=%d  median=%.2fM  p75=%.2fM  max=%.2fM (token units as reported)"
              % (len(tok_totals), statistics.median(tok_totals) / 1e6,
                 sorted(tok_totals)[int(len(tok_totals) * 0.75)] / 1e6, max(tok_totals) / 1e6))

if __name__ == "__main__":
    main()
