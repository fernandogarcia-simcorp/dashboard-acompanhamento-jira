# -*- coding: utf-8 -*-
"""
Resumo semanal por e-mail (SMTP). Calcula o periodo a partir de dashboard_data.json (allIssues).
  --previous-week : semana ANTERIOR fechada (uso na segunda 08:30). Sem flag = semana corrente.
  --dry-run       : grava email_preview.html sem enviar.

Variaveis: SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, MAIL_FROM, MAIL_TO, DASHBOARD_URL
"""
import os, sys, json, smtplib, datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

ROOT = os.path.dirname(os.path.abspath(__file__))
DRY = '--dry-run' in sys.argv
PREV = '--previous-week' in sys.argv
d = json.load(open(os.path.join(ROOT, 'dashboard_data.json'), encoding='utf-8'))
ALL = [i for i in d.get('allIssues', []) if not i.get('isEpic')]
WL = d.get('scupokrWorklogs', [])

URL = os.environ.get('DASHBOARD_URL', '#')
NAVY, GREEN, GREENd, ORANGE, GRAY, BLUE, DANGER = '#023859', '#84BF04', '#4A6E03', '#E67E22', '#B3B3B3', '#0079C1', '#C0392B'
MES = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']

# ---- periodo: semana (seg-dom) corrente ou anterior ----
today = datetime.date.today()
monday = today - datetime.timedelta(days=today.weekday())
if PREV:
    monday = monday - datetime.timedelta(days=7)
sunday = monday + datetime.timedelta(days=6)
S, E = monday.isoformat(), sunday.isoformat()
wk_label = f'{monday.day} {MES[monday.month-1]} – {sunday.day} {MES[sunday.month-1]}'

def esc(s): return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
def fmtH(sec):
    if not sec: return '0h'
    h, m = sec // 3600, round((sec % 3600) / 60)
    return (f'{h}h' if h else '') + (f' {m}min' if m else '') or '0h'
def inR(s, a, b): return bool(s) and a <= s <= b
def isAct(i): return inR(i.get('created'), S, E) or inR(i.get('updated'), S, E) or inR(i.get('resolved'), S, E)
def resolvedIn(i): return inR(i.get('resolved'), S, E) or (i.get('cat') == 'done' and inR(i.get('updated'), S, E))

PROJ = ['SCUPOKR'] + [p['key'] for p in (d.get('support') or {}).get('projects', [])]
PNAME = {'SCUPOKR': 'SCUPDATA · OKR'}
for p in (d.get('support') or {}).get('projects', []):
    PNAME[p['key']] = p['name']

act = [i for i in ALL if isAct(i)]
def proj_act(k): return [i for i in act if i['project'] == k]

# ---- horas da semana ----
hlogs = []
for w in WL:
    if inR(w.get('started'), S, E):
        hlogs.append((w['person'], w['seconds']))
for i in ALL:
    if i['project'] != 'SCUPOKR' and i.get('logged', 0) > 0 and isAct(i):
        hlogs.append((i['assignee'], i['logged']))
hours_total = sum(s for _, s in hlogs)
byp = {}
for person, s in hlogs:
    byp[person] = byp.get(person, 0) + s
by_person = sorted(byp.items(), key=lambda x: -x[1])

alerts = d.get('alerts', [])

g = datetime.date.fromisoformat(d['generated'])
gen_str = f"{g.day:02d}/{g.month:02d}/{g.year}"

# ---- montar HTML ----
def bar(done, prog, todo, total):
    total = total or 1
    seg = lambda v, c: f'<td width="{round(v/total*100)}%" bgcolor="{c}" style="font-size:0;line-height:6px">&nbsp;</td>' if v else ''
    return ('<table width="100%" cellpadding="0" cellspacing="0" style="border-collapse:collapse;height:6px"><tr>'
            f'{seg(done,GREEN)}{seg(prog,ORANGE)}{seg(todo,GRAY)}</tr></table>')

prows = ''
for k in PROJ:
    a = proj_act(k)
    done = sum(1 for i in a if i['cat'] == 'done'); prog = sum(1 for i in a if i['cat'] == 'indeterminate'); todo = len(a)-done-prog
    pct = round(done/len(a)*100) if a else 0
    prows += (f'<tr><td style="padding:10px 0;border-bottom:1px solid #E4E7E5">'
              f'<table width="100%" cellpadding="0" cellspacing="0"><tr>'
              f'<td style="font-family:Arial,sans-serif;font-size:13px;color:{NAVY}"><b>{esc(k)}</b> '
              f'<span style="color:#5A5247">— {esc(PNAME.get(k,k))}</span></td>'
              f'<td align="right" style="font-family:Arial,sans-serif;font-size:13px;color:{NAVY}"><b>{len(a)}</b> ativos · <b style="color:{GREENd}">{pct}%</b></td>'
              f'</tr></table><div style="margin-top:6px">{bar(done,prog,todo,len(a))}</div></td></tr>')

person_rows = ''.join(
    f'<tr><td style="font-family:Arial,sans-serif;font-size:13px;color:#5A5247;padding:3px 0">{esc(n)}</td>'
    f'<td align="right" style="font-family:Arial,sans-serif;font-size:13px;color:{NAVY};font-weight:bold">{fmtH(s)}</td></tr>'
    for n, s in by_person) or '<tr><td style="font-family:Arial,sans-serif;font-size:13px;color:#5A5247">Sem lançamentos na semana.</td></tr>'

alert_rows = ''
for a in alerts[:6]:
    dd = a.get('daysIdle'); dtxt = '—' if dd is None else ('hoje' if dd == 0 else f'{dd}d parado')
    alert_rows += (f'<tr><td style="font-family:Arial,sans-serif;font-size:12px;color:{NAVY};padding:4px 0;border-bottom:1px solid #F0E2C4">'
                   f'<b>{esc(a["key"])}</b> — {esc(a["summary"][:70])}<br><span style="color:#8A4B12">{esc(a["assignee"])} · {esc(a["status"])} · {dtxt}</span></td></tr>')
alert_extra = f'<tr><td style="font-family:Arial,sans-serif;font-size:12px;color:#8A4B12;padding-top:6px">+ {len(alerts)-6} outras</td></tr>' if len(alerts) > 6 else ''

n_cri = sum(1 for i in act if inR(i.get('created'), S, E))
n_res = sum(1 for i in act if resolvedIn(i))
n_mov = sum(1 for i in act if inR(i.get('updated'), S, E))

html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
@media only screen and (max-width:600px){{
  .shell{{width:100%!important}}
  .c2{{display:block!important;width:100%!important;padding:0 0 18px 0!important}}
  .c2sp{{display:none!important}}
  .kc{{display:inline-block!important;width:50%!important;box-sizing:border-box;padding-bottom:12px!important}}
}}
</style></head><body style="margin:0;background:#F4F6F4;padding:24px 0">
<table align="center" width="640" class="shell" cellpadding="0" cellspacing="0" style="max-width:640px;width:100%;background:#fff;border-radius:8px;overflow:hidden;border:1px solid #E4E7E5">
  <tr><td style="background:#023859;padding:26px 30px">
    <div style="font-family:Arial,sans-serif;font-size:11px;letter-spacing:2px;color:{GREEN};font-weight:bold">STATUS REPORT SEMANAL</div>
    <div style="font-family:Arial,sans-serif;font-size:22px;color:#fff;font-weight:bold;margin-top:6px">Suporte <span style="color:{GREEN}">/</span> Operações <span style="color:{GREEN}">/</span> Desenvolvimento</div>
    <div style="font-family:Arial,sans-serif;font-size:13px;color:#cfe0d6;margin-top:6px">Semana de <b style="color:#fff">{wk_label}</b></div>
  </td></tr>
  <tr><td style="padding:24px 30px">
    <table width="100%" cellpadding="0" cellspacing="0"><tr>
      <td width="25%" class="kc" style="font-family:Arial,sans-serif"><div style="font-size:30px;font-weight:bold;color:{NAVY}">{len(act)}</div><div style="font-size:11px;color:{GRAY}">ATIVOS</div></td>
      <td width="25%" class="kc" style="font-family:Arial,sans-serif"><div style="font-size:30px;font-weight:bold;color:{BLUE}">{n_cri}</div><div style="font-size:11px;color:{GRAY}">CRIADOS</div></td>
      <td width="25%" class="kc" style="font-family:Arial,sans-serif"><div style="font-size:30px;font-weight:bold;color:{ORANGE}">{n_mov}</div><div style="font-size:11px;color:{GRAY}">MOVIMENTADOS</div></td>
      <td width="25%" class="kc" style="font-family:Arial,sans-serif"><div style="font-size:30px;font-weight:bold;color:{GREENd}">{n_res}</div><div style="font-size:11px;color:{GRAY}">RESOLVIDOS</div></td>
    </tr></table>

    <div style="font-family:Arial,sans-serif;font-size:11px;letter-spacing:1px;color:{GREENd};font-weight:bold;margin:22px 0 8px">PORTFÓLIO · ATIVOS NA SEMANA</div>
    <table width="100%" cellpadding="0" cellspacing="0">{prows}</table>

    <table width="100%" cellpadding="0" cellspacing="0" style="margin-top:22px"><tr>
      <td width="48%" valign="top" class="c2">
        <div style="font-family:Arial,sans-serif;font-size:11px;letter-spacing:1px;color:{GREENd};font-weight:bold;margin-bottom:6px">HORAS NA SEMANA · {fmtH(hours_total)}</div>
        <table width="100%" cellpadding="0" cellspacing="0">{person_rows}</table>
      </td>
      <td width="4%" class="c2sp"></td>
      <td width="48%" valign="top" class="c2">
        <div style="font-family:Arial,sans-serif;font-size:11px;letter-spacing:1px;color:{DANGER};font-weight:bold;margin-bottom:6px">ALERTAS SCUPOKR · {len(alerts)} sem horas</div>
        <table width="100%" cellpadding="0" cellspacing="0">{alert_rows}{alert_extra}</table>
      </td>
    </tr></table>

    <table width="100%" cellpadding="0" cellspacing="0" style="margin-top:26px"><tr><td align="center">
      <a href="{URL}" style="font-family:Arial,sans-serif;font-size:13px;font-weight:bold;color:{NAVY};background:{GREEN};text-decoration:none;padding:12px 26px;border-radius:6px;display:inline-block">ABRIR O DASHBOARD COMPLETO</a>
    </td></tr></table>
  </td></tr>
  <tr><td style="background:#023859;padding:16px 30px;font-family:Arial,sans-serif;font-size:11px;color:#9fb6c2">
    SIMCORP · Gerado automaticamente a partir do Jira e do Tempo em {gen_str}. {URL}
  </td></tr>
</table>
</body></html>"""

subject = f'Status Report Semanal · {wk_label} · {len(act)} ativos · {n_res} resolvidos'

if DRY:
    open(os.path.join(ROOT, 'email_preview.html'), 'w', encoding='utf-8').write(html)
    print('DRY-RUN -> email_preview.html | semana', wk_label, '| previous=', PREV)
    print('Assunto:', subject)
    sys.exit(0)

host = os.environ.get('SMTP_HOST'); port = int(os.environ.get('SMTP_PORT', '587'))
user = (os.environ.get('SMTP_USER') or '').strip()
# Gmail mostra a senha de app em 4 grupos separados por espaco; o valor real nao tem espacos.
pwd = (os.environ.get('SMTP_PASS') or '').replace(' ', '').strip()
mail_from = os.environ.get('MAIL_FROM', user)
mail_to = [x.strip() for x in os.environ.get('MAIL_TO', '').split(',') if x.strip()]
if not (host and user and pwd and mail_to):
    print('ERRO: defina SMTP_HOST, SMTP_USER, SMTP_PASS e MAIL_TO.'); sys.exit(1)
print(f'SMTP: conectando a {host}:{port} | user={user} | from={mail_from} | senha={len(pwd)} chars')

msg = MIMEMultipart('alternative')
msg['Subject'] = subject; msg['From'] = mail_from; msg['To'] = ', '.join(mail_to)
msg.attach(MIMEText('Seu cliente de e-mail não suporta HTML. Acesse: ' + URL, 'plain', 'utf-8'))
msg.attach(MIMEText(html, 'html', 'utf-8'))

if port == 465:
    with smtplib.SMTP_SSL(host, port, timeout=60) as s:
        s.login(user, pwd); s.sendmail(mail_from, mail_to, msg.as_string())
else:
    with smtplib.SMTP(host, port, timeout=60) as s:
        s.ehlo(); s.starttls(); s.ehlo(); s.login(user, pwd); s.sendmail(mail_from, mail_to, msg.as_string())
print(f'E-mail enviado para {len(mail_to)} destinatario(s) via {host} | semana {wk_label}.')
