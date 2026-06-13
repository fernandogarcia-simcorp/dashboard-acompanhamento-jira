# -*- coding: utf-8 -*-
"""
Ponto unico de atualizacao do dashboard, SEM depender do MCP.
Puxa os 3 projetos direto da API REST do Jira + horas do Tempo, e regenera tudo.

Variaveis de ambiente (GitHub Actions Secrets / locais):
  JIRA_EMAIL       (obrig.) e-mail Atlassian
  JIRA_API_TOKEN   (obrig.) token de API do Jira (id.atlassian.com/manage/api-tokens)
  TEMPO_TOKEN      (opc.)   token do app Tempo (sem ele, cai no worklog nativo)
  DASH_PERIOD_START (opc.)  inicio do periodo dos projetos de suporte (default 2026-04-01)

Fluxo:
  1. Jira REST -> raw/scupokr.json, raw/sde.json, raw/sds.json
  2. refresh_tempo.py -> tempo_hours.json
  3. build_support_data.py -> support_data.json
  4. build_dashboard_data.py -> dashboard_data.json
  5. generate_dashboard.py -> dashboard.html + index.html
"""
import os, sys, json, base64, subprocess, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(ROOT, 'raw')
os.makedirs(RAW, exist_ok=True)

JIRA_SITE = os.environ.get('JIRA_SITE', 'simconsultas.atlassian.net')
JIRA_EMAIL = os.environ.get('JIRA_EMAIL')
JIRA_API_TOKEN = os.environ.get('JIRA_API_TOKEN')
PERIOD = os.environ.get('DASH_PERIOD_START') or '2026-04-01'  # trata env var vazia (GH Actions)

def die(m): print('ERRO:', m); sys.exit(1)
if not (JIRA_EMAIL and JIRA_API_TOKEN):
    die('defina JIRA_EMAIL e JIRA_API_TOKEN no ambiente.')

AUTH = 'Basic ' + base64.b64encode(f'{JIRA_EMAIL}:{JIRA_API_TOKEN}'.encode()).decode()

def jira_search(jql, fields):
    """Busca paginada via endpoint enhanced /rest/api/3/search/jql. Retorna lista de nodes."""
    url = f'https://{JIRA_SITE}/rest/api/3/search/jql'
    nodes, token = [], None
    while True:
        body = {'jql': jql, 'fields': fields, 'maxResults': 100}
        if token:
            body['nextPageToken'] = token
        req = urllib.request.Request(url, data=json.dumps(body).encode('utf-8'),
                                     headers={'Authorization': AUTH, 'Accept': 'application/json',
                                              'Content-Type': 'application/json'}, method='POST')
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                d = json.loads(r.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            die(f'Jira HTTP {e.code}: {e.read().decode("utf-8","replace")[:300]}')
        except urllib.error.URLError as e:
            die(f'rede: {e}')
        nodes.extend(d.get('issues', []))
        token = d.get('nextPageToken')
        if d.get('isLast', True) or not token:
            break
    return nodes

def save_raw(name, nodes):
    payload = {'issues': {'nodes': nodes, 'webUrl': f'https://{JIRA_SITE}', 'pageInfo': {'hasNextPage': False}}}
    json.dump(payload, open(os.path.join(RAW, name), 'w', encoding='utf-8'), ensure_ascii=False)
    print(f'  raw/{name}: {len(nodes)} issues')

SCUPOKR_FIELDS = ['summary','issuetype','status','priority','assignee','created','updated','resolutiondate','parent','labels','duedate']
# inclui campos customizados de SDE (Cliente 11704, Tipo de Sistema 11400) e
# SDS (Organização 10804, Categoria 11702). Campos ausentes num projeto voltam nulos.
SUP_FIELDS = ['summary','issuetype','status','priority','assignee','created','updated','timespent',
              'customfield_11704','customfield_11400','customfield_10804','customfield_11702']

print('1) Jira REST ...')
save_raw('scupokr.json', jira_search('project = SCUPOKR ORDER BY created ASC', SCUPOKR_FIELDS))
sup_jql = f'project = {{}} AND (created >= "{PERIOD}" OR updated >= "{PERIOD}") ORDER BY updated DESC'
save_raw('sde.json', jira_search(sup_jql.format('SDE'), SUP_FIELDS))
save_raw('sds.json', jira_search(sup_jql.format('SDS'), SUP_FIELDS))

def run(script):
    print(f'-> {script}')
    r = subprocess.run([sys.executable, os.path.join(ROOT, script)], cwd=ROOT)
    if r.returncode != 0:
        die(f'falha em {script}')

print('2) Tempo ...')
if os.environ.get('TEMPO_TOKEN'):
    run('refresh_tempo.py')
else:
    print('  TEMPO_TOKEN ausente - usando worklog nativo (fallback).')

print('3-5) build + generate ...')
run('build_support_data.py')
run('build_dashboard_data.py')
run('generate_dashboard.py')
print('OK -> dashboard.html / index.html atualizados.')
