# -*- coding: utf-8 -*-
import json, datetime, collections, os

OUTDIR = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(OUTDIR, 'raw', 'scupokr.json')   # gerado por refresh_all.py (ou snapshot do MCP)

d = json.load(open(SRC, encoding='utf-8'))
nodes = d['issues']['nodes']

def simplify(n):
    f = n['fields']
    return {
        'key': n['key'],
        'summary': f['summary'],
        'type': f['issuetype']['name'],
        'status': f['status']['name'],
        'cat': f['status']['statusCategory']['key'],   # new / indeterminate / done
        'priority': (f.get('priority') or {}).get('name', '-'),
        'assignee': (f.get('assignee') or {}).get('displayName', 'Nao atribuido'),
        'created': f['created'][:10],
        'updated': (f.get('updated') or '')[:10],
        'resolved': (f.get('resolutiondate') or '')[:10],
        'parent': (f.get('parent') or {}).get('key'),
    }

issues = [simplify(n) for n in nodes]

# --- 10 issues da pagina 2 (SCUPOKR-175..184), capturados inline ---
extra = [
    ('SCUPOKR-175','Execucao de Lotes - Armazenamento do Arquivo Original','Tarefa','A Fazer','new','Baixa','Enzo Simionato','2026-06-11','',None),
    ('SCUPOKR-176','Controle de Acesso do Portal de Contas','Tarefa','A Fazer','new','Baixa','Enzo Simionato','2026-06-11','',None),
    ('SCUPOKR-177','Otimizacao da Validacao de API Key para obter o respectivo Tenant','Tarefa','A Fazer','new','Baixa','Enzo Simionato','2026-06-11','',None),
    ('SCUPOKR-178','Implementar metodos de integracao com os clientes','Tarefa','Backlog','new','Baixa','Enzo Simionato','2026-06-11','',None),
    ('SCUPOKR-179','Endpoint de Consulta de Parametros por Execucao','Tarefa','A Fazer','new','Baixa','Enzo Simionato','2026-06-11','',None),
    ('SCUPOKR-180','Melhorar Retorno de Erro do /run-sync','Tarefa','A Fazer','new','Baixa','Enzo Simionato','2026-06-11','',None),
    ('SCUPOKR-181','Reducao de Testes de Consulta Excessivos no projeto de testes','Tarefa','A Fazer','new','Baixa','Enzo Simionato','2026-06-11','',None),
    ('SCUPOKR-182','Atualizacao de Dependencias com vulnerabilidades','Tarefa','Em Validação','indeterminate','Baixa','Enzo Simionato','2026-06-11','',None),
    ('SCUPOKR-183','Remover API de Exemplo da Documentacao','Tarefa','A Fazer','new','Baixa','Enzo Simionato','2026-06-11','',None),
    ('SCUPOKR-184','Correcao da area de cadastros e atualizacao da query de detalhes das notas - Portal de Acompanhamento','Tarefa','Em Validação','indeterminate','Baixa','Alan Felipusso','2026-06-11','',None),
]
have = {i['key'] for i in issues}
for e in extra:
    if e[0] not in have:
        issues.append(dict(zip(['key','summary','type','status','cat','priority','assignee','created','updated','resolved','parent'],
                               (e[0],e[1],e[2],e[3],e[4],e[5],e[6],e[7],e[7],e[8],e[9]))))

# normaliza tipos
TYPE_MAP = {'Historia':'Historia','Historia':'Historia','Story':'Historia','História':'Historia',
            'Tópico':'Epico','Topico':'Epico','Tarefa':'Tarefa'}
for i in issues:
    i['typeNorm'] = 'Epico' if i['type'] in ('Tópico','Topico','Epic') else ('Historia' if i['type'] in ('Story','História','Historia') else 'Tarefa')

TODAY = datetime.date.today()
def dparse(s):
    return datetime.date(int(s[0:4]),int(s[5:7]),int(s[8:10])) if s else None

# ---- agregados ----
by_status = collections.Counter(i['status'] for i in issues)
by_cat = collections.Counter(i['cat'] for i in issues)
by_type = collections.Counter(i['typeNorm'] for i in issues)
by_prio = collections.Counter(i['priority'] for i in issues)
by_assignee = collections.Counter(i['assignee'] for i in issues)

# carga por responsavel decomposta por situacao (concluido / em andamento / a fazer / backlog)
def load_bucket(i):
    if i['cat']=='done': return 'done'
    if i['cat']=='indeterminate': return 'prog'
    if i['status']=='A Fazer': return 'afazer'
    return 'backlog'  # Backlog (e qualquer outro 'new')
by_assignee_breakdown = {}
for i in issues:
    a = i['assignee']
    d = by_assignee_breakdown.setdefault(a, {'done':0,'prog':0,'afazer':0,'backlog':0,'total':0})
    d[load_bucket(i)] += 1
    d['total'] += 1

total = len(issues)
done = by_cat.get('done',0)
inprog = by_cat.get('indeterminate',0)
todo = by_cat.get('new',0)
pct = round(done/total*100,1)

# ---- throughput semanal (segunda a domingo) por resolucao e por criacao ----
def week_start(dt):
    return dt - datetime.timedelta(days=dt.weekday())

created_w = collections.Counter()
# proxy de conclusao: issues concluidas, agrupadas pela semana do 'updated'
doneupd_w = collections.Counter()
for i in issues:
    c = dparse(i['created'])
    if c: created_w[week_start(c).isoformat()] += 1
    if i['cat']=='done' and i['updated']:
        doneupd_w[week_start(dparse(i['updated'])).isoformat()] += 1

all_weeks = sorted(set(created_w) | set(doneupd_w))
weekly = [{'week':w,'created':created_w.get(w,0),'doneUpd':doneupd_w.get(w,0)} for w in all_weeks]

# ---- esta semana (semana corrente seg-dom) ----
cur_ws = week_start(TODAY).isoformat()
prev_ws = (week_start(TODAY)-datetime.timedelta(days=7)).isoformat()
def in_week(dstr, ws):
    return dstr and week_start(dparse(dstr)).isoformat()==ws
# concluidas nesta semana (proxy = updated nesta semana E status concluido)
this_week_done = [i for i in issues if i['cat']=='done' and in_week(i['updated'], cur_ws)]
this_week_created = [i for i in issues if in_week(i['created'], cur_ws)]
# tudo que teve movimentacao (updated) nesta semana e nao esta concluido
this_week_touched = [i for i in issues if in_week(i['updated'], cur_ws) and i['cat']!='done']
prev_week_done = [i for i in issues if i['cat']=='done' and in_week(i['updated'], prev_ws)]

# ---- worklogs: usa dados reais do app Tempo (tempo_hours.json, gerado por refresh_tempo.py)
#      quando disponivel; caso contrario, cai no worklog nativo do Jira (apenas 2 itens). ----
# worklogs nativos conhecidos do Jira (timespent>0). Servem de fallback e de SUPLEMENTO
# para itens que o token do Tempo nao enxerga (ex.: token com escopo "apenas proprios worklogs").
NATIVE_FALLBACK = [
    {'key':'SCUPOKR-184','summary':'Correcao da area de cadastros e atualizacao da query de detalhes das notas - Portal de Acompanhamento',
     'seconds':10800,'author':'Timesheets by Tempo (app)','started':'2026-06-11','comment':'time-tracking','status':'Em Validacao','synced':True},
    {'key':'SCUPOKR-65','summary':'Deploy em ambiente de homologacao e piloto com usuarios reais',
     'seconds':300,'author':'Fernando Garcia','started':'2026-04-13','comment':'Teste de worklog para validar o time tracking nativo','status':'Concluido','synced':False,'test':True},
]
tempo_path = os.path.join(OUTDIR, 'tempo_hours.json')
hours_supplemented = 0
if os.path.exists(tempo_path):
    _t = json.load(open(tempo_path, encoding='utf-8'))
    tempo_wl = _t.get('worklogs', [])
    tempo_keys = {w['key'] for w in tempo_wl}
    suplemento = [w for w in NATIVE_FALLBACK if w['key'] not in tempo_keys]
    worklogs = list(tempo_wl) + suplemento
    hours_supplemented = len(suplemento)
    hours_source = 'tempo'
    hours_range = _t.get('range')
    hours_generated = _t.get('generated')
else:
    worklogs = list(NATIVE_FALLBACK)
    hours_source = 'jira-nativo'
    hours_range = None
    hours_generated = None

# o Tempo grava worklog nativo com a conta do app como autor; o usuario real fica no Tempo.
# regra de fallback: se nao houver 'person' (dado do Tempo) e o autor for o app, atribui ao RESPONSAVEL.
assignee_by_key = {i['key']: i['assignee'] for i in issues}
hours_total = sum(w['seconds'] for w in worklogs)
hours_by_person = collections.Counter()
worklog_sec = {}
for w in worklogs:
    if not w.get('person'):
        is_app = ('Tempo' in w.get('author','')) or w.get('synced')
        w['person'] = assignee_by_key.get(w['key'], w.get('author','')) if is_app else w.get('author','')
    hours_by_person[w['person']] += w['seconds']
    worklog_sec[w['key']] = worklog_sec.get(w['key'],0) + w['seconds']
worklogs.sort(key=lambda w:(w.get('started') or '', w['seconds']), reverse=True)  # mais recente primeiro
for i in issues:
    i['logged'] = worklog_sec.get(i['key'], 0)

# ---- epicos e progresso dos filhos ----
# Epicos "guarda-chuva" de lancamento de horas (ex.: reunioes) NAO entram na Visao por
# Iniciativa; as horas lancadas neles continuam aparecendo normalmente na secao de Horas.
EPIC_EXCLUDE_INITIATIVE = {'SCUPOKR-223'}
epics = [i for i in issues if i['typeNorm']=='Epico']
children = collections.defaultdict(list)
for i in issues:
    if i['parent']:
        children[i['parent']].append(i)
epic_rows = []
for e in sorted(epics, key=lambda x:int(x['key'].split('-')[1])):
    if e['key'] in EPIC_EXCLUDE_INITIATIVE: continue
    ch = children.get(e['key'], [])
    cdone = sum(1 for c in ch if c['cat']=='done')
    cprog = sum(1 for c in ch if c['cat']=='indeterminate')
    ctodo = sum(1 for c in ch if c['cat']=='new')
    clogged = sum(c.get('logged',0) for c in ch) + e.get('logged',0)
    epic_rows.append({
        'key':e['key'],'summary':e['summary'],'status':e['status'],'cat':e['cat'],'assignee':e['assignee'],
        'children':len(ch),'done':cdone,'inprog':cprog,'todo':ctodo,'loggedSec':clogged,
        'pct': round(cdone/len(ch)*100) if ch else (100 if e['cat']=='done' else 0)
    })

# issues sem iniciativa (sem parent e que nao sao epicos)
orphans = [i for i in issues if not i['parent'] and i['typeNorm']!='Epico']
orphan_summary = {
    'total':len(orphans),
    'done':sum(1 for i in orphans if i['cat']=='done'),
    'inprog':sum(1 for i in orphans if i['cat']=='indeterminate'),
    'todo':sum(1 for i in orphans if i['cat']=='new'),
}
# lista detalhada (andamento -> a fazer -> concluido), depois por chave
_catord = {'indeterminate':0,'new':1,'done':2}
orphan_list = [{'key':i['key'],'summary':i['summary'],'type':i['type'],'status':i['status'],
                'cat':i['cat'],'assignee':i['assignee'],'priority':i['priority']}
               for i in sorted(orphans, key=lambda x:(_catord.get(x['cat'],3), int(x['key'].split('-')[1])))]

# em andamento / a iniciar (nao concluidas) para listas
open_issues = [i for i in issues if i['cat']!='done']
inprogress_list = [i for i in issues if i['cat']=='indeterminate']

# ---- ALERTAS: atividades em andamento (Em Progresso / Em Validacao) sem horas lancadas ----
# "movimentada" = teve update; "dias parado" = dias desde a ultima movimentacao
alerts = []
for i in issues:
    if i['cat'] == 'indeterminate' and i['logged'] == 0:
        upd = dparse(i['updated'])
        days = (TODAY - upd).days if upd else None
        alerts.append({
            'key':i['key'],'summary':i['summary'],'status':i['status'],
            'assignee':i['assignee'],'updated':i['updated'],'daysIdle':days,
        })
alerts.sort(key=lambda a:(-(a['daysIdle'] if a['daysIdle'] is not None else -1)))

# projetos de suporte (SDE/SDS), filtrados pelo periodo do dashboard
support_path = os.path.join(OUTDIR, 'support_data.json')
support = json.load(open(support_path, encoding='utf-8')) if os.path.exists(support_path) else None

# ---- horas consolidadas (todos os projetos) para a Visao Geral ----
# SCUPOKR = lancamentos detalhados do Tempo; SDE/SDS = total por issue (timespent)
ov_logs, ov_byperson = [], collections.Counter()
for w in worklogs:
    ov_logs.append({'project':'SCUPOKR','key':w['key'],'summary':w.get('summary',''),
                    'seconds':w['seconds'],'person':w['person'],'started':w.get('started','')})
    ov_byperson[w['person']] += w['seconds']
if support:
    for p in support['projects']:
        for hl in p.get('hourLogs', []):
            ov_logs.append({'project':p['key'],'key':hl['key'],'summary':hl['summary'],
                            'seconds':hl['seconds'],'person':hl['person'],'started':hl['started']})
            ov_byperson[hl['person']] += hl['seconds']
ov_logs.sort(key=lambda x:(x.get('started') or '', x['seconds']), reverse=True)  # mais recente primeiro
overview_hours = {'totalSec':sum(x['seconds'] for x in ov_logs),
                  'byPerson':dict(ov_byperson.most_common()), 'logs':ov_logs}

# ---- lista unificada de issues (todos os projetos) p/ o motor de periodo no navegador ----
all_issues = []
for i in issues:  # SCUPOKR
    all_issues.append({'project':'SCUPOKR','key':i['key'],'summary':i['summary'],'type':i['typeNorm'],
        'status':i['status'],'cat':i['cat'],'priority':i['priority'],'assignee':i['assignee'],
        'created':i['created'],'updated':i['updated'],'resolved':i.get('resolved',''),
        'logged':i.get('logged',0),'parent':i.get('parent'),'isEpic':i['typeNorm']=='Epico','custom':{}})
if support:
    for p in support['projects']:
        for i in p['issues']:
            all_issues.append({'project':p['key'],'key':i['key'],'summary':i['summary'],'type':i['type'],
                'status':i['status'],'cat':i['cat'],'priority':i['priority'],'assignee':i['assignee'],
                'created':i['created'],'updated':i['updated'],'resolved':i.get('resolved',''),
                'logged':i.get('logged',0),'parent':None,'isEpic':False,'custom':i.get('custom',{})})

data = {
    'project':'SCUPDATA - OKR (SCUPOKR)',
    'generated': TODAY.isoformat(),
    'baseUrl':'https://simconsultas.atlassian.net/browse/',
    'total':total,'done':done,'inprog':inprog,'todo':todo,'pct':pct,
    'byStatus':dict(by_status),'byType':dict(by_type),'byPriority':dict(by_prio),
    'byAssignee':dict(by_assignee),
    'byAssigneeBreakdown':by_assignee_breakdown,
    'weekly':weekly,
    'curWeek':cur_ws,'prevWeek':prev_ws,
    'thisWeekDone':this_week_done,'thisWeekCreated':this_week_created,
    'thisWeekTouched':this_week_touched,'prevWeekDone':prev_week_done,
    'epics':epic_rows,
    'orphans':orphan_summary,
    'orphanList':orphan_list,
    'inprogressList':inprogress_list,
    'worklogs':worklogs,
    'hoursTotalSec':hours_total,
    'hoursByPerson':dict(hours_by_person),
    'hoursSource':hours_source,
    'hoursRange':hours_range,
    'hoursGenerated':hours_generated,
    'hoursSupplemented':hours_supplemented,
    'alerts':alerts,
    'support':support,
    'overviewHours':overview_hours,
    'allIssues':all_issues,
    'today':TODAY.isoformat(),
    'fetchFrom':f'{TODAY.year}-01-01',
    'scupokrWorklogs':[{'key':w['key'],'summary':w.get('summary',''),'seconds':w['seconds'],
                        'person':w['person'],'started':w.get('started','')} for w in worklogs],
    'issues':issues,
}
json.dump(data, open(os.path.join(OUTDIR,'dashboard_data.json'),'w',encoding='utf-8'), ensure_ascii=False, indent=1)

# ---- print resumo ----
print('TOTAL', total, '| DONE', done, f'({pct}%)', '| INPROG', inprog, '| TODO', todo)
print('STATUS', dict(by_status))
print('TYPE', dict(by_type))
print('PRIO', dict(by_prio))
print('ASSIGNEE', dict(by_assignee))
print('CUR WEEK', cur_ws, 'done(upd)', len(this_week_done), 'created', len(this_week_created), 'touched', len(this_week_touched), '| PREV', prev_ws, 'done', len(prev_week_done))
print('--- EPICS ---')
for r in epic_rows:
    print(f"{r['key']:14} {r['status']:14} {r['done']}/{r['children']} ({r['pct']}%) {r['summary'][:55]}")
print('--- WEEKLY (ult 8) ---')
for w in weekly[-8:]:
    print(w)
print('--- IN PROGRESS ---')
for i in inprogress_list:
    print(i['key'], i['status'], '|', i['assignee'], '|', i['summary'][:60])
