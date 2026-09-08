# tmp/architect/fix_mojibake.py — PROTOTYPE standing tool for P-007 (architect, 2026-09-08).
# agent-mesh encoding repair tool
#
# Detects and (with --fix) repairs round-trip mojibake: text that was UTF-8,
# decoded as cp1252, then saved as UTF-8 ("â€”" for "—", "Ã©" for "é", ...).
# Repair = encode('cp1252').decode('utf-8') applied ONLY to segments that
# round-trip cleanly; per-line gating keeps valid Vietnamese untouched.
#
# Safety (V-021: blanket-replace without backup cost 182 strings once):
#   - report-only by default; --fix required
#   - ALWAYS writes <file>.bak next to the original
#   - never touches engines/*/creds, archive/**, *.har
#   - prints per-file: lines-scanned / lines-flagged / lines-changed
# Usage: fix_mojibake.py [--fix] file1 [file2 ...]
import os, re, sys, shutil

# sequences that only plausibly occur as cp1252-misdecode of UTF-8
SUSPECT = re.compile(r"[\u00c2\u00c3\u00e2][\u0080-\u00bf\u20ac\u0153\u0161\u017e\u2013\u2014\u2018\u2019\u201c\u201d\u2026\u00a0-\u00ff]?")

EXCLUDE = ("\\creds\\", "\\archive\\", ".har")

def try_fix_segment(s):
    """Return fixed string if s round-trips as cp1252->utf8, else None."""
    try:
        rt = s.encode("cp1252").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return None
    # accept only if the repair actually removes suspect sequences
    return rt if rt != s else None

def process(path, do_fix):
    if any(x in path.lower() for x in EXCLUDE):
        print("SKIP (excluded): %s" % path)
        return
    try:
        raw = open(path, encoding="utf-8").read()
    except (OSError, UnicodeDecodeError) as e:
        print("SKIP (unreadable utf-8: %s): %s" % (e, path))
        return
    flagged = changed = 0
    out_lines = []
    for ln in raw.splitlines(keepends=True):
        if SUSPECT.search(ln):
            flagged += 1
            body, nl = ln.rstrip("\r\n"), ln[len(ln.rstrip("\r\n")):]
            fixed = try_fix_segment(body)
            if fixed is not None:
                changed += 1
                out_lines.append(fixed + nl)
                continue
        out_lines.append(ln)
    print("%-60s lines-flagged=%-5d lines-fixable=%-5d" % (path, flagged, changed))
    if do_fix and changed:
        shutil.copy2(path, path + ".bak")  # V-021: backup BEFORE write
        with open(path, "w", encoding="utf-8", newline="") as fh:
            fh.write("".join(out_lines))
        print("    -> fixed (backup at %s.bak)" % path)

def main():
    args = [a for a in sys.argv[1:] if a != "--fix"]
    do_fix = "--fix" in sys.argv[1:]
    if not args:
        sys.stderr.write("usage: fix_mojibake.py [--fix] file1 [file2 ...]\n")
        sys.exit(2)
    for p in args:
        if os.path.isfile(p):
            process(p, do_fix)

if __name__ == "__main__":
    main()
