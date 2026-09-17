#!/usr/bin/env python3
"""restore.py — rebuild the dashboard workspace after the ephemeral cloud container is reclaimed.

WHY THIS EXISTS
  This session runs in a cloud container that is reclaimed after a period of inactivity
  (it happened Thu Sep 17 2026 across the ~15.5h overnight gap: /home/claude came back empty
  and the 10am run had to be rebuilt by hand, ~25 min). Code lives durably in GitHub;
  per-run data lives durably in the Claude project. This script restores the code half in
  one command and prints the exact project_read list for the data half.

ONE-LINE RECOVERY (paste into Bash from an empty /home/claude):
  cd /home/claude && curl -fsSL https://raw.githubusercontent.com/cesaran246-ai/ai-frontier-dashboard/main/scripts/restore.py -o restore.py && python3 restore.py

USAGE
  python3 restore.py              restore missing files into the current directory
  python3 restore.py --force      overwrite files that already exist
  python3 restore.py --check      report only, write nothing
  python3 restore.py --dest DIR   restore somewhere other than the cwd

EXIT CODES: 0 all code/config present and valid · 1 one or more fetches or validations failed.
The container cannot reach ai-frontier-dashboard.vercel.app (egress proxy 403) but can reach
raw.githubusercontent.com, which is why GitHub is the fetch origin.
"""
import json, os, subprocess, sys, py_compile, tempfile

RAW = os.environ.get(
    "RESTORE_RAW",
    "https://raw.githubusercontent.com/cesaran246-ai/ai-frontier-dashboard/main/scripts/",
)
if not RAW.endswith("/"):
    RAW += "/"
TIMEOUT = 60

# Fallback list used only if MANIFEST.json itself cannot be fetched or parsed.
FALLBACK_CODE = [
    "build_html_v3.py", "build_kalshi.py", "build_events.py", "roll_pm.py",
    "kpatch.py", "spm_set.py", "call_set.py", "stake_set.py", "cpimax_set.py",
    "mk_artifact.py", "t_all.js", "patch_thu10.py", "mk_thu10am.py", "mk_thu1pm.py",
    "events_schedule.json",
]


def fetch(name):
    """Return bytes for scripts/<name>, or None. curl first (proven through the agent proxy),
    urllib as a fallback so the script still works if curl is absent."""
    url = RAW + name
    try:
        p = subprocess.run(["curl", "-fsSL", "--max-time", str(TIMEOUT), url],
                           capture_output=True)
        if p.returncode == 0 and p.stdout:
            return p.stdout
    except FileNotFoundError:
        pass
    try:
        import urllib.request
        with urllib.request.urlopen(url, timeout=TIMEOUT) as r:
            return r.read()
    except Exception as e:
        print(f"    ! urllib fallback failed: {type(e).__name__}: {e}")
    return None


def validate(path):
    """Cheap integrity check so a truncated download is caught here, not mid-run."""
    if path.endswith(".py"):
        try:
            py_compile.compile(path, cfile=os.path.join(tempfile.gettempdir(), "rc.pyc"),
                               doraise=True)
        except Exception as e:
            return f"python syntax error: {e}"
    elif path.endswith(".json"):
        try:
            json.load(open(path, encoding="utf-8"))
        except Exception as e:
            return f"invalid json: {e}"
    elif path.endswith(".js"):
        if os.path.getsize(path) < 200:
            return "suspiciously small"
    return None


def main():
    argv = sys.argv[1:]
    force = "--force" in argv
    check = "--check" in argv
    dest = os.getcwd()
    if "--dest" in argv:
        dest = argv[argv.index("--dest") + 1]
    os.makedirs(dest, exist_ok=True)

    print(f"restore.py -> {dest}   ({'check only' if check else 'force overwrite' if force else 'fill in missing'})")
    print(f"origin: {RAW}\n")

    raw_manifest = fetch("MANIFEST.json")
    if raw_manifest:
        try:
            man = json.loads(raw_manifest)
            entries = [(e["file"], e["dest"]) for e in man.get("code", []) + man.get("config", [])]
            print(f"manifest: {len(entries)} code/config entries (updated {man.get('updated', '?')})\n")
        except Exception as e:
            print(f"manifest unparseable ({e}) — using the built-in fallback list\n")
            man, entries = {}, [(f, f) for f in FALLBACK_CODE]
    else:
        print("manifest unreachable — using the built-in fallback list")
        print("  (if this is a network problem, project_read claude/restore.py and the claude/* code docs instead)\n")
        man, entries = {}, [(f, f) for f in FALLBACK_CODE]

    ok = skipped = failed = 0
    for src, tgt in entries:
        path = os.path.join(dest, tgt)
        if os.path.exists(path) and not force:
            print(f"  = {tgt:24s} already present ({os.path.getsize(path):,} B)")
            skipped += 1
            continue
        if check:
            print(f"  ? {tgt:24s} would fetch")
            continue
        data = fetch(src)
        if not data:
            print(f"  ✗ {tgt:24s} FETCH FAILED")
            failed += 1
            continue
        with open(path, "wb") as fh:
            fh.write(data)
        err = validate(path)
        if err:
            print(f"  ✗ {tgt:24s} {err}")
            failed += 1
        else:
            print(f"  + {tgt:24s} {len(data):,} B")
            ok += 1

    print(f"\ncode/config: {ok} written · {skipped} already present · {failed} failed")

    # ---- environment ----
    print("\nenvironment:")
    for label, cmd in (("node", ["node", "-v"]), ("python", [sys.executable, "-V"])):
        try:
            v = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
            print(f"  {label:8s} {(v.stdout or v.stderr).strip()}")
        except Exception:
            print(f"  {label:8s} MISSING")
    try:
        subprocess.run(["node", "-e", "require('playwright');console.log('playwright ok')"],
                       capture_output=True, text=True, timeout=40, cwd=dest)
        r = subprocess.run(["node", "-e", "require('playwright');console.log('ok')"],
                           capture_output=True, text=True, timeout=40, cwd=dest)
        print(f"  playwright {'ok' if r.returncode == 0 else 'MISSING — npm i playwright, Chromium is at /opt/pw-browsers'}")
    except Exception:
        print("  playwright unknown")

    # ---- what is still needed from the project ----
    data_entries = man.get("project_only_data") or [
        {"project": "claude/dashboard_data.json", "dest": "dashboard_data_v3.json"},
        {"project": "claude/kalshi.json", "dest": "kalshi.json"},
        {"project": "claude/events_overlay.json", "dest": "events_overlay.json"},
        {"project": "claude/av_earnings.csv", "dest": "av_earnings.csv"},
    ]
    missing = [e for e in data_entries if not os.path.exists(os.path.join(dest, e["dest"]))]
    print("\nSTILL NEEDED FROM THE PROJECT (per-run data — the project copy is always the newest):")
    if not missing:
        print("  none — all data files are already on disk")
    for e in missing:
        print(f"  project_read {e['project']:34s} -> save as {e['dest']}")
    if any(e["dest"] == "av_earnings.csv" for e in missing):
        print("    ^^ av_earnings.csv fails SILENTLY if skipped: earnings rows degrade to stubs, no error is raised.")
    print("  project_read claude/prompt_<this-run>.txt      -> the armed trigger names the file")
    print("  project_read claude/refresh-operations-notes.md -> save as _ops_notes.md (read the last section)")
    print("  on-demand only: claude/add_pm4.py · claude/add_pm5.py · claude/migrate_reports.py")
    print("\n  (large project docs arrive as files under /root/.claude/projects/-home-claude/<session>/tool-results/ —")
    print("   copy them to the dest name above; small ones come back inline and need a Write.)")

    if not check and failed == 0:
        print("\nnext: restore the data files above, then run the prompt's steps from step 1.")
        print("verify the chain with:  python3 build_events.py && python3 build_kalshi.py | tail -3 && python3 build_html_v3.py")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
