import json,sys,datetime as dt
# usage: python3 stake_set.py "UMAC:p:vol,NTEC:p:vol,ANDU:p:vol,PDW:p:vol,NVDA:p:vol,IONQ:p:vol,TSM:p:vol,LLY:p:vol,ANTH:p:vol,MU:p:vol,OAI:p:vol,TTOK:p:vol,FCX:p:vol,BA:p:vol,LMT:p:vol,PLTR:p:vol,PFE:p:vol,SPI:p:vol" [--settled K:YYYY-MM-DD ...]
# Updates the top-level `usstake` board legs (p, vol) AND every stock_pm.<TK>.usstake leg whose ticker matches (points[0][1] + vol).
# Settled legs are never touched; a newly finalized leg is marked with --settled K:date (outcome yes) — add the news to usstake.note by hand.
K=json.load(open('kalshi.json')); US=K['usstake']
vals={a:(float(b),int(c)) for a,b,c in (x.split(':') for x in sys.argv[1].split(','))}
newly=dict(x.split(':') for x in sys.argv[3:]) if len(sys.argv)>2 and sys.argv[2]=='--settled' else {}
n=0
for leg in US['legs']:
    if leg['k'] in newly and not leg.get('settled'): leg['settled']={'d':newly[leg['k']],'outcome':'yes'}; leg['p']=1.0
    if leg.get('settled'): continue
    if leg['k'] in vals: leg['p'],leg['vol']=vals[leg['k']]; n+=1
for tk,b in K['stock_pm'].items():
    if not isinstance(b,dict): continue
    for m in b.get('markets',[]):
        if m.get('key')!='usstake' or m.get('settled'): continue
        suf=m['tickers'][0].rsplit('-',1)[1]
        if suf in newly: m['settled']={'d':newly[suf],'outcome':'yes','note':'Kalshi leg finalized YES'}; m['points']=[['2027-01-01',1.0]]
        elif suf in vals: m['points']=[['2027-01-01',vals[suf][0]]]; m['vol']=vals[suf][1]
json.dump(K,open('kalshi.json','w'),indent=1,ensure_ascii=False); print('usstake legs updated:',n,'newly settled:',list(newly))

