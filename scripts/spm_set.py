import json,sys
# usage: python3 spm_set.py TK KEY vol "s:p,s:p,..."  (p_above)  |  python3 spm_set.py TK KEY vol --points "date:p,..." [TK2]
d=json.load(open('kalshi.json')); tk,key,vol=sys.argv[1],sys.argv[2],int(sys.argv[3])
if sys.argv[4]=='--points':
    pts=[[a,float(b)] for a,b in (x.split(':') for x in sys.argv[5].split(','))]; tks=[tk]+sys.argv[6:]
    for t in tks:
        for m in d['stock_pm'][t]['markets']:
            if m['key']==key: m['points']=[list(p) for p in pts]; m['vol']=vol
    print('points set on',tks,key)
else:
    pa={a:float(b) for a,b in (x.split(':') for x in sys.argv[4].split(','))}
    for m in d['stock_pm'][tk]['markets']:
        if m['key']==key: m['p_above']=pa; m['vol']=vol; print('set',tk,key,len(pa),'strikes')
json.dump(d,open('kalshi.json','w'),indent=1,ensure_ascii=False)

