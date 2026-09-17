"""call_set.py TK "K:p:vol,K:p:vol,..." — update stock_pm.<TK>.call.items p/vol by ticker suffix k"""
import json,sys
K=json.load(open('kalshi.json')); tk=sys.argv[1]; call=K['stock_pm'][tk]['call']
upd={x.split(':')[0]:(float(x.split(':')[1]),int(x.split(':')[2])) for x in sys.argv[2].split(',')}
n=0
for it in call['items']:
    if it['k'] in upd: it['p'],it['vol']=upd[it['k']]; n+=1
json.dump(K,open('kalshi.json','w'),indent=1,ensure_ascii=False); print('call',tk,n,'items updated')

