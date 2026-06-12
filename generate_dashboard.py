# -*- coding: utf-8 -*-
"""Gera dashboard.html (auto-contido, dados embutidos) a partir de dashboard_data.json.
Estilo: SIMCORP Design System (Raleway, navy + verde lima, sem emoji)."""
import json, os, datetime

OUT = r'C:\Desenvolvimento\ProjetoSCUPOKR'
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
<title>SCUPDATA · OKR — Status Report Semanal</title>
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
.h-title{font-weight:800;font-size:clamp(38px,6vw,68px);line-height:1;letter-spacing:-.02em;color:#fff;margin:12px 0 0}
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

/* ---------- footer ---------- */
footer{background:var(--grad-blue);margin-top:36px}
footer .wrap{padding:34px 32px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:18px}
footer .logo-plate{background:#fff;border-radius:7px;padding:8px 14px;display:inline-flex;box-shadow:var(--sh-sm)}
footer .logo-plate img{height:26px;display:block}
footer .ft{font-size:12.5px;color:rgba(255,255,255,.7);text-align:right;line-height:1.7}
footer .ft .mono{color:rgba(255,255,255,.85)}

@media(max-width:980px){.epic-grid{grid-template-columns:repeat(2,1fr)}.portfolio{grid-template-columns:1fr}.sup-kpis{grid-template-columns:repeat(3,1fr)}}
@media(max-width:880px){
  .kpis{grid-template-columns:repeat(2,1fr)}
  .cols,.rep-grid,.two-small,.epic-grid,.sup-cols{grid-template-columns:1fr}
  .asg .a{grid-template-columns:110px 1fr 38px}
  .statbars .sb{grid-template-columns:120px 1fr 30px}
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
    <div class="h-eyebrow">Status Report Semanal</div>
    <h1 class="h-title">SCUP<b>DATA</b> · OKR</h1>
    <div class="h-meta">
      <span class="h-chip"><span class="d"></span> Projeto SCUPOKR</span>
      <span>Emitido em <b id="genDate"></b></span>
      <span>Semana de referência <b id="weekRef"></b></span>
    </div>
    <div id="alertBanner"></div>
  </div>
</div>

<div class="wrap">

<!-- 00 PORTFOLIO -->
<section id="portfolioSec">
  <div class="sec-head"><div class="l"><div class="eyebrow">Portfólio</div><h2>Projetos Acompanhados</h2></div><span class="sec-num" id="portfolioNum">3 PROJETOS</span></div>
  <div class="portfolio" id="portfolio"></div>
  <p style="font-size:11.5px;color:var(--gray-400);margin-top:12px" id="portfolioNote"></p>
</section>

<!-- 01 PANORAMA -->
<section>
  <div class="sec-head"><div class="l"><div class="eyebrow">SCUPDATA · OKR — visão executiva</div><h2>Panorama Geral</h2></div><span class="sec-num">01</span></div>
  <div class="kpis" id="kpis"></div>
  <div class="hero-prog">
    <div class="row"><span class="t">Conclusão do escopo registrado</span><span class="pct" id="heroPct"></span></div>
    <div class="bar" id="heroBar"></div>
    <div class="legend" id="heroLegend"></div>
  </div>
</section>

<!-- 02 EPICS -->
<section>
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
<section>
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
<section>
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
<section>
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
<section>
  <div class="sec-head"><div class="l"><div class="eyebrow">Destaques</div><h2>Relatório da Semana</h2></div><span class="sec-num">06</span></div>
  <div class="rep-grid">
    <div class="panel"><h3><svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg> Concluído nesta semana <span class="count-badge" id="cntDone"></span></h3><div id="weekDone"></div></div>
    <div class="panel"><h3><svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg> Em validação / andamento <span class="count-badge" id="cntProg"></span></h3><div id="weekProg"></div></div>
  </div>
  <div class="rep-grid" style="margin-top:24px">
    <div class="panel"><h3><svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="16"/><line x1="8" y1="12" x2="16" y2="12"/></svg> Novos itens registrados <span class="count-badge" id="cntNew"></span></h3><div id="weekNew"></div></div>
    <div class="panel"><h3><svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z"/><line x1="4" y1="22" x2="4" y2="15"/></svg> Observações & Riscos</h3><div class="note warnbox" id="notes"></div></div>
  </div>
</section>

<!-- 07 SUPORTE -->
<section id="supportSec">
  <div class="sec-head"><div class="l"><div class="eyebrow">Suporte · no período</div><h2>Projetos de Suporte</h2></div><span class="sec-num" id="supportNum">07</span></div>
  <p style="font-size:12.5px;color:var(--gray-700);margin:-12px 0 22px" id="supportIntro"></p>
  <div id="supportBody"></div>
</section>

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
const DATA = __DATA__;
const BASE = DATA.baseUrl;
const $ = (s)=>document.querySelector(s);
const el = (t,c,h)=>{const e=document.createElement(t);if(c)e.className=c;if(h!=null)e.innerHTML=h;return e;};
const esc = (s)=>String(s).replace(/[&<>]/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[m]));
const MES=['jan','fev','mar','abr','mai','jun','jul','ago','set','out','nov','dez'];

const COL={done:'#84BF04',prog:'#E67E22',progblue:'#0079C1',todo:'#B3B3B3',backlog:'#4D4D4D',navy:'#023859'};
const STATUS_COLOR={'Concluído':COL.done,'Em Progresso':COL.progblue,'Em Validação':COL.prog,'A Fazer':COL.todo,'Backlog':COL.backlog};
const STATUS_ORDER=['Concluído','Em Validação','Em Progresso','A Fazer','Backlog'];
const PILL=(cat)=>cat==='done'?'done':(cat==='indeterminate'?'prog':'todo');

$('#genDate').textContent='__GEN__';
function fmtWeek(iso){const d=new Date(iso+'T00:00:00');const e=new Date(d);e.setDate(e.getDate()+6);
  return `${d.getDate()} ${MES[d.getMonth()]} – ${e.getDate()} ${MES[e.getMonth()]}`;}
$('#weekRef').textContent=fmtWeek(DATA.curWeek);
$('#footTotal').textContent=DATA.total+' issues · '+DATA.epics.length+' iniciativas · '+DATA.pct+'% concluído';

// ---- KPIs ----
[
 {lab:'Issues totais',num:DATA.total,meta:DATA.epics.length+' iniciativas',c:'var(--navy)'},
 {lab:'Concluídas',num:DATA.done,meta:DATA.pct+'% do escopo',c:'var(--green)'},
 {lab:'Em andamento',num:DATA.inprog,meta:'progresso + validação',c:'var(--warn)'},
 {lab:'A fazer / backlog',num:DATA.todo,meta:'pendentes de início',c:'var(--gray-400)'},
].forEach(k=>{const c=el('div','kpi');c.style.setProperty('--c',k.c);
  c.innerHTML=`<div class="lab">${k.lab}</div><div class="num">${k.num}</div><div class="meta">${k.meta}</div>`;
  $('#kpis').appendChild(c);});

// ---- portfolio (SCUPOKR + projetos de suporte) ----
const SUP = DATA.support;
function miniStrip(done,prog,todo,total){
  const segs=[[done,COL.done],[prog,COL.prog],[todo,COL.todo]].filter(s=>s[0]>0);
  return segs.map(([v,c])=>`<span style="width:${v/total*100}%;background:${c}"></span>`).join('')||'<span style="width:100%;background:var(--gray-50)"></span>';
}
const pcards=[{key:'SCUPOKR',name:'SCUPDATA · OKR',tag:'OKR · Épicos',c:'var(--navy)',
  total:DATA.total,done:DATA.done,prog:DATA.inprog,todo:DATA.todo,pct:Math.round(DATA.pct),foot:DATA.epics.length+' iniciativas',scope:'projeto completo'}];
if(SUP){SUP.projects.forEach(p=>pcards.push({key:p.key,name:p.name,tag:'Suporte · período',c:'var(--green)',
  total:p.total,done:p.done,prog:p.inprog,todo:p.todo,pct:p.pct,foot:p.created+' criados no período',scope:'no período'}));}
$('#portfolioNum').textContent=pcards.length+' PROJETOS';
pcards.forEach(p=>{const c=el('div','pcard');c.style.setProperty('--c',p.c);
  c.innerHTML=`<div class="ptop"><span class="pk">${p.key}</span><span class="ptag">${p.tag}</span></div>
    <div class="pn">${esc(p.name)}</div>
    <div class="prow"><span class="ptot">${p.total}</span><span class="ppct"><b>${p.pct}%</b><span>concluído</span></span></div>
    <div class="pstrip">${miniStrip(p.done,p.prog,p.todo,p.total||1)}</div>
    <div class="pleg"><span><i style="background:${COL.done}"></i>${p.done}</span><span><i style="background:${COL.prog}"></i>${p.prog}</span><span><i style="background:${COL.todo}"></i>${p.todo}</span></div>
    <div class="pfoot"><span>${p.foot}</span><span>${p.scope}</span></div>`;
  $('#portfolio').appendChild(c);});
$('#portfolioNote').textContent = SUP
  ? `SCUPDATA · OKR mostrado em detalhe abaixo (visão completa do projeto). SDE e SDS são projetos de suporte, considerados apenas no período do dashboard (desde ${SUP.period}, criados ou movimentados).`
  : 'SCUPDATA · OKR — visão completa do projeto abaixo.';

// ---- hero progress ----
$('#heroPct').textContent=DATA.pct+'%';
const heroCats=[['Concluído',DATA.done,COL.done],['Em andamento',DATA.inprog,COL.prog],['Pendente',DATA.todo,COL.todo]];
heroCats.forEach(([nm,v,col])=>{const s=el('span');s.style.width=(v/DATA.total*100)+'%';s.style.background=col;
  if(v/DATA.total>0.06)s.textContent=v;$('#heroBar').appendChild(s);});
$('#heroLegend').innerHTML=heroCats.map(([nm,v,col])=>`<span><i style="background:${col}"></i>${nm} · ${v}</span>`).join('');

// ---- epic cards ----
function fmtH(sec){if(!sec)return '0h';const h=Math.floor(sec/3600);const m=Math.round((sec%3600)/60);
  return (h?h+'h':'')+(m?(h?' ':'')+m+'min':'')||'0h';}
function epicCard(e){const c=el('div','epic-card');
  const segs=[[e.done,COL.done],[e.inprog,COL.prog],[e.todo,COL.todo]].filter(s=>s[0]>0);
  const stack=segs.map(([v,col])=>`<span style="width:${v/e.children*100}%;background:${col}"></span>`).join('')||'<span style="width:100%;background:var(--gray-50)"></span>';
  c.innerHTML=`<div class="ec-top"><a href="${BASE}${e.key}" target="_blank" class="ec-key">${e.key}</a>
      <span class="pill ${PILL(e.cat)}"><span class="d"></span>${e.status}</span></div>
    <div class="ec-title">${esc(e.summary)}</div>
    <div class="ec-pctrow"><span class="ec-pct">${e.pct}%</span><span class="ec-pctlab">concluído</span></div>
    <div class="ec-stack">${stack}</div>
    <div class="ec-legend">
      <span><i style="background:${COL.done}"></i>${e.done} concl.</span>
      <span><i style="background:${COL.prog}"></i>${e.inprog} andam.</span>
      <span><i style="background:${COL.todo}"></i>${e.todo} pend.</span>
    </div>
    <div class="ec-foot"><span>${e.children} sub-itens</span><span class="h">${fmtH(e.loggedSec)}</span></div>`;
  return c;}
// separa ativos (nao concluidos) x concluidos, ordena por progresso desc
const epActive=DATA.epics.filter(e=>e.cat!=='done').sort((a,b)=>b.pct-a.pct||b.children-a.children);
const epDone=DATA.epics.filter(e=>e.cat==='done').sort((a,b)=>b.children-a.children);
epActive.forEach(e=>$('#epicActive').appendChild(epicCard(e)));
epDone.forEach(e=>$('#epicDone').appendChild(epicCard(e)));
$('#epicActiveCt').textContent=epActive.length+(epActive.length===1?' iniciativa':' iniciativas');
$('#epicDoneCt').textContent=epDone.length+(epDone.length===1?' iniciativa':' iniciativas');

// ---- itens sem epic (lista) ----
const ol=DATA.orphanList||[];
$('#orphanCount').textContent=ol.length;
ol.forEach(o=>{const r=el('div','orow');
  r.innerHTML=`<a href="${BASE}${o.key}" target="_blank" class="k">${o.key}</a>
    <div><div class="s">${esc(o.summary)}</div><div class="w">${esc(o.assignee)} · ${esc(o.type)}</div></div>
    <span class="pill ${PILL(o.cat)}"><span class="d"></span>${o.status}</span>`;
  $('#orphanList').appendChild(r);});

// ---- weekly chart ----
const wk=DATA.weekly;const maxV=Math.max(...wk.map(w=>Math.max(w.created,w.doneUpd)),1);
wk.forEach(w=>{const c=el('div','wk');const d=new Date(w.week+'T00:00:00');
  c.innerHTML=`<div class="bars">
    <div class="b c" title="${w.created} criadas" style="height:${w.created/maxV*100}%"></div>
    <div class="b d" title="${w.doneUpd} concluídas" style="height:${w.doneUpd/maxV*100}%"></div>
  </div><div class="lbl">${d.getDate()}/${MES[d.getMonth()]}</div>`;
  $('#weeklyChart').appendChild(c);});

// ---- donut ----
const sc=DATA.byStatus;const totS=Object.values(sc).reduce((a,b)=>a+b,0);
const ordered=STATUS_ORDER.filter(s=>sc[s]).map(s=>[s,sc[s]]);
const svg=$('#donut');const R=66,C=2*Math.PI*R,cx=84,cy=84;let off=0;
svg.innerHTML=`<circle cx="${cx}" cy="${cy}" r="${R}" fill="none" stroke="#EFF1EF" stroke-width="20"/>`;
ordered.forEach(([s,v])=>{const len=v/totS*C;
  const ci=document.createElementNS('http://www.w3.org/2000/svg','circle');
  ci.setAttribute('cx',cx);ci.setAttribute('cy',cy);ci.setAttribute('r',R);ci.setAttribute('fill','none');
  ci.setAttribute('stroke',STATUS_COLOR[s]||COL.todo);ci.setAttribute('stroke-width','20');
  ci.setAttribute('stroke-dasharray',`${len} ${C-len}`);ci.setAttribute('stroke-dashoffset',-off);
  ci.setAttribute('transform',`rotate(-90 ${cx} ${cy})`);svg.appendChild(ci);off+=len;});
function svtext(y,size,weight,fill,fam,txt){const t=document.createElementNS('http://www.w3.org/2000/svg','text');
  t.setAttribute('x',cx);t.setAttribute('y',y);t.setAttribute('text-anchor','middle');t.setAttribute('font-family',fam);
  t.setAttribute('font-size',size);t.setAttribute('font-weight',weight);t.setAttribute('fill',fill);t.textContent=txt;svg.appendChild(t);}
svtext(cy-2,'32','800',COL.navy,'Raleway',DATA.pct+'%');
svtext(cy+16,'10','700','#B3B3B3','Raleway','CONCLUÍDO');
$('#donutLegend').innerHTML=ordered.map(([s,v])=>
  `<div class="li"><span class="nm"><i style="width:10px;height:10px;border-radius:3px;background:${STATUS_COLOR[s]||COL.todo};display:inline-block"></i>${s}</span><b>${v} · ${(v/totS*100).toFixed(0)}%</b></div>`).join('');

// ---- assignees (carga decomposta por situacao) ----
const bd=DATA.byAssigneeBreakdown;
const asg=Object.entries(bd).sort((a,b)=>b[1].total-a[1].total);
const maxA=Math.max(...asg.map(([n,d])=>d.total));
asg.forEach(([nm,d])=>{const c=el('div','a');
  const segs=[[d.done,COL.done,'Concluído'],[d.prog,COL.prog,'Em andamento'],[d.afazer,COL.todo,'A Fazer'],[d.backlog,COL.backlog,'Backlog']];
  const inner=segs.map(([v,col,lab])=>v?`<span style="width:${v/maxA*100}%;background:${col}" title="${lab}: ${v}"></span>`:'').join('');
  c.innerHTML=`<div class="nm">${esc(nm)}</div><div class="track stacked">${inner}</div><div class="n">${d.total}</div>`;
  $('#assignees').appendChild(c);});

// ---- type / prio ----
function miniBars(obj,target,palette){const ent=Object.entries(obj).sort((a,b)=>b[1]-a[1]);const mx=Math.max(...ent.map(e=>e[1]));
  ent.forEach(([k,v],i)=>{const r=el('div','r');
    r.innerHTML=`<span class="lab">${esc(k)}</span><span class="t" style="width:${Math.max(v/mx*110,5)}px;max-width:120px;background:${palette[i%palette.length]}"></span><span class="n">${v}</span>`;
    target.appendChild(r);});}
miniBars(DATA.byType,$('#byType'),[COL.navy,'#0079C1','#6c8f7f']);
miniBars(DATA.byPriority,$('#byPrio'),[COL.danger,COL.prog,COL.todo,COL.backlog]);

// ---- alertas ----
const AL=DATA.alerts||[];
function idleClass(d){return d>=14?'idle-hi':(d>=5?'idle-md':'idle-lo');}
if(AL.length){const crit=AL.filter(a=>a.daysIdle>=14).length;
  $('#alertBanner').innerHTML=`<div class="alert-banner">
    <span class="ab-ic"><svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg></span>
    <span class="ab-n">${AL.length}</span>
    <span class="ab-tx"><b>atividade(s) em andamento sem horas lançadas.</b><br>
    ${crit?`${crit} parada(s) há 14+ dias sem movimentação. `:''}Lance as horas no Tempo para manter o acompanhamento fiel.</span>
    <a class="ab-cta" href="#alertPanelWrap">Ver lista</a></div>`;}
$('#alertCount').textContent=AL.length;
const alList=$('#alertList');
if(!AL.length){alList.innerHTML='<p style="font-size:13px;color:var(--gray-700)">Nenhuma atividade em andamento sem apontamento.</p>';}
AL.forEach(a=>{const r=el('div','alert-row');const d=a.daysIdle;
  const dtxt=(d==null)?'—':(d===0?'hoje':d+'d');
  r.innerHTML=`<a href="${BASE}${a.key}" target="_blank" class="k">${a.key}</a>
    <div class="info"><div class="s">${esc(a.summary)}</div><div class="m">${esc(a.assignee)} · últ. mov. ${a.updated}</div></div>
    <span class="pill ${a.status==='Em Progresso'?'prog':'prog'}"><span class="d"></span>${a.status}</span>
    <span class="idle ${idleClass(d||0)}">${dtxt} · <span class="zero">0h</span></span>`;
  alList.appendChild(r);});

// ---- horas ----
const wlTable=$('#wlTable');
DATA.worklogs.forEach(w=>{const tr=document.createElement('tr');
  const tag=w.test?'<span class="tag tag-test">TESTE</span>':(w.synced?'<span class="tag tag-tempo">VIA TEMPO</span>':'');
  const note=(w.comment && w.comment.toLowerCase()!=='time-tracking')?` · "${esc(w.comment)}"`:'';
  tr.innerHTML=`<td><a href="${BASE}${w.key}" target="_blank" class="k">${w.key}</a></td>
    <td><div class="sm">${esc(w.summary)}${tag}</div><div class="meta">${esc(w.person)} · ${w.started}${note}</div></td>
    <td class="hrs">${fmtH(w.seconds)}</td>`;
  wlTable.appendChild(tr);});
$('#hoursTotal').textContent=fmtH(DATA.hoursTotalSec);
const ha=Object.entries(DATA.hoursByPerson).sort((a,b)=>b[1]-a[1]);const maxHsec=Math.max(...ha.map(a=>a[1]));
ha.forEach(([nm,sec])=>{const c=el('div','a');
  c.innerHTML=`<div class="nm">${esc(nm)}</div><div class="track"><span style="width:${sec/maxHsec*100}%;background:var(--grad-green)"></span></div><div class="n" style="width:auto;white-space:nowrap">${fmtH(sec)}</div>`;
  $('#hoursByAuthor').appendChild(c);});
if(DATA.hoursSource==='tempo'){
  const rg=DATA.hoursRange?`${DATA.hoursRange.from} a ${DATA.hoursRange.to}`:'período completo';
  const sup=DATA.hoursSupplemented||0;
  $('#hoursNote').innerHTML=`<b>Fonte: app Tempo (api.tempo.io)</b>
  <ul>
    <li>Horas reais lançadas no Tempo, com o <b>autor real</b> de cada apontamento.</li>
    <li>Período coberto: <b>${rg}</b>${DATA.hoursGenerated?` · extraído em ${DATA.hoursGenerated}`:''}.</li>
    <li>Total de <b>${DATA.worklogs.length} lançamentos</b> no projeto SCUPOKR.</li>
    ${sup?`<li style="color:var(--warn-deep)"><b>Atenção:</b> ${sup} lançamento(s) vieram do Jira nativo como complemento — o token atual do Tempo não os retornou (provável escopo "apenas próprios worklogs"). Gere o token com permissão <b>View All Worklogs</b> para cobertura total.</li>`:''}
  </ul>
  <div style="margin-top:8px;font-size:11.5px;color:var(--blue)">Atualize com <code>python refresh_tempo.py</code> seguido de <code>build</code> + <code>generate</code>.</div>`;
} else {
  $('#hoursNote').innerHTML=`<b>Cobertura do time tracking</b>
  <ul>
    <li>A equipe <b>começou a usar o app Tempo agora</b> — até o momento apenas a <b>SCUPOKR-184 (3h, Alan Felipusso)</b> teve horas lançadas.</li>
    <li>A SCUPOKR-65 (5min) foi um <b>teste</b> de validação do time tracking, não esforço real.</li>
    <li>O Jira nativo só enxerga worklogs sincronizados; as horas reais do Tempo entram via <code>refresh_tempo.py</code> (token do Tempo).</li>
    <li>No worklog sincronizado o autor nativo é a <b>conta do app Tempo</b>; por isso as horas são atribuídas ao <b>responsável da issue</b>.</li>
  </ul>
  <div style="margin-top:8px;font-size:11.5px;color:var(--blue)">Base atual: ${DATA.worklogs.length} lançamentos em ${DATA.total} issues. Ainda não representa o esforço total do projeto.</div>`;
}

// ---- relatorio semana ----
function taskList(arr,target,showWho){
  if(!arr.length){target.appendChild(el('p','',`<span style="color:var(--gray-700);font-size:13px">Nenhum item nesta categoria.</span>`));return;}
  arr.forEach(t=>{const c=el('div','task');
    c.innerHTML=`<a href="${BASE}${t.key}" target="_blank" class="k">${t.key}</a>
      <div><div class="tx">${esc(t.summary)}</div>${showWho?`<div class="who">${esc(t.assignee)} · ${t.status}</div>`:''}</div>`;
    target.appendChild(c);});}
$('#cntDone').textContent=DATA.thisWeekDone.length;
$('#cntProg').textContent=DATA.inprogressList.length;
$('#cntNew').textContent=DATA.thisWeekCreated.length;
taskList(DATA.thisWeekDone.slice(0,12),$('#weekDone'),true);
taskList(DATA.inprogressList,$('#weekProg'),true);
taskList(DATA.thisWeekCreated.slice(0,12),$('#weekNew'),true);

function topAssigneeOf(status){const m={};DATA.issues.filter(i=>i.status===status).forEach(i=>m[i.assignee]=(m[i.assignee]||0)+1);
  const e=Object.entries(m).sort((a,b)=>b[1]-a[1])[0];return e?e[0]:'—';}
const openHigh=DATA.issues.filter(i=>i.cat!=='done'&&(i.priority==='Alta'||i.priority==='Imediata')).length;
const valid=(DATA.byStatus['Em Validação']||0);
$('#notes').innerHTML=`<b>Leitura da semana</b>
<ul>
  <li><b>${DATA.thisWeekCreated.length} novos itens</b> registrados — refletem o planejamento das frentes de Portal de Contas, API Key/Tenant e integrações.</li>
  <li><b>${valid} itens em validação</b> aguardando verificação para fechamento — concentrados em ${esc(topAssigneeOf('Em Validação'))}.</li>
  <li><b>${openHigh} itens de prioridade Alta/Imediata</b> ainda em aberto — acompanhar para não represar entregas.</li>
  <li>Iniciativas <b>SCUPOKR-83</b> (base CNPJ/ML) e <b>SCUPOKR-123</b> (Portal SaaS Multi-Tenant) seguem 100% em backlog — definir início.</li>
</ul>
<div style="margin-top:8px;font-size:11.5px">Nota metodológica: o projeto não preenche data de resolução; conclusão por semana usa a última movimentação como aproximação.</div>`;

// ---- projetos de suporte (SDE / SDS) ----
if(SUP){
  $('#supportIntro').innerHTML=`Itens dos projetos de suporte <b>${SUP.projects.map(p=>p.key).join(' e ')}</b> criados ou movimentados no período do dashboard (desde <b>${SUP.period}</b>). Visão operacional — sem épicos/OKR.`;
  const STATCAT_COL={done:COL.done,indeterminate:COL.prog,'new':COL.todo};
  SUP.projects.forEach(p=>{
    const wrap=el('div','sup-proj panel');
    wrap.innerHTML=`<div class="sup-head"><span class="sk">${p.key}</span><span class="sn">${esc(p.name)}</span><span class="ln"></span></div>
      <div class="sup-kpis">
        <div class="sup-kpi"><div class="n">${p.total}</div><div class="l">No período</div></div>
        <div class="sup-kpi"><div class="n">${p.created}</div><div class="l">Criados</div></div>
        <div class="sup-kpi"><div class="n">${p.moved}</div><div class="l">Movimentados</div></div>
        <div class="sup-kpi"><div class="n" style="color:var(--green-deep)">${p.done}</div><div class="l">Concluídos</div></div>
        <div class="sup-kpi"><div class="n" style="color:var(--warn-deep)">${p.inprog+p.todo}</div><div class="l">Em aberto</div></div>
      </div>
      <div class="sup-cols">
        <div><div class="sub-eyebrow">Por status</div><div class="statbars sb-host"></div></div>
        <div><div class="sub-eyebrow">Por tipo</div><div class="minib ty-host"></div>
          <div class="sub-eyebrow" style="margin-top:18px">Responsáveis</div><div class="asg as-host"></div></div>
      </div>`;
    $('#supportBody').appendChild(wrap);
    // status bars (coloridos por categoria)
    const stEnt=Object.entries(p.byStatus).sort((a,b)=>b[1]-a[1]);const stMax=Math.max(...stEnt.map(e=>e[1]));
    const sbHost=wrap.querySelector('.sb-host');
    stEnt.forEach(([s,v])=>{const col=STATCAT_COL[p.statusCat[s]]||COL.todo;const r=el('div','sb');
      r.innerHTML=`<span class="nm" title="${esc(s)}">${esc(s)}</span><div class="tr"><span style="width:${Math.max(v/stMax*100,3)}%;background:${col}"></span></div><span class="n">${v}</span>`;
      sbHost.appendChild(r);});
    // tipos
    miniBars(p.byType,wrap.querySelector('.ty-host'),[COL.navy,'#0079C1','#6c8f7f','#9bb0a5']);
    // responsaveis
    const aEnt=Object.entries(p.byAssignee).sort((a,b)=>b[1]-a[1]);const aMax=Math.max(...aEnt.map(e=>e[1]));
    const asHost=wrap.querySelector('.as-host');
    aEnt.forEach(([nm,v])=>{const c=el('div','a');
      c.innerHTML=`<div class="nm">${esc(nm)}</div><div class="track"><span style="width:${v/aMax*100}%"></span></div><div class="n">${v}</div>`;
      asHost.appendChild(c);});
  });
} else { const ss=$('#supportSec'); if(ss) ss.style.display='none'; }
</script>
</body>
</html>"""

html = TEMPLATE.replace('__DATA__', data_js).replace('__GEN__', gen_str)
open(os.path.join(OUT,'dashboard.html'),'w',encoding='utf-8').write(html)
open(os.path.join(OUT,'index.html'),'w',encoding='utf-8').write(html)  # raiz servida pelo Amplify
print('OK -> dashboard.html / index.html ({} bytes)'.format(len(html)))
