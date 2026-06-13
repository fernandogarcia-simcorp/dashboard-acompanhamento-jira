# -*- coding: utf-8 -*-
"""Processa os projetos de suporte SDE e SDS (filtrados pelo periodo do dashboard,
criados OU movimentados) e grava support_data.json para o build do dashboard.

Fonte: arquivos de resultado do searchJiraIssuesUsingJql (MCP Atlassian).
Snapshot: para atualizar, re-puxe via MCP e regenere este arquivo.
"""
import json, os, collections, datetime

OUT = os.path.dirname(os.path.abspath(__file__))
PERIOD_START = os.environ.get('DASH_PERIOD_START') or '2026-04-01'  # trata env var vazia (GH Actions)
TODAY = datetime.date.today()

# arquivos de dados (gerados por refresh_all.py, ou snapshot do MCP em raw/)
SRC = {
    'SDE': (os.path.join(OUT, 'raw', 'sde.json'), 'Suporte Desenvolvimento'),
    'SDS': (os.path.join(OUT, 'raw', 'sds.json'), 'Suporte Sim>Consultas'),
}

# campos customizados por projeto: (rotulo, fieldId, tipo) | tipo: 'select' = {value} | 'org' = [{name}]
CUSTOM = {
    'SDE': [('Cliente', 'customfield_11704', 'select'), ('Tipo de Sistema', 'customfield_11400', 'select')],
    'SDS': [('Organização', 'customfield_10804', 'org'), ('Categoria', 'customfield_11702', 'select')],
}

def custom_summaries(nodes, key):
    out = []
    for label, fid, ftype in CUSTOM.get(key, []):
        cnt = collections.Counter()
        for n in nodes:
            v = n['fields'].get(fid)
            if ftype == 'org':
                if v:
                    for o in v: cnt[o.get('name') or 'Não informado'] += 1
                else:
                    cnt['Não informado'] += 1
            else:  # select
                cnt[v['value'] if v else 'Não informado'] += 1
        out.append({'label': label, 'counts': dict(cnt.most_common())})
    return out

def dparse(s):
    return datetime.date(int(s[0:4]), int(s[5:7]), int(s[8:10])) if s else None
def week_start(dt):
    return dt - datetime.timedelta(days=dt.weekday())

projects = []
for key, (path, name) in SRC.items():
    d = json.load(open(path, encoding='utf-8'))
    nodes = d['issues']['nodes']
    issues = []
    for n in nodes:
        f = n['fields']
        issues.append({
            'key': n['key'],
            'summary': f['summary'],
            'type': f['issuetype']['name'],
            'status': f['status']['name'],
            'cat': f['status']['statusCategory']['key'],   # new/indeterminate/done
            'priority': (f.get('priority') or {}).get('name', '-'),
            'assignee': (f.get('assignee') or {}).get('displayName', 'Nao atribuido'),
            'created': f['created'][:10],
            'updated': (f.get('updated') or '')[:10],
            'logged': f.get('timespent') or 0,   # horas apontadas (total por issue, seg)
        })
    # horas apontadas (timespent por issue, atribuido ao responsavel)
    hour_logs = sorted(
        [{'key': i['key'], 'summary': i['summary'], 'seconds': i['logged'],
          'person': i['assignee'], 'started': i['updated']} for i in issues if i['logged'] > 0],
        key=lambda x: -x['seconds'])
    hours_by_person = collections.Counter()
    for i in issues:
        if i['logged'] > 0:
            hours_by_person[i['assignee']] += i['logged']
    hours_total = sum(i['logged'] for i in issues)
    by_status = collections.Counter(i['status'] for i in issues)
    by_cat = collections.Counter(i['cat'] for i in issues)
    by_type = collections.Counter(i['type'] for i in issues)
    by_prio = collections.Counter(i['priority'] for i in issues)
    by_asg = collections.Counter(i['assignee'] for i in issues)
    created_in = sum(1 for i in issues if i['created'] >= PERIOD_START)
    moved_in = sum(1 for i in issues if i['updated'] >= PERIOD_START)
    # throughput semanal: criadas (por created) e concluidas (cat done, por updated)
    cw = collections.Counter(); dw = collections.Counter()
    for i in issues:
        c = dparse(i['created'])
        if c and i['created'] >= PERIOD_START:
            cw[week_start(c).isoformat()] += 1
        if i['cat'] == 'done' and i['updated'] and i['updated'] >= PERIOD_START:
            dw[week_start(dparse(i['updated'])).isoformat()] += 1
    weeks = sorted(set(cw) | set(dw))
    weekly = [{'week': w, 'created': cw.get(w, 0), 'doneUpd': dw.get(w, 0)} for w in weeks]
    # ordena issues abertas primeiro (andamento, todo) depois concluidas
    catord = {'indeterminate': 0, 'new': 1, 'done': 2}
    issues.sort(key=lambda x: (catord.get(x['cat'], 3), x['key']))
    projects.append({
        'key': key, 'name': name,
        'total': len(issues), 'created': created_in, 'moved': moved_in,
        'done': by_cat.get('done', 0), 'inprog': by_cat.get('indeterminate', 0), 'todo': by_cat.get('new', 0),
        'pct': round(by_cat.get('done', 0) / len(issues) * 100) if issues else 0,
        'byStatus': dict(by_status), 'statusCat': {i['status']: i['cat'] for i in issues}, 'byType': dict(by_type),
        'byPriority': dict(by_prio), 'byAssignee': dict(by_asg),
        'custom': custom_summaries(nodes, key),
        'hoursTotalSec': hours_total, 'hoursByPerson': dict(hours_by_person.most_common()), 'hourLogs': hour_logs,
        'weekly': weekly, 'issues': issues,
    })
    print(f"{key}: {len(issues)} no periodo | done {by_cat.get('done',0)} prog {by_cat.get('indeterminate',0)} todo {by_cat.get('new',0)}")

data = {'period': PERIOD_START, 'generated': TODAY.isoformat(), 'projects': projects}
json.dump(data, open(os.path.join(OUT, 'support_data.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('OK -> support_data.json')
