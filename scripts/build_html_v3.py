import json
data = json.load(open('dashboard_data_v3.json'))
payload = json.dumps(data, separators=(',',':')).replace('</','<\\/').replace('\u2028','\\u2028').replace('\u2029','\\u2029')
html = r'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>AI & Frontier Tech — Financial Dashboard</title>
<style>
:root{--bg:#0a0d13;--panel:#111624;--panel2:#0e1320;--panel3:#141b2c;--card:#111624;--bd:#212a3d;--bd2:#2c3852;--tx:#e7ebf3;--tx2:#cfd6e4;--mut:#8a95a9;--mut2:#5f6b81;--grn:#2fbf71;--red:#f2555a;--amb:#f5a623;--cyan:#3fbdf1;--pur:#a879f0;--chip:#1a2133;--chip2:#1c2334;--bar:#4b5568;--ink:#06121c;}
/* ---- Light theme (opt-in; dark stays the default) ---- */
:root[data-theme=light]{--bg:#f4f6fa;--panel:#ffffff;--panel2:#f1f4f9;--panel3:#e7ecf4;--card:#ffffff;--bd:#d6dde8;--bd2:#b9c4d6;--tx:#141a26;--tx2:#2b3446;--mut:#5b6678;--mut2:#7d889b;--grn:#178f52;--red:#d23a41;--amb:#b46a00;--cyan:#0b6fb3;--pur:#6b3fd0;--chip:#e9edf4;--chip2:#dfe5ef;--bar:#c3cbd9;--ink:#ffffff;color-scheme:light}
:root[data-theme=light] body{-webkit-font-smoothing:auto}
:root[data-theme=light] .b.sb{background:rgba(23,143,82,.12);color:#137a45;border-color:rgba(23,143,82,.35)}
:root[data-theme=light] .b.buy{background:rgba(23,143,82,.09);color:#137a45;border-color:rgba(23,143,82,.25)}
:root[data-theme=light] .b.hold{background:rgba(180,106,0,.10);color:#9a5a00;border-color:rgba(180,106,0,.3)}
:root[data-theme=light] .b.sell,:root[data-theme=light] .b.ins-sell{background:rgba(210,58,65,.10);color:#b52f36;border-color:rgba(210,58,65,.3)}
:root[data-theme=light] .b.ins-buy{background:rgba(23,143,82,.10);color:#137a45;border-color:rgba(23,143,82,.3)}
:root[data-theme=light] .b.ktag,:root[data-theme=light] .ktag{background:rgba(107,63,208,.10);color:#5a2fc0;border-color:rgba(107,63,208,.35)}
:root[data-theme=light] .msg .mt.Bullish{background:rgba(23,143,82,.12);color:#137a45}:root[data-theme=light] .msg .mt.Bearish{background:rgba(210,58,65,.12);color:#b52f36}
:root[data-theme=light] .otbox h4,:root[data-theme=light] .cbuy,:root[data-theme=light] .tmkl.hi{color:#137a45}
:root[data-theme=light] .tmkl.lo{color:#b52f36}
:root[data-theme=light] .bm.beat{background:rgba(23,143,82,.13);color:#137a45}:root[data-theme=light] .bm.miss{background:rgba(210,58,65,.13);color:#b52f36}
:root[data-theme=light] .vs.beat{color:#137a45}:root[data-theme=light] .vs.miss{color:#b52f36}
:root[data-theme=light] .cp.us{color:#0b6fb3;background:rgba(11,111,179,.10)}:root[data-theme=light] .cp.jp{color:#c02a4d;background:rgba(192,42,77,.10)}:root[data-theme=light] .cp.eu{color:#2a5bd7;background:rgba(42,91,215,.10)}:root[data-theme=light] .cp.corp{color:#5a2fc0;background:rgba(107,63,208,.10)}
:root[data-theme=light] .cp.rep{color:#137a45;background:rgba(23,143,82,.10)}
:root[data-theme=light] .kstrip,:root[data-theme=light] .kearn{background:rgba(107,63,208,.06);border-color:rgba(107,63,208,.25)}
:root[data-theme=light] .kstrip .klab,:root[data-theme=light] .kearn .klab,:root[data-theme=light] .kearn summary,:root[data-theme=light] .pmx,:root[data-theme=light] .stf-x{color:#5a2fc0;border-color:rgba(107,63,208,.35)}
:root[data-theme=light] .pmchip{background:rgba(107,63,208,.07);border-color:rgba(107,63,208,.25);color:#2b1a5e}:root[data-theme=light] .pmchip b{color:#141a26}
:root[data-theme=light] .fm .fe,:root[data-theme=light] .pmtile .pv{color:#4a2bb0}
:root[data-theme=light] .stf-n{color:#4a2bb0;background:rgba(107,63,208,.10);border-color:rgba(107,63,208,.3)}
:root[data-theme=light] .kb span,:root[data-theme=light] .kb.on span{color:#5b6678}
:root[data-theme=light] .kcall .kt i,:root[data-theme=light] .hbar .ht i{background:linear-gradient(90deg,#6b3fd0,#9b7be6)}
:root[data-theme=light] .kb i{background:linear-gradient(180deg,#9b7be6,#6b3fd0)}:root[data-theme=light] .kb.on i{background:linear-gradient(180deg,#c39cf5,#7b4fe0)}
:root[data-theme=light] .rsibar{background:linear-gradient(90deg,#178f52 0%,#178f52 30%,#c3cbd9 30%,#c3cbd9 70%,#d23a41 70%,#d23a41 100%)}
:root[data-theme=light] .rsibar .dot{background:#141a26;border-color:#fff}
:root[data-theme=light] .idx.hask:hover{border-color:#6b3fd0}
:root[data-theme=light] .ov{background:rgba(20,26,38,.55)}
:root[data-theme=light] .tabs{background:linear-gradient(180deg,var(--bg) 82%,transparent)}
:root[data-theme=light] .tabbtn.on{background:rgba(11,111,179,.08)}
:root[data-theme=light] .pendingbar{background:linear-gradient(180deg,#eaf3fb,#f1f4f9);border-color:rgba(11,111,179,.35)}
:root[data-theme=light] .hitpill.y{background:rgba(23,143,82,.13);color:#137a45}:root[data-theme=light] .hitpill.n{background:rgba(210,58,65,.13);color:#b52f36}
:root[data-theme=light] .copybtn,:root[data-theme=light] .openbtn{color:#fff}
:root[data-theme=light] .mscibox{color:#9a5a00}
:root[data-theme=light] .thesis{color:#2b3446}
:root[data-theme=light] svg text[fill="#e9d5ff"]{fill:#4a2bb0}:root[data-theme=light] svg text[fill="#a7f3d0"]{fill:#137a45}:root[data-theme=light] svg text[fill="#94a3b8"]{fill:#5b6678}:root[data-theme=light] svg text[fill="#38bdf8"]{fill:#0b6fb3}
.thbtn{cursor:pointer;user-select:none}.thbtn:hover{border-color:var(--cyan)}

*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--tx);font:14px/1.45 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;-webkit-font-smoothing:antialiased}
a{color:var(--cyan);text-decoration:none}a:hover{text-decoration:underline}
.wrap{max-width:1840px;margin:0 auto;padding:16px 18px 60px}
header{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;margin-bottom:8px}
h1{font-size:19px;margin:0;font-weight:700;letter-spacing:.2px}h1 span{color:var(--cyan)}
.sub{color:var(--mut);font-size:12px}
.pulse{display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.pill{background:var(--chip);border:1px solid var(--bd);border-radius:20px;padding:5px 11px;font-size:12px;color:var(--mut);white-space:nowrap}
.pill b{color:var(--tx)}
.strip{display:grid;grid-template-columns:repeat(auto-fill,minmax(122px,1fr));gap:8px;margin:14px 0 20px}
.idx{background:var(--panel);border:1px solid var(--bd);border-radius:10px;padding:9px 11px}
.idx .nm{font-size:11px;color:var(--mut);display:flex;justify-content:space-between;align-items:center}
.idx .vl{font-size:16px;font-weight:700;margin-top:3px}.idx .ch{font-size:12px;font-weight:600;margin-top:1px}.idx .rsi{font-size:10px;color:var(--mut2);margin-top:2px}
.up{color:var(--grn)}.down{color:var(--red)}.flat{color:var(--mut)}
.tag{font-size:9px;padding:1px 5px;border-radius:6px;background:var(--chip2);color:var(--mut2);border:1px solid var(--bd)}
.controls{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin-bottom:14px}
.controls input,.controls select{background:var(--panel);border:1px solid var(--bd);color:var(--tx);border-radius:8px;padding:8px 11px;font-size:13px}
.controls input{min-width:220px}
.legend{margin-left:auto;color:var(--mut2);font-size:11px;display:flex;gap:12px;flex-wrap:wrap}.legend i{font-style:normal}
.sector{margin-bottom:26px}
.sechd{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap;border-bottom:1px solid var(--bd);padding-bottom:7px;margin-bottom:12px}
.sechd h2{font-size:15px;margin:0;font-weight:700}.sechd .bl{color:var(--mut);font-size:12px}
.sechd .cnt{color:var(--mut2);font-size:11px;background:var(--chip);border-radius:12px;padding:2px 9px;border:1px solid var(--bd)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(272px,1fr));gap:11px}
.card{background:var(--panel);border:1px solid var(--bd);border-radius:12px;padding:13px;cursor:pointer;transition:.13s;position:relative}
.card:hover{border-color:var(--bd2);transform:translateY(-2px)}
.card .top{display:flex;justify-content:space-between;align-items:flex-start;gap:8px}
.tk{font-size:16px;font-weight:800;letter-spacing:.3px}
.cn{font-size:11px;color:var(--mut);margin-top:1px;max-width:150px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.px{text-align:right}.px .p{font-size:16px;font-weight:700}.px .c{font-size:12px;font-weight:600}
.spark{margin-top:9px;height:34px;width:100%;display:block}
/* ---- My List: compact table view ---- */
.vtog{display:inline-flex;border:1px solid var(--bd);border-radius:8px;overflow:hidden}
.vtog button{font:600 12px/1 inherit;font-family:inherit;background:var(--panel);color:var(--mut);border:none;padding:8px 12px;cursor:pointer}
.vtog button.on{background:rgba(63,189,241,.14);color:var(--cyan)}
.ltwrap{overflow-x:auto;border:1px solid var(--bd);border-radius:12px;background:var(--panel)}
.ltbl{width:100%;border-collapse:collapse;font-size:12px;min-width:820px}
.ltbl th{font-size:9.5px;text-transform:uppercase;letter-spacing:.4px;color:var(--mut2);font-weight:700;text-align:right;padding:8px 7px;border-bottom:1px solid var(--bd);white-space:nowrap;background:var(--panel2)}
.ltbl th:first-child,.ltbl td:first-child{text-align:left}
.ltbl th.c,.ltbl td.c{text-align:center}
.ltbl td{padding:7px 7px;border-bottom:1px solid var(--bd);text-align:right;font-variant-numeric:tabular-nums;color:var(--tx);white-space:nowrap}
.ltbl tr.lr{cursor:pointer;transition:background .12s}
.ltbl tr.lr:hover td{background:rgba(63,189,241,.05)}
.ltbl tr.lr.open td{background:rgba(63,189,241,.08);border-bottom-color:transparent}
.ltbl td.tkc{font-weight:800;font-size:13.5px;letter-spacing:.3px}
.ltbl td.tkc small{display:block;font-weight:400;font-size:10px;color:var(--mut);max-width:150px;overflow:hidden;text-overflow:ellipsis;letter-spacing:0}
.ltbl td.pxc{font-weight:700;font-size:13.5px}
.ltbl td.chc{font-weight:700}
.ltbl td.spc{width:74px;padding:4px 6px}.ltbl td.spc .spark{height:22px;margin:0;width:68px}
.ltbl td.rt{font-size:10.5px;color:var(--mut);white-space:nowrap}
.seebtn{font:700 11px/1 inherit;font-family:inherit;background:rgba(63,189,241,.12);border:1px solid rgba(63,189,241,.4);color:var(--cyan);border-radius:7px;padding:6px 9px;cursor:pointer;white-space:nowrap}
.ltbl th.stk,.ltbl td.stk{position:sticky;right:0;background:var(--panel);box-shadow:-6px 0 8px -6px rgba(0,0,0,.6)}.ltbl th.stk{background:var(--panel2)}.ltbl tr.lr:hover td.stk{background:var(--panel3)}.ltbl tr.lr.open td.stk{background:var(--panel3)}
.seebtn:hover{background:rgba(63,189,241,.24)}
tr.lr.open .seebtn{background:rgba(63,189,241,.28)}
.ltbl tr.lx td{padding:0 10px 12px;background:rgba(63,189,241,.04);white-space:normal;text-align:left}
.ltbl tr.lx .card{max-width:520px;cursor:pointer}
.ltbl tr.lx .xrow{display:flex;gap:14px;align-items:flex-start;flex-wrap:wrap;padding-top:4px}
.ltbl tr.lx .xhint{font-size:11px;color:var(--mut2);max-width:260px;line-height:1.5;padding-top:6px}
.ltbl tr.lx .xhint b{color:var(--tx)}
.ltbl tr.lx .xhint .openbtn{display:inline-block;margin-top:8px;background:var(--cyan);color:var(--ink);border:none;border-radius:7px;padding:7px 11px;font-size:11.5px;font-weight:800;cursor:pointer}
body.searching .vtog{display:none}
/* ---- Prediction Markets: companies table ---- */
.pmtbl-wrap{grid-column:1/-1}
.pmtbl-wrap .ltwrap{border:none;border-radius:0;background:transparent;margin-top:8px}
.pmtbl{min-width:760px}
.pmtbl td{white-space:normal;vertical-align:top}
.pmtbl td.tkc{white-space:nowrap;vertical-align:middle}
.pmtbl td.pxc{white-space:nowrap;vertical-align:middle;font-size:12px}
.pmtbl td.nmk{text-align:center;vertical-align:middle;color:var(--mut);white-space:nowrap}
.pmtbl td.mks{text-align:left;min-width:320px}
.pmtbl td.mks .pmt-rows{margin-top:0;display:flex;flex-wrap:wrap;gap:3px 16px}
.pmtbl td.mks .pmt-r{grid-template-columns:8px auto auto;font-size:11px}
.pmtbl td.cbk{text-align:left;font-size:11px;color:var(--mut);max-width:260px}
.pmtbl td.cbk b{color:var(--tx)}
.pmtbl tr.lx td{padding:6px 12px 14px}
.pmtbl tr.lx td .pmbody{padding:0}

@media(max-width:700px){.ltbl{min-width:760px}}
.row2{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin-top:9px}
.row3{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;margin-top:6px}
.mini{background:var(--panel2);border:1px solid var(--bd);border-radius:8px;padding:6px 7px}
.mini .k{font-size:9px;color:var(--mut2);text-transform:uppercase;letter-spacing:.3px}
.mini .v{font-size:12.5px;font-weight:700;margin-top:1px}
.badges{display:flex;gap:5px;flex-wrap:wrap;margin-top:10px}
.b{font-size:10px;font-weight:700;padding:3px 7px;border-radius:6px;border:1px solid transparent}
.b.sb{background:rgba(47,191,113,.14);color:#4fd08a;border-color:rgba(47,191,113,.3)}
.b.buy{background:rgba(47,191,113,.10);color:#54c98a;border-color:rgba(47,191,113,.22)}
.b.hold{background:rgba(245,166,35,.13);color:var(--amb);border-color:rgba(245,166,35,.3)}
.b.sell{background:rgba(242,85,90,.13);color:var(--red);border-color:rgba(242,85,90,.3)}
.b.na{background:var(--chip);color:var(--mut2);border-color:var(--bd)}
.b.ins-buy{background:rgba(47,191,113,.12);color:#4fd08a;border-color:rgba(47,191,113,.28)}
.b.ins-sell{background:rgba(242,85,90,.10);color:#f2777b;border-color:rgba(242,85,90,.24)}
.b.ins-neu{background:var(--chip);color:var(--mut2);border-color:var(--bd)}
.ov{position:fixed;inset:0;background:rgba(4,6,11,.72);backdrop-filter:blur(3px);display:none;align-items:flex-start;justify-content:center;z-index:100;padding:26px 14px;overflow:auto}
.ov.on{display:flex}
.modal{background:var(--panel);border:1px solid var(--bd2);border-radius:16px;max-width:960px;width:100%;overflow:hidden}
.mh{padding:18px 20px;border-bottom:1px solid var(--bd);display:flex;justify-content:space-between;align-items:flex-start;gap:14px;background:linear-gradient(180deg,var(--panel3),var(--panel))}
.mh .t1{font-size:22px;font-weight:800}.mh .t2{color:var(--mut);font-size:13px;margin-top:2px}.mh .t3{color:var(--mut2);font-size:11px;margin-top:5px}
.mh .px2{text-align:right}.mh .px2 .p{font-size:24px;font-weight:800}.mh .px2 .c{font-size:14px;font-weight:700}
.close{background:var(--chip);border:1px solid var(--bd);color:var(--tx);border-radius:8px;width:30px;height:30px;cursor:pointer;font-size:16px;flex:none}
.mb{padding:18px 20px}
.sec-t{font-size:11px;text-transform:uppercase;letter-spacing:.7px;color:var(--cyan);font-weight:700;margin:18px 0 9px}.sec-t:first-child{margin-top:0}
.kpis{display:grid;grid-template-columns:repeat(auto-fill,minmax(110px,1fr));gap:8px}
.kpi{background:var(--panel2);border:1px solid var(--bd);border-radius:9px;padding:8px 10px}
.kpi .k{font-size:10px;color:var(--mut2);text-transform:uppercase;letter-spacing:.4px}.kpi .v{font-size:14px;font-weight:700;margin-top:2px}
.ot{display:grid;grid-template-columns:1fr 1fr;gap:12px}@media(max-width:640px){.ot{grid-template-columns:1fr}}
.otbox{border:1px solid var(--bd);border-radius:10px;padding:11px 13px;background:var(--panel2)}
.otbox.o{border-color:rgba(47,191,113,.25)}.otbox.t{border-color:rgba(242,85,90,.25)}
.otbox h4{margin:0 0 7px;font-size:12px}.otbox.o h4{color:#4fd08a}.otbox.t h4{color:var(--red)}
.otbox ul{margin:0;padding-left:16px}.otbox li{font-size:12.5px;color:var(--tx2);margin-bottom:5px}
.thesis{background:var(--panel2);border:1px solid var(--bd);border-left:3px solid var(--cyan);border-radius:8px;padding:11px 13px;font-size:13.5px;color:var(--tx2)}
.tech{display:grid;grid-template-columns:repeat(auto-fill,minmax(132px,1fr));gap:8px}
.desc{font-size:12.5px;color:var(--mut);line-height:1.55}
.own{display:flex;gap:8px;flex-wrap:wrap}
.own a{background:var(--chip);border:1px solid var(--bd);border-radius:8px;padding:8px 12px;font-size:12px;display:inline-flex;gap:6px;align-items:center}
.ownwrap{display:grid;grid-template-columns:1fr 1fr;gap:12px}@media(max-width:640px){.ownwrap{grid-template-columns:1fr}}
.ownbox{background:var(--panel2);border:1px solid var(--bd);border-radius:10px;padding:12px 13px}
.ownbox h4{margin:0 0 8px;font-size:12px;color:var(--tx);display:flex;justify-content:space-between;align-items:center}
.tbl{width:100%;border-collapse:collapse;font-size:11.5px}
.tbl td{padding:4px 4px;border-bottom:1px solid var(--bd);color:var(--tx2)}
.tbl td.r{text-align:right}
.cbuy{color:var(--grn);font-weight:700}.csell{color:var(--red);font-weight:700}.cneu{color:var(--mut)}
.hold-row{display:flex;justify-content:space-between;font-size:12px;padding:4px 0;border-bottom:1px solid var(--bd)}
.msg{border-bottom:1px solid var(--bd);padding:8px 0}.msg:last-child{border-bottom:none}
.msg .mu{font-size:11px;color:var(--cyan);font-weight:600}
.msg .mt{font-size:9px;padding:1px 6px;border-radius:5px;margin-left:6px}
.msg .mt.Bullish{background:rgba(47,191,113,.14);color:#4fd08a}.msg .mt.Bearish{background:rgba(242,85,90,.14);color:#f2777b}.msg .mt.Neutral{background:var(--chip);color:var(--mut2)}
.msg .mbody{font-size:12.5px;color:var(--tx2);margin-top:3px;white-space:pre-wrap}
.rsibar{height:6px;background:linear-gradient(90deg,#2fbf71 0%,#2fbf71 30%,var(--bar) 30%,var(--bar) 70%,#f2555a 70%,#f2555a 100%);border-radius:4px;position:relative;margin-top:6px}
.rsibar .dot{position:absolute;top:-3px;width:12px;height:12px;border-radius:50%;background:#fff;border:2px solid var(--bg);transform:translateX(-6px)}
/* chart */
.chartwrap{background:var(--panel2);border:1px solid var(--bd);border-radius:10px;padding:12px}
.tfbar{display:flex;gap:5px;flex-wrap:wrap;margin-bottom:10px}
.tf{background:var(--chip);border:1px solid var(--bd);color:var(--mut);border-radius:7px;padding:5px 10px;font-size:11px;font-weight:700;cursor:pointer}
.tf.on{background:rgba(63,189,241,.14);color:var(--cyan);border-color:rgba(63,189,241,.4)}
.chartmeta{display:flex;justify-content:space-between;font-size:11px;color:var(--mut2);margin-top:6px;flex-wrap:wrap;gap:8px}
canvas.pchart{width:100%;height:230px;display:block}
.tgtbar{position:relative;height:60px;margin:28px 6px 42px}
.tgttrack{position:absolute;top:27px;left:0;right:0;height:6px;background:var(--chip2);border-radius:4px}
.tgtrange{position:absolute;top:27px;height:6px;background:linear-gradient(90deg,#f2555a,#f5a623,#2fbf71);border-radius:4px;opacity:.55}
.tmk{position:absolute;top:22px;width:2px;height:16px;background:#8a95a9;transform:translateX(-1px);z-index:1}
.tmk.cur{background:#fff;height:24px;top:18px;z-index:2}
.tmk.hi{background:#2fbf71}.tmk.lo{background:#f2555a}.tmk.me{background:#3fbdf1}.tmk.md{background:#8a95a9}
.tmkl{position:absolute;bottom:20px;left:50%;transform:translateX(-50%);font-size:9px;color:var(--mut);text-align:center;white-space:nowrap;line-height:1.2}
.tmkl.below{bottom:auto;top:20px}
.tmkl.cur{color:#fff}.tmkl.hi{color:#4fd08a}.tmkl.lo{color:#f2777b}.tmkl.me{color:var(--cyan)}
.tmkl b{color:var(--tx);font-size:11px}
.tgtnums{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:2px}
.tgtnums .el{display:block;font-size:9px;color:var(--mut2);text-transform:uppercase;letter-spacing:.3px}
.tgtnums .ev{font-size:15px;font-weight:800}.tgtnums .ev small{font-size:10.5px;font-weight:600}
.rdist{display:flex;height:10px;border-radius:5px;overflow:hidden;margin-top:12px;background:var(--chip2)}
.rseg{height:100%}
.rleg{display:flex;gap:12px;flex-wrap:wrap;font-size:10.5px;color:var(--mut);margin-top:6px;align-items:center}
.rleg i{display:inline-block;width:8px;height:8px;border-radius:2px;margin-right:4px;vertical-align:middle}
.ediff{display:grid;grid-template-columns:1fr 1fr;gap:12px}@media(max-width:640px){.ediff{grid-template-columns:1fr}}
.ebox{background:var(--panel2);border:1px solid var(--bd);border-radius:10px;padding:11px 13px}
.ebox .el{font-size:10px;color:var(--mut2);text-transform:uppercase;letter-spacing:.4px}
.ebox .ev{font-size:15px;font-weight:800;margin-top:3px}
.ebox .es{font-size:12px;font-weight:700;margin-top:2px}
footer{margin-top:34px;border-top:1px solid var(--bd);padding-top:16px;color:var(--mut2);font-size:11.5px;line-height:1.7}footer b{color:var(--mut)}
.disc{margin-top:10px;color:var(--mut2);font-size:11px}
.mscibox{background:var(--panel2);border:1px solid rgba(245,166,35,.25);border-radius:8px;padding:9px 12px;margin-top:8px;color:var(--amb);font-size:11.5px}
/* search / catalog / add-to-list */
.addbtn{background:rgba(63,189,241,.14);border:1px solid rgba(63,189,241,.4);color:var(--cyan);border-radius:8px;padding:6px 11px;font-size:12px;font-weight:700;cursor:pointer;white-space:nowrap}
.addbtn:hover{background:rgba(63,189,241,.24)}
.addbtn.on{background:rgba(47,191,113,.14);border-color:rgba(47,191,113,.4);color:#4fd08a}
.addbtn.on:hover{background:rgba(242,85,90,.14);border-color:rgba(242,85,90,.4);color:#f2777b}
.card.browse{border-style:dashed;border-color:var(--bd2)}
.card.browse .cn{max-width:none;white-space:normal}
.bsector{font-size:10px;color:var(--mut2);text-transform:uppercase;letter-spacing:.4px;margin-top:8px}
.browserow{display:flex;justify-content:space-between;align-items:flex-end;gap:8px;margin-top:11px}
.browsehd{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap;border-bottom:1px solid var(--bd);padding-bottom:7px;margin:6px 0 12px}
.browsehd h2{font-size:15px;margin:0;font-weight:700;color:var(--cyan)}
.browsehd .bl{color:var(--mut);font-size:12px}
.notrk{font-size:10px;color:var(--mut2);background:var(--chip);border:1px solid var(--bd);border-radius:6px;padding:2px 6px}
.pendingbar{background:linear-gradient(180deg,var(--panel3),var(--panel2));border:1px solid rgba(63,189,241,.35);border-radius:12px;padding:12px 14px;margin:6px 0 16px;display:none}
.pendingbar.on{display:block}
.pendingbar .ph{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px}
.pendingbar .pt{font-size:13px;font-weight:700;color:var(--tx)}
.pendingbar .pt b{color:var(--cyan)}
.pendingbar .pd{font-size:11.5px;color:var(--mut);margin-top:2px}
.pchips{display:flex;gap:6px;flex-wrap:wrap;margin-top:10px}
.pchip{background:var(--chip);border:1px solid var(--bd2);border-radius:16px;padding:4px 6px 4px 11px;font-size:12px;font-weight:700;display:inline-flex;align-items:center;gap:7px}
.pchip .x{cursor:pointer;color:var(--mut2);background:var(--chip2);border-radius:50%;width:16px;height:16px;display:inline-flex;align-items:center;justify-content:center;font-size:11px}
.pchip .x:hover{color:var(--red)}
.copybtn{background:var(--cyan);color:var(--ink);border:none;border-radius:8px;padding:8px 13px;font-size:12px;font-weight:800;cursor:pointer}
.copybtn:hover{filter:brightness(1.08)}
.copybtn.done{background:var(--grn)}
.clrbtn{background:transparent;border:1px solid var(--bd2);color:var(--mut);border-radius:8px;padding:8px 12px;font-size:12px;cursor:pointer}
/* earnings rail */
.layout{display:grid;grid-template-columns:268px minmax(0,1fr) 300px;grid-template-areas:"er main nw";gap:16px;align-items:start}
.layout.noer{grid-template-columns:34px minmax(0,1fr) 300px}
.layout.nonw{grid-template-columns:268px minmax(0,1fr) 34px}
.layout.noer.nonw{grid-template-columns:34px minmax(0,1fr) 34px}
#maincol{grid-area:main}#earnrail{grid-area:er}#newsrail{grid-area:nw}
#maincol,.sector{min-width:0}
.rail{position:sticky;top:58px;max-height:calc(100vh - 70px);overflow-y:auto;overscroll-behavior:contain;scrollbar-width:thin;padding-right:3px;min-width:0}
.rhide{margin-left:auto;align-self:center;background:transparent;border:1px solid var(--bd);color:var(--mut2);border-radius:7px;padding:2px 7px;font:600 10.5px/1.4 inherit;font-family:inherit;cursor:pointer;white-space:nowrap}
.rhide:hover{color:var(--tx);border-color:var(--bd2)}
.railtab{display:none;align-items:center;justify-content:center;gap:6px;width:34px;min-height:170px;writing-mode:vertical-rl;background:var(--panel);border:1px solid var(--bd);border-radius:10px;color:var(--mut);font:600 12px/1 inherit;font-family:inherit;cursor:pointer;padding:12px 0}
.railtab:hover{color:var(--tx);border-color:var(--cyan)}
.layout.noer #earnrail .rbody,.layout.nonw #newsrail .rbody{display:none}
.layout.noer #earnrail .railtab,.layout.nonw #newsrail .railtab{display:flex}
@media(max-width:1279px){.layout,.layout.noer,.layout.nonw,.layout.noer.nonw{grid-template-columns:minmax(0,1fr);grid-template-areas:"main" "er" "nw"}
 .rail{position:static;max-height:none;overflow:visible}.railtab{writing-mode:horizontal-tb;width:auto;min-height:0;padding:9px 14px;justify-content:flex-start}}
/* news rail */
.erhd.nwhd h2{color:var(--cyan)}
.rail .erhd{flex-wrap:wrap;row-gap:2px}.rail .erhd h2{white-space:nowrap}.rail .erhd .rhide{order:2}.rail .erhd .bl{order:3;flex-basis:100%}
.nwfs{display:flex;gap:5px;flex-wrap:wrap;margin:-2px 0 9px}
.nwf{background:var(--card);border:1px solid var(--bd);color:var(--mut);border-radius:99px;padding:3px 9px;font:600 11px/1.3 inherit;font-family:inherit;cursor:pointer}
.nwf:hover{color:var(--tx)}.nwf.on{color:var(--cyan);border-color:var(--cyan)}
.nwi{background:var(--panel);border:1px solid var(--bd);border-left:3px solid var(--cyan);border-radius:10px;padding:9px 11px;margin-bottom:8px}
.nwi.macro{border-left-color:var(--amb)}
.nwm{font-size:10.5px;color:var(--mut2);display:flex;align-items:center;gap:6px;min-width:0}
.nwm .src{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;min-width:0}.nwm>span:not(.src):not(.nwd){white-space:nowrap;flex:0 0 auto}
.nwd{width:7px;height:7px;border-radius:50%;flex:0 0 7px;background:var(--mut2)}
.nwd.bull{background:var(--grn)}.nwd.sbull{background:color-mix(in srgb,var(--grn) 55%,var(--mut2))}
.nwd.bear{background:var(--red)}.nwd.sbear{background:color-mix(in srgb,var(--red) 55%,var(--mut2))}
.nwk{color:var(--amb);font-weight:700}
.nwt{display:block;color:var(--tx);font-size:12.5px;line-height:1.38;font-weight:600;text-decoration:none;margin:4px 0 6px;overflow-wrap:anywhere}
.nwt:hover{color:var(--cyan);text-decoration:underline}
.nwtk{display:flex;gap:4px;flex-wrap:wrap}
.nwc{font:700 10.5px/1.3 inherit;font-family:inherit;padding:1px 7px;border-radius:6px;cursor:pointer;background:var(--panel2);border:1px solid var(--bd2);color:var(--tx2)}
.nwc.bull,.nwc.sbull{color:var(--grn);border-color:color-mix(in srgb,var(--grn) 45%,transparent)}
.nwc.bear,.nwc.sbear{color:var(--red);border-color:color-mix(in srgb,var(--red) 45%,transparent)}
.nwe{font-size:12px;color:var(--mut);padding:10px 2px}
.nwsrc{font-size:10px;color:var(--mut2);margin:4px 0 6px;line-height:1.45}
.erhd{display:flex;align-items:baseline;gap:8px;border-bottom:1px solid var(--bd);padding-bottom:7px;margin-bottom:10px}
.erhd h2{font-size:14px;margin:0;font-weight:700;color:var(--amb)}
.erhd .bl{color:var(--mut2);font-size:11px}
.ercard{background:var(--panel);border:1px solid var(--bd);border-left:3px solid var(--amb);border-radius:11px;padding:11px 12px;margin-bottom:10px;cursor:pointer;transition:.13s}
.ercard:hover{border-color:var(--bd2);transform:translateY(-1px)}
.ercard .top{display:flex;justify-content:space-between;align-items:baseline}
.ercard .tk2{font-size:14px;font-weight:800}
.ercard .fp{font-size:10.5px;color:var(--mut2)}
.errow{display:flex;justify-content:space-between;align-items:center;margin-top:7px;font-size:11.5px}
.errow .lbl{color:var(--mut2);text-transform:uppercase;font-size:9.5px;letter-spacing:.4px;width:30px}
.errow .vals{color:var(--tx2);flex:1;text-align:right;margin-right:7px}
.errow .vals b{color:var(--tx)}
.bm{font-size:9.5px;font-weight:800;padding:2px 6px;border-radius:5px;min-width:52px;text-align:center}
.bm.beat{background:rgba(47,191,113,.15);color:#4fd08a}
.bm.miss{background:rgba(242,85,90,.15);color:#f2777b}
.ernote{font-size:10.5px;color:var(--mut);line-height:1.45;margin-top:7px;border-top:1px dashed var(--bd);padding-top:6px}
.errx{font-size:10px;font-weight:700;margin-top:6px}
/* ---- markets add ---- */
.mktbar{margin:8px 0 12px}
#mq{width:100%;box-sizing:border-box;background:var(--card);border:1px solid var(--bd);border-radius:10px;color:var(--tx);padding:9px 12px;font-size:12.5px;outline:none}
#mq:focus{border-color:var(--cyan)}
.mres{display:flex;flex-wrap:wrap;gap:7px;margin-top:8px}
.mchip{display:flex;align-items:center;gap:8px;background:var(--card);border:1px solid var(--bd);border-radius:10px;padding:7px 10px;font-size:11.5px;color:var(--tx)}
.mchip .mk{font-size:9.5px;font-weight:700;text-transform:uppercase;letter-spacing:.4px;border-radius:5px;padding:2px 6px}
.mk.index{background:rgba(56,189,248,.14);color:var(--cyan)}.mk.fx{background:rgba(167,139,250,.16);color:#c4b5fd}.mk.commodity{background:rgba(251,191,36,.14);color:#fcd34d}
.mk.rate{background:rgba(52,211,153,.14);color:#6ee7b7}.mk.crypto{background:rgba(251,146,60,.14);color:#fdba74}.mk.vol{background:rgba(242,85,90,.14);color:#f2777b}
.mchip .mt{color:var(--mut);font-size:10.5px}
.mchip .madd{margin-left:4px;font-weight:700;color:var(--cyan);cursor:pointer;border:1px solid rgba(56,189,248,.35);border-radius:6px;padding:3px 8px;white-space:nowrap}
.mchip .madd.on{color:var(--grn);border-color:rgba(47,191,113,.4)}
.mchip.live .madd{color:var(--mut);border-color:var(--bd);cursor:default}
.idx.hask{cursor:pointer;transition:border-color .15s,transform .15s}.idx.hask:hover{border-color:#7c3aed;transform:translateY(-1px)}
.ktag{background:rgba(124,58,237,.18);color:#c4b5fd;border:1px solid rgba(124,58,237,.45)}.b.ktag{background:rgba(118,185,0,.14);color:#b7e26b;border-color:rgba(118,185,0,.45)}
.kband{position:relative;height:14px;background:var(--bd);border-radius:7px;margin:8px 0 4px}.kband .kb{position:absolute;top:0;height:100%;background:linear-gradient(90deg,rgba(124,58,237,.55),rgba(167,139,250,.9),rgba(124,58,237,.55));border-radius:7px}
.kband .km{position:absolute;top:-4px;width:3px;height:22px;background:#fff;border-radius:2px}.kband .ks{position:absolute;top:-4px;width:3px;height:22px;background:var(--cyan);border-radius:2px}
.kax{display:flex;justify-content:space-between;font-size:10px;color:var(--mut2);font-variant-numeric:tabular-nums}
.engrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px;margin-top:8px}.enpanel{background:var(--panel2);border:1px solid var(--bd);border-radius:10px;padding:10px 12px;min-width:0}.enpanel .hbar{grid-template-columns:78px 1fr 40px}
body.searching #calendar,body.searching #predict,body.searching #research,body.searching #compute{display:none}
.idx.ghost{border-style:dashed;opacity:.75}
.idx.ghost .vl{color:var(--mut);font-size:12px}
/* ---- top tabs ---- */
.tabs{position:sticky;top:0;z-index:60;display:flex;gap:8px;align-items:center;padding:9px 2px;margin:0 0 10px;background:linear-gradient(180deg,var(--bg) 82%,transparent);backdrop-filter:blur(6px);overflow-x:auto;-webkit-overflow-scrolling:touch}
.tabbtn{flex:0 0 auto;font:600 12.5px/1 inherit;font-family:inherit;color:var(--mut);background:var(--card);border:1px solid var(--bd);border-radius:99px;padding:8px 14px;cursor:pointer;transition:.15s;white-space:nowrap}
.tabbtn:hover{color:var(--tx);border-color:var(--cyan)}
.tabbtn.on{color:var(--cyan);border-color:var(--cyan);background:rgba(56,189,248,.08)}
#strip,#board,#research,#browse,#earnrail,#newsrail{scroll-margin-top:64px}
/* ---- deep research ---- */
/* ---- events calendar ---- */
#calendar{margin:6px 0 14px;scroll-margin-top:64px}
.calhd{display:flex;align-items:baseline;gap:10px;margin:14px 0 8px;flex-wrap:wrap}
.calhd h2{font-size:15px;margin:0;color:var(--tx)}.calhd .bl{font-size:11px;color:var(--mut)}
.calfil{display:flex;gap:6px;flex-wrap:wrap;margin:0 0 10px}
.caldr{align-items:center;margin-top:-4px}
.caldr .lbl{font-size:10.5px;color:var(--mut2);text-transform:uppercase;letter-spacing:.5px;margin-right:2px}
.caldr .sep{width:1px;height:18px;background:var(--bd);margin:0 4px}
.caldr input[type=date]{background:var(--card);border:1px solid var(--bd);color:var(--tx);border-radius:8px;padding:5px 8px;font-size:11.5px;font-family:inherit;color-scheme:dark}
.caldr input[type=date]:focus{outline:none;border-color:var(--cyan)}
.caldr .cnt{font-size:11px;color:var(--mut2);margin-left:auto}
.caldr .cf.x{color:var(--red);border-color:rgba(242,85,90,.35)}
.cf{font:600 11px/1 inherit;font-family:inherit;color:var(--mut);background:var(--card);border:1px solid var(--bd);border-radius:99px;padding:6px 11px;cursor:pointer}
.cf:hover{color:var(--tx);border-color:var(--cyan)}.cf.on{color:var(--cyan);border-color:var(--cyan);background:rgba(56,189,248,.08)}
.calday{display:grid;grid-template-columns:86px 1fr;gap:10px;padding:10px 0;border-top:1px solid var(--bd)}
.calday.today{border-top:2px solid var(--cyan)}
.cald{position:sticky;top:58px;align-self:start}
.cald .dn{font-size:22px;font-weight:800;line-height:1;color:var(--tx);font-variant-numeric:tabular-nums}
.cald .dm{font-size:10.5px;text-transform:uppercase;letter-spacing:.6px;color:var(--mut)}
.cald .dw{font-size:10.5px;color:var(--mut2)}
.calday.past .cald .dn{color:var(--mut)}
.calev{background:var(--card);border:1px solid var(--bd);border-radius:10px;padding:9px 11px;margin-bottom:7px}
.calev.key{border-left:3px solid var(--amb)}
.calev.corp.imp3{border-left:3px solid var(--pur)}
.calev.past{opacity:.92}
.cet{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.cet .ti{font-weight:700;font-size:13px;color:var(--tx)}
.cet .tm{font-size:10.5px;color:var(--mut2);font-variant-numeric:tabular-nums}
.cet .src{font-size:10px;color:var(--mut2);margin-left:auto}
.cp{font-size:9.5px;font-weight:800;letter-spacing:.5px;border-radius:5px;padding:2.5px 6px;text-transform:uppercase}
.cp.us{color:#38bdf8;background:rgba(56,189,248,.12)}.cp.jp{color:#fb7185;background:rgba(251,113,133,.14)}.cp.eu{color:#60a5fa;background:rgba(96,165,250,.14)}.cp.corp{color:#c4b5fd;background:rgba(167,139,250,.16)}
.cp.keyt{color:var(--amb);background:rgba(245,166,35,.12)}.cp.est{color:var(--mut);background:rgba(138,149,169,.12);text-transform:none;letter-spacing:0}
.cp.rep{color:var(--grn);background:rgba(47,191,113,.12)}
.cet .tk3{font-weight:800;color:var(--cyan);cursor:pointer}
.cmt{width:100%;border-collapse:collapse;margin-top:7px;font-size:11.5px}
.cmt th{font-size:9.5px;text-transform:uppercase;letter-spacing:.5px;color:var(--mut2);font-weight:700;text-align:right;padding:2px 6px;border-bottom:1px solid var(--bd)}
.cmt th:first-child{text-align:left}
.cmt td{padding:3px 6px;text-align:right;}.pmcard .cmt td{text-align:left;white-space:normal;font-variant-numeric:tabular-nums;color:var(--mut);white-space:nowrap}
.cmt td:first-child{text-align:left;color:var(--tx);white-space:normal}
.cmt td.act{color:var(--tx);font-weight:700}
.cmt .vs{font-size:9.5px;font-weight:800;border-radius:4px;padding:1px 5px;margin-left:5px}
.vs.above{color:var(--amb);background:rgba(245,166,35,.12)}.vs.below{color:var(--cyan);background:rgba(56,189,248,.12)}.vs.inline{color:var(--mut);background:rgba(138,149,169,.12)}
.vs.beat{color:var(--grn);background:rgba(47,191,113,.12)}.vs.miss{color:var(--red);background:rgba(242,85,90,.12)}
.cnote{font-size:11px;color:var(--mut);line-height:1.5;margin-top:6px}
.cnote b{color:var(--tx)}
.calpast{margin:0 0 6px}.calpast summary{cursor:pointer;font-size:12px;color:var(--mut);padding:6px 0;list-style:none}
.calpast summary::before{content:'▸ ';color:var(--cyan)}.calpast[open] summary::before{content:'▾ '}
.calmeta{font-size:10.5px;color:var(--mut2);margin-top:6px;line-height:1.5}
.calempty{background:var(--card);border:1px dashed var(--bd);border-radius:12px;padding:16px;font-size:12px;color:var(--mut)}
/* ---- kalshi strips + prediction markets ---- */
.kstrip{margin-top:7px;padding:6px 8px;border-radius:7px;background:rgba(168,85,247,.07);border:1px solid rgba(168,85,247,.25);font-size:11px;color:var(--mut);line-height:1.5}
.kstrip .klab{font-size:9.5px;font-weight:800;letter-spacing:.5px;text-transform:uppercase;color:#c4b5fd;margin-right:6px}
.kstrip b{color:var(--tx)}
.kearn{margin-top:7px;padding:7px 9px;border-radius:7px;background:rgba(168,85,247,.07);border:1px solid rgba(168,85,247,.25);font-size:11px;color:var(--mut);line-height:1.55}
.kearn .klab{font-size:9.5px;font-weight:800;letter-spacing:.5px;text-transform:uppercase;color:#c4b5fd;margin-right:6px}
.kearn b{color:var(--tx)}.kearn .ksum{display:block}.kearn .ksum .sep{color:var(--mut2);margin:0 5px}
.kearn details{margin-top:5px}.kearn summary{cursor:pointer;color:#c4b5fd;font-weight:700;font-size:10.5px;list-style:none;display:inline-flex;align-items:center;gap:5px;user-select:none}
.kearn summary::-webkit-details-marker{display:none}.kearn summary::before{content:'▸';font-size:10px;transition:transform .15s}.kearn details[open] summary::before{transform:rotate(90deg)}
.kearn .kgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:10px;margin-top:8px}
.kcall{display:grid;grid-template-columns:96px 1fr 40px 62px;gap:7px;align-items:center;font-size:11px;color:var(--mut);margin:3px 0}
.kcall .kl{color:var(--tx);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.kcall .kt{height:7px;background:var(--bd);border-radius:4px;overflow:hidden}.kcall .kt i{display:block;height:100%;border-radius:4px;background:linear-gradient(90deg,#7c3aed,#c084fc)}
.kcall .kv{text-align:right;font-variant-numeric:tabular-nums;color:var(--tx);font-weight:700}.kcall .kd{font-size:10px;color:var(--mut2);white-space:nowrap;display:flex;align-items:center;gap:4px;justify-content:flex-end}
.kcall .kd.up{color:var(--grn)}.kcall .kd.dn{color:var(--red)}.kspark{width:44px;height:12px;flex:none}
.kcallhd{font-size:11.5px;font-weight:700;color:var(--tx);margin:8px 0 3px}.kcallhd small{font-weight:400;color:var(--mut2);margin-left:6px}
.kbars{display:flex;gap:4px;margin-top:8px;align-items:flex-end;height:auto;min-height:34px;padding-top:2px;border-top:1px dashed rgba(168,85,247,.2)}
.kline{display:block}
.kb{flex:1;display:flex;flex-direction:column;justify-content:flex-end;align-items:center;gap:2px;min-width:0}
.kb i{display:block;width:100%;background:linear-gradient(180deg,#a78bfa,#7c3aed);border-radius:3px 3px 0 0;min-height:1px}
.kb span{font-size:8.5px;color:var(--mut2);white-space:nowrap;font-variant-numeric:tabular-nums}
.kb.on i{background:linear-gradient(180deg,#f0abfc,#a855f7)}.kb.on span{color:#e9d5ff}
#predict{margin:6px 0 14px;scroll-margin-top:64px}
#settled{margin:6px 0 14px;scroll-margin-top:64px}
/* ---- compute market (Ornn) ---- */
#compute{margin:6px 0 14px;scroll-margin-top:64px}
.cmphd{display:flex;align-items:baseline;gap:10px;margin:14px 0 8px;flex-wrap:wrap}.cmphd h2{font-size:15px;margin:0;color:var(--tx)}.cmphd .bl{font-size:11px;color:var(--mut)}
.cmpsub{font-size:12px;font-weight:700;color:var(--tx);margin:14px 0 8px;display:flex;align-items:baseline;gap:8px;flex-wrap:wrap}.cmpsub span{font-size:10.5px;font-weight:400;color:var(--mut2)}
.cmptiles{display:grid;grid-template-columns:repeat(auto-fill,minmax(172px,1fr));gap:8px}
.cmpt{background:var(--panel);border:1px solid var(--bd);border-radius:10px;padding:9px 11px;min-width:0;border-top:3px solid var(--c)}
.cmpt .nm{font-size:11px;color:var(--mut);display:flex;justify-content:space-between;gap:6px}.cmpt .nm b{color:var(--tx);font-size:12px}
.cmpt .vl{font-size:18px;font-weight:800;margin-top:3px;font-variant-numeric:tabular-nums}.cmpt .vl small{font-size:10px;color:var(--mut2);font-weight:600;margin-left:3px}
.cmpt .chg{display:grid;grid-template-columns:repeat(4,1fr);gap:2px;margin-top:5px;font-size:10.5px;font-weight:700;font-variant-numeric:tabular-nums}
.cmpt .chg i{display:block;font-style:normal;font-size:8.5px;color:var(--mut2);font-weight:600;text-transform:uppercase;letter-spacing:.3px}
.cmpt svg{display:block;width:100%;height:26px;margin-top:6px}
.cmpt .kx{margin-top:6px;padding-top:5px;border-top:1px dashed var(--bd);font-size:10.5px;color:var(--mut);line-height:1.45}.cmpt .kx b{color:var(--tx)}.cmpt .kx .kl{font-size:8.5px;font-weight:800;letter-spacing:.5px;text-transform:uppercase;color:#c4b5fd;margin-right:4px}
:root[data-theme=light] .cmpt .kx .kl{color:#5a2fc0}
.cmpcard{background:var(--card);border:1px solid var(--bd);border-radius:12px;padding:12px 14px;margin-top:10px;min-width:0}
.cmpbar{display:flex;gap:6px;flex-wrap:wrap;align-items:center;margin-bottom:8px}.cmpbar .lbl{font-size:10px;color:var(--mut2);text-transform:uppercase;letter-spacing:.5px;margin-right:2px}.cmpbar .sep{width:1px;height:16px;background:var(--bd);margin:0 4px}
.cmpwrap{position:relative}.cmpwrap svg{width:100%;height:auto;display:block}
.cmptip{position:absolute;top:6px;pointer-events:none;background:var(--panel3);border:1px solid var(--bd2);border-radius:8px;padding:6px 9px;font-size:11px;color:var(--tx);white-space:nowrap;display:none;z-index:3;box-shadow:0 4px 14px rgba(0,0,0,.35);font-variant-numeric:tabular-nums}
.cmptip .d{color:var(--mut);font-size:10px;margin-bottom:3px}.cmptip i{display:inline-block;width:8px;height:8px;border-radius:2px;margin-right:5px}
.cmpleg{display:flex;gap:12px;flex-wrap:wrap;font-size:11px;color:var(--mut);margin-top:6px}.cmpleg span{cursor:pointer;user-select:none}.cmpleg span.off{opacity:.35;text-decoration:line-through}.cmpleg i{display:inline-block;width:10px;height:3px;border-radius:2px;margin-right:5px;vertical-align:middle}
.cmptbl{min-width:820px}.cmptbl td.tkc .dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:7px;vertical-align:middle}
.cmptbl td.kxc{white-space:normal;text-align:left;font-size:10.5px;color:var(--mut);min-width:170px;line-height:1.4}.cmptbl td.kxc b{color:var(--tx)}.cmptbl td.kxc .am{color:var(--amb)}
.cmptbl td.rng{font-size:11px;color:var(--mut)}
.cmptbl tr.lx .xrow{display:flex;gap:14px;align-items:flex-start;flex-wrap:wrap;padding-top:6px}.cmptbl tr.lx .cmpt{width:300px;flex:none}.cmptbl tr.lx .cmpcard{flex:1;min-width:280px;margin-top:0}
.cmpnote{font-size:10.5px;color:var(--mut2);line-height:1.55;margin-top:8px}.cmpnote b{color:var(--mut)}

.sthd{display:flex;align-items:baseline;gap:10px;margin:14px 0 8px;flex-wrap:wrap}.sthd h2{font-size:15px;margin:0;color:var(--tx)}.sthd .bl{font-size:11px;color:var(--mut)}
.stsum{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 12px}
.stsum .pmchip b{font-size:13px}
.sttbl td.q{white-space:normal;text-align:left;min-width:220px;font-size:11.5px;color:var(--mut)}
.sttbl td.q b{color:var(--tx);font-size:12.5px;display:block}
.sttbl td.oc{white-space:normal;text-align:left;max-width:280px;font-size:11.5px}
.sttbl td.oc b{color:var(--tx)}
.sttbl td.hit{text-align:center}
.hitpill{font-size:10px;font-weight:800;border-radius:6px;padding:3px 7px;white-space:nowrap}
.hitpill.y{background:rgba(47,191,113,.15);color:#4fd08a}.hitpill.n{background:rgba(242,85,90,.15);color:#f2777b}.hitpill.p{background:rgba(245,166,35,.13);color:var(--amb)}.hitpill.na{background:var(--chip);color:var(--mut2)}
.sttbl tr.lx td{padding:6px 12px 14px}
.stx{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:12px}
.stcat{margin:14px 0 6px;font-size:12.5px;font-weight:700;color:var(--cyan);letter-spacing:.3px}
.stgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:12px}
details.stfold{background:var(--card);border:1px solid var(--bd);border-radius:12px;min-width:0}
details.stfold[open]{grid-column:1/-1}
details.stfold>summary{list-style:none;cursor:pointer;padding:13px 14px;user-select:none}details.stfold>summary::-webkit-details-marker{display:none}
details.stfold>summary:hover{background:rgba(63,189,241,.04)}details.stfold[open]>summary{border-bottom:1px solid var(--bd)}
.stf-h{display:flex;align-items:center;gap:10px}.stf-t{font-weight:800;font-size:14px;color:var(--tx)}
.stf-n{font-size:15px;font-weight:800;color:#e9d5ff;background:rgba(168,85,247,.14);border:1px solid rgba(168,85,247,.35);border-radius:99px;padding:2px 11px;font-variant-numeric:tabular-nums}
.stf-m{display:flex;justify-content:space-between;align-items:center;gap:8px;margin-top:6px;font-size:11px;color:var(--mut)}.stf-m b{color:var(--tx)}
details.stfold .stf-x::before{content:'▾ see more'}details.stfold[open] .stf-x::before{content:'▴ collapse'}
.stf-b{padding:8px 14px 14px}.stf-b .ltwrap{border:none;border-radius:0;background:transparent}
.pmhd{display:flex;align-items:baseline;gap:10px;margin:14px 0 8px;flex-wrap:wrap}
.pmhd h2{font-size:15px;margin:0;color:var(--tx)}.pmhd .bl{font-size:11px;color:var(--mut)}
.pmgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:12px}
.pmcard{background:var(--card);border:1px solid var(--bd);border-radius:12px;padding:13px 14px;min-width:0}
.pmcard.wide{grid-column:1/-1}
.pmcard.span2{grid-column:span 2}@media(max-width:700px){.pmcard.span2{grid-column:1/-1}}
.kb span:last-child{overflow:visible}
.pmsec{grid-column:1/-1;display:flex;align-items:baseline;gap:10px;margin:10px 0 -4px;padding-top:6px;border-top:1px dashed var(--bd)}
.pmsec h3{margin:0;font-size:12.5px;color:var(--tx);letter-spacing:.3px}.pmsec .bl{font-size:10.5px;color:var(--mut)}
details.pmfold{padding:0}details.pmfold[open]{grid-column:1/-1}
details.pmfold>summary{list-style:none;cursor:pointer;padding:12px 14px;display:block;user-select:none}details.pmfold>summary::-webkit-details-marker{display:none}
details.pmfold>summary:hover{background:rgba(168,85,247,.04)}details.pmfold[open]>summary{border-bottom:1px solid var(--bd)}
.pmbody{padding:6px 14px 13px}
.pmt-h{display:flex;align-items:center;gap:8px;flex-wrap:wrap}.pmt-tk{font-weight:800;font-size:14px;color:var(--tx);letter-spacing:.3px}.pmt-nm{font-size:11px;color:var(--mut);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:150px}
.pmt-n{font-size:10px;color:var(--mut2);white-space:nowrap}.pmt-m{display:flex;justify-content:space-between;align-items:center;gap:8px;margin-top:5px}
.pmx{font-size:10px;font-weight:700;color:#c4b5fd;white-space:nowrap;border:1px solid rgba(168,85,247,.35);border-radius:99px;padding:2px 8px}
.pmx::before{content:'▾ details'}details.pmfold[open] .pmx::before{content:'▴ collapse'}
.pmt-rows{margin-top:8px;display:flex;flex-direction:column;gap:4px}
.pmt-r{display:grid;grid-template-columns:8px 1fr auto;gap:7px;align-items:center;font-size:11px;color:var(--mut);line-height:1.35}
.pmt-r .dot{width:8px;height:8px;border-radius:50%;display:inline-block}.pmt-r b{color:var(--tx)}.pmt-r .mut{color:var(--mut2)}
.pmt-r .kd{font-size:10px;color:var(--mut2);white-space:nowrap;display:flex;align-items:center;gap:4px}.pmt-r .kd.up{color:var(--grn)}.pmt-r .kd.dn{color:var(--red)}
.pmt-call{margin-top:6px;font-size:11px;color:var(--mut);border-top:1px dashed var(--bd);padding-top:6px}.pmt-call b{color:var(--tx)}
.pmcard .pt{font-weight:700;font-size:13px;color:var(--tx)}
.pmcard .ps{font-size:10.5px;color:var(--mut2);margin:3px 0 8px}
.pmcard .pn{font-size:11px;color:var(--mut);line-height:1.5;margin-top:8px}
.pmcard .pn b{color:var(--tx)}
.pmchips{display:flex;gap:6px;flex-wrap:wrap;margin:6px 0 2px}
.pmchip{font-size:11px;background:rgba(168,85,247,.09);border:1px solid rgba(168,85,247,.28);color:#e9d5ff;border-radius:99px;padding:4px 9px;font-variant-numeric:tabular-nums}
.pmchip b{color:#fff}
.fedpath{display:grid;grid-template-columns:repeat(5,1fr);gap:8px;margin-top:6px}
.fm{text-align:center}
.fm .fl{font-size:11px;font-weight:700;color:var(--tx)}
.fm .fe{font-size:18px;font-weight:800;color:#e9d5ff;font-variant-numeric:tabular-nums;line-height:1.1;margin:3px 0}
.fm .fe small{font-size:9.5px;color:var(--mut2);font-weight:600;display:block}
.fstack{display:flex;height:10px;border-radius:5px;overflow:hidden;background:var(--bd);margin:6px 0 4px}
.fstack i{display:block;height:100%}
.fstack .cut{background:#38bdf8}.fstack .hold{background:#64748b}.fstack .hike{background:#f5a623}
.fm .fp{font-size:9.5px;color:var(--mut);font-variant-numeric:tabular-nums;white-space:nowrap}
.fm .fp b.hk{color:#f5a623}.fm .fp b.hd{color:#94a3b8}.fm .fp b.ct{color:#38bdf8}
.pmsvg{width:100%;height:auto;display:block;margin-top:6px}
.hbar{display:grid;grid-template-columns:110px 1fr 44px;gap:8px;align-items:center;font-size:11px;color:var(--mut);margin:4px 0}
.hbar .hl{color:var(--tx);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.hbar .ht{height:8px;background:var(--bd);border-radius:4px;overflow:hidden}.hbar .ht i{display:block;height:100%;background:linear-gradient(90deg,#7c3aed,#a78bfa);border-radius:4px}
.hbar .hv{text-align:right;font-variant-numeric:tabular-nums;color:var(--tx);font-weight:700}
.pmtile{display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-top:1px solid var(--bd);font-size:12px;color:var(--tx)}
.pmtile:first-of-type{border-top:0}
.pmtile .pv{font-size:18px;font-weight:800;color:#e9d5ff;font-variant-numeric:tabular-nums}
.pmtile .pvs{font-size:10px;color:var(--mut2)}
@media(max-width:700px){.fedpath{grid-template-columns:repeat(3,1fr)}}
#research{margin:6px 0 14px}
.reshd{display:flex;align-items:baseline;gap:10px;margin:14px 0 10px}
.reshd h2{font-size:15px;margin:0;color:var(--tx)}
.reshd .bl{font-size:11px;color:var(--mut)}
.resgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:12px}
.rescard{background:var(--card);border:1px solid var(--bd);border-radius:12px;padding:14px;transition:.15s;display:flex;flex-direction:column}
.resmore{margin-top:10px;align-self:flex-start;background:var(--chip);border:1px solid var(--bd);color:var(--cyan);border-radius:8px;padding:5px 10px;font-size:11.5px;font-weight:700;cursor:pointer}.resmore:hover{border-color:var(--cyan)}
.rescard.open{border-color:var(--bd2)}.resx{margin-top:6px}.resopen{cursor:pointer}.resopen:hover{text-decoration:underline}
.rescard:hover{border-color:var(--cyan);transform:translateY(-1px)}
.rescard .rt{font-weight:700;font-size:13.5px;color:var(--tx);line-height:1.35}
.rescard .rd{font-size:10.5px;color:var(--mut2);margin:5px 0 7px}
.rescard .rs{font-size:11.5px;color:var(--mut);line-height:1.5}
.rescard .rtk{display:flex;gap:5px;flex-wrap:wrap;margin-top:9px}
.rescard .rtk span{font-size:10px;font-weight:700;color:var(--cyan);background:rgba(56,189,248,.09);border-radius:5px;padding:2.5px 7px}
.resempty{background:var(--card);border:1px dashed var(--bd);border-radius:12px;padding:18px;font-size:12px;color:var(--mut);line-height:1.65}
.resbody{font-size:13px;line-height:1.65;color:var(--tx)}
.resbody h1,.resbody h2,.resbody h3{color:var(--tx);margin:16px 0 8px}
.resbody p{margin:8px 0}.resbody table{border-collapse:collapse;width:100%;font-size:12px}.resbody td,.resbody th{border:1px solid var(--bd);padding:5px 8px}
.resbody img{max-width:100%}
.rescard.wide{grid-column:1/-1}
.reskpis{display:grid;grid-template-columns:repeat(auto-fill,minmax(118px,1fr));gap:7px;margin-top:10px}
.rk{background:rgba(56,189,248,.05);border:1px solid var(--bd);border-radius:8px;padding:7px 9px}
.rkl{font-size:9.5px;color:var(--mut);text-transform:uppercase;letter-spacing:.4px}
.rkv{font-size:12.5px;font-weight:700;color:var(--tx);margin-top:2px}
.reschart{margin-top:12px;border:1px solid var(--bd);border-radius:10px;padding:10px 12px 8px;max-width:640px}
.rcl{font-size:10.5px;color:var(--mut);font-weight:600;margin-bottom:8px}
.rcbars{display:flex;align-items:flex-end;gap:14px;padding:0 4px}
.rcb{flex:1 1 0;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;min-width:0}
.rct{height:130px;width:100%;display:flex;align-items:flex-end;justify-content:center}
.rcstack{height:100%;width:100%;display:flex;flex-direction:column;justify-content:flex-end;align-items:center}
.rcv{font-size:11.5px;font-weight:700;color:var(--tx);margin-bottom:5px;white-space:nowrap}
.rcbar{width:100%;max-width:64px;background:var(--cyan);border-radius:5px 5px 2px 2px;transition:.2s}
.rcbar.est{background:rgba(56,189,248,.28);border:1.5px dashed var(--cyan);box-sizing:border-box}
.rcx{font-size:10.5px;color:var(--mut);margin-top:6px;white-space:nowrap}
.rescomm{margin:10px 0 0;padding-left:18px;font-size:11.5px;color:var(--mut);line-height:1.55}
.rescomm li{margin:3px 0}
.rescomm b{color:var(--tx)}
.resopen{margin-top:11px;font-size:11.5px;font-weight:700;color:var(--cyan)}
.reslink{margin-top:9px;padding:7px 9px;border:1px solid rgba(56,189,248,.35);background:rgba(56,189,248,.07);border-radius:8px;font-size:11px;color:var(--cyan);cursor:pointer;line-height:1.35}
.reslink:hover{background:rgba(56,189,248,.14);border-color:var(--cyan)}
.reslink b{color:var(--tx)}
</style></head><body>
<script>(function(){var t;try{t=localStorage.getItem('aiF_theme');}catch(e){}if(t==='light')document.documentElement.setAttribute('data-theme','light');})();</script><div class="wrap">
<header><div>
  <h1><span>◆</span> AI &amp; Frontier Tech <span style="color:var(--tx)">— Live Dashboard</span></h1>
  <div class="sub"><span id="cnt"></span> · global indices, 10Y yield &amp; macro · charts, earnings digests, ownership · <span id="asof"></span></div>
 </div><div class="pulse" id="pulse"></div></header>
<nav class="tabs" id="tabs">
 <button class="tabbtn" onclick="goTab(this,'strip')">📊 Markets</button>
 <button class="tabbtn" onclick="goTab(this,'board')">🗂 My List</button>
 <button class="tabbtn" onclick="goTab(this,'earnrail')">📊 Earnings Reports</button>
 <button class="tabbtn" onclick="goTab(this,'newsrail')">📰 News</button>
 <button class="tabbtn" onclick="goTab(this,'calendar')">📅 Calendar</button>
 <button class="tabbtn" onclick="goTab(this,'compute')">🖥 Compute</button>
 <button class="tabbtn" onclick="goTab(this,'predict')">🎯 Prediction Markets</button>
 <button class="tabbtn" onclick="goTab(this,'settled')">✅ Settled Markets</button>
 <button class="tabbtn" onclick="goTab(this,'research')">🔬 Deep Research</button>
 <button class="tabbtn" onclick="goTab(this,'browse');document.getElementById('q').focus()">🔎 Search &amp; Add</button>
</nav>
<div class="strip" id="strip"></div>
<div class="mktbar"><input id="mq" placeholder="＋ Add a market — search indices (DAX, Nifty, Hang Seng…), FX (EUR/USD, USD/JPY…), commodities (copper, nat gas…), rates, crypto…" oninput="renderMkt()"/><div class="mres" id="mres"></div></div>
<div class="controls">
 <input id="q" placeholder="Search your list + 6,500+ stocks (US-listed + KOSPI)…" oninput="render()"/>
 <select id="sort" onchange="render()">
  <option value="sector">Sort: by sector</option><option value="chg">Sort: % change ▼</option><option value="chgu">Sort: % change ▲</option>
  <option value="rsi">Sort: RSI ▼</option><option value="upside">Sort: analyst upside ▼</option><option value="sent">Sort: retail sentiment ▼</option><option value="mcap">Sort: market cap ▼</option>
 </select>
 <div class="vtog" id="vtog" title="My List layout"><button id="vt-table" onclick="setView('table')">☰ Table</button><button id="vt-cards" onclick="setView('cards')">▦ Cards</button></div>
 <div class="legend"><i><b style="color:var(--grn)">▲</b> up</i><i><b style="color:var(--red)">▼</b> down</i><i>RSI <b style="color:var(--grn)">&lt;30</b>/<b style="color:var(--red)">&gt;70</b></i><i>search a ticker → <b style="color:var(--cyan)">+ Add</b> to track it live</i></div>
</div>
<div class="pendingbar" id="pending"></div>
<div class="layout"><div id="maincol">
<div id="board"></div>
<div id="browse"></div>
<div id="calendar"></div>
<div id="compute"></div>
<div id="predict"></div>
<div id="settled"></div>
<div id="research"></div>
</div><aside id="earnrail" class="rail"></aside><aside id="newsrail" class="rail"></aside></div>
<footer>
 <div><b>Data sources:</b> Prices, technicals, analyst ratings &amp; fundamentals — Stocklake. VIX/breadth/fear-greed — Stocklake. Brent, Gold, Silver, BTC, ETH, 10Y Treasury — Alpha Vantage. News headlines &amp; sentiment labels — Alpha Vantage (links open the publisher). Retail sentiment &amp; messages — Stocktwits. Insider (Form 4), net buy/sell &amp; float — Massive/SEC. Institutional % &amp; top holders — Alpha Vantage (13F). Earnings digests — Bigdata.com. Compute prices (GPU rental $/GPU-hr and model-API $/M tokens) — Ornn OCPI / OTPI. Charts — Massive (~2yr daily, all names) + Alpha Vantage (monthly long-history for NVDA/MSFT/AMZN). Index levels via liquid ETF proxies where noted.</div>
 <div class="mscibox" id="mscibox"></div>
 <div style="margin-top:8px"><b>Snapshot:</b> <span id="asof2"></span>. 1D shows the latest session (intraday not entitled). 3Y/5Y/MAX show full history where monthly data exists, otherwise the ~2-year window (see chart date axis). Insider buy/sell covers open-market transactions since Feb 2026. Prices delayed; auto-refreshes on schedule. Opportunities/threats are qualitative, not recommendations.</div>
 <div class="disc">For informational purposes only. Not investment advice. Verify all figures against primary sources before acting.</div>
</footer></div>
<div class="ov" id="ov" onclick="if(event.target===this)closeM()"><div class="modal" id="modal"></div></div>
<script>
const DATA=__PAYLOAD__;const C=DATA.companies;const CAT=DATA.catalog||{};
const R=t=>C[t]||CAT[t];                 // resolve a ticker from tracked OR catalog
const isTracked=t=>!!C[t];
// ---- pending adds (persisted per-browser via localStorage) ----
const PKEY='af_pending_adds_v1';
function getPending(){try{const a=JSON.parse(localStorage.getItem(PKEY));return Array.isArray(a)?a.filter(t=>CAT[t]&&!C[t]):[];}catch(e){return[];}}
function setPending(a){try{localStorage.setItem(PKEY,JSON.stringify(a));}catch(e){}}
function addTick(t){const p=getPending();if(!p.includes(t)){p.push(t);setPending(p);}renderPending();render();syncModalAdd(t);}
function removeTick(t){setPending(getPending().filter(x=>x!==t));renderPending();render();syncModalAdd(t);}
function toggleTick(t){getPending().includes(t)?removeTick(t):addTick(t);}
const MKEY='af_pending_mkts_v1';const MCAT=DATA.markets_catalog||{};
const LIVEM=new Set(DATA.indices.map(i=>i.key));
function getPM(){try{const a=JSON.parse(localStorage.getItem(MKEY));return Array.isArray(a)?a.filter(k=>MCAT[k]&&!LIVEM.has(k)):[];}catch(e){return[];}}
function setPM(a){try{localStorage.setItem(MKEY,JSON.stringify(a));}catch(e){}}
function toggleMkt(k){const p=getPM();const i=p.indexOf(k);if(i>=0)p.splice(i,1);else p.push(k);setPM(p);renderPending();renderStripGhosts();renderMkt();}
function renderMkt(){
 const q=(document.getElementById('mq').value||'').trim().toLowerCase();const el=document.getElementById('mres');
 if(!q){el.innerHTML='';return;}
 const keys=Object.keys(MCAT).filter(k=>k.toLowerCase().includes(q)||MCAT[k].name.toLowerCase().includes(q)||MCAT[k].kind.includes(q)||(MCAT[k].region||'').toLowerCase().includes(q));
 if(!keys.length){el.innerHTML=`<span class="mchip"><span class="mt">No market matches “${q}” — ask me in chat and I'll add it to the catalog.</span></span>`;return;}
 const pm=getPM();
 el.innerHTML=keys.slice(0,24).map(k=>{const m=MCAT[k];const live=LIVEM.has(k);const on=pm.includes(k);
  return `<span class="mchip${live?' live':''}" title="${m.track}"><span class="mk ${m.kind}">${m.kind}</span><b>${m.name}</b><span class="mt">${m.region||''} · ${m.track}</span>${live?`<span class="madd">● live</span>`:`<span class="madd${on?' on':''}" onclick="toggleMkt('${k}')">${on?'✓ queued':'+ Add'}</span>`}</span>`;}).join('');
}
function renderStripGhosts(){
 const st=document.getElementById('strip');st.querySelectorAll('.idx.ghost').forEach(e=>e.remove());
 getPM().forEach(k=>{const m=MCAT[k];st.insertAdjacentHTML('beforeend',`<div class="idx ghost" title="${m.track}"><div class="nm"><span>${m.name}</span><span class="tag">${m.kind}</span></div><div class="vl">queued</div><div class="ch"><span class="flat" style="font-size:10px">send request to activate</span></div></div>`);});
}
function renderPending(){
 const p=getPending();const pm=getPM();const el=document.getElementById('pending');
 if(!p.length&&!pm.length){el.classList.remove('on');el.innerHTML='';return;}
 el.classList.add('on');
 const chips=p.map(t=>`<span class="pchip">${t} <span class="x" title="remove" onclick="removeTick('${t}')">✕</span></span>`).join('')
  +pm.map(k=>`<span class="pchip">${MCAT[k].name} <i style="opacity:.6;font-style:normal">${MCAT[k].kind}</i> <span class="x" title="remove" onclick="toggleMkt('${k}')">✕</span></span>`).join('');
 const n=p.length+pm.length;
 el.innerHTML=`<div class="ph"><div><div class="pt">★ Added — <b>${n}</b> item${n>1?'s':''} queued for live tracking${pm.length?` (${pm.length} market${pm.length>1?'s':''})`:''}</div>
   <div class="pd">These aren't refreshed yet. Send the request below to me (Claude) and I'll pull live data, build full cards, and fold them into your 3×/day refreshes.</div></div>
  <div style="display:flex;gap:8px;flex-wrap:wrap"><button class="copybtn" id="copybtn" onclick="copyReq()">⧉ Copy request for Claude</button><button class="clrbtn" onclick="if(confirm('Clear all queued adds?')){setPending([]);setPM([]);renderPending();render();renderStripGhosts();renderMkt();}">Clear</button></div></div>
  <div class="pchips">${chips}</div>`;
}
function copyReq(){
 const p=getPending();const pm=getPM();if(!p.length&&!pm.length)return;
 const names=p.map(t=>`${t} (${(CAT[t]||{}).name||''})`).join(', ');
 let msg='';
 if(p.length) msg+='Please add these tickers to my AI & Frontier Tech dashboard and track them live going forward: '+p.join(', ')+'. \n\nNames: '+names+'.';
 if(pm.length) msg+=(msg?'\n\n':'')+'Please also add these MARKETS to the Markets strip of my dashboard and track them live going forward: '+pm.map(k=>`${MCAT[k].name} [${k} · ${MCAT[k].kind} · ${MCAT[k].track}]`).join('; ')+'.';
 const done=()=>{const b=document.getElementById('copybtn');if(b){b.textContent='✓ Copied — paste into chat';b.classList.add('done');setTimeout(()=>{b.textContent='⧉ Copy request for Claude';b.classList.remove('done');},2600);}};
 if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(msg).then(done,()=>fallbackCopy(msg,done));}else{fallbackCopy(msg,done);}
}
function fallbackCopy(txt,cb){try{const ta=document.createElement('textarea');ta.value=txt;ta.style.position='fixed';ta.style.opacity='0';document.body.appendChild(ta);ta.select();document.execCommand('copy');document.body.removeChild(ta);cb&&cb();}catch(e){alert('Copy this to chat:\n\n'+txt);}}
function syncModalAdd(t){const b=document.getElementById('modaladd');if(b&&b.dataset.t===t){const on=getPending().includes(t);b.className='addbtn'+(on?' on':'');b.textContent=on?'✓ Queued — remove':'+ Add & track live';}}
const fmtB=n=>{if(n==null)return'—';const a=Math.abs(n);if(a>=1e12)return'$'+(n/1e12).toFixed(2)+'T';if(a>=1e9)return'$'+(n/1e9).toFixed(2)+'B';if(a>=1e6)return'$'+(n/1e6).toFixed(1)+'M';return '$'+Math.round(n).toLocaleString();};
const fmtV=n=>{if(n==null)return'—';const a=Math.abs(n);if(a>=1e9)return(n/1e9).toFixed(2)+'B';if(a>=1e6)return(n/1e6).toFixed(1)+'M';if(a>=1e3)return(n/1e3).toFixed(0)+'K';return ''+Math.round(n);};
const fmtSh=n=>{if(n==null)return'—';const a=Math.abs(n);if(a>=1e9)return(n/1e9).toFixed(2)+'B';if(a>=1e6)return(n/1e6).toFixed(2)+'M';if(a>=1e3)return(n/1e3).toFixed(1)+'K';return ''+Math.round(n);};
const pct=n=>n==null?'—':(n>=0?'+':'')+n.toFixed(2)+'%';
const px=n=>n==null?'—':'$'+n.toLocaleString(undefined,{minimumFractionDigits:2,maximumFractionDigits:2});
const cls=n=>n==null?'flat':n>0?'up':n<0?'down':'flat';
const ratingClass=r=>({strong_buy:'sb',buy:'buy',hold:'hold',sell:'sell',strong_sell:'sell'})[r]||'na';
const ratingTxt=r=>r?r.replace('_',' ').replace(/\b\w/g,c=>c.toUpperCase()):'N/A';
function rsiColor(r){if(r==null)return'var(--mut)';if(r<30)return'var(--grn)';if(r>70)return'var(--red)';return'var(--tx)';}
function sentClass(s){if(!s)return'na';if(s.score>=60)return'sb';if(s.score>=45)return'hold';return'sell';}
function upside(c){const t=(c.atgt&&c.atgt.consensus)||c.analyst_target;if(t&&c.price)return (t-c.price)/c.price*100;return null;}
function atgtBar(c){
 const A=c.atgt; if(!A||!A.consensus)return '';
 const price=c.price; const up=t=>t==null?null:((t-price)/price*100);
 const segs=[['sb','Strong Buy','#16a34a'],['b','Buy','#2fbf71'],['h','Hold','#f5a623'],['s','Sell','#f2555a'],['ss','Strong Sell','#b91c1c']];
 const n=A.n||0;
 const rbar=n?'<div class="rdist">'+segs.map(([k,l,col])=>{const v=A[k]||0;return v?`<div class="rseg" style="width:${(v/n*100)}%;background:${col}" title="${l}: ${v}"></div>`:'';}).join('')+'</div>':'';
 const rleg=n?'<div class="rleg">'+segs.filter(([k])=>A[k]).map(([k,l,col])=>`<span><i style="background:${col}"></i>${l} ${A[k]}</span>`).join('')+`<span style="margin-left:auto;color:var(--mut2)">${n} analysts · consensus ${A.cons||'—'}</span></div>`:'';
 const upc=up(A.consensus);
 if(!A.has_range){
  return `<div class="sec-t">Analyst Price Targets</div><div class="chartwrap"><div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:4px"><span class="pill">Consensus <b>$${Math.round(A.consensus)}</b> <span class="${upc>=0?'up':'down'}">${upc>=0?'+':''}${upc.toFixed(0)}%</span></span><span class="pill" style="color:var(--mut2)">High/low targets N/A for this listing</span></div>${rbar}${rleg}</div>`;
 }
 const lo=Math.min(A.low,price),hi=Math.max(A.high,price);const span=(hi-lo)||1;const pos=v=>((v-lo)/span*100);
 const mk=(v,label,cls,below)=>`<div class="tmk ${cls}" style="left:${pos(v).toFixed(1)}%"><div class="tmkl ${below?'below':''} ${cls}">${label}<br><b>$${Math.round(v)}</b></div></div>`;
 return `<div class="sec-t">Analyst Price Targets <span style="color:var(--mut2);font-weight:400;text-transform:none;letter-spacing:0">· ${A.n} analysts · as of ${(A.consensus,DATA.as_of)}</span></div>
 <div class="chartwrap">
  <div class="tgtbar">
   <div class="tgttrack"></div>
   <div class="tgtrange" style="left:${pos(A.low)}%;width:${(pos(A.high)-pos(A.low)).toFixed(1)}%"></div>
   ${mk(A.low,'Low','lo',true)}${A.median?mk(A.median,'Median','md',false):''}${mk(A.consensus,'Mean','me',true)}${mk(A.high,'High','hi',false)}
   <div class="tmk cur" style="left:${pos(price)}%"><div class="tmkl below cur">Price<br><b>$${price.toFixed(2)}</b></div></div>
  </div>
  <div class="tgtnums">
   <div><span class="el">High</span><span class="ev up">$${Math.round(A.high)} <small>${up(A.high)>=0?'+':''}${up(A.high).toFixed(0)}%</small></span></div>
   <div><span class="el">Consensus</span><span class="ev ${upc>=0?'up':'down'}">$${Math.round(A.consensus)} <small>${upc>=0?'+':''}${upc.toFixed(0)}%</small></span></div>
   <div><span class="el">Median</span><span class="ev">${A.median?'$'+Math.round(A.median):'—'}</span></div>
   <div><span class="el">Low</span><span class="ev ${up(A.low)>=0?'up':'down'}">$${Math.round(A.low)} <small>${up(A.low)>=0?'+':''}${up(A.low).toFixed(0)}%</small></span></div>
  </div>
  ${rbar}${rleg}
 </div>`;
}
const CODE={P:'Buy (open mkt)',S:'Sell (open mkt)',A:'Grant/RSU',F:'Tax withhold',M:'Option exercise',G:'Gift',D:'Disposition',C:'Convert',X:'Exercise'};
function insChip(ins){if(!ins||!ins.signal)return'';var s=ins.signal;var cl=s.indexOf('buying')>=0?'ins-buy':s.indexOf('selling')>=0?'ins-sell':'ins-neu';return '<span class="b '+cl+'">Insiders: '+s+'</span>';}
const mp=DATA.market_pulse;
const _vixT=(DATA.indices.find(i=>i.key==='VIX')||{}).value;
const _t10=(DATA.indices.find(i=>i.key==='UST10Y')||{}).value;
function isLight(){return document.documentElement.getAttribute('data-theme')==='light';}
function themeLabel(){return isLight()?'☀️ Light':'🌙 Dark';}
function toggleTheme(){const n=isLight()?'dark':'light';if(n==='light')document.documentElement.setAttribute('data-theme','light');else document.documentElement.removeAttribute('data-theme');try{localStorage.setItem('aiF_theme',n);}catch(e){}document.getElementById('thm').innerHTML='<b>'+themeLabel()+'</b>';const ov=document.getElementById('ov');if(ov&&ov.classList.contains('on')&&window._lastModal)openM(window._lastModal);}
document.getElementById('pulse').innerHTML=`<span class="pill thbtn" id="thm" onclick="toggleTheme()" title="Switch between dark (default) and light"><b>${themeLabel()}</b></span><span class="pill">VIX <b>${_vixT!=null?_vixT:mp.vix}</b></span><span class="pill">10Y <b>${_t10!=null?_t10.toFixed(2)+'%':'—'}</b></span><span class="pill">Fear/Greed <b style="color:var(--amb)">${mp.fear_greed.value} ${mp.fear_greed.label}</b></span><span class="pill">Breadth <b>${mp.breadth.overbought_pct}%</b> ob / <b>${mp.breadth.oversold_pct}%</b> os</span>`;
document.getElementById('cnt').textContent=DATA.sectors.flatMap(s=>s.tickers).length+' tracked names · '+DATA.sectors.length+' sectors · '+Object.keys(CAT).length+' more searchable';
document.getElementById('asof').innerHTML='as of '+DATA.as_of+' &nbsp;·&nbsp; <b style="color:#4ea1ff">⟳ Last refreshed: '+(DATA.generated||'').replace(/\s*\(.*\)/,'')+'</b>';
document.getElementById('asof2').textContent=DATA.generated;
document.getElementById('mscibox').textContent='MSCI: '+DATA.msci_note;
function idxVal(i){if(i.unit==='fx')return i.value.toFixed(i.dp==null?4:i.dp);if(i.unit==='pct')return i.value.toFixed(2)+'%';if(['$','$/oz','$/bbl'].includes(i.unit))return '$'+i.value.toLocaleString();return i.value.toLocaleString();}
document.getElementById('strip').innerHTML=DATA.indices.map(i=>{const c=i.chg;const KA=(DATA.kalshi&&DATA.kalshi.assets)||{};const hasK=!!KA[i.key];return `<div class="idx${hasK?' hask':''}" title="${hasK?'Click for Kalshi-implied price range':i.note}"${hasK?` onclick="assetModal('${i.key}')"`:''}><div class="nm"><span>${i.name}</span>${hasK?'<span class="tag ktag">Kalshi ▸</span>':(i.proxy&&i.proxy!==i.key?`<span class="tag">${i.proxy}</span>`:'')}</div><div class="vl">${idxVal(i)}</div><div class="ch ${cls(c)}">${c==null?'<span class="flat" style="font-size:10px">'+(i.anchor?'est. · anchored '+(i.anchor_date||'').slice(5).replace('-','/'):i.note)+'</span>':pct(c)}</div>${i.rsi?`<div class="rsi">RSI ${i.rsi}</div>`:''}</div>`;}).join('');

// ---- mini sparkline on cards (last ~60 daily pts) ----
function sparkSVG(tk){
 const c=R(tk); if(!c||!c.chart||!c.chart.d)return'';
 const pts=c.chart.d.slice(-60); if(pts.length<2)return'';
 const xs=pts.map(p=>p[0]), ys=pts.map(p=>p[1]);
 const mnx=xs[0],mxx=xs[xs.length-1],mny=Math.min(...ys),mxy=Math.max(...ys);
 const W=260,H=34;
 const up=ys[ys.length-1]>=ys[0];
 const path=pts.map((p,i)=>{const x=((p[0]-mnx)/(mxx-mnx||1))*W;const y=H-((p[1]-mny)/((mxy-mny)||1))*(H-4)-2;return (i?'L':'M')+x.toFixed(1)+' '+y.toFixed(1);}).join(' ');
 const col=up?'#2fbf71':'#f2555a';
 return `<svg class="spark" viewBox="0 0 ${W} ${H}" preserveAspectRatio="none"><path d="${path}" fill="none" stroke="${col}" stroke-width="1.5"/></svg>`;
}

function card(t){
 const c=C[t];const u=upside(c);const s=c.sentiment;
 return `<div class="card" onclick="openM('${t}')">
  <div class="top"><div><div class="tk">${t}</div><div class="cn">${c.name||''}</div></div>
   <div class="px"><div class="p">${px(c.price)}</div><div class="c ${cls(c.change_pct)}">${pct(c.change_pct)}</div></div></div>
  ${sparkSVG(t)}
  <div class="row2">
   <div class="mini"><div class="k">RSI</div><div class="v" style="color:${rsiColor(c.rsi)}">${c.rsi??'—'}</div></div>
   <div class="mini"><div class="k">Fwd P/E</div><div class="v">${c.pe_forward?Math.round(c.pe_forward):'—'}</div></div>
   <div class="mini"><div class="k">Cons. Target</div><div class="v">${(c.atgt&&c.atgt.consensus)?'$'+Math.round(c.atgt.consensus):(c.analyst_target?'$'+Math.round(c.analyst_target):'—')}</div></div>
   <div class="mini"><div class="k">Upside</div><div class="v ${cls(u)}">${u==null?'—':(u>=0?'+':'')+u.toFixed(0)+'%'}</div></div>
  </div>
  <div class="row3">
   <div class="mini"><div class="k">Vol</div><div class="v">${fmtV(c.volume)}</div></div>
   <div class="mini"><div class="k">10d Avg${c.vol10_exact?'':' ≈'}</div><div class="v">${fmtV(c.vol10)}</div></div>
   <div class="mini"><div class="k">Mkt Cap</div><div class="v">${fmtB(c.market_cap)}</div></div>
  </div>
  <div class="badges">
   <span class="b ${ratingClass(c.analyst_rating)}">${ratingTxt(c.analyst_rating)}${c.analyst_count?' · '+c.analyst_count:''}</span>
   ${s?`<span class="b ${sentClass(s)}">ST ${s.score} ${s.label.replace('EXTREMELY_','X-')}</span>`:''}
   ${insChip(c.insider)}${pmBadge(t)}
  </div>${researchLink(t)}</div>`;
}
function pmFor(t){const S=DATA.kalshi&&DATA.kalshi.stock_pm;return S&&S[t]&&S[t].markets&&S[t].markets.length?S[t]:null;}
function pmU(m){const f=(m&&m.fmt)||'usd2';
 if(f==='bn')return v=>v==null?'—':(Number(v)/1e9).toFixed(2)+'B';
 if(f==='mn')return v=>v==null?'—':(Number(v)/1e6).toFixed(1)+'M';
 if(f==='usdbn')return v=>v==null?'—':'$'+(Number(v)/1e9).toFixed(1)+'B';
 if(f==='gw')return v=>v==null?'—':Number(v).toFixed(1)+' GW';
 if(f==='gwh')return v=>v==null?'—':Number(v).toFixed(0)+' GWh';
 if(f==='int')return v=>v==null?'—':Math.round(Number(v)).toLocaleString();
 if(f==='pct0')return v=>v==null?'—':(Math.round(Number(v)*10)/10)+'%';
 if(f==='date')return v=>v==null?'—':new Date(v+'T12:00:00Z').toLocaleDateString('en',{month:'short',day:'numeric',year:'numeric',timeZone:'UTC'});
 if(f==='year')return v=>v==null?'—':String(v).slice(0,4);
 return v=>v==null?'—':'$'+Number(v).toFixed(2);}
function pmSettled(m){if(!m.settled)return '';const d=new Date(m.settled.d+'T12:00:00Z').toLocaleDateString('en',{month:'short',day:'numeric',timeZone:'UTC'});return `✓ settled ${(m.settled.outcome||'yes').toUpperCase()} ${d}`;}
function pmBadge(t){const B=pmFor(t);if(!B)return '';const m=B.markets[0];const F=pmU(m);
 if(m.settled)return `<span class="b ktag" title="Kalshi prediction markets tied to ${t} — open the card">◆ Kalshi · ${m.short} ${pmSettled(m)}</span>`;
 if(B.call&&B.call.items&&B.call.items.length&&B.call.date){const dd=(new Date(B.call.date+'T12:00:00Z')-Date.now())/864e5;if(dd>-2&&dd<10){const top=B.call.items.filter(i=>i.p<0.9)[0]||B.call.items[0];return `<span class="b ktag" title="Kalshi earnings-call mention odds for ${t} — open the card">◆ Kalshi · call ${B.call.when?B.call.when.split(' ')[0]:''}: ${top.label} ${kpct(top.p)}</span>`;}}
 const hl=m.kind==='date'?`${kpct(m.p_at)} by ${F(m.hist_strike)}`:m.p50[1]==='≤'?'<'+F(m.p50[0]):m.p50[1]==='≥'?'>'+F(m.p50[0]):'≈'+F(m.p50[0]);
 return `<span class="b ktag" title="Kalshi prediction markets tied to ${t} — open the card">◆ Kalshi · ${m.short} ${hl}</span>`;}
function pmSection(t){const B=pmFor(t);if(!B)return '';const cols=['#76b900','#22d3ee','#f59e0b','#a78bfa'];
 return `<div class="sec-t">Prediction Markets — Kalshi contracts tied to ${t}</div><div class="thesis" style="margin-bottom:10px">${B.theme||''}${B.why?' — '+B.why:''}</div><div class="engrid" style="grid-template-columns:repeat(auto-fit,minmax(260px,1fr))">${B.markets.map((m,i)=>{const col=cols[i%cols.length];const mx=Math.max(...m.ladder.map(x=>x[1]))||1;const H=m.history||[];const last=H[H.length-1],first=H[0];
  const F=pmU(m);const st=m.stat||'expected peak';const isD=m.kind==='date';
  const one=isD&&m.ladder.length===1;const c1=one?'':isD?`${st} <b>${m.p50[0]?'~'+F(m.p50[0]):'beyond the listed dates'}</b>`:`${st} <b>${m.p50[1]==='≤'?'below '+F(m.p50[0]):m.p50[1]==='≥'?'above '+F(m.p50[0]):'≈ '+F(m.p50[0])}</b>`;
  const c2=m.settled?`<span style="color:var(--grn)">${pmSettled(m)}</span>`:isD?`by ${F(m.hist_strike)}: <b>${last?kpct(last.p):'—'}</b>`:`tops ${F(m.hist_strike)}: <b>${last?kpct(last.p):'—'}</b>`;
  return `<div class="enpanel"><div class="pt" style="font-size:12.5px">${m.title}</div><div class="ps" style="font-size:11px;color:var(--mut)">Kalshi ${m.ev} · ${m.horizon}</div><div class="pmchips">${c1?`<span class="pmchip">${c1}</span>`:''}<span class="pmchip">${c2}${first&&last&&first.d!==last.d?` <span style="color:var(--mut2)">(${kpct(first.p)} on ${first.d.slice(5).replace('-','/')})</span>`:''}</span></div>${m.ladder.filter(x=>x[1]>=0.03).slice(0,8).map(x=>`<div class="hbar"><span class="hl">${isD?'by':'&gt;'} ${F(x[0])}</span><span class="ht"><i style="width:${Math.max(1,x[1]/mx*100)}%;background:${col}"></i></span><span class="hv">${kpct(x[1])}</span></div>`).join('')}</div>`;}).join('')}</div>${(()=>{const ch=pmChart(B,t,DATA.kalshi,760,170);return ch?`<div style="margin-top:8px"><div class="ps" style="font-size:11px;color:var(--mut)">How the market's view has moved — implied probability over time</div>${ch.svg}${ch.legend}</div>`:'';})()}<div style="margin-top:8px;font-size:11px;color:var(--mut2)">Full ladders are in the Prediction Markets tab (${t} card). Market-implied probabilities (yes mid), read-only public data.</div>${B.call?`<div style="margin-top:10px">${callBlock(B,t,false)}</div>`:''}`;}
function researchIdx(t){const L=(typeof DR!=='undefined')?DR:(DATA.deep_research||[]);return L.findIndex(r=>(r.tickers||[]).includes(t));}
function researchLink(t){
 const i=researchIdx(t); if(i<0) return '';
 const r=DR[i];
 return `<div class="reslink" onclick="event.stopPropagation();openResearch(${i})" title="${r.title}">🔬 Deep Research: <b>${r.title.replace(/^.*?—\s*/,'')}</b> · ${r.date||''} → read</div>`;
}
function browseCard(t){
 const c=CAT[t];if(!c)return'';const on=getPending().includes(t);
 return `<div class="card browse" onclick="openM('${t}')">
  <div class="top"><div><div class="tk">${t}</div><div class="cn">${c.name||''}</div></div>
   <span class="notrk">not on your list</span></div>
  <div class="bsector">${c.sector||''}</div>
  <div class="browserow"><span class="pill" style="font-size:11px">${c.x?c.x:c.k?'KOSPI · Korea Exchange':c.b?'US-listed · broad catalog':'S&amp;P 500 / Nasdaq-100'}</span>
   <button class="addbtn${on?' on':''}" onclick="event.stopPropagation();toggleTick('${t}')">${on?'✓ Queued — remove':'+ Add &amp; track'}</button></div>
 </div>`;
}
// ---- My List view: compact table (default) or full card grid ----
const VKEY='aiF_listView';
let VIEW=(()=>{try{return localStorage.getItem(VKEY)||'table';}catch(e){return 'table';}})();
const OPEN=new Set();
function setView(v){VIEW=v;try{localStorage.setItem(VKEY,v);}catch(e){}render();}
function toggleRow(t){if(OPEN.has(t))OPEN.delete(t);else OPEN.add(t);
 const tr=document.getElementById('lr-'+t),tx=document.getElementById('lx-'+t);if(!tr||!tx)return;
 const on=OPEN.has(t);tr.classList.toggle('open',on);tx.hidden=!on;tr.querySelector('.seebtn').textContent=on?'Hide card':'See card';
 if(on&&!tx.dataset.done){tx.querySelector('td').innerHTML=`<div class="xrow">${card(t)}<div class="xhint"><b>${t}</b> — full card. Click the card (or the button) for the complete profile: price chart with timeframes, analyst targets &amp; rating distribution, earnings, technicals, ownership, insiders, retail sentiment${pmFor(t)?', Kalshi prediction markets':''}.<br><button class="openbtn" onclick="openM('${t}')">Open full profile ↗</button></div></div>`;tx.dataset.done='1';}}
function listRow(t){
 const c=C[t];const u=upside(c);const s=c.sentiment;const on=OPEN.has(t);const tg=(c.atgt&&c.atgt.consensus)?c.atgt.consensus:c.analyst_target;
 return `<tr class="lr${on?' open':''}" id="lr-${t}" onclick="toggleRow('${t}')">
  <td class="tkc">${t}<small>${c.name||''}</small></td>
  <td class="spc">${sparkSVG(t)}</td>
  <td class="pxc">${px(c.price)}</td>
  <td class="chc ${cls(c.change_pct)}">${pct(c.change_pct)}</td>
  <td style="color:${rsiColor(c.rsi)};font-weight:700">${c.rsi??'—'}</td>
  <td>${c.pe_forward?Math.round(c.pe_forward):'—'}</td>
  <td>${tg?'$'+Math.round(tg):'—'}<span class="${cls(u)}" style="font-size:10.5px;margin-left:5px">${u==null?'':(u>=0?'+':'')+u.toFixed(0)+'%'}</span></td>
  <td>${fmtV(c.volume)}</td>
  <td>${fmtV(c.vol10)}${c.vol10_exact?'':'<span style="color:var(--mut2)"> ≈</span>'}</td>
  <td>${fmtB(c.market_cap)}</td>
  <td class="rt"><span class="b ${ratingClass(c.analyst_rating)}" style="padding:2px 6px">${ratingTxt(c.analyst_rating)}</span>${pmFor(t)?' <span class="b ktag" style="padding:2px 6px" title="Kalshi markets tied to this stock">◆</span>':''}${researchIdx(t)>=0?' <span title="Deep Research available">🔬</span>':''}</td>
  <td class="c stk"><button class="seebtn" onclick="event.stopPropagation();toggleRow('${t}')">${on?'Hide card':'See card'}</button></td>
 </tr><tr class="lx" id="lx-${t}"${on?'':' hidden'}><td colspan="12"></td></tr>`;
}
function listTable(ts){
 return `<div class="ltwrap"><table class="ltbl"><thead><tr><th>Stock</th><th class="c">60d</th><th>Price</th><th>Day</th><th>RSI</th><th>Fwd P/E</th><th>Cons. target · upside</th><th>Volume</th><th>10d avg</th><th>Mkt cap</th><th>Rating</th><th class="c stk">Card</th></tr></thead><tbody>${ts.map(listRow).join('')}</tbody></table></div>`;
}
function render(){
 const q=document.getElementById('q').value.toLowerCase().trim();const sort=document.getElementById('sort').value;const board=document.getElementById('board');
 const match=t=>{const c=C[t];return !q||t.toLowerCase().includes(q)||(c.name||'').toLowerCase().includes(q);};
 const tb=document.getElementById('vt-table'),cb=document.getElementById('vt-cards');if(tb){tb.classList.toggle('on',VIEW==='table');cb.classList.toggle('on',VIEW!=='table');}
 const body=ts=>VIEW==='table'?listTable(ts):`<div class="grid">${ts.map(card).join('')}</div>`;
 if(sort==='sector'){
  board.innerHTML=DATA.sectors.map(sec=>{const ts=sec.tickers.filter(match);if(!ts.length)return'';return `<div class="sector"><div class="sechd"><h2>${sec.name}</h2><span class="bl">${sec.blurb}</span><span class="cnt">${ts.length}</span>${sec.avg_change!=null?`<span class="cnt" style="color:${sec.avg_change>=0?'var(--grn)':'var(--red)'}">avg ${pct(sec.avg_change)}</span>`:''}</div>${body(ts)}</div>`;}).join('')||'<div class="sub" style="padding:30px 0">No matches.</div>';
 }else{
  let ts=DATA.sectors.flatMap(s=>s.tickers).filter(match);
  const key={chg:t=>C[t].change_pct??-999,chgu:t=>-(C[t].change_pct??999),rsi:t=>C[t].rsi??-1,upside:t=>upside(C[t])??-999,sent:t=>C[t].sentiment?C[t].sentiment.score:-1,mcap:t=>C[t].market_cap??0}[sort];
  ts.sort((a,b)=>key(b)-key(a));board.innerHTML=body(ts);
 }
 for(const t of OPEN){const tx=document.getElementById('lx-'+t);if(tx&&!tx.dataset.done){OPEN.delete(t);toggleRow(t);}}
 renderBrowse(q);
 document.body.classList.toggle('searching',!!q);
}
function renderBrowse(q){
 const el=document.getElementById('browse');
 if(!q){
  const p=getPending();
  if(!p.length){el.innerHTML='';return;}
  el.innerHTML=`<div class="browsehd"><h2>★ My Added</h2><span class="bl">queued for live tracking · click a card to preview · use “Copy request for Claude” above to activate</span><span class="cnt" style="color:var(--mut2)">${p.length}</span></div><div class="grid">${p.map(browseCard).join('')}</div>`;
  return;
 }
 const keys=Object.keys(CAT).filter(t=>t.toLowerCase().includes(q)||(CAT[t].name||'').toLowerCase().includes(q));
 const rank=t=>{const base=t.toLowerCase()===q?0:t.toLowerCase().startsWith(q)?1:2;return base*2+((CAT[t].b||CAT[t].k||CAT[t].x)?1:0);};
 keys.sort((a,b)=>rank(a)-rank(b)||a.localeCompare(b));
 if(!keys.length){el.innerHTML=`<div class="browsehd"><h2>Add from the catalog</h2><span class="bl">No match for “${q}” among the ${Object.keys(CAT).length.toLocaleString()} searchable names (S&amp;P 500 · Nasdaq-100 · US small/mid caps · KOSPI). Try the ticker or part of the company name.</span></div>`;return;}
 const CAP=90;const shown=keys.slice(0,CAP);
 const more=keys.length>CAP?`<span class="bl">showing first ${CAP} of ${keys.length}</span>`:`<span class="bl">${keys.length} match${keys.length>1?'es':''}</span>`;
 el.innerHTML=`<div class="browsehd"><h2>Add from the catalog</h2><span class="bl">S&amp;P 500 · Nasdaq-100 · US small/mid caps · KOSPI — click <b style="color:var(--cyan)">+ Add</b> to queue for live tracking</span>${more}</div><div class="grid">${shown.map(browseCard).join('')}</div>`;
}
// ---- chart ----
let CUR=null;
const TFS=['1D','5D','1M','3M','6M','YTD','1Y','3Y','5Y','MAX'];
function tfWindow(tf,lastTs){
 const D=86400;const map={'5D':7*D,'1M':32*D,'3M':95*D,'6M':186*D,'1Y':372*D,'3Y':1105*D,'5Y':1835*D};
 if(tf==='YTD'){const d=new Date(lastTs*1000);return lastTs-Math.floor(Date.UTC(d.getUTCFullYear(),0,1)/1000);}
 return map[tf]||0;
}
function drawChart(t,tf){
 CUR={t,tf};const c=C[t];if(!c.chart)return;
 document.querySelectorAll('.tf').forEach(b=>b.classList.toggle('on',b.dataset.tf===tf));
 let base=c.chart.d;
 if((tf==='3Y'||tf==='5Y'||tf==='MAX')&&c.chart.m)base=c.chart.m;
 const lastTs=base[base.length-1][0];
 let pts;
 if(tf==='1D'){pts=c.chart.d.slice(-2);}
 else if(tf==='MAX'){pts=base;}
 else{const from=lastTs-tfWindow(tf,lastTs);pts=base.filter(p=>p[0]>=from);}
 if(!pts||pts.length<2)pts=base.slice(-2);
 const cv=document.getElementById('pchart');const meta=document.getElementById('chartmeta');
 const dpr=window.devicePixelRatio||1;const W=cv.clientWidth,H=cv.clientHeight;
 cv.width=W*dpr;cv.height=H*dpr;const ctx=cv.getContext('2d');ctx.scale(dpr,dpr);ctx.clearRect(0,0,W,H);
 const xs=pts.map(p=>p[0]),ys=pts.map(p=>p[1]);
 const mnx=xs[0],mxx=xs[xs.length-1],mny=Math.min(...ys),mxy=Math.max(...ys);
 const padL=6,padR=6,padT=10,padB=6;const cw=W-padL-padR,ch=H-padT-padB;
 const X=v=>padL+((v-mnx)/((mxx-mnx)||1))*cw;const Y=v=>padT+ch-((v-mny)/((mxy-mny)||1))*ch;
 const up=ys[ys.length-1]>=ys[0];const col=up?'#2fbf71':'#f2555a';
 // gridlines
 ctx.strokeStyle=isLight()?'rgba(0,0,0,0.07)':'rgba(255,255,255,0.05)';ctx.lineWidth=1;
 for(let i=0;i<=3;i++){const y=padT+ch*i/3;ctx.beginPath();ctx.moveTo(padL,y);ctx.lineTo(W-padR,y);ctx.stroke();}
 // area
 ctx.beginPath();ctx.moveTo(X(xs[0]),Y(ys[0]));for(let i=1;i<pts.length;i++)ctx.lineTo(X(xs[i]),Y(ys[i]));
 ctx.lineTo(X(xs[xs.length-1]),padT+ch);ctx.lineTo(X(xs[0]),padT+ch);ctx.closePath();
 const g=ctx.createLinearGradient(0,padT,0,H);g.addColorStop(0,up?'rgba(47,191,113,0.18)':'rgba(242,85,90,0.18)');g.addColorStop(1,'rgba(0,0,0,0)');ctx.fillStyle=g;ctx.fill();
 // line
 ctx.beginPath();ctx.moveTo(X(xs[0]),Y(ys[0]));for(let i=1;i<pts.length;i++)ctx.lineTo(X(xs[i]),Y(ys[i]));
 ctx.strokeStyle=col;ctx.lineWidth=1.8;ctx.lineJoin='round';ctx.stroke();
 // hi/lo labels
 ctx.fillStyle=isLight()?'#5b6678':'#8a95a9';ctx.font='10px -apple-system,Arial';ctx.textAlign='left';
 ctx.fillText('$'+mxy.toFixed(2),padL+2,padT+9);ctx.fillText('$'+mny.toFixed(2),padL+2,padT+ch-1);
 const chg=(ys[ys.length-1]-ys[0])/ys[0]*100;
 const d0=new Date(mnx*1000),d1=new Date(mxx*1000);
 const fmtd=d=>d.toISOString().slice(0,10);
 const usesM=(base===c.chart.m);
 meta.innerHTML=`<span>${fmtd(d0)} → ${fmtd(d1)}${usesM?' · monthly':''}</span><span class="${chg>=0?'up':'down'}" style="font-weight:700">${chg>=0?'+':''}${chg.toFixed(2)}% over ${tf}</span>`;
}
function catalogModal(t){
 const c=CAT[t];const on=getPending().includes(t);
 const html=`<div class="mh"><div>
   <div class="t1">${t} <span style="font-size:14px;color:var(--mut);font-weight:500">${c.name||''}</span></div>
   <div class="t2">${c.sector||''} · ${c.x?c.x:c.k?'KOSPI (Korea Exchange)':c.b?'US-listed (broad catalog)':'S&amp;P 500 / Nasdaq-100'}</div>
   <div class="t3">Not on your tracked lists yet</div></div>
  <button class="close" onclick="closeM()">✕</button></div>
 <div class="mb">
  <div class="thesis">This name is in the searchable catalog (${c.x?c.x+' constituents':c.k?'KOSPI — Korea Exchange constituents':c.b?'US-listed common stocks incl. the Russell 2000 universe':'S&amp;P 500 + Nasdaq-100'}) but isn't tracked yet, so live price, charts, technicals, earnings, ownership and chatter aren't loaded. Add it to queue it for <b>live tracking</b> — I'll pull full data and fold it into your 3×/day refreshes.${(c.k||c.x)?' <b>Note:</b> international names are tracked from their local exchange in local currency where the data feed covers them (Tokyo, Seoul, Paris and Hong Kong confirmed); a US listing/ADR is the fallback.':''}</div>
  <div style="margin:16px 0;text-align:center"><button class="addbtn${on?' on':''}" id="modaladd" data-t="${t}" style="font-size:14px;padding:11px 20px" onclick="toggleTick('${t}')">${on?'✓ Queued — remove':'+ Add &amp; track live'}</button></div>
  <div class="sec-t">What you'll get once tracked</div>
  <div class="kpis">
   <div class="kpi"><div class="k">Price &amp; chart</div><div class="v" style="font-size:12px">live + history</div></div>
   <div class="kpi"><div class="k">Technicals</div><div class="v" style="font-size:12px">RSI, MACD, SMAs</div></div>
   <div class="kpi"><div class="k">Analysts</div><div class="v" style="font-size:12px">targets &amp; ratings</div></div>
   <div class="kpi"><div class="k">Earnings</div><div class="v" style="font-size:12px">digest &amp; dates</div></div>
   <div class="kpi"><div class="k">Ownership</div><div class="v" style="font-size:12px">insider + 13F</div></div>
   <div class="kpi"><div class="k">Sentiment</div><div class="v" style="font-size:12px">Stocktwits</div></div>
  </div>
  <div class="own" style="margin-top:14px"><a href="https://finance.yahoo.com/quote/${t}" target="_blank">Quick look on Yahoo Finance ↗</a><a href="https://efts.sec.gov/LATEST/search-index?q=%22${t}%22" target="_blank">SEC filings →</a></div>
 </div>`;
 document.getElementById('modal').innerHTML=html;document.getElementById('ov').classList.add('on');document.body.style.overflow='hidden';
}
function openM(t){window._lastModal=t;
 if(!isTracked(t)){if(CAT[t])catalogModal(t);return;}
 const c=C[t];const u=upside(c);const s=c.sentiment;
 const kpi=(k,v)=>`<div class="kpi"><div class="k">${k}</div><div class="v">${v}</div></div>`;
 const pctv=v=>v==null?'—':(v*100).toFixed(1)+'%';
 const rsiPos=Math.max(0,Math.min(100,c.rsi||0));
 // insider
 let ins='';const I=c.insider;
 if(I&&(I.buy_n!=null||I.sell_n!=null)){
  ins=`<div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:8px"><span class="b ${I.signal.indexOf('buying')>=0?'ins-buy':I.signal.indexOf('selling')>=0?'ins-sell':'ins-neu'}" style="font-size:12px;padding:5px 10px">${I.signal}</span>${I.buy_n?`<span class="pill"><b class="cbuy">Buys</b> ${I.buy_n} · ${fmtSh(I.buy_sh)} sh · ${fmtB(I.buy_val)}</span>`:''}${I.sell_n?`<span class="pill"><b class="csell">Sells</b> ${I.sell_n} · ${fmtSh(I.sell_sh)} sh · ${fmtB(I.sell_val)}</span>`:''}${I.last?`<span class="pill">Last <b>${I.last}</b></span>`:''}</div>`;
 } else if(I&&I.signal){ins=`<div style="margin-bottom:8px"><span class="pill">${I.signal}</span></div>`;}
 let itbl='';
 if(c.insider_recent&&c.insider_recent.length){
  itbl=`<table class="tbl"><tr style="color:var(--mut2)"><td>Date</td><td>Insider</td><td>Action</td><td class="r">Shares</td><td class="r">Price</td></tr>`+
   c.insider_recent.map(r=>{const code=r[3];const isbuy=code=='P';const issell=code=='S';const lbl=(CODE[code]||code);const clc=isbuy?'cbuy':issell?'csell':'cneu';
    return `<tr><td>${r[0]}</td><td>${r[1]} <span style="color:var(--mut2)">${r[2]}</span></td><td class="${clc}">${lbl}</td><td class="r">${fmtSh(r[4])}</td><td class="r">${r[5]?'$'+r[5]:'—'}</td></tr>`;}).join('')+`</table>`;
 }
 let inst='';const N=c.institutional;
 if(N){inst=`<div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:8px"><span class="pill">Institutional <b>${N.pct}</b></span><span class="pill"><b class="cbuy">${N.inc}</b> added / <b class="csell">${N.dec}</b> trimmed</span></div>`+N.top.map(h=>`<div class="hold-row"><span>${h[0]}</span><span>${h[1]} sh <b class="${h[3]=='inc'?'cbuy':'csell'}">${h[2]}</b></span></div>`).join('');}
 else{inst=`<div class="desc">Institutional 13F summary loads on next refresh. <a href="https://efts.sec.gov/LATEST/search-index?q=%22${t}%22&forms=13F-HR" target="_blank">Search 13F →</a></div>`;}
 let msgs='';
 if(c.messages&&c.messages.length){msgs=c.messages.map(m=>`<div class="msg"><span class="mu">@${m[0]}</span><span class="mt ${m[1]}">${m[1]}</span><div class="mbody">${(m[2]||'').replace(/</g,'&lt;')}</div></div>`).join('');}
 // earnings digest
 let earn='';const E=c.earnings;
 if(E){
  const surpCol=v=>v>=0?'up':'down';const cur=E.cur?(' '+E.cur):'';
  earn=`<div class="sec-t">Latest Earnings Digest — Bigdata.com</div>
   <div style="font-size:12px;color:var(--mut);margin-bottom:8px">Reported <b style="color:var(--tx)">${E.d}</b> · <b style="color:var(--tx)">${E.fp}</b>${E.nx?` · next report <b style="color:var(--cyan)">${E.nx[0]}</b> (${E.nx[1]})`:' · next date TBA'}</div>
   <div class="ediff">
    <div class="ebox"><div class="el">EPS — est → actual</div><div class="ev">${E.e[1]}<span style="color:var(--mut2);font-weight:500;font-size:12px"> vs ${E.e[0]} est</span></div><div class="es ${surpCol(E.e[2])}">${E.e[2]>=0?'▲ beat ':'▼ miss '}${E.e[2]>=0?'+':''}${E.e[2].toFixed(1)}%</div></div>
    <div class="ebox"><div class="el">Revenue${cur} — est → actual</div><div class="ev">${fmtB(E.r[1]*1e6)}<span style="color:var(--mut2);font-weight:500;font-size:12px"> vs ${fmtB(E.r[0]*1e6)}</span></div><div class="es ${surpCol(E.r[2])}">${E.r[2]>=0?'▲ ':'▼ '}${E.r[2]>=0?'+':''}${E.r[2].toFixed(1)}%</div></div>
   </div>${E.note?`<div style="font-size:11px;color:var(--amb);margin-top:6px">Note: ${E.note}</div>`:''}${E.cur?`<div style="font-size:11px;color:var(--mut2);margin-top:5px">Revenue reported in ${E.cur}; EPS/revenue surprises are currency-agnostic.</div>`:''}`;
 } else if(c.sector){ earn=`<div class="sec-t">Latest Earnings Digest</div><div class="desc">No standardized earnings data available for this listing.</div>`; }
 const html=`<div class="mh"><div>
   <div class="t1">${t} <span style="font-size:14px;color:var(--mut);font-weight:500">${c.name||''}</span></div>
   <div class="t2">${c.sector||''}${c.industry?' · '+c.industry:''}${c.exchange?' · '+c.exchange:''}${c.country?' · '+c.country:''}${c.float_pct?' · Float '+c.float_pct+'%':''}</div>
   <div class="t3">${c.sector_note||''}</div></div>
  <div style="display:flex;gap:10px;align-items:flex-start"><div class="px2"><div class="p">${px(c.price)}</div><div class="c ${cls(c.change_pct)}">${pct(c.change_pct)}</div></div><button class="close" onclick="closeM()">✕</button></div></div>
 <div class="mb">
  ${researchLink(t)}
  ${c.thesis?`<div class="thesis">${c.thesis}</div>`:''}
  ${c.chart?`<div class="sec-t">Price Chart</div><div class="chartwrap"><div class="tfbar">${TFS.map(tf=>`<button class="tf" data-tf="${tf}" onclick="drawChart('${t}','${tf}')">${tf}</button>`).join('')}</div><canvas id="pchart" class="pchart"></canvas><div class="chartmeta" id="chartmeta"></div></div>`:''}
  ${earn}
  ${atgtBar(c)}
  <div class="sec-t">Snapshot KPIs</div>
  <div class="kpis">
   ${kpi('Mkt Cap',fmtB(c.market_cap))}${kpi('Analyst',ratingTxt(c.analyst_rating))}${kpi('Cons. Target',(c.atgt&&c.atgt.consensus)?'$'+Math.round(c.atgt.consensus):(c.analyst_target?'$'+Math.round(c.analyst_target):'—'))}${kpi('Upside',u==null?'—':(u>=0?'+':'')+u.toFixed(0)+'%')}
   ${kpi('Fwd P/E',c.pe_forward??'—')}${kpi('Trail P/E',c.pe_trailing??'—')}${kpi('Rev Growth',pctv(c.revenue_growth))}${kpi('EPS Growth',pctv(c.earnings_growth))}
   ${kpi('Op Margin',pctv(c.operating_margins))}${kpi('Net Margin',pctv(c.profit_margins))}${kpi('Rev TTM',fmtB(c.revenue_ttm))}${kpi('FCF',fmtB(c.free_cashflow))}
   ${kpi('Volume',fmtV(c.volume))}${kpi('10d Avg Vol'+(c.vol10_exact?'':' ≈'),fmtV(c.vol10))}${kpi('Beta',c.beta??'—')}${kpi('Next ER',c.earnings_date?c.earnings_date.slice(0,10)+(c.earnings_is_estimate?' (est)':''):'—')}
  </div>
  <div class="sec-t">Technical Analysis</div>
  <div class="tech">
   ${kpi('RSI (14)',`<span style="color:${rsiColor(c.rsi)}">${c.rsi??'—'}</span>`)}${kpi('MACD',c.macd?c.macd.histogram.toFixed(2)+(c.macd.histogram>0?' ▲':' ▼'):'—')}${kpi('SMA 20',c.sma20??'—')}${kpi('SMA 50',c.sma50??c.ma_50??'—')}
   ${kpi('SMA 200',c.sma200??c.ma_200??'—')}${kpi('vs 200d',c.ma_200&&c.price?((c.price-c.ma_200)/c.ma_200*100).toFixed(1)+'%':'—')}${kpi('Boll Up',c.bollinger?c.bollinger.upper_band:'—')}${kpi('Boll Low',c.bollinger?c.bollinger.lower_band:'—')}
   ${kpi('ATR(20)',c.atr_20??'—')}${kpi('Williams %R',c.williams_r??'—')}${kpi('TD Seq',c.td_sequential||'—')}${kpi('52w Range',(c.week52_low?'$'+c.week52_low:'—')+' – '+(c.week52_high?'$'+c.week52_high:'—'))}
  </div>
  <div style="margin-top:8px"><div style="font-size:11px;color:var(--mut2)">RSI ${c.rsi??'—'} — oversold &lt;30 · overbought &gt;70</div><div class="rsibar"><div class="dot" style="left:${rsiPos}%"></div></div></div>
  ${pmSection(t)}
  ${(c.opportunities||c.threats)?`<div class="sec-t">Opportunities &amp; Threats</div><div class="ot"><div class="otbox o"><h4>▲ Opportunities</h4><ul>${(c.opportunities||[]).map(o=>`<li>${o}</li>`).join('')}</ul></div><div class="otbox t"><h4>▼ Threats</h4><ul>${(c.threats||[]).map(o=>`<li>${o}</li>`).join('')}</ul></div></div>`:''}
  <div class="sec-t">Ownership — Insider &amp; Institutional</div>
  <div class="ownwrap">
   <div class="ownbox"><h4>🧾 Insider activity (Form 4, since Feb 2026)</h4>${ins}${itbl||'<div class="desc" style="font-size:11.5px">No open-market buys/sells in window.</div>'}</div>
   <div class="ownbox"><h4>🏦 Institutional ownership (13F)</h4>${inst}${c.float_pct?`<div style="margin-top:8px"><span class="pill">Free float <b>${c.float_pct}%</b></span></div>`:''}</div>
  </div>
  <div class="own" style="margin-top:10px"><a href="${c.edgar_insider}" target="_blank">SEC EDGAR: insider Form 3/4/5 →</a><a href="${c.edgar_all}" target="_blank">All filings →</a></div>
  <div class="sec-t">Retail Chatter — Stocktwits ${s?`· score ${s.score} ${s.label.replace('_',' ')} · ${s.bullish_pct}% bullish tags`:''}</div>
  ${msgs?`<div>${msgs}</div><div style="margin-top:8px"><a href="${c.stocktwits}" target="_blank">Open live Stocktwits feed →</a></div>`:`<div class="desc">No stream. <a href="${c.stocktwits}" target="_blank">Check live →</a></div>`}
  ${c.officers?`<div class="sec-t">Key Officers</div><div class="kpis">${c.officers.slice(0,5).map(o=>`<div class="kpi"><div class="k">${o.title||''}</div><div class="v" style="font-size:12px">${o.name||''}</div></div>`).join('')}</div>`:''}
  ${c.description?`<div class="sec-t">Business</div><div class="desc">${c.description}</div>`:''}
  <div style="margin-top:14px;display:flex;gap:8px;flex-wrap:wrap">${c.website?`<a class="pill" href="${c.website}" target="_blank" style="color:var(--cyan)">Company site ↗</a>`:''}<span class="pill">Data updated <b>${(c.updated_at||DATA.generated||'').slice(0,16).replace('T',' ')}</b></span></div>
 </div>`;
 document.getElementById('modal').innerHTML=html;document.getElementById('ov').classList.add('on');document.body.style.overflow='hidden';
 if(c.chart){setTimeout(()=>drawChart(t,'6M'),30);}
}
function closeM(){document.getElementById('ov').classList.remove('on');document.body.style.overflow='';CUR=null;}
function kfv(v,unit){if(v==null)return '—';const r=Math.round(v);if(unit==='idx')return r.toLocaleString();if(unit==='¥')return '¥'+r.toLocaleString();if(unit==='$/bbl')return '$'+r;return '$'+r.toLocaleString();}
function kfq(q,unit){if(!q)return '—';return (q[1]||'')+kfv(q[0],unit);}
function assetModal(key){
 const A=DATA.kalshi&&DATA.kalshi.assets&&DATA.kalshi.assets[key];if(!A)return;
 const tile=DATA.indices.find(i=>i.key===key)||{};const spot=A.no_spot?null:tile.value;const u=A.unit;
 const kpi=(k,v,sub)=>`<div class="kpi"><div class="k">${k}</div><div class="v">${v}</div>${sub?`<div style="font-size:10px;color:var(--mut2);margin-top:2px">${sub}</div>`:''}</div>`;
 const vsSpot=v=>spot&&v!=null?((v/spot-1)*100).toFixed(1).replace(/^(-?)/,(m,s)=>s?'−':'+')+'% vs spot':'';
 let body='';
 if(A.type==='cum'||A.type==='range'){
  const lo=A.p10[0],md=A.p50[0],hi=A.p90[0];
  const bk=A.buckets.filter(b=>b.p>=0.02);
  const axLo=Math.min(lo,spot||lo)*0.97,axHi=Math.max(hi,spot||hi)*1.03;const X=v=>Math.max(0,Math.min(100,(v-axLo)/(axHi-axLo)*100));
  body=`<div class="kpis">${kpi('Expected (median)',kfq(A.p50,u),vsSpot(md))}${kpi('Low · 10th pct',kfq(A.p10,u),vsSpot(lo))}${kpi('High · 90th pct',kfq(A.p90,u),vsSpot(hi))}${kpi('Most likely bucket',A.mode[0]==null?'≤ '+kfv(A.mode[1],u):A.mode[1]==null?'> '+kfv(A.mode[0],u):kfv(A.mode[0],u)+'–'+kfv(A.mode[1],u),kpct(A.mode[2])+' odds')}${spot?kpi('Spot (dashboard)',kfv(spot,u),tile.chg!=null?pct(tile.chg)+' today':''):''}</div>
  <div class="sec-t">Implied range · 80% band (10th–90th percentile)</div>
  <div class="kband"><div class="kb" style="left:${X(lo)}%;width:${X(hi)-X(lo)}%"></div><div class="km" style="left:${X(md)}%" title="median"></div>${spot?`<div class="ks" style="left:${X(spot)}%" title="spot"></div>`:''}</div>
  <div class="kax"><span>${kfv(axLo,u)}</span><span style="color:var(--cyan)">▎spot ${kfv(spot,u)}</span><span style="color:#fff">▎median ${kfv(md,u)}</span><span>${kfv(axHi,u)}</span></div>
  <div class="sec-t">Probability by ${A.type==='range'?'closing bucket':'price bucket'} · ${A.horizon}</div>
  ${bk.map(b=>`<div class="hbar"><span class="hl">${b.lo==null?'≤ '+kfv(b.hi,u):b.hi==null?'> '+kfv(b.lo,u):kfv(b.lo,u)+'–'+kfv(b.hi,u)}</span><span class="ht"><i style="width:${Math.min(100,b.p*100/Math.max(...bk.map(x=>x.p)))}%"></i></span><span class="hv">${kpct(b.p)}</span></div>`).join('')}
  <div class="sec-t">Odds the ${A.horizon.split(' close')[0]} close is above…</div>
  <div style="display:flex;gap:6px;flex-wrap:wrap">${A.cum.filter((c,i)=>A.cum.length<=12||i%Math.ceil(A.cum.length/12)===0).map(c=>`<span class="pill">${kfv(c[0],u)} <b>${kpct(c[1])}</b></span>`).join('')}</div>`;
 } else {
  const H=A.hi,L=A.lo,B=A.band;
  const hiTxt=H?(H.p50[1]==='≤'?'below '+kfv(H.p50[0],u)+' ('+kpct(1-H.ladder[0][1])+')':'≈ '+kfv(H.p50[0],u)):'—';
  const loTxt=L?(L.p50[1]==='≥'?'above '+kfv(L.p50[0],u)+' ('+kpct(1-L.ladder[0][1])+')':'≈ '+kfv(L.p50[0],u)):'—';
  const mx=H?Math.max(...H.ladder.map(x=>x[1])):1,mn=L?Math.max(...L.ladder.map(x=>x[1])):1;
  body=`<div class="kpis">${kpi('Expected 2026 high',hiTxt,H&&H.p50[1]===''?vsSpot(H.p50[0]):'median of the "how high" ladder')}${L?kpi('Expected 2026 low',loTxt,L.p50[1]===''?vsSpot(L.p50[0]):'median of the "how low" ladder'):kpi('2026 low','not listed','Kalshi has no low-of-year market')}${H?kpi('25% chance high ≥',kfv(H.p25,u),vsSpot(H.p25)):''}${L?kpi('25% chance low ≤',kfv(L.p25,u),vsSpot(L.p25)):''}${spot?kpi('Spot (dashboard)',kfv(spot,u),tile.chg!=null?pct(tile.chg)+' today':''):''}</div>
  ${B?`<div class="thesis" style="margin-top:12px">Market-implied 2026 range: <b>${kfv(B.lo,u)} – ${kfv(B.hi,u)}</b> with <b>${kpct(B.p_within)}</b> odds ${A.name} stays inside it for the rest of the year (${kpct(B.p_hi)} it trades above ${kfv(B.hi,u)}, ${kpct(B.p_lo)} it trades below ${kfv(B.lo,u)}).</div>`:''}
  ${H?`<div class="sec-t">Odds ${A.name} trades above… (any time in 2026)</div>${H.ladder.map(x=>`<div class="hbar"><span class="hl">≥ ${kfv(x[0],u)}</span><span class="ht"><i style="width:${x[1]/mx*100}%"></i></span><span class="hv">${kpct(x[1])}</span></div>`).join('')}`:''}
  ${L?`<div class="sec-t">Odds ${A.name} trades below… (any time in 2026)</div>${L.ladder.map(x=>`<div class="hbar"><span class="hl">≤ ${kfv(x[0],u)}</span><span class="ht"><i style="width:${x[1]/mn*100}%;background:linear-gradient(90deg,#b91c1c,#f87171)"></i></span><span class="hv">${kpct(x[1])}</span></div>`).join('')}`:''}`;
 }
 const html=`<div class="mh"><div>
   <div class="t1">${A.name} <span style="font-size:14px;color:var(--mut);font-weight:500">Kalshi-implied price expectations</span></div>
   <div class="t2">${A.horizon} · ${A.ev}</div>
   <div class="t3">Prices are the market's implied probability (yes mid) · as of ${(DATA.kalshi.asof||'').replace('T',' ')}${A.vol?' · ~'+Math.round(A.vol/1000).toLocaleString()+'K contracts traded':''}</div></div>
  <div style="display:flex;gap:8px;align-items:flex-start">${spot?`<div class="px2"><div class="p">${kfv(spot,u)}</div>${tile.chg!=null?`<div class="c ${cls(tile.chg)}">${pct(tile.chg)}</div>`:''}</div>`:''}<button class="close" onclick="closeM()">✕</button></div></div>
 <div class="mb">${body}
  ${A.note?`<div style="margin-top:12px;font-size:11px;color:var(--mut2)">${A.note}</div>`:''}
  <div style="margin-top:12px;font-size:11px;color:var(--mut2)">Read-only public Kalshi market data pulled through the Kalshi MCP on refresh. Percentiles are interpolated from the strike ladder; "≤"/"≥" means the level sits beyond the outermost listed strike. Not a forecast — it is what traders are pricing.</div>
 </div>`;
 document.getElementById('modal').innerHTML=html;document.getElementById('ov').classList.add('on');document.body.style.overflow='hidden';CUR=null;
}
document.addEventListener('keydown',e=>{if(e.key==='Escape')closeM();});
window.addEventListener('resize',()=>{if(CUR)drawChart(CUR.t,CUR.tf);});
function fmtRevM(m){if(m==null)return'—';return m>=1000? '$'+(m/1000).toFixed(2)+'B' : '$'+m.toFixed(1)+'M';}
function fmtEps(v){if(v==null)return'—';return (v<0?'-$':'$')+Math.abs(v).toFixed(2);}
function erSurp(est,act){if(est==null||act==null||est===0)return null;return (act-est)/Math.abs(est)*100;}
function renderEarnRail(){
 const el=document.getElementById('earnrail');const R=DATA.earnings_reports||[];
 if(!R.length){el.innerHTML='';return;}
 const card=e=>{
  const se=erSurp(e.eps_est,e.eps_act), sr=erSurp(e.rev_est,e.rev_act);
  const bm=(s)=>s==null?'':`<span class="bm ${s>=0?'beat':'miss'}">${s>=0?'BEAT':'MISS'} ${s>=0?'+':''}${s.toFixed(1)}%</span>`;
  return `<div class="ercard" onclick="openM('${e.tk}')">
   <div class="top"><span class="tk2">${e.tk}</span><span class="fp">${e.fp} · ${e.d}${e.when?' '+e.when:''}</span></div>
   <div class="errow"><span class="lbl">EPS</span><span class="vals"><b>${fmtEps(e.eps_act)}</b> vs ${fmtEps(e.eps_est)} est</span>${bm(se)}</div>
   <div class="errow"><span class="lbl">REV</span><span class="vals"><b>${fmtRevM(e.rev_act)}</b> vs ${fmtRevM(e.rev_est)} est</span>${bm(sr)}</div>
   ${e.rx!=null?`<div class="errx ${e.rx>=0?'up':'down'}">${e.rx>=0?'▲':'▼'} ${e.rx>=0?'+':''}${e.rx}% next-session reaction</div>`:''}
   ${e.note?`<div class="ernote">${e.note}</div>`:''}
  </div>`;};
 el.innerHTML=railTab('er','📊 Earnings')+`<div class="rbody"><div class="erhd"><h2>📊 Earnings Reports</h2><span class="bl">vs consensus · newest first</span><button class="rhide" onclick="setRail('er',0)" title="Hide the earnings panel">✕ hide</button></div>`+R.map(card).join('')+'</div>';
}
// ---- side rails (earnings left, news right) — per-viewer show/hide, remembered in localStorage ----
let RAILS={er:1,nw:1};
try{const s=JSON.parse(localStorage.getItem('aiF_rails')||'null');if(s&&typeof s==='object')RAILS=Object.assign(RAILS,s);}catch(e){}
function applyRails(){const L=document.querySelector('.layout');if(!L)return;L.classList.toggle('noer',!RAILS.er);L.classList.toggle('nonw',!RAILS.nw);}
function setRail(k,v){RAILS[k]=v?1:0;try{localStorage.setItem('aiF_rails',JSON.stringify(RAILS));}catch(e){}applyRails();}
function railTab(k,label){return `<button class="railtab" onclick="setRail('${k}',1)" title="Show this panel">${label} ${k==='er'?'›':'‹'}</button>`;}
// ---- news feed (Alpha Vantage NEWS_SENTIMENT via news_set.py → DATA.news) ----
let NWF='all';
const NWLAB={bull:'Bullish',sbull:'Somewhat bullish',neu:'Neutral',sbear:'Somewhat bearish',bear:'Bearish'};
function nwEsc(x){return String(x==null?'':x).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
function nwAgo(ts){const m=(Date.now()-Date.parse(ts))/60000;if(!(m>=0))return '';if(m<60)return Math.max(1,Math.round(m))+'m ago';if(m<1440)return Math.round(m/60)+'h ago';return Math.round(m/1440)+'d ago';}
function setNWF(f){NWF=f;renderNews();}
function renderNews(){
 const el=document.getElementById('newsrail');if(!el)return;
 const N=(DATA.news&&DATA.news.items)||[];
 let L=N;
 if(NWF==='co')L=N.filter(i=>i.k==='co');else if(NWF==='macro')L=N.filter(i=>i.k==='macro');else if(NWF!=='all')L=N.filter(i=>(i.tk||[]).some(t=>t[0]===NWF));
 const item=i=>`<div class="nwi${i.k==='macro'?' macro':''}"><div class="nwm"><span class="nwd ${i.sent}" title="Overall sentiment: ${NWLAB[i.sent]||'—'} (${i.ss})"></span><span class="src">${nwEsc(i.s)}</span><span>· ${nwAgo(i.ts)}</span>${i.k==='macro'?'<span class="nwk">· markets</span>':''}</div>`+
  `<a class="nwt" href="${nwEsc(i.u)}" target="_blank" rel="noopener noreferrer">${nwEsc(i.t)}</a>`+
  ((i.tk||[]).length?`<div class="nwtk">${i.tk.map(t=>`<button class="nwc ${t[1]}" onclick="setNWF('${t[0]}')" title="${t[0]} · ${NWLAB[t[1]]||''} (${t[2]}) — show only ${t[0]} stories">${t[0]}</button>`).join('')}</div>`:'')+`</div>`;
 const pill=(f,l)=>`<button class="nwf${NWF===f?' on':''}" onclick="setNWF('${f}')">${l}</button>`;
 const tkp=(NWF!=='all'&&NWF!=='co'&&NWF!=='macro')?`<button class="nwf on" onclick="setNWF('all')" title="Clear the ticker filter">${nwEsc(NWF)} ✕</button>`:'';
 const asof=DATA.news&&DATA.news.asof?DATA.news.asof.replace('T',' '):'—';
 el.innerHTML=railTab('nw','📰 News')+`<div class="rbody"><div class="erhd nwhd"><h2>📰 News</h2><span class="bl">${N.length} stories · last ${(DATA.news&&DATA.news.keep_h)||72}h</span><button class="rhide" onclick="setRail('nw',0)" title="Hide the news panel">✕ hide</button></div>`+
  `<div class="nwfs">${pill('all','All')}${pill('co','My list')}${pill('macro','Markets')}${tkp}</div>`+
  (L.length?L.map(item).join(''):'<div class="nwe">No stories for this filter in the window.</div>')+
  `<div class="nwsrc">Headlines &amp; sentiment labels: Alpha Vantage NEWS_SENTIMENT, filtered to your list · updated ${asof} · each headline opens the publisher's page. Dot = overall tone, chip colour = tone toward that ticker.</div></div>`;
}
// ---- events calendar ----
let CALF='all';
let CALR={preset:'all',from:null,to:null};
function _d(dt){return dt.toISOString().slice(0,10);}
function calRange(preset){const t=new Date();t.setUTCHours(12,0,0,0);const add=n=>{const x=new Date(t);x.setUTCDate(x.getUTCDate()+n);return _d(x);};const today=_d(t);
 if(preset==='today')return[today,today];
 if(preset==='week'){const dow=(t.getUTCDay()+6)%7;if(dow>=5)return[add(7-dow),add(13-dow)];return[add(-dow),add(6-dow)];}
 if(preset==='n7')return[today,add(6)];
 if(preset==='n14')return[today,add(13)];
 if(preset==='n30')return[today,add(29)];
 if(preset==='month'){const e=new Date(Date.UTC(t.getUTCFullYear(),t.getUTCMonth()+1,0,12));return[today.slice(0,8)+'01',_d(e)];}
 if(preset==='nmonth'){const a=new Date(Date.UTC(t.getUTCFullYear(),t.getUTCMonth()+1,1,12)),e=new Date(Date.UTC(t.getUTCFullYear(),t.getUTCMonth()+2,0,12));return[_d(a),_d(e)];}
 return[null,null];}
function setCalRange(preset){const r=calRange(preset);CALR={preset,from:r[0],to:r[1]};renderCalendar();}
// default view = "This week" for everyone (Cesar, Sep 12): on Sat/Sun the current week is mostly over, so it rolls to the coming Mon–Sun
(function(){const r=calRange('week');CALR={preset:'week',from:r[0],to:r[1]};})();
function setCalCustom(){const f=document.getElementById('cal-from').value||null,t=document.getElementById('cal-to').value||null;CALR={preset:(f||t)?'custom':'all',from:f,to:t};renderCalendar();}
const CATN={us:'US',jp:'Japan',eu:'Euro area',corp:'Corporate'};
function numOf(v){if(v==null||v==='')return null;const m=String(v).replace(/,/g,'').match(/-?−?\+?\d+(\.\d+)?/);if(!m)return null;return parseFloat(m[0].replace('−','-').replace('+',''));}
function vsTag(m,isCorp){
 const c=numOf(m.c),a=numOf(m.a);if(c==null||a==null)return'';
 const d=a-c;const tol=Math.abs(c)*0.002+1e-9;
 if(isCorp){ if(Math.abs(d)<=tol) return `<span class="vs inline">IN LINE</span>`; return `<span class="vs ${d>0?'beat':'miss'}">${d>0?'BEAT':'MISS'}</span>`; }
 if(Math.abs(d)<=tol) return `<span class="vs inline">IN LINE</span>`;
 return `<span class="vs ${d>0?'above':'below'}">${d>0?'▲ ABOVE':'▼ BELOW'} CONS.</span>`;
}
function calEv(e){
 const isCorp=e.cat==='corp';
 const pills=`<span class="cp ${e.cat}">${CATN[e.cat]}</span>${e.key?'<span class="cp keyt">key</span>':''}${e.est&&!e.has_actual?'<span class="cp est">date est.</span>':''}${e.has_actual?'<span class="cp rep">reported</span>':''}`;
 const tk=e.tk&&C[e.tk]?`<span class="tk3" onclick="openM('${e.tk}')">${e.tk}</span>`:'';
 const title=e.tk?e.title.replace(new RegExp('^'+e.tk+' '),''):e.title;
 let tbl='';
 if(e.metrics&&e.metrics.length){
  const fv=(m,v)=>{if(v==null||v==='')return'';if(!isCorp)return v;if(/^EPS/.test(m.l))return fmtEps(v);if(/^Revenue/.test(m.l))return fmtRevM(v);return v;};
  tbl=`<table class="cmt"><tr><th></th><th>Consensus</th><th>Actual</th><th>Prior</th></tr>`+e.metrics.map(m=>`<tr><td>${m.l.replace(' ($M)','')}</td><td>${fv(m,m.c)}</td><td class="act">${fv(m,m.a)}${vsTag(m,isCorp)}</td><td>${fv(m,m.p)}</td></tr>`).join('')+`</table>`;
 }
 const rx=e.rx!=null?`<div class="cnote"><b style="color:${e.rx>=0?'var(--grn)':'var(--red)'}">${e.rx>=0?'▲':'▼'} ${e.rx>=0?'+':''}${e.rx}%</b> next-session reaction</div>`:'';
 const note=e.note?`<div class="cnote">${e.note}</div>`:'';
 const ds=e.data_src?`<div class="calmeta">Data: ${e.data_src}</div>`:'';
 return `<div class="calev ${e.cat} imp${e.imp}${e.key?' key':''}${e.past?' past':''}">
  <div class="cet">${tk}<span class="ti">${title}</span>${pills}<span class="tm">${e.time||''}${e.start&&e.start!==e.date?' · meeting from '+e.start.slice(5).replace('-','/'):''}</span><span class="src">${e.src||''}</span></div>
  ${kstrip(e)}${kearn(e)}${tbl}${rx}${note}${ds}</div>`;
}
function kstrip(e){
 if(!e.k) return '';
 const bars=(e.k.bars||[]).length?`<div class="kbars">${e.k.bars.map(b=>{const p=Math.round(b[1]*100);return `<div class="kb${p>=30?' on':''}"><span>${p}%</span><i style="height:${Math.max(2,Math.round(b[1]*100*0.26))}px"></i><span>${b[0]}</span></div>`;}).join('')}</div>`:'';
 return `<div class="kstrip"><span class="kline"><span class="klab">🎯 Kalshi implied</span>${e.k.line}${e.k.vol?` <span style="color:var(--mut2)">· vol ${Math.round(e.k.vol).toLocaleString()}</span>`:''}</span>${bars}</div>`;
}
// ---- Kalshi × earnings calendar: company KPI ladders + earnings-call "mentions" for names on your lists ----
function kspark(h,col){if(!h||h.length<2)return '';const W=44,H=12;const xs=h.map((x,i)=>i/(h.length-1)*(W-2)+1),ys=h.map(x=>H-1-(x.p*(H-2)));
 return `<svg class="kspark" viewBox="0 0 ${W} ${H}"><path d="${h.map((x,i)=>`${i?'L':'M'}${xs[i].toFixed(1)},${ys[i].toFixed(1)}`).join(' ')}" fill="none" stroke="${col||'#a78bfa'}" stroke-width="1.4"/><circle cx="${xs[xs.length-1].toFixed(1)}" cy="${ys[ys.length-1].toFixed(1)}" r="1.6" fill="${col||'#a78bfa'}"/></svg>`;}
function callRows(call,n){const items=(call.items||[]).slice(0,n||99);const mx=Math.max(...items.map(i=>i.p))||1;
 return items.map(i=>{const d=i.first!=null?Math.round((i.p-i.first)*100):0;const cls=d>1?'up':d<-1?'dn':'';
  return `<div class="kcall" title="${call.ev}-${i.k} · vol ${Math.round(i.vol||0).toLocaleString()}"><span class="kl">${i.label}</span><span class="kt"><i style="width:${Math.max(1,i.p/mx*100)}%"></i></span><span class="kv">${kpct(i.p)}</span><span class="kd ${cls}">${kspark(i.history,d>1?'#2fbf71':d<-1?'#f2555a':'#a78bfa')}${i.first!=null&&i.history&&i.history.length>1?`${d>0?'+':''}${d}`:''}</span></div>`;}).join('');}
function callBlock(B,tk,compact){const call=B&&B.call;if(!call||!call.items||!call.items.length)return '';
 return `<div class="kcallhd">🎙 What ${tk} says on the call — Kalshi mention odds<small>${call.when||call.date||''} · ${call.items.length} topics · Kalshi ${call.ev}</small></div>${callRows(call,compact?8:99)}${compact&&call.items.length>8?`<div class="calmeta">+${call.items.length-8} more topics in the ${tk} card.</div>`:''}${!compact&&call.note?`<div class="pn" style="font-size:11.5px;line-height:1.5;margin-top:6px">${call.note}</div>`:''}${!compact&&call.rules?`<div class="calmeta">${call.rules}</div>`:''}`;}
function kpiLine(m){const F=pmU(m);if(m.kind==='date')return `<b>${m.short}</b> ${m.p50[0]?'~'+F(m.p50[0]):'—'}`;
 const v=m.p50[1]==='≤'?'&lt;'+F(m.p50[0]):m.p50[1]==='≥'?'&gt;'+F(m.p50[0]):'≈'+F(m.p50[0]);const H=m.history||[],last=H[H.length-1];
 return `<b>${m.short}</b> ${v}${last?` <span style="color:var(--mut2)">(${kpct(last.p)} tops ${F(m.hist_strike)})</span>`:''}`;}
function kpiMini(m,col){const F=pmU(m);const isD=m.kind==='date';const mx=Math.max(...m.ladder.map(x=>x[1]))||1;const H=m.history||[],last=H[H.length-1],first=H[0];
 return `<div class="enpanel" style="padding:8px 10px"><div class="pt" style="font-size:12px">${m.title}</div><div class="ps" style="font-size:10.5px;color:var(--mut)">Kalshi ${m.ev} · ${m.period||m.horizon||''}${m.vol?' · vol '+Math.round(m.vol).toLocaleString():''}</div><div class="pmchips" style="margin:4px 0"><span class="pmchip">${m.stat||'expected'} <b>${isD?(m.p50[0]?'~'+F(m.p50[0]):'—'):(m.p50[1]==='≤'?'below '+F(m.p50[0]):m.p50[1]==='≥'?'above '+F(m.p50[0]):'≈ '+F(m.p50[0]))}</b></span>${last?`<span class="pmchip">${isD?'by':'tops'} ${F(m.hist_strike)}: <b>${kpct(last.p)}</b>${first&&first.d!==last.d?` <span style="color:var(--mut2)">(${kpct(first.p)} on ${first.d.slice(5).replace('-','/')})</span>`:''}</span>`:''}</div>${m.ladder.filter(x=>x[1]>=0.03).slice(0,6).map(x=>`<div class="hbar"><span class="hl">${isD?'by':'&gt;'} ${F(x[0])}</span><span class="ht"><i style="width:${Math.max(1,x[1]/mx*100)}%;background:${col||'#a78bfa'}"></i></span><span class="hv">${kpct(x[1])}</span></div>`).join('')}</div>`;}
function kearn(e){if(e.cat!=='corp'||e.kind!=='earn'||!e.tk)return '';const B0=pmFor(e.tk);if(!B0)return '';
 const call=B0.call&&B0.call.items&&B0.call.items.length?B0.call:null;
 const B=Object.assign({},B0,{markets:B0.markets.filter(m=>m.cal!==false)});if(!B.markets.length&&!call)return '';
 const kp=B.markets.slice(0,3).map(kpiLine);
 const top=call?call.items.slice(0,3).map(i=>`${i.label} <b>${kpct(i.p)}</b>`):[];
 const sum=`<span class="ksum"><span class="klab">🎯 Kalshi implied</span>${kp.join('<span class="sep">·</span>')}${top.length?`<span class="sep">·</span>call mentions: ${top.join('<span class="sep">·</span>')}`:''}</span>`;
 const more=`<details><summary>See all Kalshi markets for ${e.tk} (${B.markets.length} KPI ladder${B.markets.length===1?'':'s'}${call?` · ${call.items.length} call topics`:''})</summary><div class="kgrid">${B.markets.map((m,i)=>kpiMini(m,['#a78bfa','#22d3ee','#f59e0b','#76b900'][i%4])).join('')}${call?`<div class="enpanel" style="padding:8px 10px">${callBlock(B,e.tk,false)}</div>`:''}</div><div class="calmeta">Market-implied probabilities (yes mid) · Δ = change since the first read · the same data sits on the ${e.tk} tile badge, inside its card, and in the Prediction Markets tab.</div></details>`;
 return `<div class="kearn">${sum}${more}</div>`;}
function renderCalendar(){
 const el=document.getElementById('calendar');const E=DATA.events||[];const M=DATA.events_meta||{};
 const hd=`<div class="calhd"><h2>📅 Events Calendar</h2><span class="bl">macro (Fed · BLS · BEA · BoJ · ECB · Eurostat) + your tracked names · consensus vs actual once released</span></div>`;
 if(!E.length){el.innerHTML=hd+`<div class="calempty">No events loaded yet.</div>`;return;}
 const F=[['all','All'],['key','⭐ Key only'],['us','🇺🇸 US macro'],['jp','🇯🇵 Japan'],['eu','🇪🇺 Euro area'],['corp','🏢 Corporate']];
 const fil=`<div class="calfil">${F.map(f=>`<button class="cf${CALF===f[0]?' on':''}" onclick="CALF='${f[0]}';renderCalendar()">${f[1]}</button>`).join('')}</div>`;
 const keepCat=e=>CALF==='all'||(CALF==='key'?(e.key||(e.cat==='corp'&&e.imp===3)):e.cat===CALF);
 const inRange=e=>(!CALR.from||e.date>=CALR.from)&&(!CALR.to||e.date<=CALR.to);
 const keep=e=>keepCat(e)&&inRange(e);
 const list=E.filter(keep);
 const P=[['all','All dates'],['today','Today'],['week','This week'],['n7','Next 7d'],['n14','Next 14d'],['month','This month'],['n30','Next 30d'],['nmonth','Next month']];
 const fmtR=d=>d?new Date(d+'T12:00:00Z').toLocaleDateString('en',{month:'short',day:'numeric',timeZone:'UTC'}):'';
 const rangeTxt=CALR.preset==='all'?`${list.length} events in the full window`:`${list.length} event${list.length===1?'':'s'} · ${CALR.from&&CALR.to?fmtR(CALR.from)+' – '+fmtR(CALR.to):CALR.from?'from '+fmtR(CALR.from):'through '+fmtR(CALR.to)}`;
 const dr=`<div class="calfil caldr"><span class="lbl">📆 Dates</span>${P.map(f=>`<button class="cf${CALR.preset===f[0]?' on':''}" onclick="setCalRange('${f[0]}')">${f[1]}</button>`).join('')}<span class="sep"></span><input type="date" id="cal-from" value="${CALR.from||''}" onchange="setCalCustom()" title="From"/><span class="lbl">to</span><input type="date" id="cal-to" value="${CALR.to||''}" onchange="setCalCustom()" title="To"/><span class="cnt" style="display:inline-flex;align-items:center;gap:8px">${rangeTxt}${CALR.preset!=='all'?`<button class="cf x" onclick="setCalRange('all')" title="Clear the date filter">✕ clear</button>`:''}</span></div>`;
 const today=new Date();const tkey=today.toISOString().slice(0,10);
 const days={};list.forEach(e=>{(days[e.date]=days[e.date]||[]).push(e);});
 const MON=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],DOW=['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];
 const dayBlock=d=>{const dt=new Date(d+'T12:00:00Z');const past=d<tkey;
  return `<div class="calday${past?' past':''}${d===tkey?' today':''}"><div class="cald"><div class="dn">${dt.getUTCDate()}</div><div class="dm">${MON[dt.getUTCMonth()]}</div><div class="dw">${DOW[dt.getUTCDay()]}${d===tkey?' · today':''}</div></div><div>${days[d].map(calEv).join('')}</div></div>`;};
 const pastDays=Object.keys(days).filter(d=>d<tkey).sort(),upDays=Object.keys(days).filter(d=>d>=tkey).sort();
 const pastN=pastDays.reduce((n,d)=>n+days[d].length,0);
 const pastHtml=pastDays.length?`<details class="calpast" open><summary>Recent — ${CALR.preset==='all'?'last 2 weeks with results':'earlier dates in this range'} (${pastN})</summary>${pastDays.map(dayBlock).join('')}</details>`:'';
 const upHtml=upDays.length?upDays.map(dayBlock).join(''):`<div class="calempty">Nothing ${CALR.preset==='all'?'upcoming in this filter':'scheduled in this date range'+(CALF!=='all'?' for this category':'')}.</div>`;
 const meta=`<div class="calmeta">Window ${M.window||''} · built ${M.built||''} · sources: ${M.sources||''}. Dates tagged <i>date est.</i> follow the agency's usual cadence and are confirmed when the official calendar posts. Above/below tags compare the actual to consensus, not good/bad.</div>`;
 el.innerHTML=hd+fil+dr+pastHtml+upHtml+meta;
}
// ---- prediction markets (Kalshi) ----
function kpct(p){return Math.round(p*100)+'%';}
function valRows(keys){
 const V=(DATA.kalshi&&DATA.kalshi.ipo&&DATA.kalshi.ipo.valuations)||{};const NM={anthropic:'Anthropic',openai:'OpenAI',anduril:'Anduril',databricks:'Databricks'};
 const rows=keys.filter(k=>V[k]).map(k=>`<tr><td>${NM[k]}</td><td>${V[k].last_private||''}</td><td>${V[k].ipo_target||''}</td><td style="color:var(--mut2)">${V[k].src||''}</td></tr>`).join('');
 if(!rows) return '';
 return `<div class="ps" style="margin:10px 0 2px"><b style="color:var(--tx)">Expected valuation</b> — Kalshi lists no valuation markets for these names (only timing), so these are press-reported figures, refreshed weekly.</div><div style="overflow-x:auto"><table class="cmt"><tr><th></th><th style="text-align:left">Last private mark</th><th style="text-align:left">Reported IPO valuation / target</th><th style="text-align:left">Source</th></tr>${rows}</table></div>`;
}
function pmDelta(H){if(!H||H.length<2)return '';const d=Math.round((H[H.length-1].p-H[0].p)*100);const cls=d>1?'up':d<-1?'dn':'';return `<span class="kd ${cls}">${kspark(H,d>1?'#2fbf71':d<-1?'#f2555a':'#a78bfa')}${d>0?'+':''}${d}<span style="color:var(--mut2)"> since ${H[0].d.slice(5).replace('-','/')}</span></span>`;}
const PMB={};const PMOPEN=new Set();
function togglePM(t){if(PMOPEN.has(t))PMOPEN.delete(t);else PMOPEN.add(t);const on=PMOPEN.has(t);
 const tr=document.getElementById('pmr-'+t),tx=document.getElementById('pmx-'+t);if(!tr||!tx)return;
 tr.classList.toggle('open',on);tx.hidden=!on;tr.querySelector('.seebtn').textContent=on?'Hide':'Details';
 if(on&&!tx.dataset.done){tx.querySelector('td').innerHTML=`<div class="pmbody">${PMB[t]||''}</div>`;tx.dataset.done='1';}}
function pmFold(head,body,open){return `<details class="pmcard pmfold"${open?' open':''}><summary>${head}</summary><div class="pmbody">${body}</div></details>`;}
function pmTileRow(m,col){const F=pmU(m);const H=m.history||[],last=H[H.length-1];const isD=m.kind==='date';
 const v=isD?(m.p50[0]?'~'+F(m.p50[0]):'—'):(m.p50[1]==='≤'?'&lt;'+F(m.p50[0]):m.p50[1]==='≥'?'&gt;'+F(m.p50[0]):'≈'+F(m.p50[0]));
 if(isD&&m.ladder.length===1&&!m.settled)return `<div class="pmt-r"><span class="dot" style="background:${col}"></span><span><b>${m.short}</b> ${kpct(m.p_at)} <span class="mut">by ${F(m.hist_strike)}</span></span>${pmDelta(H)}</div>`;
 if(m.settled)return `<div class="pmt-r"><span class="dot" style="background:${col}"></span><span><b>${m.short}</b> <span style="color:var(--grn)">${pmSettled(m)}</span>${last?` <span class="mut">· last read ${kpct(last.p)}</span>`:''}</span>${pmDelta(H)}</div>`;
 return `<div class="pmt-r"><span class="dot" style="background:${col}"></span><span><b>${m.short}</b> ${v}${last?` <span class="mut">· ${kpct(last.p)} ${isD?'by':'tops'} ${F(m.hist_strike)}</span>`:''}</span>${pmDelta(H)}</div>`;}
function pmLines(B){const cols=['#76b900','#22d3ee','#f59e0b','#a78bfa','#f87171','#34d399','#fb923c','#e879f9'];const out=[];
 B.markets.forEach(m=>{const F=pmU(m);
  if(m.history_all&&m.history_all.length){const ks=[...new Set(m.history_all.map(x=>x.k))].sort();ks.forEach(k=>out.push({m,k,label:`${m.short} by ${F(k)}`,pts:m.history_all.filter(x=>x.k===k)}));}
  else out.push({m,k:m.hist_strike,label:`${m.short} ${m.kind==='date'?'by':'tops'} ${F(m.hist_strike)}${m.settled?' · settled':''}`,pts:m.history||[]});});
 out.forEach((l,i)=>l.col=cols[i%cols.length]);return out;}
function pmColor(lines,m){const l=lines.find(x=>x.m===m);return l?l.col:'#a78bfa';}
function pmChart(B,tk,KD,W4,H4){return pmChartLines(pmLines(B),tk,KD,W4,H4);}
function pmChartLines(lines,tk,KD,W4,H4){const allH=[].concat(...lines.map(l=>l.pts));if(!allH.length)return null;
 const ds=allH.map(x=>x.d).sort();const d0=new Date(ds[0]+'T00:00:00Z').getTime(),d1=new Date(KD.asof.slice(0,10)+'T00:00:00Z').getTime()+86400000;
 const L4=36,R4=12,T4=14,B4=24;const X4=d=>L4+(W4-L4-R4)*((new Date(d+'T00:00:00Z').getTime()-d0)/Math.max(1,d1-d0));const Y4=p=>T4+(H4-T4-B4)*(1-p);
 const line4=(pts,col,F,lab)=>{const g={};pts.forEach(x=>{(g[x.ev||'']=g[x.ev||'']||[]).push(x)});return Object.values(g).map(q=>`<path d="${q.map((x,i)=>`${i?'L':'M'}${X4(x.d).toFixed(1)},${Y4(x.p).toFixed(1)}`).join(' ')}" fill="none" stroke="${col}" stroke-width="2.2"/>`+q.map(x=>`<circle cx="${X4(x.d).toFixed(1)}" cy="${Y4(x.p).toFixed(1)}" r="2.3" fill="${col}"><title>${x.d} · ${lab} · ${kpct(x.p)}</title></circle>`).join('')).join('');};
 const span=(d1-d0)/86400000;const tk4=[];{const t=new Date(d0);const step=span>200?2:1;for(let i=0;i<14;i++){const dd=new Date(Date.UTC(t.getUTCFullYear(),t.getUTCMonth()+i*step,1));if(dd.getTime()>d1)break;if(dd.getTime()>=d0)tk4.push(dd.toISOString().slice(0,10));}}
 const ax4=tk4.map(d=>`<line x1="${X4(d).toFixed(1)}" x2="${X4(d).toFixed(1)}" y1="${T4}" y2="${H4-B4}" stroke="var(--bd)"/><text x="${X4(d).toFixed(1)}" y="${H4-8}" font-size="9" text-anchor="middle" fill="var(--mut2)">${new Date(d+'T12:00:00Z').toLocaleString('en',{month:'short',timeZone:'UTC'})}</text>`).join('');
 const gy4=[0,0.25,0.5,0.75,1].map(p=>`<line x1="${L4}" x2="${W4-R4}" y1="${Y4(p).toFixed(1)}" y2="${Y4(p).toFixed(1)}" stroke="var(--bd)"/><text x="${L4-4}" y="${(Y4(p)+3.5).toFixed(1)}" font-size="9" text-anchor="end" fill="var(--mut2)">${Math.round(p*100)}%</text>`).join('');
 const svg=`<svg class="pmsvg" viewBox="0 0 ${W4} ${H4}" role="img" aria-label="${tk} prediction markets over time">${gy4}${ax4}${lines.map(l=>line4(l.pts,l.col,l.m?pmU(l.m):(v=>v),l.label)).join('')}</svg>`;
 const legend=`<div class="pmchips" style="margin-top:2px">${lines.map(l=>`<span class="pmchip" style="color:${l.col}">■ ${l.label}</span>`).join('')}<span class="pmchip">${allH.length} points · since ${ds[0]||''}</span></div>`;
 return {svg,legend,lines,n:allH.length,since:ds[0]};}
function renderPredict(){
 const el=document.getElementById('predict');const KD=DATA.kalshi;
 const hd=`<div class="pmhd"><h2>🎯 Prediction Markets</h2><span class="bl">Kalshi market-implied odds · read-only feed · ${KD?('as of '+KD.asof):''}</span></div>`;
 if(!KD){el.innerHTML=hd+`<div class="calempty">Kalshi feed not loaded in this build.</div>`;return;}
 // Fed path
 const F=KD.fed.meetings;const cur=KD.fed.cur_upper;
 const W=640,H=120,PL=40,PR=30,PT=16,PB=22;const ys=[3.50,3.75,4.00,4.25];
 const ymin=3.45,ymax=4.30;const X=i=>PL+(W-PL-PR)*(F.length===1?0.5:i/(F.length-1));const Y=v=>PT+(H-PT-PB)*(1-(v-ymin)/(ymax-ymin));
 const grid=ys.map(v=>`<line x1="${PL}" x2="${W-PR}" y1="${Y(v).toFixed(1)}" y2="${Y(v).toFixed(1)}" stroke="var(--bd)" stroke-width="1"/><text x="${PL-4}" y="${(Y(v)+3.5).toFixed(1)}" font-size="9" text-anchor="end" fill="var(--mut2)">${v.toFixed(2)}</text>`).join('');
 const curLine=`<line x1="${PL}" x2="${W-PR}" y1="${Y(cur).toFixed(1)}" y2="${Y(cur).toFixed(1)}" stroke="#94a3b8" stroke-dasharray="3 3" stroke-width="1"/><text x="${PL+4}" y="${(Y(cur)+11).toFixed(1)}" font-size="9" text-anchor="start" fill="#94a3b8">current upper bound ${cur.toFixed(2)}%</text>`;
 const path=F.map((m,i)=>`${i?'L':'M'}${X(i).toFixed(1)},${Y(m.exp_upper).toFixed(1)}`).join(' ');
 const dots=F.map((m,i)=>`<circle cx="${X(i).toFixed(1)}" cy="${Y(m.exp_upper).toFixed(1)}" r="3.5" fill="#e9d5ff" stroke="#7c3aed" stroke-width="1.5"/><text x="${(X(i)+(i===0?7:i===F.length-1?-7:0)).toFixed(1)}" y="${(Y(m.exp_upper)-8).toFixed(1)}" font-size="9.5" font-weight="700" text-anchor="${i===0?'start':i===F.length-1?'end':'middle'}" fill="#e9d5ff">${m.exp_upper.toFixed(2)}</text><text x="${X(i).toFixed(1)}" y="${H-6}" font-size="9.5" text-anchor="middle" fill="var(--mut)">${m.label}</text>`).join('');
 const svg=`<svg class="pmsvg" viewBox="0 0 ${W} ${H}" role="img" aria-label="Expected fed funds upper bound by meeting">${grid}${curLine}<path d="${path}" fill="none" stroke="#a78bfa" stroke-width="2"/>${dots}</svg>`;
 const cols=F.map(m=>`<div class="fm"><div class="fl">${m.label}</div><div class="fe">${m.exp_upper.toFixed(2)}%<small>expected upper bound</small></div><div class="fstack"><i class="cut" style="width:${m.p_cut*100}%"></i><i class="hold" style="width:${m.p_hold*100}%"></i><i class="hike" style="width:${m.p_hike*100}%"></i></div><div class="fp"><b class="ct">cut ${kpct(m.p_cut)}</b> · <b class="hd">hold ${kpct(m.p_hold)}</b> · <b class="hk">hike ${kpct(m.p_hike)}</b></div></div>`).join('');
 const fed=`<div class="pmcard wide"><div class="pt">Fed path — probability-weighted upper bound by meeting</div><div class="ps">Kalshi KXFED ladders (P[upper bound > strike]) → per-level probabilities → expected rate. Current range ${(cur-0.25).toFixed(2)}–${cur.toFixed(2)}%.</div>${svg}<div class="fedpath">${cols}</div><div class="pn">Hike/hold/cut are relative to the <b>current</b> ${cur.toFixed(2)}% upper bound, so a "hike" at a later meeting means the rate ends above today's level, not necessarily a move at that meeting. Thin later-dated ladders (Jan/Mar) carry wide spreads.</div></div>`;
 // ladders
 const ladE=Object.entries(KD.ladders||{}).sort((a,b)=>(a[1].settled?1:0)-(b[1].settled?1:0));
 const lad=ladE.map(([id,L])=>{
  const mx=Math.max(...L.buckets.map(b=>b.p));
  const bars=`<div class="kbars" style="height:70px">${L.buckets.filter(b=>b.p>=0.035).map(b=>`<div class="kb${b.p===mx?' on':''}"><span>${kpct(b.p)}</span><i style="height:${Math.max(2,Math.round(b.p/mx*52))}px"></i><span>${b.label}</span></div>`).join('')}</div>`;
  if(L.settled)return `<div class="pmcard" style="opacity:.8"><div class="pt">${L.name} <span class="pmchip" style="font-size:10px;color:var(--grn)">✓ settled</span></div><div class="ps">Kalshi ${L.ev} · vol ${L.vol?Math.round(L.vol).toLocaleString():'—'} · final book before the print</div>${bars}<div class="pn">${L.settled}</div></div>`;
  const nb=L.buckets.filter(b=>b.p>=0.035).length;
  return `<div class="pmcard${nb>7?' span2':''}"><div class="pt">${L.name}</div><div class="ps">Kalshi ${L.ev} · vol ${L.vol?Math.round(L.vol).toLocaleString():'—'}</div>${bars}<div class="pmchips"><span class="pmchip">mode <b>${L.mode}</b></span><span class="pmchip">median <b>${L.median}</b></span></div></div>`;
 }).join('');
 // ---- how high will CPI y/y get this year (KXHIGHINFLATION) — standalone macro card with multi-strike history ----
 let cpimax='';
 const CM=KD.cpimax;
 if(CM&&CM.ladder&&CM.ladder.length){const F=v=>Number(v).toFixed(1)+'%';const cols=['#f87171','#f59e0b','#a78bfa','#22d3ee','#76b900'];
  const ks=[...new Set((CM.history_all||[]).map(x=>x.k))].sort((a,b)=>Number(a)-Number(b));
  const lines=ks.map((k,i)=>({label:`any 2026 print > ${F(k)}`,pts:(CM.history_all||[]).filter(x=>x.k===k),col:cols[i%cols.length]}));
  const ch=pmChartLines(lines,'CPI max',KD,760,190);const mx=Math.max(...CM.ladder.map(x=>x[1]))||1;
  const H=CM.history||[],last=H[H.length-1],first=H[0];const d=first&&last?Math.round((last.p-first.p)*100):0;
  const chips=`<span class="pmchip">tops ${F(CM.hist_strike)}: <b>${last?kpct(last.p):'—'}</b>${first&&last&&first.d!==last.d?` <span style="color:var(--mut2)">(${kpct(first.p)} on ${first.d.slice(5).replace('-','/')} · ${d>0?'+':''}${d})</span>`:''}</span>`+
   (CM.p50&&CM.p50[0]!=null?`<span class="pmchip">median 2026 peak <b>${CM.p50[1]==='≤'?'below '+F(CM.p50[0]):CM.p50[1]==='≥'?'above '+F(CM.p50[0]):'≈ '+F(CM.p50[0])}</b></span>`:'')+
   (CM.p25&&CM.p25[0]!=null&&CM.p25[1]===''?`<span class="pmchip">1-in-4 it tops <b>${F(CM.p25[0])}</b></span>`:'')+
   `<span class="pmchip">> ${F(CM.ladder[CM.ladder.length-1][0])}: <b>${kpct(CM.ladder[CM.ladder.length-1][1])}</b></span>`;
  cpimax=`<div class="pmcard wide"><div class="pt">📈 ${CM.title} <span class="pmt-n" style="font-weight:400">— market-implied odds that a 2026 CPI y/y print exceeds each level</span></div><div class="ps">Kalshi ${CM.ev} · ${CM.horizon||''} · vol ${Math.round(CM.vol||0).toLocaleString()} · lines = implied probability over time for the ${ks.map(F).join(' · ')} strikes</div>${ch?ch.svg+ch.legend:''}<div class="pmchips">${chips}</div><div class="engrid" style="grid-template-columns:repeat(auto-fit,minmax(300px,1fr))"><div class="enpanel"><div class="pt" style="font-size:13px">Cumulative odds by strike</div>${CM.ladder.map(x=>`<div class="hbar"><span class="hl">&gt; ${F(x[0])}</span><span class="ht"><i style="width:${Math.max(1,x[1]/mx*100)}%;background:linear-gradient(90deg,#b91c1c,#f87171)"></i></span><span class="hv">${kpct(x[1])}</span></div>`).join('')}</div><div class="enpanel"><div class="pt" style="font-size:13px">Context</div><div class="pn" style="margin-top:4px">${CM.context||''}</div><div class="pn">${CM.note||''}</div><div class="calmeta">${CM.rules||''}</div></div></div></div>`;}
 // BoJ decisions
 const dec=Object.entries(KD.decisions||{}).map(([id,D])=>{
  const opts=Object.entries(D.opts).sort((a,b)=>b[1]-a[1]);
  return `<div class="pt" style="margin-top:8px">${D.name}</div><div class="ps">Kalshi ${D.ev} · vol ${Math.round(D.vol||0).toLocaleString()}</div>`+opts.map(([o,p])=>`<div class="hbar"><span class="hl">${o}</span><span class="ht"><i style="width:${p*100}%"></i></span><span class="hv">${kpct(p)}</span></div>`).join('');
 }).join('');
 const boj=`<div class="pmcard"><div class="pt">Bank of Japan — decision odds</div>${dec}</div>`;
 // binary tiles
 const bin=`<div class="pmcard"><div class="pt">Macro tail risks</div><div class="ps">Kalshi binary markets</div>${(KD.binary||[]).map(b=>`<div class="pmtile"><span>${b.title}<br><span class="pvs">${b.tk} · vol ${Math.round(b.vol).toLocaleString()}</span></span><span class="pv">${kpct(b.p)}</span></div>`).join('')}</div>`;
 // IPO tracker
 const I=KD.ipo;const A=I.anthropic.points,O=I.openai.points;
 const t0=new Date('2026-09-15').getTime(),t1=new Date('2027-06-15').getTime();
 const W2=640,H2=150,L2=36,R2=12,T2=12,B2=24;const XX=d=>L2+(W2-L2-R2)*((new Date(d).getTime()-t0)/(t1-t0));const YY=p=>T2+(H2-T2-B2)*(1-p);
 const line=(pts,col)=>`<path d="${pts.map((q,i)=>`${i?'L':'M'}${XX(q[0]).toFixed(1)},${YY(q[1]).toFixed(1)}`).join(' ')}" fill="none" stroke="${col}" stroke-width="2.2"/>`+pts.map(q=>`<circle cx="${XX(q[0]).toFixed(1)}" cy="${YY(q[1]).toFixed(1)}" r="2.6" fill="${col}"/>`).join('');
 const months=['2026-10-01','2026-11-01','2026-12-01','2027-01-01','2027-02-01','2027-03-01','2027-04-01','2027-05-01','2027-06-01'];
 const ax=months.map(d=>`<line x1="${XX(d).toFixed(1)}" x2="${XX(d).toFixed(1)}" y1="${T2}" y2="${H2-B2}" stroke="var(--bd)"/><text x="${XX(d).toFixed(1)}" y="${H2-8}" font-size="9" text-anchor="middle" fill="var(--mut2)">${d.slice(5,7)==='01'?'Jan 27':new Date(d+'T12:00:00Z').toLocaleString('en',{month:'short',timeZone:'UTC'})}</text>`).join('');
 const gy=[0,0.25,0.5,0.75,1].map(p=>`<line x1="${L2}" x2="${W2-R2}" y1="${YY(p).toFixed(1)}" y2="${YY(p).toFixed(1)}" stroke="var(--bd)"/><text x="${L2-4}" y="${(YY(p)+3.5).toFixed(1)}" font-size="9" text-anchor="end" fill="var(--mut2)">${Math.round(p*100)}%</text>`).join('');
 const svg2=`<svg class="pmsvg" viewBox="0 0 ${W2} ${H2}" role="img" aria-label="Probability of an IPO announcement by date">${gy}${ax}${line(A,'#f0abfc')}${line(O,'#38bdf8')}<text x="${W2-R2}" y="${T2+10}" font-size="10" text-anchor="end" fill="#f0abfc">■ Anthropic</text><text x="${W2-R2}" y="${T2+22}" font-size="10" text-anchor="end" fill="#38bdf8">■ OpenAI</text></svg>`;
 const S=I.summary;const ll=Object.entries(I.leadleft_anthropic.opts).sort((a,b)=>b[1]-a[1]).slice(0,3);
 const ipo=`<div class="pmcard wide"><div class="pt">The AI IPO race — Anthropic vs OpenAI</div><div class="ps">Cumulative probability that each company <i>confirms</i> an IPO before the date (Kalshi ${I.anthropic.ev} / ${I.openai.ev}). Volumes ~${Math.round(I.anthropic.vol/1000)}K / ~${Math.round(I.openai.vol/1000)}K contracts.</div>${svg2}
  <div class="pmchips"><span class="pmchip">IPOs first: <b>Anthropic ${kpct(I.first.Anthropic)}</b> · OpenAI ${kpct(I.first.OpenAI)}</span><span class="pmchip">Anthropic by Nov 1: <b>${kpct(S.anthropic_by_nov1)}</b></span><span class="pmchip">Anthropic by year-end: <b>${kpct(S.anthropic_by_year_end)}</b></span><span class="pmchip">OpenAI by year-end: <b>${kpct(S.openai_by_year_end)}</b></span><span class="pmchip">Anthropic lead-left: <b>${ll[0][0]} ${kpct(ll[0][1])}</b> · ${ll[1][0]} ${kpct(ll[1][1])}</span></div>
  ${valRows(['anthropic','openai'])}
  <div class="pn">Why it matters for the list: an Anthropic listing re-rates the AI-infrastructure complex (compute, memory, neoclouds) and sets the public comp for OpenAI; the market has the announcement window centred on the second half of October.</div></div>`;
 // IPO pipeline — Anduril & Databricks (separate card, longer horizon)
 let pipe='';
 if(I.anduril||I.databricks){
  const u0=new Date('2026-09-15').getTime(),u1=new Date('2028-01-15').getTime();const XU=d=>L2+(W2-L2-R2)*((new Date(d).getTime()-u0)/(u1-u0));
  const lineU=(pts,col)=>`<path d="${pts.map((q,i)=>`${i?'L':'M'}${XU(q[0]).toFixed(1)},${YY(q[1]).toFixed(1)}`).join(' ')}" fill="none" stroke="${col}" stroke-width="2.2"/>`+pts.map(q=>`<circle cx="${XU(q[0]).toFixed(1)}" cy="${YY(q[1]).toFixed(1)}" r="2.6" fill="${col}"/>`).join('');
  const qs=['2026-10-01','2027-01-01','2027-04-01','2027-07-01','2027-10-01','2028-01-01'];
  const axU=qs.map(d=>`<line x1="${XU(d).toFixed(1)}" x2="${XU(d).toFixed(1)}" y1="${T2}" y2="${H2-B2}" stroke="var(--bd)"/><text x="${XU(d).toFixed(1)}" y="${H2-8}" font-size="9" text-anchor="middle" fill="var(--mut2)">${new Date(d+'T12:00:00Z').toLocaleString('en',{month:'short',year:'2-digit',timeZone:'UTC'})}</text>`).join('');
  const svg3=`<svg class="pmsvg" viewBox="0 0 ${W2} ${H2}" role="img" aria-label="Probability of an IPO announcement by date — Anduril and Databricks">${gy}${axU}${I.anduril?lineU(I.anduril.points,'#f5a623'):''}${I.databricks?lineU(I.databricks.points,'#2fbf71'):''}<text x="${W2-R2}" y="${T2+10}" font-size="10" text-anchor="end" fill="#f5a623">■ Anduril</text><text x="${W2-R2}" y="${T2+22}" font-size="10" text-anchor="end" fill="#2fbf71">■ Databricks</text></svg>`;
  const chips=[];
  if(I.anduril) chips.push(`<span class="pmchip">Anduril by year-end: <b>${kpct(S.anduril_by_year_end||0)}</b></span>`,`<span class="pmchip">Anduril by Jun 2027: <b>${kpct(S.anduril_by_mid2027||0)}</b></span>`);
  if(I.databricks) chips.push(`<span class="pmchip">Databricks by Jun 2027: <b>${kpct(S.databricks_by_mid2027||0)}</b></span>`,`<span class="pmchip">Databricks by end-2027: <b>${kpct(S.databricks_by_end2027||0)}</b></span>`);
  pipe=`<div class="pmcard wide"><div class="pt">IPO pipeline — Anduril &amp; Databricks</div><div class="ps">Cumulative probability of an IPO confirmation before the date (Kalshi ${I.anduril?I.anduril.ev:''}${I.databricks?' / '+I.databricks.ev:''}). Thinner markets than the AI pair — volumes ~${I.anduril?Math.round(I.anduril.vol/1000):0}K / ~${I.databricks?Math.round(I.databricks.vol/1000):0}K contracts.</div>${svg3}<div class="pmchips">${chips.join('')}</div>${valRows(['anduril','databricks'])}<div class="pn">Read: the market puts both listings mostly in 2027 — Databricks a slow climb through the year, Anduril only picking up from spring 2027.</div></div>`;
 }
 // Texas energy — data-center demand read-through
 let energy='';
 const EN=KD.energy;
 if(EN&&(EN.ercot_year||EN.ercot_daily||EN.tx_oil)){
  const fmw=v=>v==null?'—':(Math.round(v/100)/10).toFixed(1)+' GW';
  const fbd=v=>v==null?'—':v.toFixed(2)+' mb/d';
  const rows=(lad,fmt,col)=>{const mx=Math.max(...lad.map(x=>x[1]))||1;return lad.map(x=>`<div class="hbar"><span class="hl">&gt; ${fmt(x[0])}</span><span class="ht"><i style="width:${Math.max(1,x[1]/mx*100)}%${col?';background:'+col:''}"></i></span><span class="hv">${kpct(x[1])}</span></div>`).join('');};
  const panel=(t,sub,body,foot)=>`<div class="enpanel"><div class="pt" style="font-size:13px">${t}</div><div class="ps">${sub}</div>${body}${foot?`<div class="pn">${foot}</div>`:''}</div>`;
  let p1='',p2='',p3='';
  if(EN.ercot_year){const E=EN.ercot_year;
   p1=panel('ERCOT 2026 peak load — how high?',`Kalshi ${E.ev} · vol ${Math.round(E.vol||0).toLocaleString()}`,
    `<div class="pmchips"><span class="pmchip">tops 91.5 GW: <b>${kpct(E.ladder[0][1])}</b></span><span class="pmchip">tops 94 GW: <b>${kpct((E.ladder.find(x=>x[0]===94000)||[0,0])[1])}</b></span><span class="pmchip">tops 98 GW: <b>${kpct((E.ladder.find(x=>x[0]===98000)||[0,0])[1])}</b></span></div>`+rows(E.ladder,fmw),
    (E.context||'')+(E.context_src?` <a href="${E.context_src}" target="_blank" style="color:var(--cyan)">EIA ↗</a>`:''));}
  if(EN.ercot_daily){const E=EN.ercot_daily;const d=new Date(E.date+'T12:00:00Z').toLocaleString('en',{month:'short',day:'numeric',timeZone:'UTC'});
   const inner=E.ladder.filter(x=>x[1]>0.015&&x[1]<0.985);const lo=E.p10[0],md=E.p50[0],hi=E.p90[0];
   p2=panel(`ERCOT daily peak load — ${d}`,`Kalshi ${E.ev} · settles on ERCOT's highest hourly load for the day · vol ${Math.round(E.vol||0).toLocaleString()}`,
    `<div class="pmchips"><span class="pmchip">implied peak <b>${fmw(md)}</b></span><span class="pmchip">80% band <b>${fmw(lo)}–${fmw(hi)}</b></span></div>`+rows(E.ladder.filter(x=>x[0]>=Math.max(E.ladder[0][0],(inner[0]||E.ladder[0])[0]-3000)),fmw,'linear-gradient(90deg,#b45309,#f59e0b)'),
    'Rolls every day — the daily strip is the live read on Texas load (weather + data-center build-out). The year card above is the record-watch.');}
  if(EN.tx_oil){const E=EN.tx_oil;
   p3=panel('Texas crude production 2026 (annual avg)',`Kalshi ${E.ev} · settles on EIA annual-average field production · vol ${Math.round(E.vol||0).toLocaleString()}`,
    `<div class="pmchips"><span class="pmchip">implied <b>${fbd(E.p50[0])}</b></span><span class="pmchip">80% band <b>${E.p10[1]||''}${fbd(E.p10[0])} – ${E.p90[1]||''}${fbd(E.p90[0])}</b></span></div>`+rows(E.ladder,fbd,'linear-gradient(90deg,#065f46,#2fbf71)'),
    E.context||'');}
  const enRows=[];
  if(EN.ercot_daily){const E=EN.ercot_daily;const d=new Date(E.date+'T12:00:00Z').toLocaleString('en',{month:'short',day:'numeric',timeZone:'UTC'});enRows.push(`<div class="pmt-r"><span class="dot" style="background:#f59e0b"></span><span><b>ERCOT daily peak · ${d}</b> implied ${fmw(E.p50[0])} <span class="mut">· 80% band ${fmw(E.p10[0])}–${fmw(E.p90[0])}</span></span><span></span></div>`);}
  if(EN.ercot_year){const E=EN.ercot_year;enRows.push(`<div class="pmt-r"><span class="dot" style="background:#a78bfa"></span><span><b>2026 record watch</b> tops 91.5 GW <span class="mut">·</span> ${kpct(E.ladder[0][1])} <span class="mut">· tops 94 GW ${kpct((E.ladder.find(x=>x[0]===94000)||[0,0])[1])}</span></span><span></span></div>`);}
  if(EN.tx_oil){const E=EN.tx_oil;enRows.push(`<div class="pmt-r"><span class="dot" style="background:#2fbf71"></span><span><b>Texas crude 2026</b> implied ${fbd(E.p50[0])} <span class="mut">· 80% band ${fbd(E.p10[0])}–${fbd(E.p90[0])}</span></span><span></span></div>`);}
  const enHead=`<div class="pmt-h"><span class="pmt-tk">⚡ Texas energy</span><span class="pmt-nm">data-center demand read-through</span></div><div class="pmt-m"><span class="pmt-n">${enRows.length} markets · settle on ERCOT + EIA data</span><span class="pmx"></span></div><div class="pmt-rows">${enRows.join('')}</div>`;
  energy=pmFold(enHead,`<div class="ps" style="margin-top:4px">Kalshi markets on the ERCOT grid (where much of the new AI data-center load is landing) and Texas oil output. Prices = market-implied probability the value ends above each strike.</div><div class="engrid">${p1}${p2}${p3}</div>`,false);
 }
 // Strait of Hormuz — shipping traffic (weekly / month max / year avg) with a time chart of the headline contracts
 let hormuz='';
 const HZ=KD.hormuz;
 if(HZ&&HZ.weekly){
  const HH=HZ.history||{};
  const all=[].concat(HH.weekly||[],HH.month_max||[],HH.year_avg||[],HH.normal||[]);
  const ds=all.map(x=>x.d).sort();const d0=new Date((ds[0]||KD.asof.slice(0,10))+'T00:00:00Z').getTime(),d1=new Date(KD.asof.slice(0,10)+'T00:00:00Z').getTime()+86400000;
  const W3=760,H3=200,L3=36,R3=12,T3=14,B3=24;const XH=d=>L3+(W3-L3-R3)*((new Date(d+'T00:00:00Z').getTime()-d0)/Math.max(1,d1-d0));const YH=p=>T3+(H3-T3-B3)*(1-p);
  const seg=(pts,col,dash)=>{const groups={};pts.forEach(x=>{(groups[x.ev]=groups[x.ev]||[]).push(x)});return Object.values(groups).map(g=>`<path d="${g.map((q,i)=>`${i?'L':'M'}${XH(q.d).toFixed(1)},${YH(q.p).toFixed(1)}`).join(' ')}" fill="none" stroke="${col}" stroke-width="2.2"${dash?' stroke-dasharray="4 3"':''}/>`+g.map(q=>`<circle cx="${XH(q.d).toFixed(1)}" cy="${YH(q.p).toFixed(1)}" r="2.4" fill="${col}"><title>${q.d} · ${q.ev} · ${kpct(q.p)}</title></circle>`).join('')+(g.length>1?`<text x="${XH(g[0].d).toFixed(1)}" y="${(YH(g[0].p)-6).toFixed(1)}" font-size="8.5" fill="${col}" opacity=".85">${g[0].lbl||''}</text>`:'')).join('');};
  // month ticks
  const ticks=[];{const t=new Date(d0);t.setUTCDate(1);for(let i=0;i<8;i++){const dd=new Date(Date.UTC(t.getUTCFullYear(),t.getUTCMonth()+i,1));if(dd.getTime()>d1)break;if(dd.getTime()>=d0)ticks.push(dd.toISOString().slice(0,10));}}
  const axH=ticks.map(d=>`<line x1="${XH(d).toFixed(1)}" x2="${XH(d).toFixed(1)}" y1="${T3}" y2="${H3-B3}" stroke="var(--bd)"/><text x="${XH(d).toFixed(1)}" y="${H3-8}" font-size="9" text-anchor="middle" fill="var(--mut2)">${new Date(d+'T12:00:00Z').toLocaleString('en',{month:'short',timeZone:'UTC'})}</text>`).join('');
  const gyH=[0,0.25,0.5,0.75,1].map(p=>`<line x1="${L3}" x2="${W3-R3}" y1="${YH(p).toFixed(1)}" y2="${YH(p).toFixed(1)}" stroke="var(--bd)"/><text x="${L3-4}" y="${(YH(p)+3.5).toFixed(1)}" font-size="9" text-anchor="end" fill="var(--mut2)">${Math.round(p*100)}%</text>`).join('');
  const kW=HZ.weekly.hist_strike,kM=HZ.month_max.hist_strike,kY=HZ.year_avg.hist_strike;
  const svgH=`<svg class="pmsvg" viewBox="0 0 ${W3} ${H3}" role="img" aria-label="Kalshi Hormuz traffic contracts over time">${gyH}${axH}${seg(HH.year_avg||[],'#a78bfa')}${seg(HH.month_max||[],'#f59e0b')}${seg(HH.weekly||[],'#22d3ee')}${seg(HH.normal||[],'#2fbf71',true)}</svg><div class="pmchips" style="margin-top:2px"><span class="pmchip" style="color:#22d3ee">■ this week's transits &gt; ${kW}</span><span class="pmchip" style="color:#2fbf71">┅ back to normal before Jan 1, 2027</span><span class="pmchip" style="color:#f59e0b">■ month's best single day ≥ ${kM}</span><span class="pmchip" style="color:#a78bfa">■ 2026 peak 7-day average &gt; ${kY}</span><span class="pmchip">${all.length} points · since ${ds[0]||''}</span></div>`;
  const fm=v=>v==null?'—':Math.round(v).toString();
  const rowsH=(lad,kind,col)=>{const mx=Math.max(...lad.map(x=>x[1]))||1;return lad.map(x=>`<div class="hbar"><span class="hl">${kind==='atleast'?'≥':'&gt;'} ${fm(x[0])}</span><span class="ht"><i style="width:${Math.max(1,x[1]/mx*100)}%;background:${col}"></i></span><span class="hv">${kpct(x[1])}</span></div>`).join('');};
  const pan=(M,title,sub,col)=>`<div class="enpanel"><div class="pt" style="font-size:13px">${title}</div><div class="ps">Kalshi ${M.ev} · vol ${Math.round(M.vol||0).toLocaleString()}${sub?' · '+sub:''}</div><div class="pmchips"><span class="pmchip">implied median <b>${M.p50[1]||''}${fm(M.p50[0])}</b></span><span class="pmchip">80% band <b>${M.p10[1]||''}${fm(M.p10[0])}–${M.p90[1]||''}${fm(M.p90[0])}</b></span></div>${rowsH(M.ladder,M.kind,col)}</div>`;
  const Wk=HZ.weekly,Mm=HZ.month_max,Ya=HZ.year_avg;
  let normal='';
  if(HZ.normal){const N=HZ.normal;const P=N.points;
   const WN=760,HN=170,LN=36,RN=14,TN=14,BN=26;const n0=new Date('2026-09-01T00:00:00Z').getTime(),n1=new Date(P[P.length-1][0]+'T00:00:00Z').getTime()+86400000*20;
   const XN=d=>LN+(WN-LN-RN)*((new Date(d+'T00:00:00Z').getTime()-n0)/(n1-n0));const YN=p=>TN+(HN-TN-BN)*(1-p);
   const qs=[];for(let y=2026;y<=2029;y++)for(const m of ['01','04','07','10']){const d=`${y}-${m}-01`;const t=new Date(d+'T00:00:00Z').getTime();if(t>=n0&&t<=n1)qs.push(d);}
   const axN=qs.map(d=>`<line x1="${XN(d).toFixed(1)}" x2="${XN(d).toFixed(1)}" y1="${TN}" y2="${HN-BN}" stroke="var(--bd)"/><text x="${XN(d).toFixed(1)}" y="${HN-9}" font-size="9" text-anchor="middle" fill="var(--mut2)">${d.slice(5,7)==='01'?d.slice(0,4):new Date(d+'T12:00:00Z').toLocaleString('en',{month:'short',timeZone:'UTC'})}</text>`).join('');
   const gyN=[0,0.25,0.5,0.75,1].map(p=>`<line x1="${LN}" x2="${WN-RN}" y1="${YN(p).toFixed(1)}" y2="${YN(p).toFixed(1)}" stroke="var(--bd)"${p===0.5?' stroke-dasharray="3 3"':''}/><text x="${LN-4}" y="${(YN(p)+3.5).toFixed(1)}" font-size="9" text-anchor="end" fill="var(--mut2)">${Math.round(p*100)}%</text>`).join('');
   const curve=`<path d="${P.map((q,i)=>`${i?'L':'M'}${XN(q[0]).toFixed(1)},${YN(q[1]).toFixed(1)}`).join(' ')}" fill="none" stroke="#2fbf71" stroke-width="2.4"/>`+P.map(q=>`<circle cx="${XN(q[0]).toFixed(1)}" cy="${YN(q[1]).toFixed(1)}" r="3" fill="#2fbf71"><title>before ${q[0]} · ${kpct(q[1])}</title></circle><text x="${XN(q[0]).toFixed(1)}" y="${(YN(q[1])-7).toFixed(1)}" font-size="9" text-anchor="middle" fill="#a7f3d0">${kpct(q[1])}</text>`).join('');
   const medl=N.median_date?`<line x1="${XN(N.median_date).toFixed(1)}" x2="${XN(N.median_date).toFixed(1)}" y1="${TN}" y2="${HN-BN}" stroke="#fff" stroke-dasharray="4 3" opacity=".7"/><text x="${(XN(N.median_date)+4).toFixed(1)}" y="${TN+10}" font-size="9.5" fill="#fff">50% by ${new Date(N.median_date+'T12:00:00Z').toLocaleString('en',{month:'short',year:'numeric',timeZone:'UTC'})}</text>`:'';
   const svgN=`<svg class="pmsvg" viewBox="0 0 ${WN} ${HN}" role="img" aria-label="Cumulative probability the Strait of Hormuz returns to normal by date">${gyN}${axN}${curve}${medl}</svg>`;
   normal=`<div class="enpanel" style="margin-top:12px"><div class="pt" style="font-size:13px">When does traffic return to normal? · cumulative odds by date</div><div class="ps">Kalshi ${N.ev} · "normal" = 7-day average back above 60 transits/day · vol ${Math.round((N.vol||0)/1e6*10)/10}M contracts (Kalshi's most-traded Hormuz market)</div>${svgN}<div class="pmchips"><span class="pmchip">by Jan 1, 2027: <b>${kpct(N.by['2027-01-01'])}</b></span><span class="pmchip">by Jul 1, 2027: <b>${kpct(N.by['2027-07-01'])}</b></span><span class="pmchip">by Jan 1, 2029: <b>${kpct(N.by['2029-01-01'])}</b></span>${N.median_date?`<span class="pmchip">even odds around <b>${new Date(N.median_date+'T12:00:00Z').toLocaleString('en',{month:'long',year:'numeric',timeZone:'UTC'})}</b></span>`:''}<span class="pmchip">never by 2029: <b>${kpct(1-N.by['2029-01-01'])}</b></span></div><div class="pn">${N.note||''} The green dashed line in the time chart above tracks the Jan 1, 2027 contract, so you can see the market's view of a 2026 reopening drifting over time.</div></div>`;
  }
  const hzLast=k=>{const h=HH[k]||[];return h.length?h[h.length-1].p:null;};
  const hzRows=[
   `<div class="pmt-r"><span class="dot" style="background:#22d3ee"></span><span><b>This week's transits</b> median ~${fm(Wk.p50[0])} <span class="mut">· &gt;${kW}: ${kpct(hzLast('weekly')??(Wk.ladder.find(x=>x[0]==kW)||[0,0])[1])}</span></span>${pmDelta(HH.weekly||[])}</div>`,
   `<div class="pmt-r"><span class="dot" style="background:#f59e0b"></span><span><b>Best single day · ${Mm.month||''}</b> median ~${fm(Mm.p50[0])} <span class="mut">· ≥${kM}: ${kpct(hzLast('month_max')??(Mm.ladder.find(x=>x[0]==kM)||[0,0])[1])}</span></span>${pmDelta(HH.month_max||[])}</div>`,
   `<div class="pmt-r"><span class="dot" style="background:#a78bfa"></span><span><b>2026 peak 7-day avg</b> ${Ya.p50[1]||''}${fm(Ya.p50[0])} <span class="mut">· &gt;${kY}: ${kpct(hzLast('year_avg')??(Ya.ladder.find(x=>x[0]==kY)||[0,0])[1])}</span></span>${pmDelta(HH.year_avg||[])}</div>`,
   HZ.normal?`<div class="pmt-r"><span class="dot" style="background:#2fbf71"></span><span><b>Back to normal</b> by Jan 1, 2027: ${kpct((HZ.normal.by||{})['2027-01-01']||0)} <span class="mut">· median ${HZ.normal.median_date?new Date(HZ.normal.median_date+'T12:00:00Z').toLocaleDateString('en',{month:'short',year:'numeric',timeZone:'UTC'}):'beyond listed dates'}</span></span>${pmDelta(HH.normal||[])}</div>`:''].join('');
  const hzHead=`<div class="pmt-h"><span class="pmt-tk">🚢 Strait of Hormuz</span><span class="pmt-nm">shipping traffic · IMF PortWatch</span></div><div class="pmt-m"><span class="pmt-n">${HZ.normal?4:3} markets · ${all.length} pts · IMF PortWatch transits</span><span class="pmx"></span></div><div class="pmt-rows">${hzRows}</div>`;
  hormuz=pmFold(hzHead,`<div class="ps" style="margin-top:4px">Four contracts on how much shipping is getting through the strait: this week's count, the best single day this month, the highest 7-day average the year reaches, and when traffic gets back to normal. Lines = market-implied probability of the headline strike over time; the weekly line restarts with each new week's contract.</div>${svgH}
   <div class="engrid">${pan(Wk,`Traffic through the strait · ${Wk.range}`,'transits this week','linear-gradient(90deg,#0e7490,#22d3ee)')}${pan(Mm,`Highest single-day traffic · ${Mm.month}`,'best day of the month','linear-gradient(90deg,#b45309,#f59e0b)')}${pan(Ya,'Highest 7-day average in 2026','any time before Jan 1, 2027','linear-gradient(90deg,#7c3aed,#a78bfa)')}</div>${normal}
   <div class="pn">${Wk.prev?`Previous week (${Wk.prev.range}): ${Wk.prev.note}. `:''}Contracts roll automatically — the weekly one every Monday, the monthly one on the 1st — and the history keeps accumulating one point per refresh so the chart shows how the market's view has moved. Normal pre-crisis traffic was roughly 100+ transits a day, which is why the year-avg strikes run to 120.</div>`,false);
 }
 // Stock-linked prediction markets (keyed by ticker) — reusable: one wide card per ticker with a time chart + ladders
 let spmRows='';
 const SP=KD.stock_pm||{};
 Object.keys(SP).filter(k=>!k.startsWith('_')).forEach(tk=>{
  const B0=SP[tk];const c=C[tk]||{};const B=Object.assign({},B0,{markets:(B0.markets||[]).filter(m=>m.pm_tile!==false)});if(!B.markets.length&&!(B.call&&B.call.items&&B.call.items.length))return;
  const ch=pmChart(B,tk,KD,760,190)||{svg:'',legend:'',lines:pmLines(B),n:0};const allH={length:ch.n};const cols=ch.lines.map(l=>l.col);const mcol=m=>pmColor(ch.lines,m);
  const svg4=ch.svg,legend=ch.legend;
  const panels=B.markets.map((m,i)=>{const col=mcol(m);const mx=Math.max(...m.ladder.map(x=>x[1]))||1;const F=pmU(m);const st=m.stat||'expected peak';const isD=m.kind==='date';
   const one=isD&&m.ladder.length===1;const hiTxt=isD?(m.p50[0]?'~'+F(m.p50[0]):'beyond the listed dates'):m.p50[1]==='≤'?`below ${F(m.p50[0])} (${kpct(1-m.ladder[0][1])})`:m.p50[1]==='≥'?`above ${F(m.p50[0])}`:`≈ ${F(m.p50[0])}`;
   const chip2=isD?`<span class="pmchip">by ${F(m.hist_strike)}: <b>${kpct(m.p_at)}</b></span>${m.p25[0]?`<span class="pmchip">1-in-4 by <b>${F(m.p25[0])}</b></span>`:''}`
     :(m.p25[1]===''?`<span class="pmchip">25% chance it tops <b>${F(m.p25[0])}</b></span>`:`<span class="pmchip">tops ${F(m.hist_strike)}: <b>${kpct(m.ladder[0][1])}</b></span>`);
   const prior=(m.prior&&m.prior.length)?m.prior.map(q=>`<span class="pmchip" title="${q.ev}">${q.period}: settled${q.actual!=null?' at <b>'+F(q.actual)+'</b>':''} · last read ${kpct(q.last_p)} for ${F(q.hist_strike)}</span>`).join(''):'';
   const settled=(m.settled?`<span class="pmchip" style="color:var(--grn)">${pmSettled(m)}${m.settled.note?' · '+m.settled.note:''}</span>`:'')+(isD?(m.settled_no&&m.settled_no.length?`<span class="pmchip">settled NO: <b>${m.settled_no.map(F).join(' · ')}</b></span>`:''):(m.settled_yes&&m.settled_yes.length?`<span class="pmchip">already above <b>${F(m.settled_yes[m.settled_yes.length-1])}</b></span>`:''));
   return `<div class="enpanel"><div class="pt" style="font-size:13px">${m.title}</div><div class="ps">Kalshi ${m.ev} · ${m.horizon} · vol ${Math.round(m.vol||0).toLocaleString()}</div><div class="pmchips">${one?'':`<span class="pmchip">${st} <b>${hiTxt}</b></span>`}${m.settled?'':chip2}${settled}${prior}</div>${m.ladder.map(x=>`<div class="hbar"><span class="hl">${isD?'by':'&gt;'} ${F(x[0])}</span><span class="ht"><i style="width:${Math.max(1,x[1]/mx*100)}%;background:${col}"></i></span><span class="hv">${kpct(x[1])}</span></div>`).join('')}${m.note?`<div class="pn">${m.note}</div>`:''}</div>`;}).join('');
  const callPanel=B.call&&B.call.items&&B.call.items.length?`<div class="enpanel">${callBlock(B,tk,false)}</div>`:'';
  const nm=(c.name||'').replace(/,? (Inc|Corp|Corporation|Ltd|plc|Holdings|Co)\.?$/i,'');
  const callRow=B.call&&B.call.items&&B.call.items.length?`<div class="pmt-call">🎙 <b>Call ${B.call.when?B.call.when.replace(' after close',''):B.call.date}</b> · ${B.call.items.slice(0,3).map(i=>`${i.label} <b>${kpct(i.p)}</b>`).join(' · ')}${B.call.items.length>3?` <span style="color:var(--mut2)">+${B.call.items.length-3} topics</span>`:''}</div>`:'';
  const head=`<div class="pmt-h"><span class="pmt-tk">${tk}</span><span class="pmt-nm" title="${c.name||''}">${nm}</span>${c.price?`<span class="b" style="font-size:10px;color:${c.change_pct>=0?'var(--grn)':'var(--red)'};background:${c.change_pct>=0?'rgba(47,191,113,.12)':'rgba(242,85,90,.12)'}">$${px(c.price).replace('$','')} ${c.change_pct!=null?(c.change_pct>=0?'+':'')+c.change_pct.toFixed(2)+'%':''}</span>`:''}</div><div class="pmt-m"><span class="pmt-n">${B.markets.length} market${B.markets.length===1?'':'s'}${B.call?' + call book':''} · ${allH.length} pts · Kalshi</span><span class="pmx"></span></div><div class="pmt-rows">${B.markets.map((m,i)=>pmTileRow(m,mcol(m))).join('')}</div>${callRow}`;
  const body=`<div class="pt" style="font-size:12.5px;margin-top:4px">${B.theme||'stock-linked prediction markets'}</div><div class="ps">${B.src_note||'Kalshi contracts tied to a name you track. Lines = market-implied probability the headline strike is topped, over time.'}</div>${svg4}${legend}<div class="engrid" style="grid-template-columns:repeat(auto-fit,minmax(300px,1fr))">${panels}${callPanel}</div>${B.why?`<div class="pn">${B.why} ${B.roll_note||''} The same data shows on the ${tk} tile (badge) and inside its detail panel${B.markets.some(m=>m.cal!==false)?' and on its earnings-calendar entry':''}.</div>`:''}`;
  PMB[tk]=body;const on=PMOPEN.has(tk);
  const chips=`<div class="pmt-rows">${B.markets.map((m,i)=>pmTileRow(m,mcol(m))).join('')}</div>`;
  const cbk=B.call&&B.call.items&&B.call.items.length?`🎙 <b>Call ${B.call.when?B.call.when.replace(' after close',''):B.call.date}</b>${B.call.settled?' <span style="color:var(--grn)">✓ settled</span>':''}<br>${B.call.items.slice(0,3).map(i=>`${i.label} <b>${kpct(i.p)}</b>`).join(' · ')}${B.call.items.length>3?` <span style="color:var(--mut2)">+${B.call.items.length-3}</span>`:''}`:'<span style="color:var(--mut2)">—</span>';
  const pxc=c.price?`<span class="${c.change_pct>=0?'up':'down'}">${px(c.price)}<br><small>${c.change_pct!=null?(c.change_pct>=0?'+':'')+c.change_pct.toFixed(2)+'%':''}</small></span>`:'—';
  spmRows+=`<tr class="lr pmr${on?' open':''}" id="pmr-${tk}" onclick="togglePM('${tk}')"><td class="tkc"><span style="color:var(--cyan);cursor:pointer" onclick="event.stopPropagation();openM('${tk}')" title="Open the ${tk} card">${tk}</span><small title="${c.name||''}">${nm}</small></td><td class="pxc">${pxc}</td><td class="nmk">${B.markets.length}${B.call?'<br><small>+ call</small>':''}</td><td class="mks">${chips}</td><td class="cbk">${cbk}</td><td class="c stk"><button class="seebtn" onclick="event.stopPropagation();togglePM('${tk}')">${on?'Hide':'Details'}</button></td></tr><tr class="lx pmxr" id="pmx-${tk}"${on?'':' hidden'}><td colspan="6">${on?`<div class="pmbody">${body}</div>`:''}</td></tr>`;
 });
 const spm=spmRows?`<div class="pmcard wide pmtbl-wrap"><div class="pt">Kalshi markets by company</div><div class="ps">one row per name · chips = the headline read of each market (Δ since first read) · <b>Details</b> expands the ladders, the change-over-time chart and the earnings-call book · ticker opens the stock card</div><div class="ltwrap"><table class="ltbl pmtbl"><thead><tr><th>Company</th><th>Price</th><th class="c">Markets</th><th style="text-align:left">Prediction markets · headline read</th><th style="text-align:left">Earnings-call book</th><th class="c stk">Details</th></tr></thead><tbody>${spmRows}</tbody></table></div></div>`:'';
 // Standalone frontier cards: quantum timing + US-stake board (own cards, like the Fed path / IPO race — not company tiles)
 let quantum='',stake='';
 const Q=KD.quantum;
 if(Q){const F=pmU(Q);const ch=pmChart({markets:[Q]},'Quantum',KD,760,190);const mx=Math.max(...Q.ladder.map(x=>x[1]))||1;const H=Q.history||[],last=H[H.length-1],first=H[0];
  const names=['IONQ','RGTI','QUBT','QBTS'].filter(t=>C[t]);
  quantum=`<div class="pmcard wide"><div class="pt">When will the first useful quantum computer be developed?</div><div class="ps">Kalshi ${Q.ev} · one contract per "before <b>year</b>" threshold (${Q.ladder.map(x=>F(x[0])).join(' · ')}) · vol ${Math.round(Q.vol||0).toLocaleString()} · lines = market-implied cumulative odds over time</div>${ch?ch.svg:''}<div class="pmchips">${Q.p50[0]?`<span class="pmchip">median arrival <b>~${F(Q.p50[0])}</b></span>`:''}${Q.p25[0]?`<span class="pmchip">1-in-4 by <b>${F(Q.p25[0])}</b></span>`:''}${last?`<span class="pmchip">by ${F(Q.hist_strike)}: <b>${kpct(last.p)}</b>${first&&first.d!==last.d?` <span style="color:var(--mut2)">(${kpct(first.p)} on ${first.d.slice(5).replace('-','/')})</span>`:''}</span>`:''}<span class="pmchip">never before ${F(Q.ladder[Q.ladder.length-1][0])}: <b>${kpct(1-Q.ladder[Q.ladder.length-1][1])}</b></span>${ch?ch.legend.replace('<div class="pmchips" style="margin-top:2px">','').replace(/<\/div>$/,''):''}</div><div class="engrid" style="grid-template-columns:repeat(auto-fit,minmax(300px,1fr))"><div class="enpanel"><div class="pt" style="font-size:13px">Cumulative odds by year</div>${Q.ladder.map(x=>`<div class="hbar"><span class="hl">by ${F(x[0])}</span><span class="ht"><i style="width:${Math.max(1,x[1]/mx*100)}%;background:linear-gradient(90deg,#7c3aed,#a78bfa)"></i></span><span class="hv">${kpct(x[1])}</span></div>`).join('')}</div><div class="enpanel"><div class="pt" style="font-size:13px">What counts as "useful"</div><div class="pn" style="margin-top:4px">${Q.note||''}</div><div class="pn">On your list: ${names.map(t=>`<b style="color:var(--cyan);cursor:pointer" onclick="openM('${t}')">${t}</b>`).join(' · ')} — the same curve sits on each of those stock cards.</div></div></div></div>`;}
 const U=KD.usstake;
 if(U&&U.legs&&U.legs.length){const act=U.legs.filter(l=>!l.settled),set=U.legs.filter(l=>l.settled);
  const lines=U.legs.filter(l=>(l.history||[]).length>1).map(l=>({label:`${l.label}${l.settled?' · settled YES':''}`,pts:(l.history||[]).map(x=>({d:x.d,p:x.p,ev:U.ev,k:l.k}))}));
  const cols=['#f87171','#76b900','#22d3ee','#f59e0b','#a78bfa','#34d399','#fb923c','#e879f9'];lines.forEach((l,i)=>l.col=cols[i%cols.length]);
  const ch=pmChartLines(lines,'US stake',KD,760,190);
  const fmtD=d=>new Date(d+'T12:00:00Z').toLocaleDateString('en',{month:'short',day:'numeric',timeZone:'UTC'});
  const rows=(items)=>{const mx=Math.max(...items.map(i=>i.p))||1;return items.map(i=>{const d=i.first!=null?Math.round((i.p-i.first)*100):0;const cls=i.settled?'up':d>1?'up':d<-1?'dn':'';const H=i.history||[];
    return `<div class="kcall" title="${U.ev}-${i.k} · vol ${Math.round(i.vol||0).toLocaleString()}"><span class="kl">${i.tk&&C[i.tk]?`<b style="color:var(--cyan);cursor:pointer" onclick="openM('${i.tk}')">${i.label}</b>`:i.label}</span><span class="kt"><i style="width:${Math.max(1,i.p/mx*100)}%${i.settled?';background:linear-gradient(90deg,#15803d,#4ade80)':''}"></i></span><span class="kv">${i.settled?'✓ YES':kpct(i.p)}</span><span class="kd ${cls}">${i.settled?fmtD(i.settled.d):`${kspark(H,d>1?'#2fbf71':d<-1?'#f2555a':'#a78bfa')}${H.length>1?`${d>0?'+':''}${d}`:''}`}</span></div>`;}).join('');};
  const half=Math.ceil(act.length/2);
  stake=`<div class="pmcard wide"><div class="pt">Which companies will the US take a stake in this year?</div><div class="ps">Kalshi ${U.ev} · one yes/no contract per company · ${U.horizon} · ${act.length} open legs · ${set.length} settled YES (${set.map(l=>l.label).join(', ')}) · names in <b style="color:var(--cyan)">blue</b> are on your list — click to open the card</div>${ch?ch.svg+ch.legend:''}<div class="engrid" style="grid-template-columns:repeat(auto-fit,minmax(300px,1fr))"><div class="enpanel"><div class="pt" style="font-size:13px">Open legs — implied odds by Jan 1, 2027 <small style="color:var(--mut2);font-weight:400">· Δ since first read</small></div>${rows(act.slice(0,half))}</div><div class="enpanel"><div class="pt" style="font-size:13px">&nbsp;</div>${rows(act.slice(half))}</div><div class="enpanel"><div class="pt" style="font-size:13px">Settled YES · 2026</div>${rows(set)}<div class="pn" style="margin-top:6px">${U.note||''}</div><div class="calmeta">${U.rules||''}</div></div></div></div>`;}
 const secQ=`<div class="pmsec"><h3>⚛️ Frontier tech &amp; industrial policy</h3><span class="bl">quantum timing · the US-stake board — each also shows on the matching stock cards in My List</span></div>`;
 const nco=Object.keys(SP).filter(k=>!k.startsWith('_')&&SP[k].markets&&SP[k].markets.some(m=>m.pm_tile!==false)).length;
 const secM=`<div class="pmsec"><h3>🌐 Macro & geopolitics</h3><span class="bl">Fed path · inflation prints · how high CPI gets this year · BoJ · recession odds · Texas grid · Hormuz — click a tile for the ladders and the change-over-time chart${(KD.settled&&KD.settled.length)?` · <b style="color:var(--grn);cursor:pointer" onclick="goTab([...document.querySelectorAll('.tabbtn')].find(b=>/Settled/.test(b.textContent)),'settled')">${KD.settled.length} settled → Settled Markets tab</b>`:''}</span></div>`;
 const secC=`<div class="pmsec"><h3>🏢 Companies on your lists</h3><span class="bl">${nco} names · Kalshi KPI ladders and earnings-call books, one row per company — Details expands the full view</span></div>`;
 const secI=`<div class="pmsec"><h3>🚀 AI IPO pipeline</h3><span class="bl">timing curves and reported valuations</span></div>`;
 el.innerHTML=hd+`<div class="pmgrid">${secM}${fed}${lad}${cpimax}${boj}${bin}${energy}${hormuz}${(quantum||stake)?secQ+quantum+stake:''}${secC}${spm}${secI}${ipo}${pipe}</div><div class="calmeta">${KD.note||''}</div>`;
}
// ---- Settled markets — the tracking database fed automatically by build_kalshi.py (anything that settles leaves the live PM section) ----
function toggleST(id){const tr=document.getElementById('st-'+id),tx=document.getElementById('stx-'+id);if(!tr||!tx)return;const on=tx.hidden;tx.hidden=!on;tr.classList.toggle('open',on);tr.querySelector('.seebtn').textContent=on?'Hide':'Details';}
function stHit(r){if(r.status==='pending')return '<span class="hitpill p">⏳ settling</span>';if(r.hit==null)return '<span class="hitpill na">n/a</span>';if(typeof r.hit==='number')return `<span class="hitpill ${r.hit>=0.5?'y':'n'}">${Math.round(r.hit*100)}% · ${r.hit_label||''}</span>`;return r.hit?'<span class="hitpill y">✓ called it</span>':'<span class="hitpill n">✗ missed</span>';}
function stFinal(r){const f=r.final;if(!f)return '<span style="color:var(--mut2)">—</span>';if(f.text)return `<b>${f.text}</b><br><small style="color:var(--mut2)">${f.label||''}</small>`;if(f.p!=null)return `<b>${kpct(f.p)}</b><br><small style="color:var(--mut2)">${f.label||''}</small>`;return '—';}
function stDetail(r){const parts=[];
 if(r.buckets&&r.buckets.length){const mx=Math.max(...r.buckets.map(b=>b.p))||1;parts.push(`<div class="enpanel"><div class="pt" style="font-size:12.5px">Final book before the print</div><div class="kbars" style="height:70px">${r.buckets.filter(b=>b.p>=0.03).map(b=>`<div class="kb${b.p===mx?' on':''}"><span>${kpct(b.p)}</span><i style="height:${Math.max(2,Math.round(b.p/mx*52))}px"></i><span>${b.label}</span></div>`).join('')}</div><div class="pmchips"><span class="pmchip">mode <b>${r.mode}</b></span><span class="pmchip">median <b>${r.median}</b></span>${r.actual!=null?`<span class="pmchip">actual <b>${r.actual}</b></span>`:''}</div></div>`);}
 else if(r.ladder&&r.ladder.length){const mx=Math.max(...r.ladder.map(x=>x[1]))||1;const F=v=>Number(v)>=1000?Math.round(Number(v)).toLocaleString():v;parts.push(`<div class="enpanel"><div class="pt" style="font-size:12.5px">Final ladder (last read)</div>${r.ladder.map(x=>`<div class="hbar"><span class="hl">&gt; ${F(x[0])}</span><span class="ht"><i style="width:${Math.max(1,x[1]/mx*100)}%"></i></span><span class="hv">${kpct(x[1])}</span></div>`).join('')}</div>`);}
 if(r.rows&&r.rows.length){parts.push(`<div class="enpanel"><div class="pt" style="font-size:12.5px">Topics — pre-call odds vs outcome</div>${r.rows.map(x=>`<div class="kcall"><span class="kl">${x.label}</span><span class="kt"><i style="width:${Math.max(1,(x.p_precall||0)*100)}%${x.outcome==='yes'?';background:linear-gradient(90deg,#15803d,#4ade80)':';background:linear-gradient(90deg,#7f1d1d,#f87171)'}"></i></span><span class="kv">${x.p_precall!=null?kpct(x.p_precall):'—'}</span><span class="kd ${x.outcome==='yes'?'up':'dn'}">${x.outcome==='yes'?'✓ said':'✗ not said'}</span></div>`).join('')}</div>`);}
 if(r.history&&r.history.length>1){const H=r.history;const lines=[{label:r.title,pts:H.map(x=>({d:x.d,p:x.p,ev:r.ev,k:'x'})),col:'#a78bfa'}];const ch=pmChartLines(lines,'settled',DATA.kalshi,520,150);if(ch)parts.push(`<div class="enpanel"><div class="pt" style="font-size:12.5px">How the odds moved before settlement</div>${ch.svg}</div>`);}
 parts.push(`<div class="enpanel"><div class="pt" style="font-size:12.5px">Outcome</div><div class="pn" style="margin-top:4px">${r.outcome||'—'}</div><div class="calmeta">Kalshi ${r.ev}${r.vol?' · vol '+Math.round(r.vol).toLocaleString():''}${r.settled_on?' · settled '+r.settled_on:''}${r.closes?' · closes '+r.closes.slice(0,10):''} · archived ${r.archived||''}</div></div>`);
 return `<div class="stx">${parts.join('')}</div>`;}
function renderSettled(){
 const el=document.getElementById('settled');const S=(DATA.kalshi&&DATA.kalshi.settled)||[];
 const hd=`<div class="sthd"><h2>✅ Settled Markets</h2><span class="bl">the tracking database — every Kalshi market that settled (or is settling) moves here automatically from the Prediction Markets tab, with its final read, the outcome, and whether the market called it</span></div>`;
 if(!S.length){el.innerHTML=hd+`<div class="calempty">Nothing has settled yet.</div>`;return;}
 const done=S.filter(r=>r.status!=='pending'),pend=S.filter(r=>r.status==='pending');
 const scored=done.filter(r=>r.hit!=null).map(r=>typeof r.hit==='number'?r.hit:(r.hit?1:0));const rate=scored.length?Math.round(scored.reduce((a,b)=>a+b,0)/scored.length*100):null;
 const sum=`<div class="stsum"><span class="pmchip"><b>${done.length}</b> settled</span><span class="pmchip"><b>${pend.length}</b> settling</span>${rate!=null?`<span class="pmchip">market called it <b>${rate}%</b> <span style="color:var(--mut2)">(${scored.length} scorable)</span></span>`:''}<span class="pmchip">since <b>${S.map(r=>r.settled_on||r.archived).filter(Boolean).sort()[0]||''}</b></span></div>`;
 const CATS=[['macro','🌐 Macro'],['energy','⚡ Texas energy'],['hormuz','🚢 Strait of Hormuz'],['company','🏢 Companies on your lists']];
 const row=r=>{const id=r.id.replace(/[^A-Za-z0-9_-]/g,'_');const tk=r.tk&&C[r.tk]?`<span style="color:var(--cyan);cursor:pointer" onclick="event.stopPropagation();openM('${r.tk}')">${r.tk}</span> `:'';
  return `<tr class="lr" id="st-${id}" onclick="toggleST('${id}')"><td class="q">${tk}<b>${r.title}</b>${r.question||''}</td><td style="white-space:normal;text-align:left;font-size:11.5px">${r.period||''}</td><td style="font-size:11.5px">${r.status==='pending'?'<span style="color:var(--amb)">pending</span>':(r.settled_on||'—')}</td><td>${stFinal(r)}</td><td class="oc"><b>${r.actual||(r.status==='pending'?'awaiting settlement':'—')}</b></td><td class="hit">${stHit(r)}</td><td class="c stk"><button class="seebtn" onclick="event.stopPropagation();toggleST('${id}')">Details</button></td></tr><tr class="lx" id="stx-${id}" hidden><td colspan="7">${stDetail(r)}</td></tr>`;};
 const tbl=rows=>`<div class="ltwrap"><table class="ltbl sttbl"><thead><tr><th>Market</th><th style="text-align:left">Period</th><th>Settled</th><th>Kalshi's final read</th><th style="text-align:left">Outcome</th><th class="c">Called it?</th><th class="c stk">Details</th></tr></thead><tbody>${rows.map(row).join('')}</tbody></table></div>`;
 const body=`<div class="stgrid">${CATS.map(([c,label])=>{const rs=S.filter(r=>r.cat===c);if(!rs.length)return '';const n=rs.length,pn=rs.filter(r=>r.status==='pending').length;
  const sc=rs.filter(r=>r.status!=='pending'&&r.hit!=null).map(r=>typeof r.hit==='number'?r.hit:(r.hit?1:0));const rt=sc.length?Math.round(sc.reduce((a,b)=>a+b,0)/sc.length*100):null;
  const last=rs.map(r=>r.settled_on||r.archived).filter(Boolean).sort().slice(-1)[0]||'';
  return `<details class="stfold" id="stf-${c}"><summary><div class="stf-h"><span class="stf-t">${label}</span><span class="stf-n">${n}</span></div><div class="stf-m"><span>${n-pn} settled${pn?` · <span style="color:var(--amb)">${pn} settling</span>`:''}${rt!=null?` · called it <b>${rt}%</b>`:''}${last?` · last ${last}`:''}</span><span class="pmx stf-x"></span></div></summary><div class="stf-b">${tbl(rs)}</div></details>`;}).join('')}</div>`;
 el.innerHTML=hd+sum+body+`<div class="calmeta">Records are written by the refresh pipeline the moment a market settles (macro ladders with a settlement note, ERCOT daily peaks, Hormuz weekly books, company KPI markets and earnings-call books, US-stake legs). "Called it" = the mode bucket matched the print (ladders), the tracked strike's last read was on the right side of 50% (binary books), or the share of call topics priced correctly. Pending rows are contracts whose period ended but Kalshi has not finalized yet.</div>`;
}


// ---- compute market (Ornn OCPI / OTPI) ----
const CMP=DATA.compute||null;
const CMPCOL={'B200':'#a78bfa','H200':'#38bdf8','H100 SXM':'#2fbf71','A100 SXM4':'#f5a623','RTX 5090':'#f2555a','anthropic':'#e8825f','openai':'#14b8a6','google':'#60a5fa','deepseek':'#c084fc'};
const LABNM={anthropic:'Anthropic',openai:'OpenAI',google:'Google',deepseek:'DeepSeek',minimax:'MiniMax',xiaomi:'Xiaomi',qwen:'Qwen','moonshotai':'Moonshot','z-ai':'Z.ai',mistralai:'Mistral','meta-llama':'Meta Llama'};
let CMPST={g:{mode:'usd',rng:0,off:[]},l:{mode:'usd',rng:0,smooth:true,off:[]}};
try{const s=JSON.parse(localStorage.getItem('aiF_cmp')||'null');if(s&&s.g&&s.l)CMPST=s;}catch(e){}
function cmpSave(){try{localStorage.setItem('aiF_cmp',JSON.stringify(CMPST));}catch(e){}}
const cmpT=s=>new Date(s+'T00:00:00Z').getTime();
function cmpChg(h,days){if(!h||h.length<2)return null;const L=h[h.length-1];let b=null;
 if(days==='all')b=h[0][1];else{const t=cmpT(L[0])-days*864e5;for(let i=h.length-1;i>=0;i--){if(cmpT(h[i][0])<=t){b=h[i][1];break;}}}
 return b?(L[1]/b-1)*100:null;}
function cmpUsd(v,lab){if(v==null)return '—';return '$'+(lab&&v<0.1?v.toFixed(3):v.toFixed(2));}
function cmpPct(p){if(p==null)return '<span class="flat">—</span>';const c=p>0.05?'up':p<-0.05?'down':'flat';return `<span class="${c}">${p>0?'+':''}${Math.abs(p)>=100?p.toFixed(0):p.toFixed(1)}%</span>`;}
function cmpSmooth(h,w){return h.map((p,i)=>{const s=h.slice(Math.max(0,i-w+1),i+1);return [p[0],s.reduce((a,x)=>a+x[1],0)/s.length];});}
function cmpSpark(h,col){if(!h||h.length<2)return '';const v=h.map(p=>p[1]),mn=Math.min(...v),mx=Math.max(...v),r=(mx-mn)||1;
 const pts=v.map((y,i)=>`${(i/(v.length-1)*100).toFixed(2)},${(24-(y-mn)/r*22).toFixed(2)}`).join(' ');
 return `<svg viewBox="0 0 100 26" preserveAspectRatio="none"><polyline points="${pts}" fill="none" stroke="${col}" stroke-width="1.6" vector-effect="non-scaling-stroke"/></svg>`;}
function cmpKalshi(gpu,spot){const key=CMP&&CMP.kalshi_link&&CMP.kalshi_link[gpu];const N=DATA.kalshi&&DATA.kalshi.stock_pm&&DATA.kalshi.stock_pm.NVDA;
 if(!key||!N)return '';const m=(N.markets||[]).find(x=>x.key===key);if(!m||!m.ladder||!m.ladder.length)return '';
 const nxt=m.ladder.find(x=>x[0]>spot),below=m.ladder.filter(x=>x[0]<=spot).map(x=>'$'+x[0].toFixed(2));
 const med=m.p50?`${m.p50[1]||''}$${(+m.p50[0]).toFixed(2)}`:'';
 return `<div class="kx"><span class="kl">Kalshi</span>2026 peak median <b>${med}</b>${nxt?` · &gt;$${nxt[0].toFixed(2)} <b>${Math.round(nxt[1]*100)}%</b>`:''}${below.length?`<br><span style="color:var(--amb)">spot is already above ${below.join(', ')}</span>`:''}</div>`;}
function cmpTile(name,h,kind){const col=CMPCOL[name]||'#94a3b8',L=h[h.length-1],lab=kind==='lab';
 const sp=lab?cmpSmooth(h,7):h;
 return `<div class="cmpt" style="--c:${col}"><div class="nm"><b>${lab?(LABNM[name]||name):name}</b><span>${L[0].slice(5)}</span></div>
 <div class="vl">${cmpUsd(L[1],lab)}<small>${lab?'/M tok':'/GPU-hr'}</small></div>
 <div class="chg"><span><i>1d</i>${cmpPct(cmpChg(h,1))}</span><span><i>7d</i>${cmpPct(cmpChg(h,7))}</span><span><i>30d</i>${cmpPct(cmpChg(h,30))}</span>${(cmpT(L[0])-cmpT(h[0][0]))/864e5>35?`<span><i>${Math.round((cmpT(L[0])-cmpT(h[0][0]))/864e5)}d</i>${cmpPct(cmpChg(h,'all'))}</span>`:''}</div>
 ${cmpSpark(sp,col)}${lab?'':cmpKalshi(name,L[1])}</div>`;}
const CMPDATA={};const CMPOPEN=new Set();
function cmpId(k,n){return k+'-'+n.replace(/[^A-Za-z0-9]/g,'_');}
function toggleCMP(id){if(CMPOPEN.has(id))CMPOPEN.delete(id);else CMPOPEN.add(id);renderCompute();const r=document.getElementById('cr-'+id);if(r&&CMPOPEN.has(id))r.scrollIntoView({behavior:'smooth',block:'nearest'});}
function cmpKxCell(gpu,spot){const key=CMP&&CMP.kalshi_link&&CMP.kalshi_link[gpu];const N=DATA.kalshi&&DATA.kalshi.stock_pm&&DATA.kalshi.stock_pm.NVDA;
 if(!key||!N)return '<span style="color:var(--mut2)">—</span>';const m=(N.markets||[]).find(x=>x.key===key);if(!m||!m.ladder||!m.ladder.length)return '<span style="color:var(--mut2)">—</span>';
 const nxt=m.ladder.find(x=>x[0]>spot),below=m.ladder.filter(x=>x[0]<=spot).length;
 return `2026 peak median <b>${m.p50?(m.p50[1]||'')+'$'+(+m.p50[0]).toFixed(2):'—'}</b>${nxt?` · &gt;$${nxt[0].toFixed(2)} <b>${Math.round(nxt[1]*100)}%</b>`:''}${below?`<br><span class="am">spot above ${below} open strike${below>1?'s':''}</span>`:''}`;}
function cmpTable(k,series,kind){const lab=kind==='lab';const h0=series.length?series[0].hist[0][0]:'';
 const head=`<tr><th>${lab?'Lab':'GPU'}</th><th class="c">Trend</th><th>${lab?'$ / M tokens':'$ / GPU-hr'}</th><th>1D</th><th>7D</th><th>30D</th>${lab?'':`<th>Since ${h0.slice(5)}</th>`}<th>Range (low – high)</th>${lab?'':'<th style="text-align:left">Kalshi (settles on this index)</th>'}<th class="c stk">Card</th></tr>`;
 const rows=series.map(s=>{const h=s.hist,L=h[h.length-1],id=cmpId(k,s.name),open=CMPOPEN.has(id),v=h.map(p=>p[1]),mn=Math.min(...v),mx=Math.max(...v);
  const sp=lab?cmpSmooth(h,7):h;
  let r=`<tr class="lr${open?' open':''}" id="cr-${id}" onclick="toggleCMP('${id}')"><td class="tkc"><span class="dot" style="background:${s.col}"></span>${s.label}<small>${lab?'OTPI blend · '+L[0]:'OCPI daily settle · '+L[0]}</small></td>
  <td class="spc">${cmpSpark(sp,s.col).replace('<svg ','<svg class="spark" ')}</td><td class="pxc">${cmpUsd(L[1],lab)}</td><td class="chc">${cmpPct(cmpChg(h,1))}</td><td class="chc">${cmpPct(cmpChg(h,7))}</td><td class="chc">${cmpPct(cmpChg(h,30))}</td>${lab?'':`<td class="chc">${cmpPct(cmpChg(h,'all'))}</td>`}
  <td class="rng">${cmpUsd(mn,lab)} – ${cmpUsd(mx,lab)}</td>${lab?'':`<td class="kxc">${cmpKxCell(s.name,L[1])}</td>`}<td class="c stk"><button class="seebtn" onclick="event.stopPropagation();toggleCMP('${id}')">${open?'Hide card':'See card'}</button></td></tr>`;
  if(open){const st={mode:'usd',rng:0,off:[],smooth:lab};const ncol=lab?8:10;
   r+=`<tr class="lx"><td colspan="${ncol}"><div class="xrow">${cmpTile(s.name,h,kind)}<div class="cmpcard"><div class="cmpsub" style="margin:0 0 6px">${s.label} — full history<span>${lab?'7-day average · log scale':'$ per GPU-hour'} · hover for values</span></div>${cmpChart('one-'+id,[s],st,kind)}</div></div></td></tr>`;}
  return r;}).join('');
 return `<div class="ltwrap"><table class="ltbl cmptbl"><thead>${head}</thead><tbody>${rows}</tbody></table></div>`;}
function cmpChart(id,series,st,kind){
 const W=760,H=270,pl=50,pr=14,pt=10,pb=24,lab=kind==='lab';
 const lastT=Math.max(...series.map(s=>cmpT(s.hist[s.hist.length-1][0])));const cut=st.rng?lastT-st.rng*864e5:-Infinity;
 let S=series.filter(s=>!(st.off||[]).includes(s.name)).map(s=>{let h=s.hist.filter(p=>cmpT(p[0])>=cut);if(lab&&st.smooth)h=cmpSmooth(h,7);
  if(st.mode==='idx'&&h.length){const b=h[0][1];h=h.map(p=>[p[0],p[1]/b*100]);}return {...s,h};}).filter(s=>s.h.length>1);
 if(!S.length)return `<div class="calempty">All series hidden — click a legend entry to show it.</div>`;
 const log=lab&&st.mode==='usd';const f=v=>log?Math.log10(v):v;
 const xs=[].concat(...S.map(s=>s.h.map(p=>cmpT(p[0])))),x0=Math.min(...xs),x1=Math.max(...xs);
 const ys=[].concat(...S.map(s=>s.h.map(p=>f(p[1])))),ymn=Math.min(...ys),ymx=Math.max(...ys),pad=(ymx-ymn)*.08||.1,y0=(st.mode==='usd'&&!log)?Math.max(0,ymn-pad):ymn-pad,y1=ymx+pad;
 const X=t=>pl+(t-x0)/((x1-x0)||1)*(W-pl-pr),Y=v=>pt+(1-(f(v)-y0)/(y1-y0))*(H-pt-pb);
 let g='';const nt=4;
 for(let i=0;i<=nt;i++){const fv=y0+(y1-y0)*i/nt,v=log?Math.pow(10,fv):fv,yy=pt+(1-i/nt)*(H-pt-pb);
  const lb=st.mode==='idx'?v.toFixed(0):(v<0.1?'$'+v.toFixed(3):v<10?'$'+v.toFixed(2):'$'+v.toFixed(1));
  g+=`<line x1="${pl}" x2="${W-pr}" y1="${yy}" y2="${yy}" stroke="var(--bd)" stroke-width="1"/><text x="${pl-6}" y="${yy+3.5}" text-anchor="end" font-size="10" fill="var(--mut2)">${lb}</text>`;}
 if(st.mode==='idx'&&100>=Math.pow(10,0)&&(y0<100&&y1>100))g+=`<line x1="${pl}" x2="${W-pr}" y1="${Y(100)}" y2="${Y(100)}" stroke="var(--mut2)" stroke-dasharray="3 3" stroke-width="1"/>`;
 const nx=Math.min(6,Math.round((x1-x0)/864e5/7)||2);for(let i=0;i<=nx;i++){const t=x0+(x1-x0)*i/nx,dd=new Date(t).toISOString().slice(5,10);g+=`<text x="${X(t)}" y="${H-6}" text-anchor="middle" font-size="10" fill="var(--mut2)">${dd}</text>`;}
 const paths=S.map(s=>`<polyline points="${s.h.map(p=>X(cmpT(p[0])).toFixed(1)+','+Y(p[1]).toFixed(1)).join(' ')}" fill="none" stroke="${s.col}" stroke-width="2" stroke-linejoin="round"/>`).join('');
 CMPDATA[id]={S,X,Y,W,x0,x1,pl,pr,mode:st.mode,lab};
 return `<div class="cmpwrap" onmousemove="cmpHover(event,'${id}')" onmouseleave="cmpHide('${id}')"><svg id="svg-${id}" viewBox="0 0 ${W} ${H}">${g}${paths}<line id="hl-${id}" x1="0" x2="0" y1="${pt}" y2="${H-pb}" stroke="var(--mut)" stroke-width="1" style="display:none"/></svg><div class="cmptip" id="tip-${id}"></div></div>`;}
function cmpHover(e,id){const D=CMPDATA[id];if(!D)return;const svg=document.getElementById('svg-'+id),r=svg.getBoundingClientRect(),sx=(e.clientX-r.left)/r.width*D.W;
 const t=D.x0+(sx-D.pl)/((D.W-D.pl-D.pr))*(D.x1-D.x0);let best=null;D.S.forEach(s=>s.h.forEach(p=>{const dt=Math.abs(cmpT(p[0])-t);if(!best||dt<best.dt)best={dt,d:p[0]};}));if(!best)return;
 const rows=D.S.map(s=>{const p=s.h.find(q=>q[0]===best.d);return p?{s,v:p[1]}:null;}).filter(Boolean).sort((a,b)=>b.v-a.v);
 const fmt=v=>D.mode==='idx'?v.toFixed(1):cmpUsd(v,D.lab);
 const tip=document.getElementById('tip-'+id),hl=document.getElementById('hl-'+id);hl.setAttribute('x1',D.X(cmpT(best.d)));hl.setAttribute('x2',D.X(cmpT(best.d)));hl.style.display='';
 tip.innerHTML=`<div class="d">${best.d}${D.lab&&CMPST.l.smooth?' · 7-day avg':''}</div>`+rows.map(x=>`<div><i style="background:${x.s.col}"></i>${x.s.label} <b>${fmt(x.v)}</b></div>`).join('');tip.style.display='block';
 const px=(D.X(cmpT(best.d))/D.W)*r.width,tw=tip.offsetWidth;tip.style.left=Math.max(4,Math.min(r.width-tw-4,px+12>r.width-tw-4?px-tw-12:px+12))+'px';}
function cmpHide(id){const t=document.getElementById('tip-'+id),h=document.getElementById('hl-'+id);if(t)t.style.display='none';if(h)h.style.display='none';}
function cmpSet(k,f,v){if(f==='off'){const o=CMPST[k].off||(CMPST[k].off=[]);const i=o.indexOf(v);if(i>=0)o.splice(i,1);else o.push(v);}else CMPST[k][f]=v;cmpSave();renderCompute();}
function cmpBar(k,st,lab){const b=(f,v,t)=>`<button class="cf${st[f]===v?' on':''}" onclick="cmpSet('${k}','${f}',${JSON.stringify(v).replace(/"/g,"'")})">${t}</button>`;
 return `<div class="cmpbar"><span class="lbl">View</span>${b('mode','usd',lab?'$ / M tokens (log)':'$ / GPU-hr')}${b('mode','idx','Indexed (start = 100)')}<span class="sep"></span><span class="lbl">Range</span>${b('rng',30,'30D')}${b('rng',60,'60D')}${b('rng',0,'All')}${lab?`<span class="sep"></span>${b('smooth',true,'7-day avg')}${b('smooth',false,'Daily')}`:''}</div>`;}
function cmpLeg(k,series){const off=CMPST[k].off||[];return `<div class="cmpleg">${series.map(s=>`<span class="${off.includes(s.name)?'off':''}" onclick="cmpSet('${k}','off','${s.name}')"><i style="background:${s.col}"></i>${s.label}</span>`).join('')}<span style="cursor:default;color:var(--mut2)">· click to hide / show</span></div>`;}
function renderCompute(){
 const el=document.getElementById('compute');if(!el)return;
 const hd=`<div class="cmphd"><h2>🖥 Compute Market</h2><span class="bl">what AI compute actually costs — GPU rental rates (Ornn Compute Price Index, $ per GPU-hour, daily settle) and model-API prices by lab (Ornn Token Price Index, $ per million tokens)</span></div>`;
 if(!CMP||!CMP.gpus){el.innerHTML=hd+`<div class="calempty">No compute data yet.</div>`;return;}
 const gs=(CMP.gpu_order||Object.keys(CMP.gpus)).filter(n=>CMP.gpus[n]&&CMP.gpus[n].hist&&CMP.gpus[n].hist.length).map(n=>({name:n,label:n,col:CMPCOL[n]||'#94a3b8',hist:CMP.gpus[n].hist}));
 const ls=(CMP.lab_order||Object.keys(CMP.labs||{})).filter(n=>CMP.labs[n]&&CMP.labs[n].hist&&CMP.labs[n].hist.length).map(n=>({name:n,label:LABNM[n]||n,col:CMPCOL[n]||'#94a3b8',hist:CMP.labs[n].hist}));
 const gT=`<div class="cmpsub">GPU rental — $ per GPU-hour<span>daily settle · ${CMP.last_gpu_day||''} · history since ${gs.length?gs[0].hist[0][0]:''}</span></div>${cmpTable('g',gs,'gpu')}`;
 const gC=`<div class="cmpcard">${cmpBar('g',CMPST.g,false)}${cmpChart('g',gs,CMPST.g,'gpu')}${cmpLeg('g',gs)}</div>`;
 const lT=ls.length?`<div class="cmpsub">Model API prices by lab — $ per million tokens<span>volume-weighted blend across each lab's models · ${CMP.last_lab_day||''} · history since ${ls[0].hist[0][0]}</span></div>${cmpTable('l',ls,'lab')}`:'';
 const lC=ls.length?`<div class="cmpcard">${cmpBar('l',CMPST.l,true)}${cmpChart('l',ls,CMPST.l,'lab')}${cmpLeg('l',ls)}</div>`:'';
 const lk=CMP.locked||{};const note=`<div class="cmpnote"><b>How to read it.</b> GPU lines are the market hourly rental rate for one GPU (the index Kalshi's B200 / H200 / RTX 5090 year-end markets settle on — see the Kalshi column in the GPU table and the NVDA card in Prediction Markets). Lab lines are a usage-weighted blend of each lab's API prices, so they move when the model mix shifts as well as when list prices change — OpenAI's in particular is noisy day to day, hence the 7-day-average default. The history is stored with the dashboard and grows every day, beyond the 3-month window the free Ornn feed returns. <b>Not on the free tier:</b> ${(lk.gpus||[]).join(', ')}${(lk.labs||[]).length?'; labs '+lk.labs.map(x=>LABNM[x]||x).join(', '):''}. Source: Ornn · updated ${(CMP.asof||'').replace('T',' ')}.</div>`;
 el.innerHTML=hd+gT+gC+lT+lC+note;}

// ---- deep research ----
const DR=(DATA.deep_research||[]);
function renderResearch(){
 const el=document.getElementById('research');
 const hd=`<div class="reshd"><h2>🔬 Deep Research</h2><span class="bl">your long-form reports · “See more” expands the summary · then open the full report</span><span class="cnt" style="color:var(--mut2)">${DR.length||''}</span></div>`;
 if(!DR.length){
  el.innerHTML=hd+`<div class="resempty"><b style="color:var(--tx)">No reports loaded yet.</b> To add one, attach the report to the chat (HTML artifact export or PDF) with a note like <i>“Add to Deep Research: &lt;title&gt;”</i> — it is hosted under /reports on the dashboard site, gets a summary card here, and is tagged to its tickers. Updates work the same way: send a new version and it replaces the old one in the next refresh.</div>`;
  return;
 }
 el.innerHTML=hd+`<div class="resgrid">`+DR.map((r,i)=>{
  let kpis='';
  if(r.kpis&&r.kpis.length) kpis=`<div class="reskpis">${r.kpis.map(k=>`<div class="rk"><div class="rkl">${k[0]}</div><div class="rkv">${k[1]}</div></div>`).join('')}</div>`;
  let chart='';
  if(r.chart&&r.chart.series&&r.chart.series.length){
   const S=r.chart.series,mx=Math.max(...S.map(s=>s[1]));
   chart=`<div class="reschart"><div class="rcl">${r.chart.label||''}</div><div class="rcbars">${S.map(s=>{
    const h=Math.max(4,Math.round((s[1]/mx)*82)),est=(''+s[0]).includes('E');
    return `<div class="rcb"><div class="rct"><div class="rcstack"><div class="rcv">${s[2]||s[1]}</div><div class="rcbar${est?' est':''}" style="height:${h}%"></div></div></div><div class="rcx">${s[0]}</div></div>`;
   }).join('')}</div></div>`;
  }
  let comm='';
  if(r.commentary&&r.commentary.length) comm=`<ul class="rescomm">${r.commentary.map(c=>`<li>${c}</li>`).join('')}</ul>`;
  const open=RX_OPEN.has(i);
  return `
  <div class="rescard${open&&r.wide?' wide':''}${open?' open':''}" id="rescard-${i}">
   <div class="rt">${r.title}</div>
   <div class="rd">${r.date||''}${r.author?' · '+r.author:''}${r.src?' · '+r.src:''}</div>
   <div class="rs">${r.summary||''}</div>
   ${(r.tickers&&r.tickers.length)?`<div class="rtk">${r.tickers.map(t=>`<span>${t}</span>`).join('')}</div>`:''}
   <div class="resx"${open?'':' hidden'}>${kpis}${chart}${comm}<div class="resopen" onclick="event.stopPropagation();openResearch(${i})">${r.url?'📖 Open the full report ↗ <span style="font-weight:400;color:var(--mut)">(hosted, new tab)</span>':'📖 Read the full report →'}</div>${r.url&&r.body_html?`<div class="resopen" style="margin-top:5px;font-weight:500;color:var(--mut)" onclick="event.stopPropagation();openResearch(${i},true)">text-only version (offline)</div>`:''}</div>
   <button class="resmore" onclick="event.stopPropagation();toggleResearch(${i})">${open?'See less ▴':'See more ▾'}</button>
  </div>`;}).join('')+`</div>`;
}
const RX_OPEN=new Set();
function toggleResearch(i){if(RX_OPEN.has(i))RX_OPEN.delete(i);else RX_OPEN.add(i);renderResearch();const el=document.getElementById('rescard-'+i);if(el&&RX_OPEN.has(i))el.scrollIntoView({behavior:'smooth',block:'nearest'});}
function openResearch(i,textOnly){
 const r=DR[i]; if(!r) return;
 if(r.url&&!textOnly){window.open(r.url,'_blank','noopener');return;}
 const m=document.getElementById('modal');
 if(r.doc){
  m.innerHTML=`<div class="mhd"><div><div class="t1">${r.title}</div><div class="t2">${r.date||''}${r.src?' · '+r.src:''} · Deep Research — full report</div></div>
   <span class="x" onclick="closeM()">✕</span></div>
   <iframe id="drframe" style="width:100%;height:78vh;border:0;border-radius:0 0 12px 12px;background:#fff"></iframe>`;
  document.getElementById('drframe').srcdoc=r.doc;
 }else{
  m.innerHTML=`<div class="mhd"><div><div class="t1">${r.title}</div><div class="t2">${r.date||''}${r.src?' · '+r.src:''} · Deep Research</div></div>
   <span class="x" onclick="closeM()">✕</span></div>
   <div class="mbody"><div class="resbody">${r.body_html||('<p>'+(r.summary||'')+'</p><p style="color:var(--mut)">Full text not embedded'+(r.link?' — <a href="'+r.link+'" target="_blank" style="color:var(--cyan)">open the source report ↗</a>':'')+'.</p>')}</div></div>`;
 }
 document.getElementById('ov').classList.add('on');document.body.style.overflow='hidden';
}
// ---- tabs ----
function goTab(btn,id){
 if(id==='earnrail'&&!RAILS.er)setRail('er',1);
 if(id==='newsrail'&&!RAILS.nw)setRail('nw',1);
 document.querySelectorAll('.tabbtn').forEach(b=>b.classList.remove('on'));
 btn.classList.add('on');
 const t=document.getElementById(id);
 if(t) t.scrollIntoView({behavior:'smooth',block:'start'});
}
applyRails();renderPending();render();renderEarnRail();renderNews();renderCalendar();renderCompute();renderPredict();renderSettled();renderResearch();renderStripGhosts();
</script></body></html>'''
html=html.replace('__PAYLOAD__',payload)
open('index.html','w').write(html)
print("index.html written:",len(html),"bytes")

# ---------------- WEB BUILD (Vercel) ----------------
# Vercel's API is unreachable from this workspace, so deploys go through the chat connector
# (file contents inline). The page is therefore split into small plain-JSON shards, each its
# own Vercel project, so only the LIVE shard is re-pushed at each refresh:
#   deploy/app/     index.html (markup + loader) + app.js + research.json + vercel.json   (rare: renderer/report changes)
#   deploy/live/    live.json   = indices/sectors/pulse/earnings + per-company LIVE fields  (EVERY refresh, ~100KB)
#   deploy/static/  static.json = per-company static fields (description, officers, charts, thesis…) (weekly / when roster changes)
#   deploy/cat1/ cat2/  cat.json = compact catalog halves (when the catalog changes)
# Data-shard hosts live in deploy/hosts.json (filled after the first deploy of each shard).
import os, copy
STATIC_KEYS={'description','officers','website','chart','edgar_insider','edgar_all','edgar_13f','stocktwits',
             'name','sector','industry','country','exchange','employees','thesis','opportunities','threats'}
if os.environ.get('WEB'):
    for sub in ('app','live','static','cat1','cat2'): os.makedirs('deploy/'+sub, exist_ok=True)
    J=lambda o: json.dumps(o,separators=(',',':'),ensure_ascii=False)
    def w(path,obj): open(path,'w').write(J(obj)); return os.path.getsize(path)
    live={k:v for k,v in data.items() if k not in ('catalog','markets_catalog','deep_research','companies')}
    live['companies']={t:{k:v for k,v in c.items() if k not in STATIC_KEYS} for t,c in data['companies'].items()}
    stat={t:{k:v for k,v in c.items() if k in STATIC_KEYS} for t,c in data['companies'].items()}
    for t,c in stat.items():   # trim monthly history to ~10y to keep the shard small
        ch=c.get('chart') or {}
        if isinstance(ch.get('m'),list) and len(ch['m'])>120: ch['m']=ch['m'][-120:]
    cat=data.get('catalog',{})
    S=sorted(set(c['sector'] for c in cat.values())); XL=sorted(set(c['x'] for c in cat.values() if c.get('x')))
    comp={}
    for t,c in cat.items():
        f=0
        if c.get('b'): f=1
        if c.get('k'): f=2
        if c.get('x'): f=3+XL.index(c['x'])
        comp[t]=[c['name'],S.index(c['sector']),f]
    ks=sorted(comp); half=len(ks)//2
    res=copy.deepcopy(data.get('deep_research',[]))
    for r in res: r.pop('doc',None); r.pop('doc_ref',None)
    n_live=w('deploy/live/live.json',live)
    n_stat=w('deploy/static/static.json',stat)
    n_c1=w('deploy/cat1/cat.json',{'S':S,'X':XL,'C':{k:comp[k] for k in ks[:half]}})
    n_c2=w('deploy/cat2/cat.json',{'S':S,'X':XL,'C':{k:comp[k] for k in ks[half:]},'markets_catalog':data.get('markets_catalog',[]),'catalog_as_of':data.get('catalog_as_of')})
    n_res=w('deploy/app/research.json',{'deep_research':res})
    cors=json.dumps({"headers":[{"source":"/(.*)","headers":[
        {"key":"Access-Control-Allow-Origin","value":"*"},
        {"key":"Cache-Control","value":"public, max-age=0, must-revalidate"}]}]},indent=1)
    for sub in ('live','static','cat1','cat2'): open(f'deploy/{sub}/vercel.json','w').write(cors)
    open('deploy/app/vercel.json','w').write(json.dumps({"headers":[{"source":"/(.*)","headers":[
        {"key":"Cache-Control","value":"public, max-age=0, must-revalidate"},
        {"key":"X-Robots-Tag","value":"noindex, nofollow"}]}]},indent=1))
    hosts={'live':'','static':'','cat1':'','cat2':''}
    if os.path.exists('deploy/hosts.json'): hosts.update(json.load(open('deploy/hosts.json')))
    s0=html.index('<script>\nconst DATA='); s1=html.rindex('</script></body></html>')
    script=html[s0+len('<script>\n'):s1].replace('const DATA='+payload+';','const DATA=window.__DATA__;',1)
    open('deploy/app/app.js','w').write(script)
    loader=open('web_loader.js').read().replace('__HOSTS__',json.dumps(hosts))
    shell=html[:s0]+'<script>\n'+loader+'\n</script></body></html>'
    shell=shell.replace('<title>AI & Frontier Tech — Financial Dashboard</title>','<title>AI & Frontier Tech — Financial Dashboard</title>\n<meta name="robots" content="noindex,nofollow"/>')
    open('deploy/app/index.html','w').write(shell)
    print(f"web build: app/index.html {len(shell)}  app.js {len(script)}  research.json {n_res} | live.json {n_live} | static.json {n_stat} | cat1 {n_c1} cat2 {n_c2} | hosts={hosts}")
