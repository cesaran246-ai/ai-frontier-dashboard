"""kpatch.py — incremental kalshi.json writer.
 fed  MEETING "s:p,..."          → fed.meetings[ev].p_above
 lad  LADDER_ID "s:p,..." [vol]  → ladders[id].p_above
 dec  DEC_ID "HOLD:p,H25:p,..." [vol] → decisions[id].p and opts
 ipo  NAME "date:p,..." [vol]    → ipo[name].points
 asset KEY FIELD "s:p,..."       → assets[KEY][FIELD] (hi|lo|p_above)
 buckets KEY "lo-hi:p,..."       → assets[KEY].buckets (lo/hi 'null' allowed)
 energy KEY "s:p,..." [vol] [ev] [date] → energy[KEY].p_above (+ev/date)
 hormuz KEY FIELD "s:p,..." [vol] → hormuz[KEY][FIELD]
 hormuz_pts "date:p,..." [vol]   → hormuz.normal.points
 asof                            → set asof now"""
import json,sys,datetime as dt
K=json.load(open('kalshi.json')); a=sys.argv[1:]; cmd=a[0]
def kv(s): return {x.split(':')[0]:float(x.split(':')[1]) for x in s.split(',') if x}
if cmd=='fed':
    m=[m for m in K['fed']['meetings'] if m['ev']==a[1]][0]; m['p_above']=kv(a[2])
    if len(a)>3: m['vol']=int(a[3])
elif cmd=='lad':
    K['ladders'][a[1]]['p_above']=kv(a[2]);
    if len(a)>3: K['ladders'][a[1]]['vol']=int(a[3])
elif cmd=='dec':
    d=K['decisions'][a[1]]; p=kv(a[2]); d['p']=p
    nm={'HOLD':'Hold','H25':'Hike 25bp','H25P':'Hike >25bp','C25':'Cut 25bp','C25P':'Cut >25bp'}
    d['opts']={nm[k]:v for k,v in p.items() if k in nm}
    if len(a)>3: d['vol']=int(a[3])
elif cmd=='ipo':
    K['ipo'][a[1]]['points']=[[x.split(':')[0],float(x.split(':')[1])] for x in a[2].split(',')]
    if len(a)>3: K['ipo'][a[1]]['vol']=int(a[3])
elif cmd=='asset':
    K['assets'].setdefault(a[1],{})[a[2]]=kv(a[3])
elif cmd=='buckets':
    b=[]
    for x in a[2].split(','):
        r,p=x.rsplit(':',1); lo,hi=r.split('-'); b.append([None if lo=='null' else float(lo),None if hi=='null' else float(hi),float(p)])
    K['assets'].setdefault(a[1],{})['buckets']=b
elif cmd=='energy':
    e=K['energy'][a[1]]; e['p_above']=kv(a[2])
    if len(a)>3: e['vol']=int(a[3])
    if len(a)>4: e['ev']=a[4]
    if len(a)>5: e['date']=a[5]
elif cmd=='hormuz':
    h=K['hormuz'][a[1]]; h[a[2]]=kv(a[3])
    if len(a)>4: h['vol']=int(a[4])
elif cmd=='hormuz_pts':
    K['hormuz']['normal']['points']=[[x.split(':')[0],float(x.split(':')[1])] for x in a[1].split(',')]
    if len(a)>2: K['hormuz']['normal']['vol']=int(a[2])
elif cmd=='asof':
    K['asof']=dt.datetime.utcnow().strftime('%Y-%m-%dT%H:%MZ')
json.dump(K,open('kalshi.json','w'),indent=1,ensure_ascii=False); print('ok',cmd,a[1:3])

