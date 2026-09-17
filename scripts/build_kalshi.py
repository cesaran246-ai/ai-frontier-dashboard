#!/usr/bin/env python3
"""Turn kalshi.json (compact Kalshi quotes) into:
  * data['kalshi']  — the Prediction Markets section (Fed path curve, macro ladders, BoJ decisions, recession, IPO tracker)
  * ev['k'] on matching calendar events — a one-line 'Kalshi implied' strip + mini distribution
Run AFTER build_events.py and BEFORE build_html_v3.py. Never touches other keys.
"""
import json, datetime as dt

K = json.load(open('kalshi.json'))
data = json.load(open('dashboard_data_v3.json'))

def monotone(p_above):
    """cumulative P(x > strike) must be non-increasing in strike; enforce with a running min."""
    items = sorted(((float(k), v) for k, v in p_above.items()))
    out, m = [], 1.0
    for s, p in items:
        m = min(m, p); out.append((s, m))
    return out

def distribution(p_above, step):
    """bucket probabilities from cumulative P(>strike). Buckets: (-inf, s0], (s0,s1], … (sn, inf)."""
    cum = monotone(p_above)
    buckets = []
    prev = 1.0
    for i, (s, p) in enumerate(cum):
        lo = cum[i-1][0] if i else None
        buckets.append({'lo': lo, 'hi': s, 'p': round(max(0.0, prev - p), 3)})
        prev = p
    buckets.append({'lo': cum[-1][0], 'hi': None, 'p': round(max(0.0, prev), 3)})
    return buckets

def fmt(v, unit, step):
    if v is None: return ''
    if unit == 'K':   # strikes are raw jobs (25000 = 25K)
        k = v / 1000.0
        return f"{k:+.0f}K" if k < 0 else f"{k:.0f}K"
    d = 2 if abs(step-0.25) < 1e-9 else (1 if step < 1 else 0)   # Fed ladders (step 0.25) need two decimals: 3.75 / 4.00
    return f"{v:.{d}f}%"

def bucket_label(b, unit, step):
    if b['lo'] is None: return f"≤ {fmt(b['hi'], unit, step)}"
    if b['hi'] is None: return f"> {fmt(b['lo'], unit, step)}"
    if abs(b['hi'] - b['lo'] - step) < 1e-9: return fmt(b['hi'], unit, step)   # single print value
    if unit == 'K':   # compact range: 60–70K (one suffix)
        lo, hi = fmt(b['lo'], unit, step), fmt(b['hi'], unit, step)
        return f"{lo[:-1]}–{hi}" if b['lo'] >= 0 else f"{lo}–{hi}"
    return f"{fmt(b['lo'], unit, step)}–{fmt(b['hi'], unit, step)}"

def mode_and_median(buckets, unit, step):
    mode = max(buckets, key=lambda b: b['p'])
    acc, med = 0.0, None
    for b in buckets:
        acc += b['p']
        if acc >= 0.5: med = b; break
    return bucket_label(mode, unit, step), bucket_label(med, unit, step) if med else ''

# ---------- Fed path ----------
LEVELS = [3.25, 3.50, 3.75, 4.00, 4.25, 4.50]
fed_out = []
cur = K['fed']['cur_upper']
for m in K['fed']['meetings']:
    if m.get('settled'): continue   # settled meetings live in the Settled tab (block a2 below)
    cum = dict(monotone(m['p_above']))
    # P(upper bound == L) = P(> L-0.25) - P(> L)
    probs = {}
    for L in LEVELS:
        p_gt_prev = cum.get(L - 0.25, 1.0 if L - 0.25 < min(cum) else None)
        if p_gt_prev is None: p_gt_prev = 1.0
        p_gt = cum.get(L, 0.0)
        probs[f"{L:.2f}"] = round(max(0.0, p_gt_prev - p_gt), 3)
    # tail below lowest level
    probs[f"≤{min(LEVELS)-0.25:.2f}"] = round(max(0.0, 1 - cum.get(min(LEVELS) - 0.25, 1.0)), 3) if (min(LEVELS)-0.25) in cum else 0.0
    exp = sum(float(k) * p for k, p in probs.items() if not k.startswith('≤'))
    p_hike = sum(p for k, p in probs.items() if not k.startswith('≤') and float(k) > cur)
    p_cut = sum(p for k, p in probs.items() if k.startswith('≤') or float(k) < cur)
    p_hold = probs.get(f"{cur:.2f}", 0.0)
    fed_out.append({'ev': m['ev'], 'date': m['date'], 'label': m['label'], 'probs': probs, 'exp_upper': round(exp, 3),
                    'p_hike': round(p_hike, 3), 'p_hold': round(p_hold, 3), 'p_cut': round(p_cut, 3), 'vol': m.get('vol')})

# ---------- settled-markets database (Cesar, Sep 13): anything that settles leaves the live PM section and lands in K['settled'] ----------
SETTLED = K.setdefault('settled', [])
def _put(rec):
    """idempotent upsert by id; keeps the first `archived` date"""
    for i, r in enumerate(SETTLED):
        if r['id'] == rec['id']:
            rec['archived'] = r.get('archived', K['asof'][:10]); SETTLED[i] = rec; return
    rec.setdefault('archived', K['asof'][:10]); SETTLED.append(rec)
def _hist_for(h, k=None):
    return [{'d': x['d'], 'p': x['p']} for x in (h or []) if k is None or str(x.get('k')) == str(k)]
# (a) macro ladders carrying a `settled` note → archive with their final book, then drop from the live ladders
for eid in [e for e, L in K['ladders'].items() if L.get('settled')]:
    L = K['ladders'].pop(eid)
    pa = L.get('pre_print') or L['p_above']   # pre_print = the book captured at the last run BEFORE the release (5pm run the day before)
    b = distribution(pa, L['step']); mode, med = mode_and_median(b, L['unit'], L['step'])
    act = L.get('actual')
    _put({'id': f'ladder:{eid}:{L["ev"]}', 'cat': 'macro', 'kind': 'ladder', 'title': L['name'], 'ev': L['ev'], 'question': f"{L['metric']} — Kalshi strike ladder",
          'period': eid.split(':')[2], 'settled_on': L.get('settled_on') or eid.split(':')[2], 'status': 'settled',
          'final': {'label': 'mode / median before the print', 'text': f"{mode} / {med}"}, 'mode': mode, 'median': med, 'actual': act,
          'hit': (None if act is None else (str(act) == str(mode))), 'ladder': [[s_, round(p_, 3)] for s_, p_ in monotone(pa)],
          'buckets': [{'label': bucket_label(x, L['unit'], L['step']), 'p': x['p']} for x in b], 'vol': L.get('vol'), 'outcome': L['settled'], 'event_id': eid.split(':core')[0]})
# (a2) Fed meetings carrying a `settled` note (Sep 16: KXFED-26SEP) → archive the pre_print book (Tue 5pm close) scored against the actual upper bound
for M_ in [m for m in K['fed']['meetings'] if m.get('settled')]:
    pa = M_.get('pre_print') or M_['p_above']
    b = distribution(pa, 0.25); mode, med = mode_and_median(b, '%', 0.25)
    act = M_.get('actual')
    act_up = None
    if act:
        import re as _re
        nums = _re.findall(r'\d+\.\d+', str(act)); act_up = f"{float(nums[-1]):.2f}" if nums else None
    mode_up = None
    try:
        # mode is a bucket label like '3.75–4.00' or '≤3.00'; the upper bound is its last number
        import re as _re
        nums = _re.findall(r'\d+\.\d+', str(mode)); mode_up = f"{float(nums[-1]):.2f}" if nums else None
    except Exception: pass
    _put({'id': f"fed:{M_['ev']}", 'cat': 'macro', 'kind': 'ladder', 'title': f"Fed funds — {M_.get('label', M_['ev'])} meeting", 'ev': M_['ev'],
          'question': 'Upper bound of the fed funds target range after the meeting — Kalshi strike ladder',
          'period': M_.get('date', ''), 'settled_on': M_.get('settled_on') or M_.get('date', ''), 'status': 'settled',
          'final': {'label': 'mode / median before the decision (pre_print = Tue 5pm close book)', 'text': f"{mode} / {med}"}, 'mode': mode, 'median': med, 'actual': act,
          'hit': (None if (act_up is None or mode_up is None) else (act_up == mode_up)), 'ladder': [[s_, round(p_, 3)] for s_, p_ in monotone(pa)],
          'buckets': [{'label': bucket_label(x, '%', 0.25), 'p': x['p']} for x in b], 'vol': M_.get('vol'), 'outcome': M_['settled'], 'event_id': f"us:fomc:{M_.get('date','')}"})
# (b) ERCOT daily peaks (energy.archive) — the run appends an entry when the day's event finalizes
for a in K.get('energy', {}).get('archive', []):
    lad_ = [[s_, round(p_, 3)] for s_, p_ in monotone(a['p_above'])] if a.get('p_above') else None
    hit_ = None
    if lad_ and a.get('lo') is not None and a.get('hi') is not None and len(lad_) > 1:
        # mode bucket = the 1,000-MW step where the cumulative curve drops the most; hit if it matches the settled bucket
        drops = [(lad_[i][1] - lad_[i+1][1], lad_[i][0], lad_[i+1][0]) for i in range(len(lad_)-1)]
        _, mlo, mhi = max(drops)
        hit_ = (float(mlo) == float(a['lo']) and float(mhi) == float(a['hi']))
    _put({'id': f"energy:{a['ev']}", 'cat': 'energy', 'kind': 'daily_peak', 'title': f"ERCOT peak load — {a['date']}", 'ev': a['ev'], 'question': 'Highest hourly ERCOT system load on the day (MW)',
          'period': a['date'], 'settled_on': a.get('settled_on'), 'status': 'settled' if a.get('result') else 'pending',
          'final': a.get('final_read'), 'actual': a.get('result'), 'hit': hit_, 'ladder': lad_, 'vol': a.get('vol'), 'outcome': a.get('note', '')})
# (c) Hormuz weekly books (hormuz.archive) — pending until PortWatch settles them
for a in K.get('hormuz', {}).get('archive', []):
    ks = a.get('hist_strike', 25); res = a.get('result')
    hit = None if res is None else ((res == 'yes') == (a.get('p25_final', 0) >= 0.5))
    lad_ = [[s_, round(p_, 3)] for s_, p_ in monotone(a['p_above'])] if a.get('p_above') else None
    _put({'id': f"hormuz:{a['ev']}", 'cat': 'hormuz', 'kind': 'weekly', 'title': f"Hormuz transits — {a['range']}", 'ev': a['ev'], 'question': f'Weekly transit calls through the Strait (IMF PortWatch) — tracked strike >{ks}',
          'period': a['range'], 'settled_on': a.get('settled_on'), 'status': 'settled' if res else 'pending', 'closes': a.get('closes'),
          'final': {'label': f"P(>{ks}) at the last read", 'p': a.get('p25_final')}, 'actual': (None if res is None else f"'>{ks}' settled {res.upper()}"), 'hit': hit,
          'ladder': lad_, 'vol': a.get('vol'), 'outcome': a.get('note', ''), 'history': _hist_for(K.get('hormuz', {}).get('history', {}).get('weekly'), None) and [x for x in K['hormuz']['history']['weekly'] if x.get('ev') == a['ev']]})
# (d) company markets: settled KPI markets, rolled priors, the earnings-call books, US-stake legs
for tk, blk in K.get('stock_pm', {}).items():
    if tk.startswith('_'): continue
    for M in blk.get('markets', []):
        if M.get('settled') and M['key'] != 'usstake':
            _put({'id': f"spm:{tk}:{M['key']}:{M['ev']}", 'cat': 'company', 'kind': 'kpi', 'tk': tk, 'title': f"{tk} · {M.get('title', M.get('short'))}", 'ev': M['ev'], 'question': M.get('title', ''),
                  'period': M.get('period') or M.get('horizon', ''), 'settled_on': M['settled'].get('d'), 'status': 'settled',
                  'final': {'label': f"last read for {M.get('hist_strike')}", 'p': (M['history'][-1]['p'] if M.get('history') else None)}, 'actual': f"settled {M['settled'].get('outcome', 'yes').upper()}", 'hit': None,
                  'ladder': None, 'vol': M.get('vol'), 'outcome': M['settled'].get('note', ''), 'history': _hist_for(M.get('history'))})
        for q in M.get('prior', []) or []:
            _put({'id': f"spm:{tk}:{M['key']}:{q['ev']}", 'cat': 'company', 'kind': 'kpi', 'tk': tk, 'title': f"{tk} · {M.get('short')} — {q.get('period', '')}", 'ev': q['ev'], 'question': M.get('title', ''),
                  'period': q.get('period', ''), 'settled_on': q.get('d'), 'status': 'settled', 'final': {'label': f"last read for {q.get('hist_strike')}", 'p': q.get('last_p')},
                  'actual': (f"actual {q['actual']}" if q.get('actual') is not None else None), 'hit': None, 'ladder': None, 'vol': None, 'outcome': q.get('note', ''), 'history': []})
    C_ = blk.get('call')
    if C_ and C_.get('settled') and C_.get('prior'):
        n_yes = sum(1 for r in C_['prior'] if r['outcome'] == 'yes'); calls = [(r['p_precall'] >= 0.5) == (r['outcome'] == 'yes') for r in C_['prior'] if r.get('p_precall') is not None]
        _put({'id': f"call:{tk}:{C_['prior'][0]['ev']}", 'cat': 'company', 'kind': 'call', 'tk': tk, 'title': f"{tk} earnings-call mentions — {C_['prior'][0].get('fp', '')}", 'ev': C_['prior'][0]['ev'],
              'question': f"Which topics {tk} management says on the call (Kalshi mention markets, {len(C_['prior'])} topics)", 'period': C_['prior'][0].get('fp', ''), 'settled_on': C_['settled'], 'status': 'settled',
              'final': {'label': 'pre-call book', 'text': f"{sum(1 for r in C_['prior'] if r['p_precall'] >= 0.5)} topics priced > 50%"}, 'actual': f"{n_yes} of {len(C_['prior'])} said",
              'hit': (sum(calls) / len(calls)) if calls else None, 'hit_label': f"{sum(calls)}/{len(calls)} topics called correctly" if calls else None,
              'ladder': None, 'vol': None, 'outcome': C_.get('note', ''), 'rows': [{'label': r['label'], 'outcome': r['outcome'], 'p_precall': r.get('p_precall'), 'p_final': r.get('p_final')} for r in C_['prior']]})
US_ = K.get('usstake')
if US_:
    for leg in US_.get('legs', []):
        if leg.get('settled'):
            _put({'id': f"stake:{leg['k']}", 'cat': 'company', 'kind': 'leg', 'tk': leg.get('tk'), 'title': f"US stake in {leg['label']}", 'ev': f"{US_['ev']}-{leg['k']}", 'question': 'Will the US government take a stake in the company in 2026?',
                  'period': '2026', 'settled_on': leg['settled'].get('d'), 'status': 'settled', 'final': {'label': 'first read', 'p': (leg['history'][0]['p'] if leg.get('history') else None)},
                  'actual': f"settled {leg['settled'].get('outcome', 'yes').upper()}", 'hit': None, 'ladder': None, 'vol': leg.get('vol'), 'outcome': leg['settled'].get('note', ''), 'history': _hist_for(leg.get('history'))})
SETTLED.sort(key=lambda r: (r['status'] != 'pending', r.get('settled_on') or r.get('archived') or ''), reverse=True)
settled_out = SETTLED
print(f"settled db: {len(SETTLED)} records ({sum(1 for r in SETTLED if r['status']=='pending')} pending)")

# ---------- ladders ----------
lad_out = {}
for eid, L in K['ladders'].items():
    b = distribution(L['p_above'], L['step'])
    mode, med = mode_and_median(b, L['unit'], L['step'])
    cum = monotone(L['p_above'])
    lad_out[eid] = {'name': L['name'], 'metric': L['metric'], 'unit': L['unit'], 'ev': L['ev'], 'vol': L.get('vol'),
                    'buckets': [{'label': bucket_label(x, L['unit'], L['step']), 'p': x['p']} for x in b],
                    'cum': [[s, p] for s, p in cum], 'mode': mode, 'median': med, 'settled': L.get('settled')}

# ---------- attach to calendar events ----------
E = data.get('events', [])
byid = {e['id']: e for e in E}
def strip_line(parts): return ' · '.join(parts)
# Fed
for f in fed_out:
    eid = f"us:fomc:{f['date']}"
    if eid in byid:
        byid[eid]['k'] = {'src': 'Kalshi ' + f['ev'], 'line': strip_line([f"hike {f['p_hike']*100:.0f}%", f"hold {f['p_hold']*100:.0f}%", f"cut {f['p_cut']*100:.0f}%"]) + f" · expected upper bound {f['exp_upper']:.2f}%",
                          'bars': [[k, v] for k, v in f['probs'].items() if not k.startswith('≤')], 'vol': f['vol']}
# settled ladders keep a short strip on their (past) calendar event
for r in SETTLED:
    if r['kind'] == 'ladder' and r.get('event_id') in byid and r.get('buckets'):
        ev = byid[r['event_id']]; top = sorted(r['buckets'], key=lambda x: -x['p'])[:3]
        line = f"{r['title']}: mode {r['mode']} · " + strip_line([f"{x['label']} {x['p']*100:.0f}%" for x in sorted(top, key=lambda x: r['buckets'].index(x))]) + " · settled"
        if ev.get('k'):
            if line not in ev['k']['line']: ev['k']['line'] += ' | ' + line   # idempotent: a 2nd build_kalshi in the same session must not duplicate the strip
        else: ev['k'] = {'src': 'Kalshi ' + r['ev'], 'line': line, 'bars': [], 'vol': r.get('vol')}
# ladders
for eid, L in lad_out.items():
    base = eid.split(':core')[0]
    if base in byid:
        ev = byid[base]
        top = sorted(L['buckets'], key=lambda x: -x['p'])[:3]
        line = f"{L['metric']}: mode {L['mode']} · " + strip_line([f"{x['label']} {x['p']*100:.0f}%" for x in sorted(top, key=lambda x: L['buckets'].index(x))])
        k = ev.setdefault('k', {'src': 'Kalshi ' + L['ev'], 'line': '', 'bars': [], 'vol': L.get('vol')})
        if line not in k['line']: k['line'] = (k['line'] + ' | ' if k['line'] else '') + line   # idempotent (see note above)
        if not k['bars']: k['bars'] = [[x['label'], x['p']] for x in L['buckets'] if x['p'] >= 0.02]
# decisions
for eid, Dc in K['decisions'].items():
    if eid in byid:
        opts = sorted(Dc['opts'].items(), key=lambda x: -x[1])
        byid[eid]['k'] = {'src': 'Kalshi ' + Dc['ev'], 'line': strip_line([f"{o} {p*100:.0f}%" for o, p in opts if p >= 0.01]),
                          'bars': [[o, p] for o, p in opts], 'vol': Dc.get('vol')}

# ---------- IPO tracker ----------
ipo = K['ipo']
def cum_points(pts):
    out, m = [], 0.0
    for d, p in pts:
        m = max(m, p); out.append([d, round(m, 3)])
    return out
ipo_out = {
    'anthropic': dict(ipo['anthropic'], points=cum_points(ipo['anthropic']['points'])),
    'openai': dict(ipo['openai'], points=cum_points(ipo['openai']['points'])),
    'anduril': dict(ipo['anduril'], points=cum_points(ipo['anduril']['points'])) if 'anduril' in ipo else None,
    'databricks': dict(ipo['databricks'], points=cum_points(ipo['databricks']['points'])) if 'databricks' in ipo else None,
    'first': ipo['first'], 'leadleft_anthropic': ipo['leadleft_anthropic'], 'valuations': ipo.get('valuations', {}),
}
def by_date(pts, d):
    v = 0.0
    for x, p in pts:
        if x <= d: v = p
    return v
ipo_out['summary'] = {
    'anthropic_by_year_end': by_date(ipo_out['anthropic']['points'], '2027-01-01'),
    'openai_by_year_end': by_date(ipo_out['openai']['points'], '2027-01-01'),
    'anthropic_by_nov1': by_date(ipo_out['anthropic']['points'], '2026-11-01'),
    'anduril_by_mid2027': by_date(ipo_out['anduril']['points'], '2027-06-01') if ipo_out.get('anduril') else None,
    'anduril_by_year_end': by_date(ipo_out['anduril']['points'], '2027-01-01') if ipo_out.get('anduril') else None,
    'databricks_by_mid2027': by_date(ipo_out['databricks']['points'], '2027-06-01') if ipo_out.get('databricks') else None,
    'databricks_by_end2027': by_date(ipo_out['databricks']['points'], '2028-01-01') if ipo_out.get('databricks') else None,
}

# ---------- market-tile price expectations (S&P, Dow, BTC, ETH, Brent, Gold, Silver) ----------
def quantile_from_cum(cum, q):
    """cum: sorted [(strike, P(>strike))] non-increasing. Return x with P(>x)=q by linear interpolation.
    Returns (value, flag) flag='' | '≤' (below lowest strike) | '≥' (above highest strike)."""
    if not cum: return None, ''
    if q >= cum[0][1]: return cum[0][0], '≤'
    if q <= cum[-1][1]: return cum[-1][0], '≥'
    for (s0, p0), (s1, p1) in zip(cum, cum[1:]):
        if p1 <= q <= p0:
            if p0 == p1: return s1, ''
            return s0 + (s1 - s0) * (p0 - q) / (p0 - p1), ''
    return None, ''

def level_at(ladder, q, increasing_strike_decreasing_p=True):
    """ladder: {strike: p}. Find strike where p crosses q (linear)."""
    items = sorted(((float(k), v) for k, v in ladder.items()), key=lambda x: x[0])
    if not increasing_strike_decreasing_p: items = items[::-1]      # for 'lo': P(low<=s) increases with s; walk from high strike down
    # make monotone non-increasing in the walking order
    out, m = [], 1.0
    for s, p in items:
        m = min(m, p); out.append((s, m))
    return quantile_from_cum(out, q)

assets_out = {}
for key, A in K.get('assets', {}).items():
    if key.startswith('_'): continue
    o = {'name': A['name'], 'type': A['type'], 'horizon': A['horizon'], 'unit': A['unit'], 'vol': A.get('vol'), 'note': A.get('note', ''), 'no_spot': A.get('no_spot', False),
         'ev': A.get('ev') or f"{A.get('hi_ev','')} / {A.get('lo_ev','')}"}
    if A['type'] in ('cum', 'range'):
        if A['type'] == 'cum':
            cum = monotone(A['p_above'])
            b = distribution(A['p_above'], 0)
            o['buckets'] = [{'lo': x['lo'], 'hi': x['hi'], 'p': x['p']} for x in b]
        else:
            # buckets [lo,hi,p] → cumulative P(> hi)
            bk = A['buckets']; tot = sum(x[2] for x in bk) or 1.0
            o['buckets'] = [{'lo': x[0], 'hi': x[1], 'p': round(x[2] / tot, 3)} for x in bk]
            cum, acc = [], 1.0
            for lo, hi, p in bk:
                if hi is None: break
                acc -= p / tot; cum.append((float(hi), max(0.0, acc)))
        o['cum'] = [[s, round(p, 3)] for s, p in cum]
        lo, lf = quantile_from_cum(cum, 0.9); md, mf = quantile_from_cum(cum, 0.5); hi, hf = quantile_from_cum(cum, 0.1)
        o['p10'], o['p50'], o['p90'] = [round(lo), lf], [round(md), mf], [round(hi), hf]
        inner = [x for x in o['buckets'] if x['lo'] is not None and x['hi'] is not None] or o['buckets']
        mode = max(inner, key=lambda x: x['p']); o['mode'] = [mode['lo'], mode['hi'], mode['p']]
    else:
        if 'hi' in A:
            hi50, hf = level_at(A['hi'], 0.5); hi25, _ = level_at(A['hi'], 0.25); hi10, _ = level_at(A['hi'], 0.10)
            o['hi'] = {'ladder': sorted(([float(k), v] for k, v in A['hi'].items()), key=lambda x: x[0]), 'p50': [round(hi50), hf], 'p25': round(hi25), 'p10': round(hi10)}
        if 'lo' in A:
            lo50, lf = level_at(A['lo'], 0.5, False); lo25, _ = level_at(A['lo'], 0.25, False); lo10, _ = level_at(A['lo'], 0.10, False)
            flip = {'≤': '≥', '≥': '≤', '': ''}
            o['lo'] = {'ladder': sorted(([float(k), v] for k, v in A['lo'].items()), key=lambda x: -x[0]), 'p50': [round(lo50), flip[lf]], 'p25': round(lo25), 'p10': round(lo10)}
        # implied "stays inside" band from the innermost listed strikes
        if 'hi' in A and 'lo' in A:
            hs, hp = o['hi']['ladder'][0]; ls, lp = o['lo']['ladder'][0]
            o['band'] = {'lo': ls, 'p_lo': lp, 'hi': hs, 'p_hi': hp, 'p_within': round(max(0.0, 1 - lp - hp), 3)}
    assets_out[key] = o

# ---------- Texas energy (ERCOT peak load year + daily, Texas crude production) ----------
energy_out = {}
for key, Eg in K.get('energy', {}).items():
    if key.startswith('_') or key == 'archive': continue
    cum = monotone(Eg['p_above'])
    lo, lf = quantile_from_cum(cum, 0.9); md, mf = quantile_from_cum(cum, 0.5); hi, hf = quantile_from_cum(cum, 0.1)
    step = 0.1 if Eg['unit'] == 'mb/d' else 1000
    b = distribution(Eg['p_above'], step)
    energy_out[key] = dict({k: v for k, v in Eg.items() if k not in ('p_above', 'tickers')},
                           ladder=[[s, round(p, 3)] for s, p in cum],
                           buckets=[{'lo': x['lo'], 'hi': x['hi'], 'p': x['p']} for x in b],
                           p10=[lo, lf], p50=[md, mf], p90=[hi, hf])

# ---------- Strait of Hormuz shipping (weekly, month max, year avg) + self-appending history ----------
hormuz_out = None
HZ = K.get('hormuz')
if HZ:
    asof_day = K['asof'][:10]
    hist = HZ.setdefault('history', {'weekly': [], 'month_max': [], 'year_avg': []})
    def lad(p):  # {strike: p} -> monotone cumulative
        return monotone(p)
    def pack(key, M, pkey):
        cum = lad(M[pkey])
        lo, lf = quantile_from_cum(cum, 0.9); md, mf = quantile_from_cum(cum, 0.5); hi, hf = quantile_from_cum(cum, 0.1)
        ks = M['hist_strike']; live = M[pkey].get(str(ks))
        if live is not None:  # append/replace today's point
            h = hist.setdefault(key, [])
            h[:] = [x for x in h if not (x['d'] == asof_day and x['ev'] == M['ev'])]
            pt = {'d': asof_day, 'p': round(live, 3), 'ev': M['ev'], 'k': ks}
            if M.get('range'): pt['lbl'] = M['range'].replace(', 2026', '')
            h.append(pt); h.sort(key=lambda x: x['d'])
        return dict({k: v for k, v in M.items() if k not in (pkey,)}, ladder=[[s, round(p, 3)] for s, p in cum],
                    p10=[lo, lf], p50=[md, mf], p90=[hi, hf], kind='atleast' if pkey == 'p_atleast' else 'above')
    normal_out = None
    if HZ.get('normal'):
        N = HZ['normal']; pts = cum_points(N['points'])
        ks = N['hist_strike']; live = dict(N['points']).get(ks)
        if live is not None:
            h = hist.setdefault('normal', [])
            h[:] = [x for x in h if not (x['d'] == asof_day and x['ev'] == N['ev'])]
            h.append({'d': asof_day, 'p': round(live, 3), 'ev': N['ev'], 'k': ks}); h.sort(key=lambda x: x['d'])
        # date at which cumulative probability crosses 50% (linear between listed dates)
        med = None
        for (d0, p0), (d1, p1) in zip(pts, pts[1:]):
            if p0 < 0.5 <= p1:
                t0, t1 = dt.date.fromisoformat(d0), dt.date.fromisoformat(d1)
                med = (t0 + dt.timedelta(days=round((t1 - t0).days * (0.5 - p0) / max(1e-9, p1 - p0)))).isoformat(); break
        normal_out = dict({k: v for k, v in N.items() if k != 'tickers'}, points=pts, median_date=med,
                          by={'2027-01-01': by_date(pts, '2027-01-01'), '2027-07-01': by_date(pts, '2027-07-01'), '2029-01-01': by_date(pts, '2029-01-01')})
    hormuz_out = {'weekly': pack('weekly', HZ['weekly'], 'p_above'), 'month_max': pack('month_max', HZ['month_max'], 'p_atleast'),
                  'year_avg': pack('year_avg', HZ['year_avg'], 'p_above'), 'normal': normal_out, 'history': hist, 'note': HZ.get('_note', '')}
    json.dump(K, open('kalshi.json', 'w'), indent=1, ensure_ascii=False)   # persist the appended history

# ---------- stock-linked prediction markets (keyed by ticker; reusable for any tracked name) ----------
stock_pm_out = {}
SPM = K.get('stock_pm', {})
for tk, block in SPM.items():
    if tk.startswith('_'): continue
    asof_day = K['asof'][:10]
    mk_out = []
    for M in block.get('markets', []):
        if M.get('kind') == 'date':
            pts = cum_points(M['points'])
            live = dict(pts).get(M['hist_strike'])
            if M.get('settled'):
                live = 1.0 if M['settled'].get('outcome') == 'yes' else 0.0   # frozen: no new history points after settlement
            elif live is not None:
                h = M.setdefault('history', [])
                h[:] = [x for x in h if not (x['d'] == asof_day and x['ev'] == M['ev'])]
                h.append({'d': asof_day, 'p': round(live, 3), 'ev': M['ev'], 'k': M['hist_strike']}); h.sort(key=lambda x: x['d'])
                if M.get('track_all'):   # multi-threshold curves (e.g. "useful quantum computer before 2027/2030/2035/2040"): one line per threshold
                    ha = M.setdefault('history_all', [])
                    ha[:] = [x for x in ha if not (x['d'] == asof_day and x['ev'] == M['ev'])]
                    for d_, p_ in pts: ha.append({'d': asof_day, 'p': round(p_, 3), 'ev': M['ev'], 'k': d_})
                    ha.sort(key=lambda x: (x['d'], x['k']))
            med = None
            for (d0, p0), (d1, p1) in zip(pts, pts[1:]):
                if p0 < 0.5 <= p1:
                    t0, t1 = dt.date.fromisoformat(d0), dt.date.fromisoformat(d1)
                    med = (t0 + dt.timedelta(days=round((t1 - t0).days * (0.5 - p0) / max(1e-9, p1 - p0)))).isoformat(); break
            q25 = None
            for (d0, p0), (d1, p1) in zip(pts, pts[1:]):
                if p0 < 0.25 <= p1:
                    t0, t1 = dt.date.fromisoformat(d0), dt.date.fromisoformat(d1)
                    q25 = (t0 + dt.timedelta(days=round((t1 - t0).days * (0.25 - p0) / max(1e-9, p1 - p0)))).isoformat(); break
            mk_out.append(dict({k: v for k, v in M.items() if k not in ('points', 'tickers')},
                               ladder=[[d, round(p, 3)] for d, p in pts], p50=[med, 'date'], p25=[q25, 'date'],
                               p75=[None, 'date'], p_at=(round(live, 3) if live is not None else None), median_date=med))
            continue
        cum = monotone(M['p_above'])
        hi50, hf = quantile_from_cum(cum, 0.5); hi25, _f25 = quantile_from_cum(cum, 0.25); hi75, _ = quantile_from_cum(cum, 0.75)
        ks = str(M['hist_strike']); live = M['p_above'].get(ks)
        if live is not None and not M.get('settled'):
            h = M.setdefault('history', [])
            h[:] = [x for x in h if not (x['d'] == asof_day and x['ev'] == M['ev'])]
            h.append({'d': asof_day, 'p': round(live, 3), 'ev': M['ev'], 'k': ks}); h.sort(key=lambda x: x['d'])
        mk_out.append(dict({k: v for k, v in M.items() if k not in ('p_above', 'tickers')},
                           ladder=[[s, round(p, 3)] for s, p in cum], p50=[hi50, hf], p25=[hi25, _f25], p75=[hi75, '']))
    call_out = None
    CALL = block.get('call')
    if CALL and CALL.get('items'):
        for it in CALL['items']:
            h = it.setdefault('history', [])
            h[:] = [x for x in h if x['d'] != asof_day]
            h.append({'d': asof_day, 'p': round(it['p'], 3)}); h.sort(key=lambda x: x['d'])
        items_out = sorted(CALL['items'], key=lambda i: -i['p'])
        call_out = dict(CALL, items=[dict(i, first=(i['history'][0]['p'] if i['history'] else i['p']), first_d=(i['history'][0]['d'] if i['history'] else asof_day)) for i in items_out])
    stock_pm_out[tk] = dict({k: v for k, v in block.items() if k not in ('markets', 'call')}, markets=mk_out, **({'call': call_out} if call_out else {}))
# ---------- standalone cards: quantum timing (from stock_pm.IONQ.useful_qc) + US-stake board (top-level `usstake`) ----------
quantum_out = next((m for m in stock_pm_out.get('IONQ', {}).get('markets', []) if m['key'] == 'useful_qc'), None)
usstake_out = None
US = K.get('usstake')
if US and US.get('legs'):
    asof_day = K['asof'][:10]
    for leg in US['legs']:
        h = leg.setdefault('history', [])
        if not leg.get('settled'):
            h[:] = [x for x in h if x['d'] != asof_day]
            h.append({'d': asof_day, 'p': round(leg['p'], 3)}); h.sort(key=lambda x: x['d'])
    legs_out = sorted(US['legs'], key=lambda l: (-(1.5 if l.get('settled') else l['p']), l['label']))
    usstake_out = dict(US, legs=[dict(l, first=(l['history'][0]['p'] if l['history'] else l['p']), first_d=(l['history'][0]['d'] if l['history'] else asof_day)) for l in legs_out],
                       n_settled=sum(1 for l in US['legs'] if l.get('settled')), list_tickers=[l['tk'] for l in legs_out if l.get('tk')])
# ---------- standalone macro card: how high will CPI y/y get this year (KXHIGHINFLATION-26DEC) ----------
cpimax_out = None
CM = K.get('cpimax')
if CM and CM.get('p_above'):
    asof_day = K['asof'][:10]
    cum = monotone(CM['p_above'])
    hi50, hf = quantile_from_cum(cum, 0.5); hi25, f25 = quantile_from_cum(cum, 0.25); hi75, f75 = quantile_from_cum(cum, 0.75)
    ha = CM.setdefault('history_all', [])
    ha[:] = [x for x in ha if not (x['d'] == asof_day and x['ev'] == CM['ev'])]
    for k in CM.get('track', [CM['hist_strike']]):
        if CM['p_above'].get(k) is not None: ha.append({'d': asof_day, 'p': round(CM['p_above'][k], 3), 'ev': CM['ev'], 'k': k})
    ha.sort(key=lambda x: (x['d'], x['k']))
    live = CM['p_above'].get(str(CM['hist_strike']))
    cpimax_out = dict({k: v for k, v in CM.items() if k != 'p_above'}, ladder=[[s, round(p, 3)] for s, p in cum],
                      p50=[hi50, hf], p25=[hi25, f25], p75=[hi75, f75], p_at=(round(live, 3) if live is not None else None), kind='above',
                      history=[x for x in ha if x['k'] == str(CM['hist_strike'])])
json.dump(K, open('kalshi.json', 'w'), indent=1, ensure_ascii=False)   # persists settled db + histories
try:
    import roll_pm; print('  roll check (stock_pm):'); roll_pm.check(K)
except Exception as e: print('  roll check skipped:', e)

data['kalshi'] = {'asof': K['asof'], 'energy': energy_out, 'hormuz': hormuz_out, 'stock_pm': stock_pm_out, 'fed': {'cur_upper': cur, 'meetings': fed_out}, 'ladders': lad_out,
                  'decisions': K['decisions'], 'binary': K['binary'], 'ipo': ipo_out, 'assets': assets_out,
                  'quantum': quantum_out, 'usstake': usstake_out, 'cpimax': cpimax_out, 'settled': settled_out,
                  'note': 'Kalshi prices are the market-implied probability (yes mid). Read-only public market data; no account positions are shown.'}
data['events'] = E
json.dump(data, open('dashboard_data_v3.json', 'w'), separators=(',', ':'), ensure_ascii=False)
attached = [e['id'] for e in E if e.get('k')]
print(f"kalshi: {len(fed_out)} Fed meetings, {len(lad_out)} ladders, {len(K['decisions'])} decisions; attached to {len(attached)} events: {attached}")
for f in fed_out: print(f"  {f['label']}: hike {f['p_hike']:.2f} hold {f['p_hold']:.2f} cut {f['p_cut']:.2f} exp {f['exp_upper']:.2f}")
for eid, L in lad_out.items(): print(f"  {eid}: mode {L['mode']} median {L['median']} | " + ', '.join(f"{b['label']} {b['p']:.2f}" for b in L['buckets'] if b['p']>=0.03))
for k, a in assets_out.items():
    if a['type'] in ('cum', 'range'): print(f"  asset {k}: p10 {a['p10']} p50 {a['p50']} p90 {a['p90']} mode {a['mode']} ({a['horizon']})")
    else: print(f"  asset {k}: high50 {a.get('hi',{}).get('p50')} low50 {a.get('lo',{}).get('p50')} ({a['horizon']})")
for k, e in energy_out.items(): print(f"  energy {k}: p10 {e['p10']} p50 {e['p50']} p90 {e['p90']} ladder {e['ladder']}")
if hormuz_out:
    for k in ('weekly', 'month_max', 'year_avg'): print(f"  hormuz {k}: {hormuz_out[k]['ev']} p50 {hormuz_out[k]['p50']} p10 {hormuz_out[k]['p10']} p90 {hormuz_out[k]['p90']} hist {len(hormuz_out['history'].get(k, []))} pts")
    if hormuz_out.get('normal'): print(f"  hormuz normal: median date {hormuz_out['normal']['median_date']} by {hormuz_out['normal']['by']} hist {len(hormuz_out['history'].get('normal', []))} pts")
for tk, b in stock_pm_out.items():
    for m in b['markets']: print(f"  stock_pm {tk}/{m['key']}: {m['ev']} p50 {m['p50']} p25 {m['p25'][0]} hist {len(m.get('history', []))} pts")
    if b.get('call'): print(f"  stock_pm {tk}/call: {b['call']['ev']} {len(b['call']['items'])} topics, top {b['call']['items'][0]['label']} {b['call']['items'][0]['p']}")
if cpimax_out: print(f"  cpimax card: {cpimax_out['ev']} p50 {cpimax_out['p50']} tops {cpimax_out['hist_strike']} {cpimax_out['p_at']} lines {len(set(x['k'] for x in cpimax_out['history_all']))} pts {len(cpimax_out['history_all'])}")
if quantum_out: print(f"  quantum card: median {quantum_out['p50'][0]} by-2030 {quantum_out['p_at']} lines {len(set(x['k'] for x in quantum_out.get('history_all', [])))}")
if usstake_out: print(f"  usstake card: {len(usstake_out['legs'])} legs, {usstake_out['n_settled']} settled, top {usstake_out['legs'][usstake_out['n_settled']]['label']} {usstake_out['legs'][usstake_out['n_settled']]['p']}")
