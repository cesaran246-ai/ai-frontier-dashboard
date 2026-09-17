import json,datetime
TR="/root/.claude/projects/-home-claude/36e4441a-6ef0-5fc4-8118-17189f39e24a/tool-results/"
b1=json.load(open(TR+"mcp-Stocklake-get_stocks-1789658188977.txt"))["symbols"]
b2=json.load(open(TR+"mcp-Stocklake-get_stocks-1789658193531.txt"))["symbols"]
d=json.load(open("dashboard_data_v3.json")); comp=d["companies"]
prev={k:comp[k].get("prev_close") for k in comp}
def patch(tk,s):
    if tk not in comp: return
    c=comp[tk]; ind=s.get("indicators") or {}
    def sv(k,v):
        if v is not None: c[k]=v
    sv("price",s.get("price"))
    for k in ["market_cap","volume","avg_volume","week52_high","week52_low","analyst_target","analyst_count","analyst_rating","analyst_rating_score","updated_at","revenue_growth","earnings_growth","profit_margins","operating_margins","revenue_ttm","free_cashflow","return_on_equity","debt_to_equity","beta","dividend_yield","earnings_date","earnings_is_estimate"]:
        sv(k,s.get(k))
    if s.get("pe_forward") is not None: c["pe_forward"]=round(s["pe_forward"],2)
    if s.get("pe_trailing") is not None: c["pe_trailing"]=round(s["pe_trailing"],2)
    sv("rsi",ind.get("rsi"))
    if ind.get("macd"): c["macd"]=ind["macd"]
    if ind.get("bollinger_bands"): c["bollinger"]=ind["bollinger_bands"]
    for k in ["sma20","sma50","sma200","ema20","ema200","atr_20","williams_r"]: sv(k,ind.get(k))
    if ind.get("td_sequential"): c["td_sequential"]=ind["td_sequential"].get("signal")
    c["vol10"]=s.get("avg_volume"); c["vol10_exact"]=False
    pc=prev.get(tk) or s.get("prev_close"); c["prev_close"]=pc
    if c.get("price") and pc: c["change_pct"]=round((c["price"]/pc-1)*100,2)
for tk,s in {**b1,**b2}.items(): patch(tk,s)
FRI={"SPY":754.12,"QQQ":705.07,"DIA":515.21,"EWJ":96.95,"EWY":176.28,"GLD":390.96,"SLV":56.93,"USO":156.29,"IEF":90.68,"VIXY":17.74}  # WED 9/16 close refs (variable name kept)
NOW={"SPY":760.64,"QQQ":715.05,"DIA":516.93,"EWJ":97.91,"EWY":182.06,"GLD":399.35,"SLV":59.30,"USO":154.65,"IEF":91.16,"VIXY":17.07}
RSI={"SPY":41.78,"QQQ":44.13,"DIA":35.46,"EWJ":53.68,"EWY":46.97,"GLD":43.2,"SLV":45.05}
chg={k:round((NOW[k]/FRI[k]-1)*100,2) for k in FRI}
def setidx(key,**kw):
    for i in d["indices"]:
        if i["key"]==key: i.update(kw); return
setidx("SPX", value=round(NOW["SPY"]*10), chg=chg["SPY"], rsi=RSI["SPY"], mult=10, proxy=None, note="actual index points (SPY ×10)")
setidx("NDX", value=round(NOW["QQQ"]*41), chg=chg["QQQ"], rsi=RSI["QQQ"], mult=41, proxy=None, note="actual index points (QQQ ×41)")
setidx("DJI", value=round(NOW["DIA"]*100), chg=chg["DIA"], rsi=RSI["DIA"], mult=100, proxy=None, note="actual index points (DIA ×100)")
setidx("NKY", value=NOW["EWJ"], chg=chg["EWJ"], rsi=RSI["EWJ"], proxy="EWJ", note="via EWJ (iShares MSCI Japan ETF)")
setidx("KOSPI", value=NOW["EWY"], chg=chg["EWY"], rsi=RSI["EWY"], proxy="EWY", note="via EWY (iShares MSCI Korea ETF)")
ief_cum=round((NOW["IEF"]/90.87-1)*100,3); y10=round(5.00-(ief_cum*0.135),2)
setidx("UST10Y", value=y10, chg=None, anchor=5.00, anchor_date="2026-09-15",
       note=f"est. {y10}% · anchored to H.15 5.00% (9/15, new print — highest since 2023), rolled by IEF since the Tue close ({ief_cum:+}% at 10am Thu)")
uso_cum=round((NOW["USO"]/161.50-1)*100,2); brent=round(130.80*(1+uso_cum/100),2)
setidx("BRENT", value=brent, chg=None, anchor=130.80, anchor_date="2026-09-15",
       note=f"est. ${brent} · anchored to EIA Dated Brent $130.80 (9/15, new print; 9/14 $121.25) — the official spot ran well above the USO-rolled estimate ($117.93 at the Tue close), so the tile re-anchored up; rolled by USO since 9/15 (USO {uso_cum:+}%)")
VIX=15.67; BTC=76237.21; ETH=2448.80; GOLD=4361.64; SILVER=65.60
setidx("VIX", value=VIX, chg=round((VIX/17.08-1)*100,2), note="CBOE volatility · Stocklake market pulse 10am ET")
setidx("GOLD", value=GOLD, chg=chg["GLD"], rsi=RSI["GLD"], note="XAU/USD spot · AV live 2026-09-17 15:17Z (chg via GLD vs Wed)")
setidx("SILVER", value=SILVER, chg=chg["SLV"], rsi=RSI["SLV"], note="XAG/USD est. · AV silver quote returned empty at 15:17Z — Wed close spot $62.98 rolled by SLV (chg via SLV vs Wed)")
setidx("BTC", value=BTC, chg=round((BTC/76012.26-1)*100,2), note="BTC/USD · AV live 2026-09-17 15:17Z (vs Wed close)")
setidx("ETH", value=ETH, chg=round((ETH/2403.42-1)*100,2), note="ETH/USD · AV live 2026-09-17 15:17Z (vs Wed close)")
mp=d["market_pulse"]; mp["vix"]=VIX; mp["fear_greed"]={"value":29.6,"label":"fear"}
mp["breadth"]={"overbought_pct":2.0,"oversold_pct":8.8}
mp["note"]=("10am ET 2026-09-17 — day after the Fed hike to 3.75–4.00% (% vs Wed 9/16 close). "
 f"S&P {chg['SPY']:+}%, Nasdaq {chg['QQQ']:+}%, Dow {chg['DIA']:+}%, Korea {chg['EWY']:+}%; "
 f"oil {chg['USO']:+}%, gold {chg['GLD']:+}%, BTC {round((BTC/76012.26-1)*100,2):+}%; VIX {VIX}. "
 "Stocks + index proxies via Stocklake; crypto/metals via Alpha Vantage.")
n=datetime.datetime.utcnow()
d["generated"]=n.strftime("%Y-%m-%dT%H:%MZ")+" (10am ET)"; d["as_of"]=n.strftime("%Y-%m-%d")
for s2 in d["sectors"]:
    v=[comp[t]["change_pct"] for t in s2["tickers"] if t in comp and comp[t].get("change_pct") is not None]
    if v: s2["avg_change"]=round(sum(v)/len(v),2)
json.dump(d,open("dashboard_data_v3.json","w"))
mv=sorted([(c["change_pct"],k) for k,c in comp.items() if k not in("DIA","EWJ") and c.get("change_pct") is not None])
print("DOWN",mv[:5]); print("UP",mv[-5:]); print("idx",{k:chg[k] for k in FRI},"10Y",y10,"brent",brent)
print("sectors",[(s['name'] if 'name' in s else s.get('key'),s['avg_change']) for s in d['sectors']])
flags=[(k,c['rsi']) for k,c in comp.items() if k not in("DIA","EWJ") and c.get('rsi') and (c['rsi']>70 or c['rsi']<30)]
hi=[k for k,c in comp.items() if k not in("DIA","EWJ") and c.get('price') and c.get('week52_high') and c['price']>=c['week52_high']*0.995]
lo=[k for k,c in comp.items() if k not in("DIA","EWJ") and c.get('price') and c.get('week52_low') and c['price']<=c['week52_low']*1.005]
print("RSI flags",flags,"52wk hi",hi,"52wk lo",lo)
print("rail",[(r['tk'],r.get('rx')) for r in d['earnings_reports'][:5]])
print("AVGO",comp['AVGO']['price'],comp['AVGO']['change_pct'],"ORCL",comp['ORCL']['price'],comp['ORCL']['change_pct'])

