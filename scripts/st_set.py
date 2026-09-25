# st_set.py — merge Stocktwits CONSENSUS into the dashboard's single news feed (Cesar, Fri 9/25: "add stocktwits feed info for
# the companies on my lists … merge with the news feed so there is only one … focus on stocktwits that represent consensus").
#
# Input: /home/claude/st_raw.json, written each run by a read-only subagent:
#   {"asof": "...Z", "items": {TK: {"score","label","bull","bear","delta", ["vol_now","vol_label","vol_1d","top":[{id,username,body,
#   likes,sentiment,created_at}]]} | {"error": "..."}}}
#   (get_sentiment for all 47 names; get_message_volume + get_symbol_messages filter=top limit=30 for names with score ≥58 or ≤42)
#
# CONSENSUS RULE (what keeps the feed from being flooded):
#   * Signal = Stocktwits' canonical normalized sentiment score (0–100) and label. The legacy "% of tagged posts bullish" is shown
#     for context only — it is structurally bullish-skewed (retail tags) and often disagrees with the canonical label.
#   * A name qualifies only when the crowd is decisively one-sided: score ≥ 70 (bullish) or ≤ 30 (bearish), OR label
#     EXTREMELY_BULLISH / EXTREMELY_BEARISH — and message volume is not negligible (normalized 'now' ≥ 25).
#   * At most MAX_ITEMS names, strongest |score − 50| first. One card per name, REPLACED every run (never accumulated).
#   * (QUOTES=False since Fri 9/25) An optional one-line representative post would be attached only if a top post agrees with the consensus and passes a strict
#     quality filter (on-topic, no profanity, no options-lotto/pump spam, not a bot/hashtag dump, ≥2 likes). Most posts fail —
#     that is intended; the card still shows the consensus numbers and a link to the live stream.
# Also refreshes companies[TK]['sentiment'] (the detail panel's "Retail Chatter" header) for every name with data.
import html, json, re, sys

DATA = 'dashboard_data_v3.json'
RAW = sys.argv[1] if len(sys.argv) > 1 else 'st_raw.json'
MAX_ITEMS = 10
QUOTES = False   # post quotes disabled (Fri 9/25): top posts were mostly off-topic/spam — the card shows the consensus numbers only
BULL_T, BEAR_T, VOL_MIN = 70, 30, 25
PROF = re.compile(r'\b(fuck\w*|shit\w*|bitch\w*|cuck\w*|ass(hole)?|retard\w*|damn|wtf|stfu)\b', re.I)
SPAM = re.compile(r'\b(calls?|puts?|lotto\w*|load(ing)?|entry:|gain:|closed \d|disclaimer|not financial advice|come to|'
                  r'parabolic|moon|squeeze|rocket|pump)\b|https?://|!!!|\?\?\?', re.I)
CASH = re.compile(r'\$[A-Z]{1,6}(\.[A-Z])?\b')


def clean(b):
    return re.sub(r'\s+', ' ', html.unescape(b or '')).strip()


def quote_for(tk, it, want):
    best = None
    for m in it.get('top') or []:
        if m.get('sentiment') != want or (m.get('likes') or 0) < 2:
            continue
        b = clean(m.get('body'))
        tags = CASH.findall(b)
        first = CASH.search(b)
        if not first or first.group(0).lstrip('$') not in (tk, 'GOOGL' if tk == 'GOOG' else tk):
            continue
        if len(CASH.findall(b)) > 2 or b.count('#') >= 3 or PROF.search(b) or SPAM.search(b):
            continue
        txt = CASH.sub('', b).strip(' -–—:|')
        letters = [c for c in txt if c.isalpha()]
        if not (30 <= len(txt) <= 220) or not letters or sum(c.isupper() for c in letters) / len(letters) > 0.5:
            continue
        if best is None or (m.get('likes') or 0) > (best['likes']):
            best = {'id': m['id'], 'user': m.get('username'), 'likes': m.get('likes') or 0, 'body': b, 'ts': m.get('created_at')}
    return best


def main():
    d = json.load(open(DATA))
    R = json.load(open(RAW))
    comp = d['companies']
    cands, n_ok = [], 0
    for tk, it in R['items'].items():
        if 'error' in it or it.get('score') is None:
            continue
        n_ok += 1
        if tk in comp:
            comp[tk]['sentiment'] = {'score': it['score'], 'label': it['label'], 'bullish_pct': it.get('bull'), 'asof': R['asof']}
        s, lab = it['score'], (it.get('label') or '').upper()
        bull = s >= BULL_T or lab == 'EXTREMELY_BULLISH'
        bear = s <= BEAR_T or lab == 'EXTREMELY_BEARISH'
        if not (bull or bear) or (it.get('vol_now') or 0) < VOL_MIN:
            continue
        cands.append((abs(s - 50), tk, it, 'Bullish' if bull else 'Bearish'))
    cands.sort(key=lambda x: -x[0])
    out = []
    for _, tk, it, want in cands[:MAX_ITEMS]:
        q = quote_for(tk, it, want) if QUOTES else None
        out.append({'tk': tk, 'score': it['score'], 'label': it['label'], 'dir': 'bull' if want == 'Bullish' else 'bear',
                    'bull': it.get('bull'), 'bear': it.get('bear'), 'delta': it.get('delta'),
                    'vol': it.get('vol_label'), 'vol_now': it.get('vol_now'),
                    'u': f'https://stocktwits.com/symbol/{"GOOGL" if tk == "GOOG" else tk}', 'q': q})
    d.setdefault('news', {})['st'] = {'asof': R['asof'], 'src': 'Stocktwits (canonical sentiment score + message volume)',
                                     'rule': f'score ≥{BULL_T} or ≤{BEAR_T} (or Extremely label), volume ≥{VOL_MIN}; top {MAX_ITEMS}',
                                     'items': out}
    json.dump(d, open(DATA, 'w'))
    print(f'stocktwits: {n_ok} names with data | consensus {len(out)} (of {len(cands)} qualifying):',
          [(o['tk'], o['score'], o['label'], 'q' if o['q'] else '-') for o in out])


if __name__ == '__main__':
    main()
