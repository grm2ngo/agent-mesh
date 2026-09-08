# tmp/architect/check_tiers.py — PROTOTYPE for P-007 extension (architect, 2026-09-08).
# agent-mesh tier gate — see PROTOCOL.md section 5
#
# Mechanical tier gate (TIER SYSTEM, AGENT_VERDICTS.md): every explicit VERIFIED tag
# in docs AND code comments must map to a VERIFIED-LEDGER V-id (or carry an inline
# "(pending re-tag)" marker, counted as debt). Exit 1 if unmapped tags remain.
#
# Scope of a "VERIFIED tag" (deliberately narrow — prose like "live-verified
# 2026-09-05" is NOT a tier claim and stays legal):
#   - the bracket tag [VERIFIED]
#   - the phrase VERIFIED-tier / VERIFIED LEDGER-ledger claims ("listed in the VERIFIED LEDGER")
# For each occurrence we look for a V-id (V-NNN) in the same line (table row cells
# count: same physical line). Ledger ids are parsed from AGENT_VERDICTS.md
# "VERIFIED LEDGER" table + rows whose verdict cell contains VERIFIED.
#
# Usage: check_tiers.py [--root DIR]   (default: project root above tools/)
import os, re, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = None  # resolved below (script-relative project root)
import pathlib
ROOT = str(pathlib.Path(__file__).resolve().parent.parent)
VERDICTS = os.path.join(ROOT, "AGENT_VERDICTS.md")
TAG_RE = re.compile(r"\[VERIFIED\]|VERIFIED-tier")
VID_RE = re.compile(r"V-\d{3}")
PENDING_RE = re.compile(r"pending re-tag", re.I)
SKIP_DIRS = {"tmp", "node_modules", "__pycache__", "creds", "archive", ".git", ".zcode"}
TEXT_EXT = (".md", ".py", ".mjs", ".js", ".cmd", ".txt")
# files that DEFINE the tier system legislate the concept; their prose mentions are
# not claims. Knowledge files (MAP/FINDINGS/HARNESS_STATUS/LESSONS/docs) + code
# comments ARE claims and get gated.
SYSTEM_FILES = {"AGENT_VERDICTS.md", "DISPATCH.md", "AGENTS.md", "PROPOSALS.md",
                "STATE.md", "CRITIQUE.md", "STANDARD.md"}

def ledger_ids():
    ids = set()
    in_ledger = False
    import os
    if not os.path.exists(VERDICTS):
        print(f"[check_tiers] no AGENT_VERDICTS.md at {VERDICTS} - not a mesh host project? nothing to check")
        return set()
    for line in open(VERDICTS, encoding="utf-8", errors="replace"):
        if line.startswith("### VERIFIED LEDGER"):
            in_ledger = True
            continue
        if in_ledger and line.startswith("## "):
            in_ledger = False
        m = VID_RE.findall(line)
        verdict_cell = re.match(r"\|\s*V-\d{3}\s*\|\s*([A-Z-]+)", line)
        promoted = verdict_cell and verdict_cell.group(1).startswith("VERIFIED") \
            and not verdict_cell.group(1).startswith("UNVERIFIED")
        if m and (in_ledger or promoted):
            ids.update(m)
    return ids

def comment_stripped(line, ext):
    # only check code-comment lines for the tag phrase (docs checked wholesale)
    if ext in (".py", ".js", ".mjs", ".cmd"):
        s = line.lstrip()
        if s.startswith(("#", "//", "rem ", "REM ", "::")):
            return line
        return ""
    return line

def main():
    root = sys.argv[sys.argv.index("--root") + 1] if "--root" in sys.argv else ROOT
    ok_ids = ledger_ids()
    print("VERIFIED-LEDGER ids parsed: %d -> %s" % (len(ok_ids), ", ".join(sorted(ok_ids))[:120]))
    findings, pending = [], 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for f in filenames:
            if not f.endswith(TEXT_EXT):
                continue
            p = os.path.join(dirpath, f)
            rel = os.path.relpath(p, root)
            if f in SYSTEM_FILES and os.path.dirname(p) == root:
                continue  # system-defining files legislate the concept, not claims
            try:
                lines = open(p, encoding="utf-8", errors="replace").read().splitlines()
            except OSError:
                continue
            for i, line in enumerate(lines, 1):
                scope = comment_stripped(line, os.path.splitext(f)[1])
                if not scope or not TAG_RE.search(scope):
                    continue
                if PENDING_RE.search(scope):
                    pending += 1
                    continue
                cited = VID_RE.findall(scope)
                if cited and all(v in ok_ids for v in cited):
                    continue
                findings.append((rel, i, line.strip()[:120],
                                 "V-id not in ledger" if cited else "no V-id cited"))
    print("\nUNMAPPED VERIFIED tags: %d   (pending re-tag markers: %d)" % (len(findings), pending))
    for rel, i, snip, why in findings:
        print("  %-52s L%-4d %-9s %s" % (rel, i, why, snip))
    sys.exit(1 if findings else 0)

if __name__ == "__main__":
    main()
