# -*- coding: utf-8 -*-
"""
Monta o resumo semanal (a partir de dashboard_data.json) e envia por SMTP.
Use --dry-run para gravar email_preview.html sem enviar.

Variaveis de ambiente:
  SMTP_HOST   (ex.: smtp.office365.com  |  smtp.gmail.com)
  SMTP_PORT   (587 STARTTLS - default)
  SMTP_USER   conta de envio
  SMTP_PASS   senha de app
  MAIL_FROM   remetente (default = SMTP_USER)
  MAIL_TO     destinatarios separados por virgula
  DASHBOARD_URL  link publico do dashboard (Amplify)
"""
import os, sys, json, smtplib, datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

ROOT = os.path.dirname(os.path.abspath(__file__))
DRY = '--dry-run' in sys.argv
d = json.load(open(os.path.join(ROOT, 'dashboard_data.json'), encoding='utf-8'))

URL = os.environ.get('DASHBOARD_URL', '#')
NAVY, GREEN, GREENd, ORANGE, GRAY, DANGER = '#023859', '#84BF04', '#4A6E03', '#E67E22', '#B3B3B3', '#C0392B'
MES = ['janeiro','fevereiro','março','abril','maio','junho','julho','agosto','setembro','outubro','novembro','dezembro']
g = datetime.date.fromisoformat(d['generated'])
gen_str = f'{g.day:02d} de {MES[g.month-1]} de {g.year}'

def esc(s): return str(s).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
def fmtH(sec):
    if not sec: return '0h'
    h, m = sec//3600, round((sec%3600)/60)
    return (f'{h}h' if h else '') + (f' {m}min' if m else '') or '0h'

alerts = d.get('alerts', [])
hours_total = fmtH(d.get('hoursTotalSec', 0))
by_person = sorted(d.get('hoursByPerson', {}).items(), key=lambda x: -x[1])

# linhas do portfolio
projects = [('SCUPOKR', 'SCUPDATA · OKR', d['total'], d['done'], d['inprog'], d['todo'], round(d['pct']))]
if d.get('support'):
    for p in d['support']['projects']:
        projects.append((p['key'], p['name'], p['total'], p['done'], p['inprog'], p['todo'], p['pct']))

def bar(done, prog, todo, total):
    total = total or 1
    seg = lambda v, c: f'<td width="{round(v/total*100)}%" bgcolor="{c}" style="font-size:0;line-height:6px">&nbsp;</td>' if v else ''
    return ('<table width="100%" cellpadding="0" cellspacing="0" style="border-collapse:collapse;height:6px">'
            f'<tr>{seg(done,GREEN)}{seg(prog,ORANGE)}{seg(todo,GRAY)}</tr></table>')

prows = ''
for key, name, total, done, prog, todo, pct in projects:
    prows += (f'<tr><td style="padding:10px 0;border-bottom:1px solid #E4E7E5">'
              f'<table width="100%" cellpadding="0" cellspacing="0"><tr>'
              f'<td style="font-family:Arial,sans-serif;font-size:13px;color:{NAVY}"><b>{esc(key)}</b> '
              f'<span style="color:#5A5247">— {esc(name)}</span></td>'
              f'<td align="right" style="font-family:Arial,sans-serif;font-size:13px;color:{NAVY}">'
              f'<b>{total}</b> itens · <b style="color:{GREENd}">{pct}%</b></td></tr></table>'
              f'<div style="margin-top:6px">{bar(done,prog,todo,total)}</div></td></tr>')

person_rows = ''.join(
    f'<tr><td style="font-family:Arial,sans-serif;font-size:13px;color:#5A5247;padding:3px 0">{esc(n)}</td>'
    f'<td align="right" style="font-family:Arial,sans-serif;font-size:13px;color:{NAVY};font-weight:bold">{fmtH(s)}</td></tr>'
    for n, s in by_person) or '<tr><td style="font-family:Arial,sans-serif;font-size:13px;color:#5A5247">Sem lançamentos.</td></tr>'

alert_rows = ''
for a in alerts[:6]:
    dd = a.get('daysIdle')
    dtxt = '—' if dd is None else ('hoje' if dd == 0 else f'{dd}d parado')
    alert_rows += (f'<tr><td style="font-family:Arial,sans-serif;font-size:12px;color:{NAVY};padding:4px 0;border-bottom:1px solid #F0E2C4">'
                   f'<b>{esc(a["key"])}</b> — {esc(a["summary"][:70])}<br>'
                   f'<span style="color:#8A4B12">{esc(a["assignee"])} · {esc(a["status"])} · {dtxt}</span></td></tr>')
alert_extra = f'<tr><td style="font-family:Arial,sans-serif;font-size:12px;color:#8A4B12;padding-top:6px">+ {len(alerts)-6} outras</td></tr>' if len(alerts) > 6 else ''

html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body style="margin:0;background:#F4F6F4;padding:24px 0">
<table align="center" width="640" cellpadding="0" cellspacing="0" style="background:#fff;border-radius:8px;overflow:hidden;border:1px solid #E4E7E5">
  <tr><td style="background:#023859;padding:26px 30px">
    <div style="font-family:Arial,sans-serif;font-size:11px;letter-spacing:2px;color:{GREEN};font-weight:bold">STATUS REPORT SEMANAL</div>
    <div style="font-family:Arial,sans-serif;font-size:26px;color:#fff;font-weight:bold;margin-top:6px">Projetos <span style="color:{GREEN}">Ativos</span></div>
    <div style="font-family:Arial,sans-serif;font-size:12px;color:#cfe0d6;margin-top:6px">Emitido em {gen_str}</div>
  </td></tr>
  <tr><td style="padding:24px 30px">
    <div style="font-family:Arial,sans-serif;font-size:11px;letter-spacing:1px;color:{GREENd};font-weight:bold;margin-bottom:8px">PORTFÓLIO</div>
    <table width="100%" cellpadding="0" cellspacing="0">{prows}</table>

    <table width="100%" cellpadding="0" cellspacing="0" style="margin-top:22px"><tr>
      <td width="25%" style="font-family:Arial,sans-serif"><div style="font-size:30px;font-weight:bold;color:{NAVY}">{d['total']}</div><div style="font-size:11px;color:{GRAY}">ISSUES (SCUPOKR)</div></td>
      <td width="25%" style="font-family:Arial,sans-serif"><div style="font-size:30px;font-weight:bold;color:{GREENd}">{d['pct']}%</div><div style="font-size:11px;color:{GRAY}">CONCLUÍDO</div></td>
      <td width="25%" style="font-family:Arial,sans-serif"><div style="font-size:30px;font-weight:bold;color:{ORANGE}">{d['inprog']}</div><div style="font-size:11px;color:{GRAY}">EM ANDAMENTO</div></td>
      <td width="25%" style="font-family:Arial,sans-serif"><div style="font-size:30px;font-weight:bold;color:{NAVY}">{d['todo']}</div><div style="font-size:11px;color:{GRAY}">A FAZER</div></td>
    </tr></table>

    <table width="100%" cellpadding="0" cellspacing="0" style="margin-top:22px"><tr>
      <td width="48%" valign="top">
        <div style="font-family:Arial,sans-serif;font-size:11px;letter-spacing:1px;color:{GREENd};font-weight:bold;margin-bottom:6px">HORAS (TEMPO) · {hours_total}</div>
        <table width="100%" cellpadding="0" cellspacing="0">{person_rows}</table>
      </td>
      <td width="4%"></td>
      <td width="48%" valign="top">
        <div style="font-family:Arial,sans-serif;font-size:11px;letter-spacing:1px;color:{DANGER};font-weight:bold;margin-bottom:6px">ALERTAS · {len(alerts)} sem horas</div>
        <table width="100%" cellpadding="0" cellspacing="0">{alert_rows}{alert_extra}</table>
      </td>
    </tr></table>

    <table width="100%" cellpadding="0" cellspacing="0" style="margin-top:26px"><tr><td align="center">
      <a href="{URL}" style="font-family:Arial,sans-serif;font-size:13px;font-weight:bold;color:{NAVY};background:{GREEN};text-decoration:none;padding:12px 26px;border-radius:6px;display:inline-block">ABRIR O DASHBOARD COMPLETO</a>
    </td></tr></table>
  </td></tr>
  <tr><td style="background:#023859;padding:16px 30px;font-family:Arial,sans-serif;font-size:11px;color:#9fb6c2">
    SIMCORP · Gerado automaticamente a partir do Jira e do Tempo. {URL}
  </td></tr>
</table>
</body></html>"""

subject = f'Status Report Semanal · Projetos Ativos ({g.day:02d}/{g.month:02d}) · {len(alerts)} alertas'

if DRY:
    open(os.path.join(ROOT, 'email_preview.html'), 'w', encoding='utf-8').write(html)
    print('DRY-RUN -> email_preview.html')
    print('Assunto:', subject)
    sys.exit(0)

host = os.environ.get('SMTP_HOST'); port = int(os.environ.get('SMTP_PORT', '587'))
user = os.environ.get('SMTP_USER'); pwd = os.environ.get('SMTP_PASS')
mail_from = os.environ.get('MAIL_FROM', user)
mail_to = [x.strip() for x in os.environ.get('MAIL_TO', '').split(',') if x.strip()]
if not (host and user and pwd and mail_to):
    print('ERRO: defina SMTP_HOST, SMTP_USER, SMTP_PASS e MAIL_TO.'); sys.exit(1)

msg = MIMEMultipart('alternative')
msg['Subject'] = subject
msg['From'] = mail_from
msg['To'] = ', '.join(mail_to)
msg.attach(MIMEText('Seu cliente de e-mail não suporta HTML. Acesse o dashboard: ' + URL, 'plain', 'utf-8'))
msg.attach(MIMEText(html, 'html', 'utf-8'))

with smtplib.SMTP(host, port, timeout=60) as s:
    s.starttls()
    s.login(user, pwd)
    s.sendmail(mail_from, mail_to, msg.as_string())
print(f'E-mail enviado para {len(mail_to)} destinatario(s).')
