#!/usr/bin/env python3
"""Build the `events` list for the dashboard (Events Calendar section).

Sources merged, in order:
  1. events_schedule.json  — official agency release calendars (Fed, BLS, BEA, BoJ, ECB, Eurostat, Stat. Bureau of Japan)
     + hand-curated corporate events (investor days, product events)
  2. AV EARNINGS_CALENDAR (av_earnings.csv, refreshed each run) + Stocklake earnings_date / earnings.nx
     → one 'earn' event per tracked name (firm date if a source has it, else est. from last report + 91d)
  3. events_overlay.json   — consensus / actual / prior metrics + notes, keyed by event id "cat:kind:date"

Window: today−14d … today+60d for macro, today+95d for corporate.
Writes `events` (sorted by date) into dashboard_data_v3.json. NEVER touches other keys.
"""
import json, csv, os, datetime as dt

TODAY = dt.date.today()
LOOKBACK, MACRO_AHEAD, CORP_AHEAD = 14, 60, 95
D = lambda s: dt.date.fromisoformat(s)

sched = json.load(open('events_schedule.json'))
overlay = json.load(open('events_overlay.json'))
data = json.load(open('dashboard_data_v3.json'))
C = data['companies']
tracked = [t for t in C if t not in ('DIA', 'EWJ')]

TITLES = {
    'fomc': 'FOMC decision', 'fomc_minutes': 'FOMC minutes', 'cpi': 'CPI', 'ppi': 'PPI', 'nfp': 'Employment Situation (NFP)',
    'jolts': 'JOLTS job openings', 'gdp': 'GDP', 'pce': 'PCE inflation / personal income', 'retail': 'Retail sales',
    'ism_mfg': 'ISM Manufacturing PMI', 'ism_svc': 'ISM Services PMI', 'empire': 'Empire State manufacturing survey',
    'boj': 'BoJ policy decision', 'boj_summary': 'BoJ Summary of Opinions', 'jp_cpi': 'Japan national CPI', 'tokyo_cpi': 'Tokyo CPI',
    'tankan': 'BoJ Tankan survey', 'jp_gdp': 'Japan GDP',
    'ecb': 'ECB rate decision', 'ecb_accounts': 'ECB monetary policy accounts', 'hicp_flash': 'Euro area HICP flash',
    'hicp_final': 'Euro area HICP final', 'eu_gdp': 'Euro area GDP', 'eu_pmi': 'Euro area flash PMI',
}
KEY_KINDS = {'fomc', 'cpi', 'nfp', 'pce', 'boj', 'ecb', 'hicp_flash', 'gdp'}

events = []

def add(ev):
    ev.setdefault('metrics', [])
    ov = overlay.get(ev['id'])
    if ov:
        ev['metrics'] = ov.get('metrics', ev['metrics'])
        if ov.get('note'): ev['note'] = ov['note']
        if ov.get('src'): ev['data_src'] = ov['src']
        if ov.get('result'): ev['result'] = ov['result']
    ev['has_actual'] = any(m.get('a') for m in ev['metrics'])
    ev['past'] = D(ev['date']) < TODAY
    events.append(ev)

# 1. macro schedules
for cat in ('us', 'jp', 'eu'):
    for kind, spec in sched[cat].items():
        for row in spec['dates']:
            est = spec.get('est', False)
            if kind in ('fomc', 'boj', 'ecb'):
                start, end, flag = row
                date, label = end, ''
                if kind == 'fomc': label = 'with Summary of Economic Projections' if flag else ''
                if kind == 'boj': label = 'with Outlook Report' if flag else ''
                if kind == 'ecb': label = 'with staff projections' if flag else ''
                title = TITLES[kind] + (' — ' + label if label else '')
                ev = {'id': f'{cat}:{kind}:{date}', 'cat': cat, 'kind': kind, 'date': date, 'start': start,
                      'time': spec['time'], 'title': title, 'src': spec['src'], 'imp': spec['imp'], 'est': False}
            else:
                date, label = row[0], row[1]
                if len(row) > 2: est = row[2]
                title = f"{TITLES[kind]} ({label})"
                ev = {'id': f'{cat}:{kind}:{date}', 'cat': cat, 'kind': kind, 'date': date,
                      'time': spec['time'], 'title': title, 'src': spec['src'], 'imp': spec['imp'], 'est': est}
            d = D(date)
            if TODAY - dt.timedelta(days=LOOKBACK) <= d <= TODAY + dt.timedelta(days=MACRO_AHEAD):
                ev['key'] = kind in KEY_KINDS
                add(ev)

# 2. corporate — earnings
av = {}
if os.path.exists('av_earnings.csv'):
    for r in csv.DictReader(open('av_earnings.csv')):
        if r['symbol'] in tracked and r['symbol'] not in av: av[r['symbol']] = r
sl = {}  # optional stocklake earnings-calendar dump {symbol: iso}
if os.path.exists('sl_earnings.json'):
    for r in json.load(open('sl_earnings.json')).get('results', []): sl[r['symbol']] = r['earnings_date'][:10]

for t in tracked:
    c = C[t]; date = None; est = True; eps_est = None; fp = None; src = None
    if t in av:
        date, est, src = av[t]['reportDate'], False, 'Alpha Vantage earnings calendar'
        eps_est = av[t].get('estimate') or None; fp = 'FQ ending ' + av[t].get('fiscalDateEnding', '')
    elif t in sl:
        date, est, src = sl[t], False, 'Stocklake earnings calendar'
    else:
        ed = (c.get('earnings_date') or '')[:10]
        nx = (c.get('earnings') or {}).get('nx')
        if ed and D(ed) >= TODAY and not c.get('earnings_is_estimate'):
            date, est, src = ed, False, 'Stocklake'
        elif nx and nx[0]:
            date, est, src, fp = nx[0], True, 'company cadence (est.)', nx[1]
        elif ed:
            date, est, src = (D(ed) + dt.timedelta(days=91)).isoformat(), True, 'last report + 91d (est.)'
    if not date: continue
    d = D(date)
    if not (TODAY - dt.timedelta(days=LOOKBACK) <= d <= TODAY + dt.timedelta(days=CORP_AHEAD)): continue
    when = (av.get(t, {}).get('timeOfTheDay') or '').replace('pre-market', 'before open').replace('post-market', 'after close')
    ev = {'id': f'corp:earn:{t}:{date}', 'cat': 'corp', 'kind': 'earn', 'tk': t, 'date': date, 'time': when or '',
          'title': f"{t} earnings" + (f" — {fp}" if fp else ''), 'src': src, 'imp': 3 if c.get('market_cap', 0) and c['market_cap'] > 2e11 else 2,
          'est': est, 'metrics': ([{'l': 'EPS', 'c': eps_est, 'a': '', 'p': ''}] if eps_est else [])}
    # past prints: pull actuals from the earnings rail if present
    for r in data.get('earnings_reports', []):
        if r['tk'] == t and r['d'] == date:
            ev['metrics'] = [{'l': 'EPS', 'c': r.get('eps_est'), 'a': r.get('eps_act'), 'p': ''},
                             {'l': 'Revenue ($M)', 'c': r.get('rev_est'), 'a': r.get('rev_act'), 'p': ''}]
            ev['note'] = r.get('note', ''); ev['rx'] = r.get('rx')
    add(ev)

# 2b. corporate — recent prints from the earnings rail (actuals)
seen={e['id'] for e in events}
for r in data.get('earnings_reports', []):
    d = D(r['d'])
    if not (TODAY - dt.timedelta(days=LOOKBACK) <= d <= TODAY): continue
    eid = f"corp:earn:{r['tk']}:{r['d']}"
    if eid in seen: continue
    ev = {'id': eid, 'cat': 'corp', 'kind': 'earn', 'tk': r['tk'], 'date': r['d'], 'time': r.get('when',''),
          'title': f"{r['tk']} earnings — {r.get('fp','')}", 'src': 'company report', 'imp': 3, 'est': False,
          'metrics': [{'l':'EPS','c':r.get('eps_est'),'a':r.get('eps_act'),'p':''},{'l':'Revenue ($M)','c':r.get('rev_est'),'a':r.get('rev_act'),'p':''}],
          'note': r.get('note',''), 'rx': r.get('rx')}
    add(ev)

# 3. corporate — curated IR / product events
for x in sched.get('corp_extra', []):
    d = D(x['date'])
    if not (TODAY - dt.timedelta(days=LOOKBACK) <= d <= TODAY + dt.timedelta(days=CORP_AHEAD)): continue
    ev = dict(x); ev.update({'id': f"corp:{x['kind']}:{x['tk']}:{x['date']}", 'cat': 'corp', 'est': x.get('est', False)})
    add(ev)

events.sort(key=lambda e: (e['date'], -e['imp'], e['title']))
data['events'] = events
data['events_meta'] = {'built': dt.datetime.utcnow().strftime('%Y-%m-%dT%H:%MZ'), 'window': f"{(TODAY-dt.timedelta(days=LOOKBACK)).isoformat()} → {(TODAY+dt.timedelta(days=CORP_AHEAD)).isoformat()}",
                       'sources': 'Fed · BLS · BEA · BoJ · ECB · Eurostat · Stat. Bureau of Japan · Alpha Vantage & Stocklake earnings calendars · company IR pages'}
json.dump(data, open('dashboard_data_v3.json', 'w'), separators=(',', ':'), ensure_ascii=False)
print(f"events: {len(events)} (macro {sum(e['cat']!='corp' for e in events)}, corp {sum(e['cat']=='corp' for e in events)}); with actuals {sum(e['has_actual'] for e in events)}")
for e in events: print(f"  {e['date']} {e['cat']:4s} {'est' if e['est'] else '   '} {e['title'][:60]}  {'✓act' if e['has_actual'] else ''}")
