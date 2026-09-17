# scripts/ — dashboard build toolchain

The generator behind [ai-frontier-dashboard.vercel.app](https://ai-frontier-dashboard.vercel.app).
The site itself is a single self-contained `index.html` at the repo root, rebuilt three times a
trading day (10am / 1pm / 5pm ET) and uploaded here; Vercel deploys on push.

This folder exists so the toolchain survives its build environment. The build runs in an
ephemeral cloud container that gets reclaimed after a few hours of inactivity — on 17 Sep 2026 it
was reclaimed overnight and the whole workspace had to be reassembled by hand. Code now lives
here; the per-run data (prices, Kalshi state, calendar overlay) lives in a private store and is
never committed.

## Recovery

From an empty workspace, one command:

```bash
curl -fsSL https://raw.githubusercontent.com/cesaran246-ai/ai-frontier-dashboard/main/scripts/restore.py -o restore.py && python3 restore.py
```

`restore.py` fetches everything listed in `MANIFEST.json`, syntax-checks each file, reports the
node/playwright environment, and prints the short list of data files to restore from the private
store. `--check` reports without writing, `--force` overwrites, `--dest DIR` targets another
directory.

## Layout

| File | Role |
|---|---|
| `build_html_v3.py` | renderer — data + derived markets → `index.html` |
| `build_kalshi.py` | Kalshi state → prediction-market cards, settled database, history |
| `build_events.py` | schedule + overlay → the events calendar |
| `roll_pm.py` | rolls a settled market to the next period automatically |
| `kpatch.py` `spm_set.py` `call_set.py` `stake_set.py` `cpimax_set.py` | incremental writers, one market group each |
| `mk_artifact.py` | strips the page wrappers for republishing |
| `t_all.js` | Playwright regression over the built page |
| `patch_thu10.py` `mk_thu10am.py` `mk_thu1pm.py` | per-run templates |
| `events_schedule.json` | static macro/corporate event schedule |

Build order is `build_events.py` → `build_kalshi.py` → `build_html_v3.py`. Run `build_kalshi.py`
after `build_events.py`, never before — the calendar strips are attached to events the first
script rebuilds.

No credentials, API keys, or account data are in this folder, and none belong here.
