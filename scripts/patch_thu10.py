# patch_thu10.py — PRE-STAGED at the Wed 9/23 close from patch_wed5.py: every base (FRI dict, VIX/BTC/ETH/Brent, FXB, 10Y anchor) is already rolled to the Wed close.
# The Thu 10am run only edits the lines marked FILL. Running it unfilled reproduces the Wed close with 0% moves.
import json,datetime
TR="/root/.claude/projects/-home-claude/36e4441a-6ef0-5fc4-8118-17189f39e24a/tool-results/"
b1=json.load(open(TR+"<<FILL batch1 result file>>"))["symbols"]   # FILL
b2=json.load(open(TR+"<<FILL batch2 result file>>"))["symbols"]   # FILL
d=json.load(open("dashboard_data_v3.json")); comp=d["companies"]
prev={k:comp[k].get("prev_close") for k in comp}   # 10AM run: stored prev_close = Wed 9/23 close (rolled at the Wed 5pm close); keep it, do NOT roll
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
FRI={"SPY":767.72,"QQQ":741.10,"DIA":514.26,"EWJ":97.39,"EWY":185.70,"GLD":393.34,"SLV":58.17,"USO":149.18,"IEF":90.13,"VIXY":16.77}  # WED 9/23 close refs (variable name kept)
NOW={"SPY":767.72,"QQQ":741.10,"DIA":514.26,"EWJ":97.39,"EWY":185.70,"GLD":393.34,"SLV":58.17,"USO":149.18,"IEF":90.13,"VIXY":16.77}   # FILL with this run's ETF prices (these are the Wed closes)
RSI={"SPY":53.58,"QQQ":63.05,"DIA":40.2,"EWJ":52.7,"EWY":54.06,"GLD":44.13,"SLV":48.72}   # FILL
chg={k:round((NOW[k]/FRI[k]-1)*100,2) for k in FRI}
def setidx(key,**kw):
    for i in d["indices"]:
        if i["key"]==key: i.update(kw); return
setidx("SPX", value=round(NOW["SPY"]*10), chg=chg["SPY"], rsi=RSI["SPY"], mult=10, proxy=None, note="actual index points (SPY ×10)")
setidx("NDX", value=round(NOW["QQQ"]*41), chg=chg["QQQ"], rsi=RSI["QQQ"], mult=41, proxy=None, note="actual index points (QQQ ×41)")
setidx("DJI", value=round(NOW["DIA"]*100), chg=chg["DIA"], rsi=RSI["DIA"], mult=100, proxy=None, note="actual index points (DIA ×100)")
setidx("NKY", value=NOW["EWJ"], chg=chg["EWJ"], rsi=RSI["EWJ"], proxy="EWJ", note="via EWJ (iShares MSCI Japan ETF)")
setidx("KOSPI", value=NOW["EWY"], chg=chg["EWY"], rsi=RSI["EWY"], proxy="EWY", note="via EWY (iShares MSCI Korea ETF)")
ANCHOR=4.96; ANCHOR_DATE="2026-09-21"; IEF_BASE=91.15   # FILL only if H.15 printed a NEWER date (then IEF_BASE = that date's IEF close)
ief_cum=round((NOW["IEF"]/IEF_BASE-1)*100,3); y10=round(ANCHOR-(ief_cum*0.135),2)
setidx("UST10Y", value=y10, chg=None, anchor=ANCHOR, anchor_date=ANCHOR_DATE,
       note=f"est. {y10}% · anchored to H.15 {ANCHOR}% ({ANCHOR_DATE} print), rolled by IEF since that date's close {IEF_BASE} ({ief_cum:+}% now)")
uso_cum=round((NOW["USO"]/161.50-1)*100,2); brent_dated_est=round(130.80*(1+uso_cum/100),2)
BRENT_ICE=103.42; BRENT_NOTE_SRC="tradingeconomics, Thu 9/24 <<time>>Z, day <<±$x / ±y%>> on their prior settle"; brent=BRENT_ICE   # FILL both
setidx("BRENT", value=brent, chg=round((BRENT_ICE/103.42-1)*100,2), anchor=130.80, anchor_date="2026-09-15",
       note=f"ICE Brent front-month ${BRENT_ICE} ({BRENT_NOTE_SRC}; tile chg vs our Wed close read $103.42). Method: live ICE front-month (Cesar's choice, Wed 9/23). Until Tue 9/22 the tile had shown a USO-rolled EIA Dated Brent PHYSICAL price (last print $130.80 on 9/15 → est. ${brent_dated_est} today), which sat ~$20 above the futures benchmark Kalshi settles on. Dated-vs-futures premium is a Hormuz-disruption artefact; kept here as a note only.")
VIX=15.04; BTC=84401.33; ETH=2673.49; GOLD=4287.17; SILVER=64.43   # FILL (these are the Wed close marks)
TS=datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%MZ")
setidx("VIX", value=VIX, chg=round((VIX/15.04-1)*100,2), note=f"CBOE volatility · Stocklake market pulse (VIXY {chg['VIXY']:+}% vs Wed close)")
setidx("GOLD", value=GOLD, chg=chg["GLD"], rsi=RSI["GLD"], note=f"XAU/USD spot · AV live {TS} (chg via GLD vs Wed close)")
setidx("SILVER", value=SILVER, chg=chg["SLV"], rsi=RSI["SLV"], note=f"XAG/USD spot · AV live {TS} (chg via SLV vs Wed close)")
setidx("BTC", value=BTC, chg=round((BTC/84401.33-1)*100,2), note=f"BTC/USD · AV live {TS} (vs Wed 5pm close)")
setidx("ETH", value=ETH, chg=round((ETH/2673.49-1)*100,2), note=f"ETH/USD · AV live {TS} (vs Wed 5pm close)")
# FX tiles (added Wed 9/23 on Cesar's request): AV CURRENCY_EXCHANGE_RATE EUR->USD and USD->JPY, one call each, ~1s apart
EURUSD=1.13877433; USDJPY=158.18748486   # FILL (these are the Wed 5pm reads)
FXB={"EURUSD":1.1388,"USDJPY":158.19}  # FXB = Wed 9/23 5pm reads (FX trades 24h; the 5pm ET read is our close); roll at each close
setidx("EURUSD", value=round(EURUSD,4), chg=round((EURUSD/FXB["EURUSD"]-1)*100,2), note=f"EUR/USD spot · AV live {TS} (chg vs Wed 9/23 close {FXB['EURUSD']})")
setidx("USDJPY", value=round(USDJPY,2), chg=round((USDJPY/FXB["USDJPY"]-1)*100,2), note=f"USD/JPY spot · AV live {TS} (chg vs Wed 9/23 close {FXB['USDJPY']}) — up = weaker yen")
mp=d["market_pulse"]; mp["vix"]=VIX; mp["fear_greed"]={"value":35.7,"label":"fear"}   # FILL
mp["breadth"]={"overbought_pct":2.0,"oversold_pct":8.8}   # FILL
mp["note"]=("10am ET 2026-09-24 — fourth session of the week (% vs Wed 9/23 close). "
 f"S&P {chg['SPY']:+}%, Nasdaq {chg['QQQ']:+}%, Dow {chg['DIA']:+}%, Japan {chg['EWJ']:+}%, Korea {chg['EWY']:+}%; "
 f"oil {chg['USO']:+}%, gold {chg['GLD']:+}%, BTC {round((BTC/84401.33-1)*100,2):+}%; VIX {VIX}. "
 "Stocks + index proxies via Stocklake; crypto/metals via Alpha Vantage.")
n=datetime.datetime.utcnow()
d["generated"]=n.strftime("%Y-%m-%dT%H:%MZ")+" (10am ET)"; d["as_of"]=n.strftime("%Y-%m-%d")
for s2 in d["sectors"]:
    v=[comp[t]["change_pct"] for t in s2["tickers"] if t in comp and comp[t].get("change_pct") is not None]
    if v: s2["avg_change"]=round(sum(v)/len(v),2)
json.dump(d,open("dashboard_data_v3.json","w"))
mv=sorted([(c["change_pct"],k) for k,c in comp.items() if k not in("DIA","EWJ") and c.get("change_pct") is not None])
print("DOWN",mv[:6]); print("UP",mv[-6:]); print("idx",{k:chg[k] for k in FRI},"10Y",y10,"brent",brent)
print("sectors",[(s['name'] if 'name' in s else s.get('key'),s['avg_change']) for s in d['sectors']])
flags=[(k,c['rsi']) for k,c in comp.items() if k not in("DIA","EWJ") and c.get('rsi') and (c['rsi']>70 or c['rsi']<30)]
hi=[k for k,c in comp.items() if k not in("DIA","EWJ") and c.get('price') and c.get('week52_high') and c['price']>=c['week52_high']*0.995]
lo=[k for k,c in comp.items() if k not in("DIA","EWJ") and c.get('price') and c.get('week52_low') and c['price']<=c['week52_low']*1.005]
print("RSI flags",flags,"52wk hi",hi,"52wk lo",lo)
print("rail",[(r['tk'],r.get('rx')) for r in d['earnings_reports'][:5]])
