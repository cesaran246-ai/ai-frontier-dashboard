"""roll_pm.py — auto-roll for stock-linked Kalshi KPI markets (kalshi.json → stock_pm).

Every stock_pm market carries:
  period        "Q3 2026" | "FY 2026" | "2026" | "to 2028"
  expires       Kalshi close_time date of the current event
  roll          {"series": "KXHOOD", "code": "FUNDED", "report_after": "2026-11-06"}
                code = the KPI suffix of the event ticker (KXHOOD-26NOVFUNDED → FUNDED); None = any event in the series
  prior         [] — filled by `roll` with the settled event's last read (and actual, if known)

Usage
  python3 roll_pm.py check                       → prints ROLL DUE lines (today >= report_after) — build_kalshi.py calls this too
  python3 roll_pm.py roll TICKER KEY events.json event.json [actual]
        events.json = raw kalshi_list_events dump for roll.series (status open)
        event.json  = raw kalshi_get_event dump of the successor event (the one `pick` names)
        actual      = optional reported figure for the settled period (goes in prior[].actual)
  python3 roll_pm.py pick TICKER KEY events.json   → prints the successor event ticker (or NONE) without changing anything

The refresh prompt runs `check` every run; when a market is due it calls kalshi_list_events for roll.series,
saves the dump, runs `pick`, then kalshi_get_event on the successor and runs `roll`. History is kept — entries
carry `ev`, so the chart draws the old and new events as separate lines.
"""
import json, sys, re, datetime as dt

P = 'kalshi.json'
MON = {m: i for i, m in enumerate(['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC'], 1)}

def ev_date(ev):
    """KXHOOD-26NOVFUNDED → (2026, 11); KXB200MAX-26DEC31 → (2026, 12). None if unparsable."""
    m = re.search(r'-(\d{2})([A-Z]{3})', ev)
    if not m or m.group(2) not in MON: return None
    return (2000 + int(m.group(1)), MON[m.group(2)])

def load():
    return json.load(open(P))

def markets(K):
    for tk, b in K.get('stock_pm', {}).items():
        if not isinstance(b, dict): continue
        for m in b.get('markets', []):
            yield tk, b, m

def check(K=None, today=None):
    K = K or load(); today = today or dt.date.today().isoformat()
    due = []
    for tk, b, m in markets(K):
        r = m.get('roll') or {}
        ra = r.get('report_after')
        if m.get('settled'): continue   # settled one-offs (e.g. US-stake YES) are kept as a record, never rolled
        if ra and today >= ra:
            due.append((tk, m['key'], m['ev'], r.get('series'), r.get('code'), ra))
    for tk, b in K.get('stock_pm', {}).items():
        if not isinstance(b, dict) or not b.get('call'): continue
        ra = (b['call'].get('roll') or {}).get('report_after')
        if ra and today >= ra:
            due.append((tk, 'call', b['call']['ev'], b['call']['roll'].get('series'), 'CALL', ra))
    for tk, key, ev, series, code, ra in due:
        print(f"  ROLL DUE: {tk}/{key} {ev} (report_after {ra}) → kalshi_list_events series_ticker={series} then roll_pm.py pick/roll")
    if not due: print("  roll check: nothing due")
    return due

def pick(K, tk, key, events):
    m = next(m for t, b, m in markets(K) if t == tk and m['key'] == key)
    r = m['roll']; code = r.get('code'); cur = m['ev']
    cands = []
    for e in events.get('result', events if isinstance(events, list) else []):
        ev = e['event_ticker']
        if ev == cur: continue
        if code and not ev.endswith(code): continue
        d = ev_date(ev)
        if d is None: continue
        cands.append((d, ev, e.get('title', '')))
    cur_d = ev_date(cur) or (0, 0)
    cands = [c for c in cands if c[0] > cur_d]
    cands.sort()
    return cands[0] if cands else None

def next_period(p):
    m = re.match(r'Q(\d) (\d{4})', p or '')
    if m:
        q, y = int(m.group(1)), int(m.group(2))
        return f"Q{q % 4 + 1} {y + (1 if q == 4 else 0)}"
    m = re.match(r'FY (\d{4})', p or '')
    if m: return f"FY {int(m.group(1)) + 1}"
    m = re.match(r'(\d{4})$', p or '')
    if m: return str(int(m.group(1)) + 1)
    return p

def roll(K, tk, key, events, event, actual=None):
    c = pick(K, tk, key, events)
    if not c: print(f"  no successor event for {tk}/{key}"); return False
    (_, new_ev, title) = c
    if event['event_ticker'] != new_ev:
        print(f"  event.json is {event['event_ticker']} but successor should be {new_ev}"); return False
    m = next(m for t, b, m in markets(K) if t == tk and m['key'] == key)
    old_ev, old_period, old_hs = m['ev'], m.get('period'), str(m['hist_strike'])
    last_p = m['p_above'].get(old_hs)
    m.setdefault('prior', []).append({'ev': old_ev, 'period': old_period, 'hist_strike': old_hs, 'last_p': last_p, 'actual': actual})
    rows = [(x['strike'], x['yes_mid'], x['ticker'], x.get('close_time', '')) for x in event['markets'] if x.get('status') == 'active' and x.get('strike') is not None]
    rows.sort()
    def sk(s): return str(int(s)) if float(s).is_integer() else str(s)
    m['p_above'] = {sk(s): round(p, 3) for s, p, _, _ in rows}
    m['hist_strike'] = sk(min(rows, key=lambda r: abs(r[1] - 0.5))[0])
    m['vol'] = round(max(x.get('volume', 0) for x in event['markets']))
    m['ev'] = new_ev
    m['tickers'] = f"{new_ev}-<{rows[0][2].split('-')[-1]} … {rows[-1][2].split('-')[-1]}>"
    m['expires'] = (rows[0][3] or '')[:10] or m.get('expires')
    newp = next_period(old_period)
    for f in ('title', 'short', 'horizon'):
        if old_period and isinstance(m.get(f), str): m[f] = m[f].replace(old_period, newp).replace(old_period.replace(' ', ' '), newp)
    m['period'] = newp
    ra = dt.date.fromisoformat(m['roll']['report_after'])
    m['roll']['report_after'] = (ra + dt.timedelta(days=365 if old_period and old_period.startswith('FY') else 91)).isoformat()
    m['note'] = f"Rolled from {old_ev} on {dt.date.today().isoformat()} (last read {last_p} for >{old_hs}). " + (m.get('note') or '')
    print(f"  rolled {tk}/{key}: {old_ev} → {new_ev} ({old_period} → {newp}); anchor {m['hist_strike']}; report_after {m['roll']['report_after']}")
    return True

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'check'
    K = load()
    if cmd == 'check': check(K)
    elif cmd == 'pick':
        tk, key, evf = sys.argv[2], sys.argv[3], sys.argv[4]
        c = pick(K, tk, key, json.load(open(evf))); print(c[1] if c else 'NONE')
    elif cmd == 'roll':
        tk, key, evf, ef = sys.argv[2:6]; actual = float(sys.argv[6]) if len(sys.argv) > 6 else None
        if roll(K, tk, key, json.load(open(evf)), json.load(open(ef)), actual):
            json.dump(K, open(P, 'w'), indent=1, ensure_ascii=False); print('  kalshi.json written')
