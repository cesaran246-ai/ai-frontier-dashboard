# compute_set.py — maintain d['compute'] (Ornn compute prices) in dashboard_data_v3.json.
# Source: Ornn MCP on Cesar's Mac (free tier): OCPI = $/GPU-hour daily settle (5 GPUs), OTPI = $/M tokens
# volume-weighted blend per lab (4 labs). History is kept in the dashboard json (append-only, keyed by date),
# so charts grow past the free API's 3-month window.
# usage:
#   python3 compute_set.py seed ornn_seed.json            # {"gpu":{name:{date:v}}, "tok":{lab:{date:v}}} — merge full histories
#   python3 compute_set.py gpu "A100 SXM4:1.015,B200:7.773,H100 SXM:2.852,H200:4.9425,RTX 5090:0.6279" 2026-09-22
#   python3 compute_set.py lab "anthropic:1.5101,openai:0.4222,google:0.5346,deepseek:0.0658" 2026-09-22
#   python3 compute_set.py live "B200:7.80,..." 2026-09-23T15:00Z  # optional hourly snapshot (shown as 'live', not charted)
import json, sys, datetime as dt
F = 'dashboard_data_v3.json'
d = json.load(open(F))
C = d.setdefault('compute', {})
C.setdefault('source', 'Ornn — Compute Price Index (OCPI, $/GPU-hour, daily settle) and Token Price Index (OTPI, $/million tokens, volume-weighted blend across each lab’s models). Free tier.')
C.setdefault('gpu_order', ['B200', 'H200', 'H100 SXM', 'A100 SXM4', 'RTX 5090'])
C.setdefault('lab_order', ['anthropic', 'openai', 'google', 'deepseek'])
C.setdefault('locked', {'gpus': ['RTX PRO 6000 WS'], 'labs': ['minimax', 'xiaomi', 'qwen', 'moonshotai', 'z-ai', 'mistralai', 'meta-llama']})
C.setdefault('kalshi_link', {'B200': 'b200', 'H200': 'h200', 'RTX 5090': 'rtx5090'})  # stock_pm.NVDA market keys settling on OCPI
G = C.setdefault('gpus', {}); T = C.setdefault('labs', {})


def merge(store, name, pts):
    h = {p[0]: p[1] for p in store.setdefault(name, {}).get('hist', [])}
    h.update(pts)
    store[name]['hist'] = [[k, round(float(v), 6)] for k, v in sorted(h.items())]


def kv(s):
    out = {}
    for x in s.split(','):
        k, v = x.rsplit(':', 1); out[k.strip()] = float(v)
    return out


cmd = sys.argv[1]
if cmd == 'seed':
    S = json.load(open(sys.argv[2]))
    for g, pts in S.get('gpu', {}).items(): merge(G, g, pts)
    for l, pts in S.get('tok', {}).items(): merge(T, l, pts)
elif cmd in ('gpu', 'lab'):
    day = sys.argv[3]; store = G if cmd == 'gpu' else T
    for k, v in kv(sys.argv[2]).items(): merge(store, k, {day: v})
elif cmd == 'live':
    C['live'] = {'ts': sys.argv[3], 'gpus': kv(sys.argv[2])}
else:
    sys.exit('unknown cmd ' + cmd)
C['asof'] = dt.datetime.utcnow().strftime('%Y-%m-%dT%H:%MZ')
lastg = max((v['hist'][-1][0] for v in G.values() if v.get('hist')), default='')
lastl = max((v['hist'][-1][0] for v in T.values() if v.get('hist')), default='')
C['last_gpu_day'] = lastg; C['last_lab_day'] = lastl
json.dump(d, open(F, 'w'), ensure_ascii=False)
print('compute:', cmd, '| gpus', {k: (len(v['hist']), v['hist'][-1]) for k, v in G.items()}, '| labs', {k: (len(v['hist']), round(v['hist'][-1][1], 4)) for k, v in T.items()})
