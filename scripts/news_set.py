# news_set.py — build dashboard_data_v3.json['news'] from an Alpha Vantage NEWS_SENTIMENT result file.
# Added Thu 9/24 (Cesar: "add alpha vantage news sentiment … a news feed … visible as you scroll", right-hand rail).
#
# Usage:  python3 news_set.py <AV result file> [<AV result file> …]
#   The standard call is ONE NEWS_SENTIMENT with no tickers (AV's `tickers` filter is AND — a list of 47 returns nothing):
#   sort=LATEST, limit=1000, return_full_data=true, time_from=<now − 24h, YYYYMMDDTHHMM>. The result lands in a tool-result file.
#
# What it keeps (the raw AV feed is mostly auto-generated noise — holdings filings, Form 4s, "stock heads into the open"):
#   * COMPANY items: an article about a tracked ticker (relevance >= 0.3) whose ticker or company name is in the headline,
#     or whose relevance to it is >= 0.9. MarketBeat holdings posts ("$AMZN Shares Acquired by …"), Form 4/8-K stubs and
#     quote-page stubs are dropped. At most 4 items per primary ticker.
#   * MARKETS items: from a short list of reputable sources, headline not about a stock/dividend/price target, and an
#     economy_* topic >= 0.7 (or >= 0.5 with a macro word such as Fed, CPI, yields, oil, tariffs in the headline).
#     (AV tags data releases with the publisher's ticker — e.g. SPGI on S&P Global PMIs — so ticker relevance is ignored here.)
# Headline, source, link, time, tickers and AV's sentiment labels only — never the article summary/body (the dashboard is
# public; the links go to the publisher). Items are MERGED with the stored feed and kept for 72h (max 90), so a morning pull
# that covers ~20h still shows yesterday's stories.
import json, re, sys, datetime

DATA = 'dashboard_data_v3.json'
KEEP_H = 72
MAX_ITEMS = 90
PER_TK = 4
MACRO_SRC = {'Reuters', 'Bloomberg.com', 'Bloomberg', 'WSJ', 'The Wall Street Journal', 'CNBC', 'MarketWatch',
             'Financial Times', 'FT', "Barron's", 'Associated Press', 'AP News', 'Newsquawk', 'CFO Dive', 'Axios',
             'The Economist', 'Fortune', 'Business Insider', 'Kiplinger', 'Yahoo Finance', 'Investing.com',
             'Crude Oil Prices Today | OilPrice.com', 'OilPrice.com', 'Benzinga', 'Forexlive', 'FXStreet', 'Kitco'}
MACRO_TOPICS = {'economy_monetary', 'economy_macro', 'economy_fiscal'}
MACRO_WORDS = re.compile(r'\b(Fed|FOMC|Powell|rate (cut|hike)s?|interest rates?|inflation|CPI|PCE|PMI|payrolls?|jobs report|jobless|'
                         r'unemployment|GDP|recession|Treasur(y|ies)|yields?|bond market|dollar|yen|euro|ECB|BoJ|Bank of Japan|'
                         r'OPEC|crude|oil prices?|Brent|Hormuz|tariffs?|stocks? (rally|slide|fall|rise)|Wall Street|S&P 500|Nasdaq|Dow)\b', re.I)
ALIAS = {'GOOGL': 'GOOG'}
# headline words that identify each tracked company (ticker is always tried too)
NAMES = {'AMD': ['AMD'], 'AMZN': ['Amazon', 'AWS'], 'CRWV': ['CoreWeave'], 'GOOG': ['Alphabet', 'Google', 'YouTube', 'Waymo'],
         'HOOD': ['Robinhood'], 'IONQ': ['IonQ'], 'IREN': ['IREN'], 'META': ['Meta'], 'MSFT': ['Microsoft'],
         'MU': ['Micron'], 'NBIS': ['Nebius'], 'NOW': ['ServiceNow'], 'NVDA': ['Nvidia', 'NVIDIA'], 'PLTR': ['Palantir'],
         'QUBT': ['Quantum Computing Inc'], 'RDDT': ['Reddit'], 'RGTI': ['Rigetti'], 'SKHY': ['SK hynix', 'SK Hynix'],
         'SNDK': ['Sandisk', 'SanDisk'], 'SPCX': ['SpaceX', 'Starlink'], 'TSLA': ['Tesla'], 'TSM': ['TSMC', 'Taiwan Semiconductor'],
         'UBER': ['Uber'], 'WDC': ['Western Digital'], 'STX': ['Seagate'], 'SMCI': ['Super Micro', 'Supermicro'],
         'ASML': ['ASML'], 'ARM': ['Arm Holdings'], 'MRVL': ['Marvell'], 'CBRS': ['Cerebras'], 'SHOP': ['Shopify'],
         'AVGO': ['Broadcom'], 'QBTS': ['D-Wave'], 'ASTS': ['AST SpaceMobile'], 'RKLB': ['Rocket Lab'], 'KLAR': ['Klarna'],
         'UNH': ['UnitedHealth'], 'MRNA': ['Moderna'], 'PFE': ['Pfizer'], 'MRK': ['Merck'], 'GEV': ['GE Vernova'],
         'BA': ['Boeing'], 'INTC': ['Intel'], 'WMT': ['Walmart'], 'BE': ['Bloom Energy'], 'CRDO': ['Credo'], 'ORCL': ['Oracle']}
NOISE = re.compile(r'^Form (3|4|5|8-?K|10-?[KQ]|S-1|13[DG])\b|Stock Price Today|stock price, news, quote|Stock forecasts|'
                   r'Liquidity Mapping|Volume Leaders|Holding\(s\) in Company|ETFs Investing in|Top \d+ .*Leaders', re.I)
MB_HOLDINGS = re.compile(r'\$[A-Z]{1,5}\b')          # MarketBeat 13F posts carry "$TICKER" in the headline
SHORT = {'Bullish': 'bull', 'Somewhat-Bullish': 'sbull', 'Neutral': 'neu', 'Somewhat-Bearish': 'sbear', 'Bearish': 'bear'}


def ts_iso(s):   # 20260924T124324 -> 2026-09-24T12:43Z
    return f'{s[0:4]}-{s[4:6]}-{s[6:8]}T{s[9:11]}:{s[11:13]}Z'


def in_title(tk, title):
    if re.search(r'(?<![A-Za-z])\$?' + re.escape(tk) + r'(?![A-Za-z])', title):
        return True
    return any(re.search(r'(?<![A-Za-z])' + re.escape(n) + r'(?![a-z])', title) for n in NAMES.get(tk, []))


def main(files):
    d = json.load(open(DATA))
    tracked = {k for k in d['companies'] if k not in ('DIA', 'EWJ')}
    feed = []
    for fn in files:
        feed += json.load(open(fn)).get('feed', [])
    old = (d.get('news') or {}).get('items', [])
    seen = {re.sub(r'\W+', '', i['t'].lower()) for i in old}
    new, stats = [], {'raw': len(feed), 'co': 0, 'macro': 0, 'noise': 0, 'dupe': 0}
    for a in feed:
        title = (a.get('title') or '').strip()
        if not title or not a.get('url'):
            continue
        key = re.sub(r'\W+', '', title.lower())
        if key in seen:
            stats['dupe'] += 1
            continue
        src = a.get('source') or ''
        disp = src.split(' | ')[-1].strip()          # 'Crude Oil Prices Today | OilPrice.com' -> 'OilPrice.com'
        if NOISE.search(title) or (src == 'MarketBeat' and MB_HOLDINGS.search(title)) or src == 'Stock Titan' and 'Form' in title:
            stats['noise'] += 1
            continue
        hits = {}
        for t in a.get('ticker_sentiment', []):
            tk = ALIAS.get(t['ticker'], t['ticker'])
            r = float(t['relevance_score'])
            if tk in tracked and r >= 0.3 and r > hits.get(tk, (0,))[0]:
                hits[tk] = (r, t['ticker_sentiment_label'], round(float(t['ticker_sentiment_score']), 3))
        good = {tk: v for tk, v in hits.items() if in_title(tk, title) or v[0] >= 0.9}
        kind = None
        if good:
            kind = 'co'
        else:
            tp = {t['topic']: float(t['relevance_score']) for t in a.get('topics', [])}
            eco = max([tp.get(k, 0) for k in MACRO_TOPICS] + [0])
            stocky = re.search(r'\b(stocks?|shares|price target|dividend|earnings call|conference|Zacks)\b', title, re.I) or re.search(r'\([A-Z]{2,5}\)', title)
            if src in MACRO_SRC and not stocky and (eco >= 0.7 or (eco >= 0.5 and MACRO_WORDS.search(title))):
                kind = 'macro'
        if not kind:
            continue
        tks = sorted(good.items(), key=lambda x: -x[1][0])[:4]
        new.append({'t': title, 'u': a['url'], 's': disp, 'ts': ts_iso(a['time_published']), 'k': kind,
                    'tk': [[tk, SHORT.get(v[1], 'neu'), v[2]] for tk, v in tks],
                    'sent': SHORT.get(a.get('overall_sentiment_label'), 'neu'),
                    'ss': round(float(a.get('overall_sentiment_score') or 0), 3)})
        seen.add(key)
        stats[kind] += 1
    # per-ticker cap on the NEW batch (newest first), then merge with the stored feed
    new.sort(key=lambda i: i['ts'], reverse=True)
    cnt, capped = {}, []
    for i in new:
        p = i['tk'][0][0] if i['tk'] else None
        if p:
            cnt[p] = cnt.get(p, 0) + 1
            if cnt[p] > PER_TK:
                continue
        capped.append(i)
    cutoff = (datetime.datetime.utcnow() - datetime.timedelta(hours=KEEP_H)).strftime('%Y-%m-%dT%H:%MZ')
    items = sorted([i for i in capped + old if i['ts'] >= cutoff], key=lambda i: i['ts'], reverse=True)[:MAX_ITEMS]
    now = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%MZ')
    d['news'] = {'asof': now, 'src': 'Alpha Vantage NEWS_SENTIMENT', 'keep_h': KEEP_H, 'items': items,
                 'window': [ts_iso(min(a['time_published'] for a in feed)), ts_iso(max(a['time_published'] for a in feed))] if feed else None}
    json.dump(d, open(DATA, 'w'))
    by = {}
    for i in items:
        for t in i['tk'][:1]:
            by[t[0]] = by.get(t[0], 0) + 1
    print('news:', stats, '| added', len(capped), '| stored', len(items),
          '(co', sum(i['k'] == 'co' for i in items), '/ macro', sum(i['k'] == 'macro' for i in items), ')',
          '| window', d['news']['window'], '| top', sorted(by.items(), key=lambda x: -x[1])[:10])


if __name__ == '__main__':
    assert len(sys.argv) > 1, 'usage: python3 news_set.py <AV NEWS_SENTIMENT result file> [...]'
    main(sys.argv[1:])
