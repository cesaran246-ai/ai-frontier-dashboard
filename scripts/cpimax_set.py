"""Kalshi 'How high will CPI get this year?' (KXHIGHINFLATION-26DEC) writer.
usage: python3 cpimax_set.py "4.2:0.405,4.3:0.21,…" [vol]
Writes kalshi.json cpimax.p_above (strike keys as strings, yes_mid) + vol. History is appended by build_kalshi.py."""
import json, sys
K = json.load(open('kalshi.json'))
C = K.setdefault('cpimax', {})
C['p_above'] = {k.strip(): float(v) for k, v in (x.split(':') for x in sys.argv[1].split(','))}
if len(sys.argv) > 2: C['vol'] = float(sys.argv[2])
json.dump(K, open('kalshi.json', 'w'), indent=1, ensure_ascii=False)
print('cpimax', C['p_above'], 'vol', C.get('vol'))
