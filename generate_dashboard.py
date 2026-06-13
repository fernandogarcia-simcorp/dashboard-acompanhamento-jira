# -*- coding: utf-8 -*-
"""Gera dashboard.html (auto-contido, dados embutidos) a partir de dashboard_data.json.
Estilo: SIMCORP Design System (Raleway, navy + verde lima, sem emoji)."""
import json, os, datetime

OUT = os.path.dirname(os.path.abspath(__file__))
data = json.load(open(os.path.join(OUT,'dashboard_data.json'), encoding='utf-8'))
data_js = json.dumps(data, ensure_ascii=False)

MES_EXT = ['janeiro','fevereiro','março','abril','maio','junho','julho','agosto','setembro','outubro','novembro','dezembro']
g = datetime.date.fromisoformat(data['generated'])
gen_str = f"{g.day:02d} de {MES_EXT[g.month-1]} de {g.year}"

TEMPLATE = r"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Suporte / Operações / Desenvolvimento — Status Report Semanal</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Raleway:ital,wght@0,400;0,500;0,600;0,700;0,800;1,500;1,600&display=swap" rel="stylesheet">
<style>
:root{
  --navy:#023859; --navy-700:#024873; --green:#84BF04; --green-300:#ACBF65;
  --green-deep:#4A6E03; --blue:#0079C1; --gray-700:#4D4D4D; --gray-400:#B3B3B3;
  --gray-50:#EFF1EF; --danger:#C0392B; --danger-deep:#8A2920; --warn:#E67E22; --warn-deep:#8A4B12;
  --border:#E4E7E5; --surface:#FFFFFF; --bg:#F4F6F4;
  --grad-blue:linear-gradient(135deg,#024873 0%,#023859 100%);
  --grad-green:linear-gradient(135deg,#84BF04 0%,#ACBF65 100%);
  --grad-brand:linear-gradient(120deg,#024873 0%,#023859 55%,#1f5e54 100%);
  --sh-xs:0 1px 2px rgba(2,56,89,.06);
  --sh-sm:0 2px 6px rgba(2,56,89,.08);
  --sh-md:0 6px 18px rgba(2,56,89,.10);
  --sh-lg:0 14px 40px rgba(2,56,89,.14);
  --font:"Raleway","Helvetica Neue",Arial,sans-serif;
  --mono:ui-monospace,"SF Mono",Menlo,Consolas,monospace;
}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:var(--font);background:var(--bg);color:var(--gray-700);
  font-size:16px;line-height:1.5;-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale}
.wrap{max-width:1200px;margin:0 auto;padding:0 32px}
.mono{font-family:var(--mono)}
a{color:var(--blue);text-decoration:none;transition:color .12s cubic-bezier(.22,1,.36,1)}
a:hover{color:var(--navy-700)}
.ic{width:1em;height:1em;display:inline-block;vertical-align:-.125em;flex-shrink:0}
.eyebrow{font-size:11px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--green)}

/* ---------- header (navy band) ---------- */
.topband{background:var(--grad-brand);position:relative;overflow:hidden}
.topband::after{content:"";position:absolute;right:-60px;top:-40px;width:340px;height:340px;
  background:radial-gradient(circle, rgba(132,191,4,.16), transparent 70%);pointer-events:none}
.topband .wrap{padding:34px 32px 38px;position:relative;z-index:1}
.brandrow{display:flex;align-items:center;justify-content:space-between;gap:20px;margin-bottom:30px}
.logo-plate{background:#fff;border-radius:7px;padding:9px 16px;display:inline-flex;box-shadow:var(--sh-sm)}
.logo-plate img{height:30px;width:auto;display:block}
.brandrow .env{font-family:var(--mono);font-size:11px;letter-spacing:.06em;color:rgba(255,255,255,.62)}
.h-eyebrow{font-size:12px;font-weight:800;letter-spacing:.22em;text-transform:uppercase;color:var(--green)}
.h-title{font-weight:800;font-size:clamp(28px,4.3vw,50px);line-height:1.04;letter-spacing:-.02em;color:#fff;margin:12px 0 0}
.h-title b{color:var(--green);font-weight:800}
.h-meta{display:flex;flex-wrap:wrap;gap:10px 22px;align-items:center;margin-top:22px;font-size:13.5px;color:rgba(255,255,255,.82)}
.h-meta b{color:#fff;font-weight:700}
.h-chip{display:inline-flex;align-items:center;gap:7px;border:1px solid rgba(255,255,255,.28);border-radius:999px;
  padding:5px 13px;font-family:var(--mono);font-size:12px;color:#fff;background:rgba(255,255,255,.06)}
.h-chip .d{width:7px;height:7px;border-radius:50%;background:var(--green)}

/* ---------- alert banner ---------- */
.alert-banner{display:flex;align-items:center;gap:16px;background:#FBEAE6;border:1px solid #E3A99B;
  border-left:5px solid var(--danger);border-radius:8px;padding:15px 20px;margin:22px 0 0;box-shadow:var(--sh-sm)}
.alert-banner .ab-ic{color:var(--danger);font-size:26px;display:flex;flex-shrink:0}
.alert-banner .ab-n{font-weight:800;font-size:34px;line-height:1;color:var(--danger);flex-shrink:0}
.alert-banner .ab-tx{font-size:13.5px;line-height:1.45;color:var(--danger-deep)}
.alert-banner .ab-tx b{font-weight:700}
.alert-banner a.ab-cta{margin-left:auto;flex-shrink:0;font-weight:700;font-size:11px;letter-spacing:.06em;
  text-transform:uppercase;background:var(--danger);color:#fff;padding:9px 16px;border-radius:4px;transition:.16s}
.alert-banner a.ab-cta:hover{background:#a5301f;color:#fff}

/* ---------- section ---------- */
section{padding:44px 0}
.sec-head{display:flex;align-items:flex-end;justify-content:space-between;gap:20px;margin-bottom:24px;
  border-bottom:2px solid var(--navy);padding-bottom:12px}
.sec-head .l .eyebrow{margin-bottom:6px}
.sec-head h2{font-weight:800;font-size:30px;letter-spacing:-.01em;color:var(--navy);line-height:1.05}
.sec-num{font-family:var(--mono);font-size:12px;color:var(--gray-400);letter-spacing:.16em;white-space:nowrap}

/* ---------- surface / panel ---------- */
.panel{background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:24px;box-shadow:var(--sh-sm)}
.panel h3{font-weight:700;font-size:19px;color:var(--navy);margin-bottom:18px;display:flex;align-items:center;gap:9px}
.panel h3 .ic{color:var(--green);font-size:20px}
.cols{display:grid;grid-template-columns:1.15fr .85fr;gap:24px}

/* ---------- pills ---------- */
.pill{display:inline-flex;align-items:center;gap:6px;padding:3px 10px;border-radius:999px;font-size:11px;
  font-weight:700;letter-spacing:.03em;white-space:nowrap}
.pill .d{width:6px;height:6px;border-radius:50%}
.pill.done{background:#EAF6D4;color:var(--green-deep)} .pill.done .d{background:var(--green)}
.pill.prog{background:#FCEBD9;color:var(--warn-deep)} .pill.prog .d{background:var(--warn)}
.pill.todo{background:#EFF1EF;color:var(--gray-700)} .pill.todo .d{background:var(--gray-400)}

/* ---------- filter bar ---------- */
.filterbar{position:sticky;top:0;z-index:60;background:var(--surface);border-bottom:1px solid var(--border);box-shadow:var(--sh-xs)}
.filterbar .wrap{display:flex;align-items:center;gap:14px;padding:11px 32px;max-width:1200px}
.fb-label{font-size:11px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--gray-400);flex-shrink:0}
.fb-btns{display:flex;gap:8px;flex-wrap:wrap}
.fbtn{font-family:var(--font);font-size:12.5px;font-weight:700;letter-spacing:.02em;color:var(--navy);background:var(--bg);
  border:1px solid var(--border);border-radius:999px;padding:7px 16px;cursor:pointer;transition:all .16s cubic-bezier(.22,1,.36,1)}
.fbtn:hover{border-color:var(--navy-700);color:var(--navy-700)}
.fbtn.active{background:var(--navy);color:#fff;border-color:var(--navy)}
.fbtn .c{opacity:.55;font-weight:600;margin-left:6px;font-family:var(--mono);font-size:11px}
.fbtn.active .c{opacity:.8}
.fb-per{margin-left:auto}
.fb-select{font-family:var(--font);font-size:12.5px;font-weight:600;color:var(--navy);background:var(--surface);
  border:1px solid var(--border);border-radius:8px;padding:7px 12px;cursor:pointer;max-width:240px}
.fb-select:hover{border-color:var(--navy-700)}
.fb-select:focus{outline:none;border-color:var(--blue);box-shadow:0 0 0 3px rgba(0,121,193,.15)}
/* ---------- portfolio ---------- */
.portfolio{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.pcard{background:var(--surface);border:1px solid var(--border);border-top:3px solid var(--c);border-radius:8px;padding:22px;box-shadow:var(--sh-sm)}
.pcard .ptop{display:flex;align-items:center;justify-content:space-between;gap:8px}
.pcard .pk{font-family:var(--mono);font-size:11px;font-weight:700;color:var(--blue)}
.pcard .ptag{font-size:9px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;padding:3px 8px;border-radius:999px;background:var(--gray-50);color:var(--gray-700)}
.pcard .pn{font-weight:700;font-size:16px;color:var(--navy);margin:8px 0 14px;line-height:1.25;min-height:40px}
.pcard .prow{display:flex;align-items:flex-end;justify-content:space-between;gap:10px}
.pcard .ptot{font-weight:800;font-size:44px;color:var(--navy);line-height:.95}
.pcard .ppct{text-align:right}
.pcard .ppct b{font-weight:800;font-size:22px;color:var(--green-deep)}
.pcard .ppct span{display:block;font-size:10px;color:var(--gray-400);font-weight:700;text-transform:uppercase;letter-spacing:.06em}
.pcard .pstrip{height:9px;border-radius:5px;display:flex;overflow:hidden;background:var(--gray-50);border:1px solid var(--border);margin:14px 0 9px}
.pcard .pstrip span{height:100%}
.pcard .pleg{display:flex;flex-wrap:wrap;gap:5px 14px;font-size:11.5px;color:var(--gray-700)}
.pcard .pleg i{width:8px;height:8px;border-radius:2px;display:inline-block;margin-right:5px}
.pcard .pfoot{margin-top:12px;padding-top:10px;border-top:1px solid var(--border);font-size:11.5px;color:var(--gray-700);display:flex;justify-content:space-between}
/* ---------- support projects ---------- */
.sup-proj{margin-bottom:26px}
.sup-proj:last-child{margin-bottom:0}
.sup-head{display:flex;align-items:center;gap:12px;margin-bottom:16px}
.sup-head .sk{font-family:var(--mono);font-size:12px;font-weight:700;color:var(--blue)}
.sup-head .sn{font-weight:700;font-size:18px;color:var(--navy)}
.sup-head .ln{flex:1;height:1px;background:var(--border)}
.sup-kpis{display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin-bottom:18px}
.sup-kpi{background:var(--bg);border:1px solid var(--border);border-radius:6px;padding:13px 15px}
.sup-kpi .n{font-weight:800;font-size:26px;color:var(--navy);line-height:1}
.sup-kpi .n small{font-size:13px;color:var(--gray-400);font-weight:700}
.sup-kpi .l{font-size:10px;text-transform:uppercase;letter-spacing:.07em;color:var(--gray-400);font-weight:700;margin-top:4px}
.sup-cols{display:grid;grid-template-columns:1.1fr .9fr;gap:24px}
.statbars{display:flex;flex-direction:column;gap:10px}
.statbars .sb{display:grid;grid-template-columns:160px 1fr 34px;align-items:center;gap:10px;font-size:12.5px}
.statbars .sb .nm{color:var(--gray-700);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.statbars .sb .tr{height:16px;background:var(--gray-50);border-radius:4px;overflow:hidden;border:1px solid var(--border)}
.statbars .sb .tr span{display:block;height:100%}
.statbars .sb .n{font-family:var(--mono);font-weight:700;text-align:right;color:var(--navy)}
.sub-eyebrow{font-size:10px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--gray-400);margin-bottom:10px}
.sup-cols.cf-row{grid-template-columns:1fr 1fr}
.cf-divider{display:flex;align-items:center;gap:10px;margin:24px 0 4px}
.cf-divider .lbl{font-size:10px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--green-deep)}
.cf-divider .ln{flex:1;height:1px;background:var(--border)}
/* ---------- KPIs ---------- */
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}
.kpi{background:var(--surface);border:1px solid var(--border);border-top:3px solid var(--c);border-radius:8px;
  padding:20px 22px;box-shadow:var(--sh-sm)}
.kpi .lab{font-size:11px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;color:var(--gray-400)}
.kpi .num{font-weight:800;font-size:52px;line-height:1.02;color:var(--navy);margin:8px 0 2px}
.kpi .num small{font-size:22px;color:var(--gray-400);font-weight:700}
.kpi .meta{font-size:12.5px;color:var(--gray-700)}

/* ---------- hero progress ---------- */
.hero-prog{margin-top:18px;background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:22px 24px;box-shadow:var(--sh-sm)}
.hero-prog .row{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:12px}
.hero-prog .row .t{font-weight:700;color:var(--navy);font-size:15px}
.hero-prog .pct{font-weight:800;font-size:28px;color:var(--navy)}
.bar{height:26px;border-radius:6px;overflow:hidden;display:flex;border:1px solid var(--border);background:var(--gray-50)}
.bar span{height:100%;display:flex;align-items:center;justify-content:center;font-family:var(--mono);font-size:11px;
  color:#fff;font-weight:600;transition:width .9s cubic-bezier(.22,1,.36,1)}
.legend{display:flex;flex-wrap:wrap;gap:18px;margin-top:13px;font-size:13px;color:var(--gray-700)}
.legend i{width:11px;height:11px;border-radius:3px;display:inline-block;margin-right:6px;vertical-align:-1px}

/* ---------- epic cards ---------- */
.epic-sub{display:flex;align-items:center;gap:12px;margin:8px 0 16px}
.epic-sub .lbl{font-size:12px;font-weight:800;letter-spacing:.12em;text-transform:uppercase;color:var(--navy)}
.epic-sub .lbl.green{color:var(--green-deep)}
.epic-sub .ct{font-family:var(--mono);font-size:11px;font-weight:700;color:var(--gray-400)}
.epic-sub .ln{flex:1;height:1px;background:var(--border)}
.epic-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.epic-grid + .epic-sub{margin-top:30px}
/* ---------- orphan list ---------- */
.orphan-grid{display:grid;grid-template-columns:1fr 1fr;gap:0 30px}
.orow{display:grid;grid-template-columns:96px 1fr auto;align-items:center;gap:12px;padding:11px 0;border-bottom:1px solid var(--border)}
.orow .k{font-family:var(--mono);font-size:11px;font-weight:700;color:var(--blue)}
.orow .s{font-size:13px;line-height:1.3;color:var(--navy);font-weight:600}
.orow .w{font-size:11px;color:var(--gray-700);margin-top:2px}
.epic-card{background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:20px;box-shadow:var(--sh-sm);
  display:flex;flex-direction:column;transition:box-shadow .2s,transform .2s}
.epic-card:hover{box-shadow:var(--sh-md);transform:translateY(-2px)}
.epic-card.orphan{background:#FAFBFA;border-style:dashed}
.ec-top{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:10px}
.ec-key{font-family:var(--mono);font-size:11px;font-weight:700;color:var(--blue)}
.ec-title{font-weight:700;font-size:15px;color:var(--navy);line-height:1.3;min-height:39px;margin-bottom:14px}
.ec-pctrow{display:flex;align-items:baseline;gap:8px;margin-bottom:10px}
.ec-pct{font-weight:800;font-size:38px;line-height:1;color:var(--navy)}
.ec-pctlab{font-size:12px;color:var(--gray-400);font-weight:700}
.ec-stack{height:10px;border-radius:5px;overflow:hidden;display:flex;background:var(--gray-50);border:1px solid var(--border)}
.ec-stack span{height:100%;transition:width .8s cubic-bezier(.22,1,.36,1)}
.ec-legend{display:flex;flex-wrap:wrap;gap:4px 14px;margin-top:11px;font-size:11.5px;color:var(--gray-700)}
.ec-legend i{width:8px;height:8px;border-radius:2px;display:inline-block;margin-right:5px;vertical-align:0}
.ec-foot{display:flex;align-items:center;justify-content:space-between;margin-top:14px;padding-top:12px;
  border-top:1px solid var(--border);font-size:12px;color:var(--gray-700)}
.ec-foot .h{font-family:var(--mono);font-weight:700;color:var(--navy)}

/* ---------- weekly chart ---------- */
.chart{display:flex;align-items:flex-end;gap:10px;height:200px;padding-top:10px;border-bottom:1px solid var(--border);margin-bottom:8px}
.wk{flex:1;display:flex;flex-direction:column;align-items:center;gap:4px;height:100%;justify-content:flex-end}
.wk .bars{display:flex;gap:3px;align-items:flex-end;height:100%;width:100%;justify-content:center}
.wk .b{width:15px;border-radius:3px 3px 0 0;transition:height .8s cubic-bezier(.22,1,.36,1)}
.wk .b.c{background:var(--grad-blue)}
.wk .b.d{background:var(--grad-green)}
.wk .lbl{font-family:var(--mono);font-size:10px;color:var(--gray-400);white-space:nowrap}

/* ---------- donut ---------- */
.donut-wrap{display:flex;align-items:center;gap:22px}
.donut{flex-shrink:0}
.donut-legend{display:flex;flex-direction:column;gap:9px;font-size:13px;width:100%}
.donut-legend .li{display:flex;align-items:center;justify-content:space-between;gap:8px;border-bottom:1px solid var(--border);padding-bottom:7px}
.donut-legend .li .nm{display:flex;align-items:center;gap:8px;color:var(--gray-700)}
.donut-legend .li b{font-family:var(--mono);color:var(--navy)}

/* ---------- assignee ---------- */
.asg{display:flex;flex-direction:column;gap:13px}
.asg .a{display:grid;grid-template-columns:140px 1fr 42px;align-items:center;gap:12px}
.asg .a .nm{font-size:13.5px;font-weight:600;color:var(--navy);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.asg .a .track{height:20px;background:var(--gray-50);border-radius:5px;overflow:hidden;border:1px solid var(--border)}
.asg .a .track span{display:block;height:100%;background:var(--grad-blue);transition:width .9s cubic-bezier(.22,1,.36,1)}
.asg .a .track.stacked{display:flex}
.asg .a .track.stacked span{background:none}
.asg .a .n{font-family:var(--mono);font-size:13px;text-align:right;font-weight:700;color:var(--navy)}
.two-small{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:22px}
.minib{display:flex;flex-direction:column;gap:9px}
.minib .r{display:flex;align-items:center;gap:10px;font-size:13px}
.minib .r .t{height:15px;border-radius:3px;flex-shrink:0}
.minib .r .lab{min-width:74px;color:var(--gray-700)}
.minib .r .n{margin-left:auto;font-family:var(--mono);font-weight:700;color:var(--navy)}

/* ---------- worklog table ---------- */
.wl{width:100%;border-collapse:collapse;font-size:13px}
.wl td{padding:12px 6px;border-bottom:1px solid var(--border);vertical-align:top}
.wl tr:last-child td{border-bottom:none}
.wl .k{font-family:var(--mono);font-size:11px;font-weight:700;color:var(--blue);white-space:nowrap}
.wl .sm{font-size:13px;line-height:1.35;color:var(--navy);font-weight:600}
.wl .meta{font-size:11px;color:var(--gray-700);margin-top:3px}
.wl .hrs{font-family:var(--mono);font-weight:700;text-align:right;white-space:nowrap;font-size:14px;color:var(--navy)}
.tag{display:inline-block;font-family:var(--mono);font-size:9.5px;letter-spacing:.05em;padding:2px 7px;border-radius:999px;margin-left:6px;vertical-align:1px;font-weight:700}
.tag-tempo{background:#EAF6D4;color:var(--green-deep)}
.tag-test{background:#EFF1EF;color:var(--gray-700)}
.wl-foot{display:flex;justify-content:space-between;align-items:baseline;margin-top:14px;padding-top:14px;border-top:2px solid var(--navy)}
.wl-foot span{font-weight:700;color:var(--navy)}
.wl-foot b{font-weight:800;font-size:28px;color:var(--navy)}
.note{background:#DDEEF8;border:1px solid #B6D6EC;border-radius:8px;padding:17px 19px;font-size:13px;line-height:1.55;color:var(--navy-700)}
.note b{font-weight:700}
.note ul{margin:8px 0 0 18px}
.note li{margin:4px 0}
.note.warnbox{background:#FCEBD9;border-color:#EBC59B;color:var(--warn-deep)}

/* ---------- alert list ---------- */
.alert-list{display:flex;flex-direction:column}
.alert-row{display:grid;grid-template-columns:96px 1fr auto auto;align-items:center;gap:14px;padding:13px 0;border-bottom:1px solid var(--border)}
.alert-row:last-child{border-bottom:none}
.alert-row .k{font-family:var(--mono);font-size:11px;font-weight:700;color:var(--blue)}
.alert-row .info .s{font-size:13.5px;line-height:1.3;color:var(--navy);font-weight:600}
.alert-row .info .m{font-size:11.5px;color:var(--gray-700);margin-top:2px}
.alert-row .idle{font-family:var(--mono);font-size:12px;font-weight:700;text-align:right;white-space:nowrap;padding:4px 10px;border-radius:4px}
.idle-hi{background:#FBEAE6;color:var(--danger)}
.idle-md{background:#FCEBD9;color:var(--warn-deep)}
.idle-lo{background:#EFF1EF;color:var(--gray-700)}
.zero{color:var(--danger);font-weight:800}

/* ---------- weekly report ---------- */
.rep-grid{display:grid;grid-template-columns:1fr 1fr;gap:24px}
.task{display:flex;gap:11px;padding:11px 0;border-bottom:1px solid var(--border);align-items:flex-start}
.task:last-child{border-bottom:none}
.task .k{font-family:var(--mono);font-size:11px;font-weight:700;color:var(--blue);flex-shrink:0;width:108px}
.task .tx{font-size:13.5px;line-height:1.4;color:var(--navy);font-weight:500}
.task .who{font-size:11.5px;color:var(--gray-700);margin-top:2px}
.count-badge{font-family:var(--mono);font-size:12px;background:var(--navy);color:#fff;border-radius:999px;padding:2px 10px;font-weight:600;margin-left:4px}
.count-badge.danger{background:var(--danger)}
.ptag2{display:inline-block;font-family:var(--mono);font-size:9.5px;font-weight:700;letter-spacing:.04em;color:#fff;padding:2px 7px;border-radius:999px;margin-left:6px;vertical-align:1px}
.projweek{display:flex;flex-direction:column;gap:10px}
.projweek .r{display:grid;grid-template-columns:1fr auto auto auto;gap:12px;align-items:center;font-size:13px;padding-bottom:9px;border-bottom:1px solid var(--border)}
.projweek .r:last-child{border-bottom:none}
.projweek .r .pn{font-weight:700;color:var(--navy)}
.projweek .r .v{font-family:var(--mono);font-weight:700;min-width:54px;text-align:right}
.projweek .hd{font-size:10px;text-transform:uppercase;letter-spacing:.06em;color:var(--gray-400);font-weight:700}

/* ---------- footer ---------- */
footer{background:var(--grad-blue);margin-top:36px}
footer .wrap{padding:34px 32px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:18px}
footer .logo-plate{background:#fff;border-radius:7px;padding:8px 14px;display:inline-flex;box-shadow:var(--sh-sm)}
footer .logo-plate img{height:26px;display:block}
footer .ft{font-size:12.5px;color:rgba(255,255,255,.7);text-align:right;line-height:1.7}
footer .ft .mono{color:rgba(255,255,255,.85)}

img,svg{max-width:100%}
/* permite que colunas de texto encolham (evita overflow horizontal no mobile) */
.orow>div,.alert-row .info,.task>div,.wl .sm{min-width:0}
.orow .s,.alert-row .info .s,.task .tx,.wl .sm{overflow-wrap:anywhere}
@media(max-width:1024px){
  .epic-grid{grid-template-columns:repeat(2,1fr)}
  .portfolio{grid-template-columns:1fr}
  .sup-kpis{grid-template-columns:repeat(3,1fr)}
}
@media(max-width:760px){
  .wrap{padding:0 20px}
  .filterbar .wrap{padding:10px 20px}
  .topband .wrap{padding:28px 20px 30px}
  .kpis{grid-template-columns:repeat(2,1fr)}
  .cols,.rep-grid,.two-small,.epic-grid,.sup-cols,.sup-cols.cf-row{grid-template-columns:1fr}
  .sup-kpis{grid-template-columns:repeat(2,1fr)}
  .orphan-grid{grid-template-columns:1fr}
  .donut-wrap{flex-wrap:wrap;justify-content:center}
  .asg .a{grid-template-columns:120px 1fr 40px}
  .statbars .sb{grid-template-columns:130px 1fr 32px}
  .sec-head{flex-wrap:wrap;gap:6px}
  .sec-head h2{font-size:26px}
  footer .wrap{flex-direction:column;align-items:flex-start;gap:14px}
  footer .ft{text-align:left}
}
@media(max-width:520px){
  .wrap{padding:0 14px}
  .filterbar .wrap{padding:9px 14px;gap:8px}
  .fb-label{display:none}
  .fbtn{padding:6px 13px;font-size:12px}
  .topband .wrap{padding:22px 16px 26px}
  .h-title{font-size:30px}
  .h-meta{font-size:12.5px;gap:8px 16px}
  .kpis{gap:12px}
  .kpi{padding:16px 16px}
  .kpi .num{font-size:40px}
  .pcard{padding:18px}
  .pcard .ptot{font-size:38px}
  .panel{padding:18px}
  .sec-head h2{font-size:22px}
  .alert-banner{flex-wrap:wrap;gap:8px 12px;padding:14px 16px}
  .alert-banner .ab-tx{flex:1 1 100%}
  .alert-banner a.ab-cta{margin-left:0}
  .alert-row{display:flex;flex-wrap:wrap;align-items:center;gap:4px 8px}
  .alert-row .info{flex:1 1 100%;order:2}
  .alert-row .idle{margin-left:auto}
  .task .k{width:80px}
  .wl td{padding:10px 4px}
  .wl-foot b{font-size:24px}
  .asg .a{grid-template-columns:96px 1fr 38px;gap:8px}
  .statbars .sb{grid-template-columns:104px 1fr 28px;gap:8px}
  .ec-title{min-height:0}
}
@media print{body{background:#fff}.panel,.kpi,.hero-prog,.epic-card{box-shadow:none}section{padding:22px 0;break-inside:avoid}.topband,footer{print-color-adjust:exact;-webkit-print-color-adjust:exact}}
</style>
</head>
<body>

<div class="topband">
  <div class="wrap">
    <div class="brandrow">
      <span class="logo-plate"><img src="logo-simcorp-full.png" alt="SIMCORP"></span>
      <span class="env">JIRA · simconsultas.atlassian.net</span>
    </div>
    <div class="h-eyebrow">SIMCORP · Status Report Semanal</div>
    <h1 class="h-title">Suporte <b>/</b> Operações <b>/</b> Desenvolvimento</h1>
    <div class="h-meta">
      <span class="h-chip"><span class="d"></span> <span id="hChipProjects">projetos ativos</span></span>
      <span>Emitido em <b id="genDate"></b></span>
      <span>Período <b id="weekRef"></b></span>
    </div>
    <div id="alertBanner"></div>
  </div>
</div>

<div class="filterbar">
  <div class="wrap">
    <span class="fb-label">Projeto</span>
    <div class="fb-btns" id="filterBtns"></div>
    <span class="fb-label fb-per">Período</span>
    <select id="periodSel" class="fb-select"></select>
  </div>
</div>

<div class="wrap">

<!-- 00 PORTFOLIO -->
<section id="portfolioSec" data-view="overview">
  <div class="sec-head"><div class="l"><div class="eyebrow">Portfólio</div><h2>Projetos Acompanhados</h2></div><span class="sec-num" id="portfolioNum">3 PROJETOS</span></div>
  <div class="portfolio" id="portfolio"></div>
  <p style="font-size:11.5px;color:var(--gray-400);margin-top:12px" id="portfolioNote"></p>
</section>

<!-- CONSOLIDADO (overview) -->
<section data-view="overview">
  <div class="sec-head"><div class="l"><div class="eyebrow">Consolidado</div><h2>Visão Geral</h2></div><span class="sec-num">TODOS OS PROJETOS</span></div>
  <div class="kpis" id="ovKpis"></div>
  <div class="panel" style="margin-top:18px">
    <h3><svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg> Carga por responsável — todos os projetos</h3>
    <div class="legend" style="margin:-6px 0 16px">
      <span><i style="background:var(--green)"></i>Concluído</span>
      <span><i style="background:var(--warn)"></i>Em andamento</span>
      <span><i style="background:var(--gray-400)"></i>A fazer / backlog</span>
    </div>
    <div class="asg" id="ovAssignees"></div>
  </div>
</section>

<!-- HORAS (overview) -->
<section data-view="overview">
  <div class="sec-head"><div class="l"><div class="eyebrow">Time tracking · todos os projetos</div><h2>Horas Apontadas</h2></div><span class="sec-num">CONSOLIDADO</span></div>
  <div class="cols">
    <div class="panel">
      <h3><svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg> Lançamentos no período</h3>
      <table class="wl" id="ovHoursTable"></table>
      <div class="wl-foot"><span>Total apontado (todos)</span><b id="ovHoursTotal" class="mono"></b></div>
    </div>
    <div class="panel">
      <h3><svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg> Horas por responsável</h3>
      <div class="asg" id="ovHoursByPerson" style="margin-bottom:18px"></div>
      <div class="note" id="ovHoursNote"></div>
    </div>
  </div>
</section>

<!-- RELATORIO DA SEMANA (overview) -->
<section data-view="overview">
  <div class="sec-head"><div class="l"><div class="eyebrow">Destaques · todos os projetos</div><h2>Relatório do Período</h2></div><span class="sec-num">CONSOLIDADO</span></div>
  <div class="rep-grid">
    <div class="panel"><h3><svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg> Concluído no período <span class="count-badge" id="ovCntDone"></span></h3><div id="ovWeekDone"></div></div>
    <div class="panel"><h3><svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg> Em andamento <span class="count-badge" id="ovCntProg"></span></h3><div id="ovWeekProg"></div></div>
  </div>
  <div class="rep-grid" style="margin-top:24px">
    <div class="panel"><h3><svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="16"/><line x1="8" y1="12" x2="16" y2="12"/></svg> Novos no período <span class="count-badge" id="ovCntNew"></span></h3><div id="ovWeekNew"></div></div>
    <div class="panel"><h3><svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg> Resumo por projeto</h3><div class="projweek" id="ovProjWeek"></div></div>
  </div>
</section>

<!-- 01 PANORAMA -->
<section data-view="SCUPOKR">
  <div class="sec-head"><div class="l"><div class="eyebrow">SCUPDATA · OKR — visão executiva</div><h2>Panorama Geral</h2></div><span class="sec-num">01</span></div>
  <div class="kpis" id="kpis"></div>
  <div class="hero-prog">
    <div class="row"><span class="t">Conclusão do escopo registrado</span><span class="pct" id="heroPct"></span></div>
    <div class="bar" id="heroBar"></div>
    <div class="legend" id="heroLegend"></div>
  </div>
</section>

<!-- 02 EPICS -->
<section data-view="SCUPOKR">
  <div class="sec-head"><div class="l"><div class="eyebrow">Frentes de trabalho</div><h2>Visão por Iniciativa</h2></div><span class="sec-num">02 · EPICS</span></div>
  <div class="epic-sub"><span class="lbl">Em andamento</span><span class="ct" id="epicActiveCt"></span><span class="ln"></span></div>
  <div class="epic-grid" id="epicActive"></div>
  <div class="epic-sub"><span class="lbl green">Concluídas</span><span class="ct" id="epicDoneCt"></span><span class="ln"></span></div>
  <div class="epic-grid" id="epicDone"></div>
  <div class="panel" style="margin-top:30px" id="orphanPanel">
    <h3><svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16v6H4z"/><path d="M4 14h16v6H4z"/></svg> Itens sem iniciativa vinculada <span class="count-badge" id="orphanCount"></span></h3>
    <p style="font-size:12.5px;color:var(--gray-700);margin:-8px 0 14px">Atividades sem épico pai — ordenadas por andamento. Considere vinculá-las a uma iniciativa para acompanhamento.</p>
    <div class="orphan-grid" id="orphanList"></div>
  </div>
</section>

<!-- 03 RITMO -->
<section data-view="SCUPOKR">
  <div class="sec-head"><div class="l"><div class="eyebrow">Throughput</div><h2>Ritmo de Entrega</h2></div><span class="sec-num">03</span></div>
  <div class="cols">
    <div class="panel">
      <h3><svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg> Atividade por semana</h3>
      <div class="chart" id="weeklyChart"></div>
      <div class="legend">
        <span><i style="background:var(--navy)"></i>Criadas</span>
        <span><i style="background:var(--green)"></i>Concluídas (mov.)</span>
      </div>
      <p style="font-size:11.5px;color:var(--gray-400);margin-top:10px">Conclusão estimada pela data da última movimentação (o projeto não registra data de resolução).</p>
    </div>
    <div class="panel">
      <h3><svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M21.21 15.89A10 10 0 1 1 8 2.83"/><path d="M22 12A10 10 0 0 0 12 2v10z"/></svg> Distribuição por status</h3>
      <div class="donut-wrap">
        <svg class="donut" id="donut" width="168" height="168" viewBox="0 0 168 168"></svg>
        <div class="donut-legend" id="donutLegend"></div>
      </div>
    </div>
  </div>
</section>

<!-- 04 DISTRIBUICAO -->
<section data-view="SCUPOKR">
  <div class="sec-head"><div class="l"><div class="eyebrow">Equipe & escopo</div><h2>Distribuição</h2></div><span class="sec-num">04</span></div>
  <div class="cols">
    <div class="panel">
      <h3><svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg> Carga por responsável</h3>
      <div class="legend" style="margin:-6px 0 16px">
        <span><i style="background:var(--green)"></i>Concluído</span>
        <span><i style="background:var(--warn)"></i>Em andamento</span>
        <span><i style="background:var(--gray-400)"></i>A Fazer</span>
        <span><i style="background:var(--gray-700)"></i>Backlog</span>
      </div>
      <div class="asg" id="assignees"></div>
    </div>
    <div class="panel">
      <h3><svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg> Tipo & prioridade</h3>
      <div class="two-small" style="margin-top:0">
        <div><div class="eyebrow" style="color:var(--gray-400);margin-bottom:10px">Por tipo</div><div class="minib" id="byType"></div></div>
        <div><div class="eyebrow" style="color:var(--gray-400);margin-bottom:10px">Por prioridade</div><div class="minib" id="byPrio"></div></div>
      </div>
    </div>
  </div>
</section>

<!-- 05 HORAS -->
<section data-view="SCUPOKR">
  <div class="sec-head"><div class="l"><div class="eyebrow">Time tracking · Tempo</div><h2>Horas Apontadas</h2></div><span class="sec-num">05</span></div>
  <div class="cols">
    <div class="panel">
      <h3><svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg> Lançamentos no período</h3>
      <table class="wl" id="wlTable"></table>
      <div class="wl-foot"><span>Total apontado</span><b id="hoursTotal" class="mono"></b></div>
    </div>
    <div class="panel">
      <h3><svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg> Horas por responsável</h3>
      <div class="asg" id="hoursByAuthor" style="margin-bottom:18px"></div>
      <div class="note" id="hoursNote"></div>
    </div>
  </div>
  <div class="panel" style="margin-top:24px" id="alertPanelWrap">
    <h3><svg class="ic" style="color:var(--danger)" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg> Em andamento sem horas lançadas <span class="count-badge danger" id="alertCount"></span></h3>
    <p style="font-size:12.5px;color:var(--gray-700);margin:-8px 0 14px">Atividades em <b>Em Progresso</b> ou <b>Em Validação</b> sem nenhum apontamento de tempo. "Dias parado" = dias desde a última movimentação no Jira.</p>
    <div class="alert-list" id="alertList"></div>
  </div>
</section>

<!-- 06 SEMANA -->
<section data-view="SCUPOKR">
  <div class="sec-head"><div class="l"><div class="eyebrow">Destaques</div><h2>Relatório do Período</h2></div><span class="sec-num">06</span></div>
  <div class="rep-grid">
    <div class="panel"><h3><svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg> Concluído no período <span class="count-badge" id="cntDone"></span></h3><div id="weekDone"></div></div>
    <div class="panel"><h3><svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg> Em andamento <span class="count-badge" id="cntProg"></span></h3><div id="weekProg"></div></div>
  </div>
  <div class="rep-grid" style="margin-top:24px">
    <div class="panel"><h3><svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="16"/><line x1="8" y1="12" x2="16" y2="12"/></svg> Novos no período <span class="count-badge" id="cntNew"></span></h3><div id="weekNew"></div></div>
    <div class="panel"><h3><svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z"/><line x1="4" y1="22" x2="4" y2="15"/></svg> Observações & Riscos</h3><div class="note warnbox" id="notes"></div></div>
  </div>
</section>

<!-- SUPORTE (uma seção por projeto, gerada via JS) -->
<div id="supportSections"></div>

</div>

<footer>
  <div class="wrap">
    <span class="logo-plate"><img src="logo-simcorp-full.png" alt="SIMCORP"></span>
    <div class="ft">
      <div>Dashboard de acompanhamento — gerado automaticamente a partir do Jira.</div>
      <div class="mono" id="footTotal"></div>
    </div>
  </div>
</footer>

<script>
const DATA=__DATA__;
const BASE=DATA.baseUrl;
const SUP=DATA.support;
const ALL=DATA.allIssues||[];
const $=(s)=>document.querySelector(s);
const el=(t,c,h)=>{const e=document.createElement(t);if(c)e.className=c;if(h!=null)e.innerHTML=h;return e;};
const esc=(s)=>String(s).replace(/[&<>]/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[m]));
const MES=['jan','fev','mar','abr','mai','jun','jul','ago','set','out','nov','dez'];
const MESF=['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro'];
const COL={done:'#84BF04',prog:'#E67E22',progblue:'#0079C1',todo:'#B3B3B3',backlog:'#4D4D4D',navy:'#023859',danger:'#C0392B'};
const STATUS_COLOR={'Concluído':COL.done,'Em Progresso':COL.progblue,'Em Validação':COL.prog,'A Fazer':COL.todo,'Backlog':COL.backlog};
const STATUS_ORDER=['Concluído','Em Validação','Em Progresso','A Fazer','Backlog'];
const PILL=(cat)=>cat==='done'?'done':(cat==='indeterminate'?'prog':'todo');
const PROJ_COL={SCUPOKR:'var(--navy)',SDE:'#0079C1',SDS:'#3a6b57'};
const projTag=(p)=>`<span class="ptag2" style="background:${PROJ_COL[p]||'var(--gray-400)'}">${esc(p)}</span>`;
function fmtH(sec){if(!sec)return '0h';const h=Math.floor(sec/3600);const m=Math.round((sec%3600)/60);return (h?h+'h':'')+(m?(h?' ':'')+m+'min':'')||'0h';}
function catCol(c){return c==='done'?COL.done:(c==='indeterminate'?COL.prog:COL.todo);}

$('#genDate').textContent='__GEN__';
$('#footTotal').textContent=ALL.length+' issues · '+(1+(SUP?SUP.projects.length:0))+' projetos';
$('#hChipProjects').textContent=(1+(SUP?SUP.projects.length:0))+' projetos ativos';

// helpers genéricos
function miniBars(obj,target,palette){target.innerHTML='';const ent=Object.entries(obj).sort((a,b)=>b[1]-a[1]);const mx=Math.max(...ent.map(e=>e[1]),1);
  ent.forEach(([k,v],i)=>{const r=el('div','r');r.innerHTML=`<span class="lab">${esc(k)}</span><span class="t" style="width:${Math.max(v/mx*110,5)}px;max-width:120px;background:${palette[i%palette.length]}"></span><span class="n">${v}</span>`;target.appendChild(r);});}
function aggCount(arr,fn){const m={};arr.forEach(i=>{const k=fn(i);if(k==null)return;(Array.isArray(k)?k:[k]).forEach(x=>m[x]=(m[x]||0)+1);});return m;}

// ===================== CUMULATIVO SCUPOKR (uma vez) =====================
[{lab:'Issues totais',num:DATA.total,meta:DATA.epics.length+' iniciativas',c:'var(--navy)'},
 {lab:'Concluídas',num:DATA.done,meta:DATA.pct+'% do escopo',c:'var(--green)'},
 {lab:'Em andamento',num:DATA.inprog,meta:'progresso + validação',c:'var(--warn)'},
 {lab:'A fazer / backlog',num:DATA.todo,meta:'pendentes de início',c:'var(--gray-400)'}].forEach(k=>{const c=el('div','kpi');c.style.setProperty('--c',k.c);c.innerHTML=`<div class="lab">${k.lab}</div><div class="num">${k.num}</div><div class="meta">${k.meta}</div>`;$('#kpis').appendChild(c);});
$('#heroPct').textContent=DATA.pct+'%';
[['Concluído',DATA.done,COL.done],['Em andamento',DATA.inprog,COL.prog],['Pendente',DATA.todo,COL.todo]].forEach(([nm,v,col])=>{const s=el('span');s.style.width=(v/DATA.total*100)+'%';s.style.background=col;if(v/DATA.total>0.06)s.textContent=v;$('#heroBar').appendChild(s);
  $('#heroLegend').insertAdjacentHTML('beforeend',`<span><i style="background:${col}"></i>${nm} · ${v}</span>`);});
function epicCard(e){const c=el('div','epic-card');const segs=[[e.done,COL.done],[e.inprog,COL.prog],[e.todo,COL.todo]].filter(s=>s[0]>0);
  const stack=segs.map(([v,col])=>`<span style="width:${v/e.children*100}%;background:${col}"></span>`).join('')||'<span style="width:100%;background:var(--gray-50)"></span>';
  c.innerHTML=`<div class="ec-top"><a href="${BASE}${e.key}" target="_blank" class="ec-key">${e.key}</a><span class="pill ${PILL(e.cat)}"><span class="d"></span>${e.status}</span></div><div class="ec-title">${esc(e.summary)}</div><div class="ec-pctrow"><span class="ec-pct">${e.pct}%</span><span class="ec-pctlab">concluído</span></div><div class="ec-stack">${stack}</div><div class="ec-legend"><span><i style="background:${COL.done}"></i>${e.done} concl.</span><span><i style="background:${COL.prog}"></i>${e.inprog} andam.</span><span><i style="background:${COL.todo}"></i>${e.todo} pend.</span></div><div class="ec-foot"><span>${e.children} sub-itens</span><span class="h">${fmtH(e.loggedSec)}</span></div>`;return c;}
const epActive=DATA.epics.filter(e=>e.cat!=='done').sort((a,b)=>b.pct-a.pct||b.children-a.children);
const epDone=DATA.epics.filter(e=>e.cat==='done').sort((a,b)=>b.children-a.children);
epActive.forEach(e=>$('#epicActive').appendChild(epicCard(e)));epDone.forEach(e=>$('#epicDone').appendChild(epicCard(e)));
$('#epicActiveCt').textContent=epActive.length+' iniciativas';$('#epicDoneCt').textContent=epDone.length+' iniciativas';
const ol=DATA.orphanList||[];$('#orphanCount').textContent=ol.length;
ol.forEach(o=>{const r=el('div','orow');r.innerHTML=`<a href="${BASE}${o.key}" target="_blank" class="k">${o.key}</a><div><div class="s">${esc(o.summary)}</div><div class="w">${esc(o.assignee)} · ${esc(o.type)}</div></div><span class="pill ${PILL(o.cat)}"><span class="d"></span>${o.status}</span>`;$('#orphanList').appendChild(r);});
const wk=DATA.weekly;const maxV=Math.max(...wk.map(w=>Math.max(w.created,w.doneUpd)),1);
wk.forEach(w=>{const c=el('div','wk');const d=new Date(w.week+'T00:00:00');c.innerHTML=`<div class="bars"><div class="b c" title="${w.created} criadas" style="height:${w.created/maxV*100}%"></div><div class="b d" title="${w.doneUpd} concluídas" style="height:${w.doneUpd/maxV*100}%"></div></div><div class="lbl">${d.getDate()}/${MES[d.getMonth()]}</div>`;$('#weeklyChart').appendChild(c);});
const sc=DATA.byStatus;const totS=Object.values(sc).reduce((a,b)=>a+b,0);const ordered=STATUS_ORDER.filter(s=>sc[s]).map(s=>[s,sc[s]]);
const svg=$('#donut');const R=66,C2=2*Math.PI*R,cx=84,cy=84;let off=0;
svg.innerHTML=`<circle cx="${cx}" cy="${cy}" r="${R}" fill="none" stroke="#EFF1EF" stroke-width="20"/>`;
ordered.forEach(([s,v])=>{const len=v/totS*C2;const ci=document.createElementNS('http://www.w3.org/2000/svg','circle');ci.setAttribute('cx',cx);ci.setAttribute('cy',cy);ci.setAttribute('r',R);ci.setAttribute('fill','none');ci.setAttribute('stroke',STATUS_COLOR[s]||COL.todo);ci.setAttribute('stroke-width','20');ci.setAttribute('stroke-dasharray',`${len} ${C2-len}`);ci.setAttribute('stroke-dashoffset',-off);ci.setAttribute('transform',`rotate(-90 ${cx} ${cy})`);svg.appendChild(ci);off+=len;});
function svtext(y,size,weight,fill,txt){const t=document.createElementNS('http://www.w3.org/2000/svg','text');t.setAttribute('x',cx);t.setAttribute('y',y);t.setAttribute('text-anchor','middle');t.setAttribute('font-family','Raleway');t.setAttribute('font-size',size);t.setAttribute('font-weight',weight);t.setAttribute('fill',fill);t.textContent=txt;svg.appendChild(t);}
svtext(cy-2,'32','800',COL.navy,DATA.pct+'%');svtext(cy+16,'10','700','#B3B3B3','CONCLUÍDO');
$('#donutLegend').innerHTML=ordered.map(([s,v])=>`<div class="li"><span class="nm"><i style="width:10px;height:10px;border-radius:3px;background:${STATUS_COLOR[s]||COL.todo};display:inline-block"></i>${s}</span><b>${v} · ${(v/totS*100).toFixed(0)}%</b></div>`).join('');
const bd=DATA.byAssigneeBreakdown;const asgE=Object.entries(bd).sort((a,b)=>b[1].total-a[1].total);const maxAA=Math.max(...asgE.map(([n,d])=>d.total),1);
asgE.forEach(([nm,d])=>{const c=el('div','a');const inner=[[d.done,COL.done],[d.prog,COL.prog],[d.afazer,COL.todo],[d.backlog,COL.backlog]].map(([v,col])=>v?`<span style="width:${v/maxAA*100}%;background:${col}"></span>`:'').join('');c.innerHTML=`<div class="nm">${esc(nm)}</div><div class="track stacked">${inner}</div><div class="n">${d.total}</div>`;$('#assignees').appendChild(c);});
miniBars(DATA.byType,$('#byType'),[COL.navy,'#0079C1','#6c8f7f']);
miniBars(DATA.byPriority,$('#byPrio'),[COL.danger,COL.prog,COL.todo,COL.backlog]);
const AL=DATA.alerts||[];
function idleClass(d){return d>=14?'idle-hi':(d>=5?'idle-md':'idle-lo');}
if(AL.length){const crit=AL.filter(a=>a.daysIdle>=14).length;$('#alertBanner').innerHTML=`<div class="alert-banner"><span class="ab-ic"><svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg></span><span class="ab-n">${AL.length}</span><span class="ab-tx"><b>atividade(s) do SCUPOKR em andamento sem horas lançadas.</b><br>${crit?`${crit} parada(s) há 14+ dias sem movimentação. `:''}Lance as horas no Tempo para manter o acompanhamento fiel.</span><a class="ab-cta" href="#alertPanelWrap">Ver lista</a></div>`;}
$('#alertCount').textContent=AL.length;const alList=$('#alertList');
if(!AL.length)alList.innerHTML='<p style="font-size:13px;color:var(--gray-700)">Nenhuma atividade em andamento sem apontamento.</p>';
AL.forEach(a=>{const r=el('div','alert-row');const d=a.daysIdle;const dtxt=(d==null)?'—':(d===0?'hoje':d+'d');r.innerHTML=`<a href="${BASE}${a.key}" target="_blank" class="k">${a.key}</a><div class="info"><div class="s">${esc(a.summary)}</div><div class="m">${esc(a.assignee)} · últ. mov. ${a.updated}</div></div><span class="pill prog"><span class="d"></span>${a.status}</span><span class="idle ${idleClass(d||0)}">${dtxt} · <span class="zero">0h</span></span>`;alList.appendChild(r);});
$('#hoursNote').innerHTML=`<b>Fonte das horas do SCUPOKR</b><ul><li>Lançamentos reais do app <b>Tempo</b> (autor real de cada apontamento), filtrados pelo período selecionado.</li><li>No worklog sincronizado o autor nativo é a conta do app Tempo; nesses casos a hora é atribuída ao responsável da issue.</li></ul>`;
$('#notes').innerHTML=`<b>Leitura</b><ul><li>Iniciativas <b>SCUPOKR-83</b> (base CNPJ/ML) e <b>SCUPOKR-123</b> (Portal SaaS Multi-Tenant) seguem em backlog — definir início.</li><li>Acompanhe os itens de prioridade Alta/Imediata em aberto para não represar entregas.</li><li>Os números acima (Concluído/Em andamento/Novos) refletem o período selecionado no topo.</li></ul>`;

// ===================== FILTRO DE PROJETO =====================
const FILTERS=[{f:'overview',label:'Visão geral'},{f:'SCUPOKR',label:'SCUPOKR'}];
if(SUP)SUP.projects.forEach(p=>FILTERS.push({f:p.key,label:p.key}));
FILTERS.forEach(x=>{const b=el('button','fbtn');b.dataset.filter=x.f;b.innerHTML=`${esc(x.label)}<span class="c" data-cnt="${x.f}"></span>`;b.onclick=()=>applyFilter(x.f);$('#filterBtns').appendChild(b);});
let CURPROJ='overview';
function applyFilter(f){CURPROJ=f;document.querySelectorAll('[data-view]').forEach(e=>{e.style.display=e.getAttribute('data-view').split(' ').includes(f)?'':'none';});document.querySelectorAll('.fbtn').forEach(b=>b.classList.toggle('active',b.dataset.filter===f));}

// ===================== MODELO DE PERÍODO =====================
function inR(s,a,b){return !!s&&s>=a&&s<=b;}
function isActive(i,p){return inR(i.created,p.start,p.end)||inR(i.updated,p.start,p.end)||inR(i.resolved,p.start,p.end);}
function resolvedInP(i,p){return inR(i.resolved,p.start,p.end)||(i.cat==='done'&&inR(i.updated,p.start,p.end));}
function actProj(p,proj){return ALL.filter(i=>(!proj||i.project===proj)&&!i.isEpic&&isActive(i,p));}
function wkStart(s){const d=new Date(s+'T00:00:00');const o=(d.getDay()+6)%7;d.setDate(d.getDate()-o);return d.toISOString().slice(0,10);}
function addD(s,n){const d=new Date(s+'T00:00:00');d.setDate(d.getDate()+n);return d.toISOString().slice(0,10);}
function dlab(s){const d=new Date(s+'T00:00:00');return d.getDate()+' '+MES[d.getMonth()];}
const TODAY=DATA.today,FROM=DATA.fetchFrom,CURW=DATA.curWeek;
const weeks=[];for(let s=wkStart(FROM);s<=TODAY;s=addD(s,7)){const e=addD(s,6);weeks.push({type:'week',start:s,end:e,id:'w'+s,label:`${dlab(s)} – ${dlab(e)}`});}
weeks.reverse();
const months=[];const ty=+TODAY.slice(0,4),tm=+TODAY.slice(5,7);
for(let m=tm;m>=1;m--){const s=`${ty}-${String(m).padStart(2,'0')}-01`;const e=(m===tm)?TODAY:addD(`${ty}-${String(m+1).padStart(2,'0')}-01`,-1);months.push({type:'month',start:s,end:e,id:'m'+m,label:MESF[m-1]});}
const totalP={type:'total',start:FROM,end:TODAY,id:'total',label:`Total (desde ${FROM.slice(8,10)}/${FROM.slice(5,7)})`};
const PMAP={};[...weeks,...months,totalP].forEach(p=>PMAP[p.id]=p);
let P=weeks.find(w=>w.start===CURW)||weeks[0]||totalP;
const sel=$('#periodSel');
function addOptg(lbl,arr){const g=document.createElement('optgroup');g.label=lbl;arr.forEach(p=>{const o=document.createElement('option');o.value=p.id;o.textContent=p.label;if(p.id===P.id)o.selected=true;g.appendChild(o);});sel.appendChild(g);}
addOptg('Semanas',weeks);addOptg('Meses',months);addOptg('Geral',[totalP]);
sel.onchange=()=>{P=PMAP[sel.value]||P;renderPeriod();};

// helpers de render por período
function stackedAsg(arr,host){host.innerHTML='';const m={};arr.forEach(i=>{const a=i.assignee||'Nao atribuido';const o=m[a]||(m[a]={done:0,prog:0,todo:0,total:0});o[i.cat==='done'?'done':(i.cat==='indeterminate'?'prog':'todo')]++;o.total++;});
  const ent=Object.entries(m).sort((a,b)=>b[1].total-a[1].total);const mx=Math.max(...ent.map(([n,o])=>o.total),1);
  ent.forEach(([nm,o])=>{const c=el('div','a');const inner=[[o.done,COL.done],[o.prog,COL.prog],[o.todo,COL.todo]].map(([v,col])=>v?`<span style="width:${v/mx*100}%;background:${col}"></span>`:'').join('');c.innerHTML=`<div class="nm">${esc(nm)}</div><div class="track stacked">${inner}</div><div class="n">${o.total}</div>`;host.appendChild(c);});}
function simpleAsg(arr,host){host.innerHTML='';const m=aggCount(arr,i=>i.assignee||'Nao atribuido');const ent=Object.entries(m).sort((a,b)=>b[1]-a[1]);const mx=Math.max(...ent.map(e=>e[1]),1);
  ent.forEach(([nm,v])=>{const c=el('div','a');c.innerHTML=`<div class="nm">${esc(nm)}</div><div class="track"><span style="width:${v/mx*100}%"></span></div><div class="n">${v}</div>`;host.appendChild(c);});}
function statusBars(arr,host){host.innerHTML='';const m={};arr.forEach(i=>{const o=m[i.status]||(m[i.status]={n:0,cat:i.cat});o.n++;});
  const ent=Object.entries(m).sort((a,b)=>b[1].n-a[1].n);const mx=Math.max(...ent.map(e=>e[1].n),1);
  ent.forEach(([s,o])=>{const r=el('div','sb');r.innerHTML=`<span class="nm" title="${esc(s)}">${esc(s)}</span><div class="tr"><span style="width:${Math.max(o.n/mx*100,3)}%;background:${catCol(o.cat)}"></span></div><span class="n">${o.n}</span>`;host.appendChild(r);});}
function customBars(counts,host){host.innerHTML='';let ent=Object.entries(counts).sort((a,b)=>b[1]-a[1]);const top=ent.slice(0,8);const rest=ent.slice(8).reduce((a,[k,v])=>a+v,0);if(rest)top.push(['Outros',rest]);const mx=Math.max(...top.map(e=>e[1]),1);
  top.forEach(([k,v])=>{const r=el('div','sb');r.innerHTML=`<span class="nm" title="${esc(k)}">${esc(k)}</span><div class="tr"><span style="width:${Math.max(v/mx*100,3)}%;background:var(--navy)"></span></div><span class="n">${v}</span>`;host.appendChild(r);});}
function cfVal(i,label){const v=(i.custom||{})[label];if(Array.isArray(v))return v.length?v:['Não informado'];return v==null?'Não informado':v;}
function taskRows(arr,host,tag){host.innerHTML='';if(!arr.length){host.innerHTML='<p style="color:var(--gray-700);font-size:13px">Nenhum item nesta categoria.</p>';return;}
  arr.slice(0,14).forEach(t=>{const c=el('div','task');c.innerHTML=`<a href="${BASE}${t.key}" target="_blank" class="k">${t.key}</a><div><div class="tx">${esc(t.summary)}${tag?projTag(t.project):''}</div><div class="who">${esc(t.assignee)} · ${esc(t.status)}</div></div>`;host.appendChild(c);});}
function hoursLogs(p,proj){const logs=[];
  (DATA.scupokrWorklogs||[]).forEach(w=>{if((!proj||proj==='SCUPOKR')&&inR(w.started,p.start,p.end))logs.push({project:'SCUPOKR',key:w.key,summary:w.summary,seconds:w.seconds,person:w.person,started:w.started});});
  ALL.forEach(i=>{if(i.project!=='SCUPOKR'&&i.logged>0&&(!proj||proj===i.project)&&isActive(i,p))logs.push({project:i.project,key:i.key,summary:i.summary,seconds:i.logged,person:i.assignee,started:i.updated});});
  logs.sort((a,b)=>(b.started||'').localeCompare(a.started||'')||b.seconds-a.seconds);return logs;}
function renderHours(logs,tableEl,totalEl,byPersonEl){
  tableEl.innerHTML='';if(!logs.length)tableEl.innerHTML='<tr><td style="color:var(--gray-700);font-size:13px">Sem horas no período.</td></tr>';
  logs.slice(0,14).forEach(l=>{const tr=document.createElement('tr');tr.innerHTML=`<td><a href="${BASE}${l.key}" target="_blank" class="k">${l.key}</a></td><td><div class="sm">${esc(l.summary)}${projTag(l.project)}</div><div class="meta">${esc(l.person)}${l.started?' · '+l.started:''}</div></td><td class="hrs">${fmtH(l.seconds)}</td>`;tableEl.appendChild(tr);});
  totalEl.textContent=fmtH(logs.reduce((a,l)=>a+l.seconds,0));
  const bp={};logs.forEach(l=>bp[l.person]=(bp[l.person]||0)+l.seconds);const ent=Object.entries(bp).sort((a,b)=>b[1]-a[1]);const mx=Math.max(...ent.map(e=>e[1]),1);
  byPersonEl.innerHTML='';ent.forEach(([nm,sec])=>{const c=el('div','a');c.innerHTML=`<div class="nm">${esc(nm)}</div><div class="track"><span style="width:${sec/mx*100}%;background:var(--grad-green)"></span></div><div class="n" style="width:auto;white-space:nowrap">${fmtH(sec)}</div>`;byPersonEl.appendChild(c);});}

// ===================== RENDER POR PERÍODO =====================
function renderPeriod(){
  $('#weekRef').textContent=P.label;
  const act=actProj(P);
  document.querySelector('[data-cnt="overview"]').textContent=act.length;
  document.querySelector('[data-cnt="SCUPOKR"]').textContent=actProj(P,'SCUPOKR').length;
  if(SUP)SUP.projects.forEach(p=>{const e=document.querySelector('[data-cnt="'+p.key+'"]');if(e)e.textContent=actProj(P,p.key).length;});
  // Portfolio
  $('#portfolio').innerHTML='';
  const cards=[{key:'SCUPOKR',name:'SCUPDATA · OKR',tag:'OKR'}].concat(SUP?SUP.projects.map(p=>({key:p.key,name:p.name,tag:'Suporte'})):[]);
  cards.forEach(cd=>{const a=actProj(P,cd.key);const done=a.filter(i=>i.cat==='done').length,prog=a.filter(i=>i.cat==='indeterminate').length,todo=a.filter(i=>i.cat==='new').length;const cr=a.filter(i=>inR(i.created,P.start,P.end)).length;
    const c=el('div','pcard');c.style.setProperty('--c',cd.key==='SCUPOKR'?'var(--navy)':'var(--green)');
    c.innerHTML=`<div class="ptop"><span class="pk">${cd.key}</span><span class="ptag">${cd.tag}</span></div><div class="pn">${esc(cd.name)}</div><div class="prow"><span class="ptot">${a.length}</span><span class="ppct"><b>${a.length?Math.round(done/a.length*100):0}%</b><span>concluído</span></span></div><div class="pstrip">${[[done,COL.done],[prog,COL.prog],[todo,COL.todo]].filter(s=>s[0]>0).map(([v,col])=>`<span style="width:${v/(a.length||1)*100}%;background:${col}"></span>`).join('')||'<span style="width:100%;background:var(--gray-50)"></span>'}</div><div class="pleg"><span><i style="background:${COL.done}"></i>${done}</span><span><i style="background:${COL.prog}"></i>${prog}</span><span><i style="background:${COL.todo}"></i>${todo}</span></div><div class="pfoot"><span>${cr} criados</span><span>no período</span></div>`;
    $('#portfolio').appendChild(c);});
  $('#portfolioNum').textContent=cards.length+' PROJETOS';
  $('#portfolioNote').textContent=`Período: ${P.label}. Considera itens criados, movimentados ou resolvidos no período. SCUPOKR também tem visão cumulativa na sua aba.`;
  // Consolidado KPIs
  $('#ovKpis').innerHTML='';
  const crd=act.filter(i=>inR(i.created,P.start,P.end)).length,mvd=act.filter(i=>inR(i.updated,P.start,P.end)).length,rsv=act.filter(i=>resolvedInP(i,P)).length;
  [{lab:'Ativos no período',num:act.length,meta:(1+(SUP?SUP.projects.length:0))+' projetos',c:'var(--navy)'},
   {lab:'Criados',num:crd,meta:'no período',c:'var(--blue)'},
   {lab:'Movimentados',num:mvd,meta:'no período',c:'var(--warn)'},
   {lab:'Resolvidos',num:rsv,meta:'no período',c:'var(--green)'}].forEach(k=>{const c=el('div','kpi');c.style.setProperty('--c',k.c);c.innerHTML=`<div class="lab">${k.lab}</div><div class="num">${k.num}</div><div class="meta">${k.meta}</div>`;$('#ovKpis').appendChild(c);});
  stackedAsg(act,$('#ovAssignees'));
  renderHours(hoursLogs(P),$('#ovHoursTable'),$('#ovHoursTotal'),$('#ovHoursByPerson'));
  $('#ovHoursNote').innerHTML=`<b>Como as horas são contadas</b><ul><li><b>SCUPOKR</b>: lançamentos do app <b>Tempo</b> com data no período.</li><li><b>SDE / SDS</b>: total apontado por issue (timespent) das issues com atividade no período.</li></ul><div style="margin-top:8px;font-size:11.5px;color:var(--blue)">Período: ${P.label}.</div>`;
  const dDone=act.filter(i=>resolvedInP(i,P)),dNew=act.filter(i=>inR(i.created,P.start,P.end)),dPrg=act.filter(i=>i.cat==='indeterminate');
  $('#ovCntDone').textContent=dDone.length;$('#ovCntProg').textContent=dPrg.length;$('#ovCntNew').textContent=dNew.length;
  taskRows(dDone,$('#ovWeekDone'),true);taskRows(dPrg,$('#ovWeekProg'),true);taskRows(dNew,$('#ovWeekNew'),true);
  const pw=$('#ovProjWeek');pw.innerHTML=`<div class="r"><span class="hd">Projeto</span><span class="hd v">Resolv.</span><span class="hd v">Novos</span><span class="hd v">Movim.</span></div>`;
  cards.forEach(cd=>{const a=actProj(P,cd.key);const r=el('div','r');r.innerHTML=`<span class="pn">${cd.key}</span><span class="v" style="color:var(--green-deep)">${a.filter(i=>resolvedInP(i,P)).length}</span><span class="v">${a.filter(i=>inR(i.created,P.start,P.end)).length}</span><span class="v">${a.filter(i=>inR(i.updated,P.start,P.end)).length}</span>`;pw.appendChild(r);});
  renderSupport();
  // SCUPOKR período: horas + relatório
  renderHours(hoursLogs(P,'SCUPOKR'),$('#wlTable'),$('#hoursTotal'),$('#hoursByAuthor'));
  const sA=actProj(P,'SCUPOKR');
  $('#cntDone').textContent=sA.filter(i=>resolvedInP(i,P)).length;$('#cntProg').textContent=sA.filter(i=>i.cat==='indeterminate').length;$('#cntNew').textContent=sA.filter(i=>inR(i.created,P.start,P.end)).length;
  taskRows(sA.filter(i=>resolvedInP(i,P)),$('#weekDone'),false);taskRows(sA.filter(i=>i.cat==='indeterminate'),$('#weekProg'),false);taskRows(sA.filter(i=>inR(i.created,P.start,P.end)),$('#weekNew'),false);
}
function renderSupport(){const host=$('#supportSections');host.innerHTML='';if(!SUP)return;
  SUP.projects.forEach(p=>{const a=actProj(P,p.key);const done=a.filter(i=>i.cat==='done').length,prog=a.filter(i=>i.cat==='indeterminate').length,todo=a.filter(i=>i.cat==='new').length;
    const cr=a.filter(i=>inR(i.created,P.start,P.end)).length,mv=a.filter(i=>inR(i.updated,P.start,P.end)).length,rs=a.filter(i=>resolvedInP(i,P)).length;
    const sec=el('section');sec.setAttribute('data-view',p.key);
    sec.innerHTML=`<div class="sec-head"><div class="l"><div class="eyebrow">Suporte · ${esc(P.label)}</div><h2>${esc(p.name)}</h2></div><span class="sec-num">${p.key}</span></div>
      <div class="panel sup-proj"><div class="sup-kpis">
        <div class="sup-kpi"><div class="n">${a.length}</div><div class="l">No período</div></div>
        <div class="sup-kpi"><div class="n">${cr}</div><div class="l">Criados</div></div>
        <div class="sup-kpi"><div class="n">${mv}</div><div class="l">Movimentados</div></div>
        <div class="sup-kpi"><div class="n" style="color:var(--green-deep)">${rs}</div><div class="l">Resolvidos</div></div>
        <div class="sup-kpi"><div class="n" style="color:var(--warn-deep)">${prog+todo}</div><div class="l">Em aberto</div></div>
      </div>
      <div class="sup-cols"><div><div class="sub-eyebrow">Por status</div><div class="statbars sb-host"></div></div>
        <div><div class="sub-eyebrow">Por tipo</div><div class="minib ty-host"></div><div class="sub-eyebrow" style="margin-top:18px">Responsáveis</div><div class="asg as-host"></div></div></div>
      ${(p.customCfg&&p.customCfg.length)?`<div class="cf-divider"><span class="lbl">Campos do projeto</span><span class="ln"></span></div><div class="sup-cols cf-row"></div>`:''}</div>`;
    host.appendChild(sec);
    statusBars(a,sec.querySelector('.sb-host'));
    miniBars(aggCount(a,i=>i.type),sec.querySelector('.ty-host'),[COL.navy,'#0079C1','#6c8f7f','#9bb0a5']);
    simpleAsg(a,sec.querySelector('.as-host'));
    const cfRow=sec.querySelector('.cf-row');
    if(cfRow)(p.customCfg||[]).forEach(cf=>{const col=el('div');col.innerHTML=`<div class="sub-eyebrow">${esc(cf.label)}</div><div class="statbars cf-host"></div>`;cfRow.appendChild(col);customBars(aggCount(a,i=>cfVal(i,cf.label)),col.querySelector('.cf-host'));});
  });
  applyFilter(CURPROJ);
}

// init
applyFilter('overview');
renderPeriod();

</script>
</body>
</html>"""

html = TEMPLATE.replace('__DATA__', data_js).replace('__GEN__', gen_str)
open(os.path.join(OUT,'dashboard.html'),'w',encoding='utf-8').write(html)
open(os.path.join(OUT,'index.html'),'w',encoding='utf-8').write(html)  # raiz servida pelo Amplify
print('OK -> dashboard.html / index.html ({} bytes)'.format(len(html)))
