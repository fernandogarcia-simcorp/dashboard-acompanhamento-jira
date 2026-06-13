# -*- coding: utf-8 -*-
"""Processa SDE e SDS (desde 01/01, criados/movimentados) e grava support_data.json.
Emite os dados POR ISSUE (com campos customizados, horas e resolucao) — a agregacao
por periodo e feita no navegador (dashboard dirigido por periodo)."""
import json, os, datetime

OUT = os.path.dirname(os.path.abspath(__file__))

SRC = {
    'SDE': (os.path.join(OUT, 'raw', 'sde.json'), 'Suporte Desenvolvimento'),
    'SDS': (os.path.join(OUT, 'raw', 'sds.json'), 'Suporte Sim>Consultas'),
}
# campos customizados por projeto: (rotulo, fieldId, tipo) | 'select' = {value} | 'org' = [{name}]
CUSTOM = {
    'SDE': [('Cliente', 'customfield_11704', 'select'), ('Tipo de Sistema', 'customfield_11400', 'select')],
    'SDS': [('Organização', 'customfield_10804', 'org'), ('Categoria', 'customfield_11702', 'select')],
}

def cf_value(fields, fid, ftype):
    v = fields.get(fid)
    if ftype == 'org':
        return [o.get('name') or 'Não informado' for o in v] if v else []
    return (v.get('value') if v else None)

projects = []
for key, (path, name) in SRC.items():
    d = json.load(open(path, encoding='utf-8'))
    nodes = d['issues']['nodes']
    cfg = CUSTOM.get(key, [])
    issues = []
    for n in nodes:
        f = n['fields']
        issues.append({
            'key': n['key'],
            'summary': f['summary'],
            'type': f['issuetype']['name'],
            'status': f['status']['name'],
            'cat': f['status']['statusCategory']['key'],     # new/indeterminate/done
            'priority': (f.get('priority') or {}).get('name', '-'),
            'assignee': (f.get('assignee') or {}).get('displayName', 'Nao atribuido'),
            'created': f['created'][:10],
            'updated': (f.get('updated') or '')[:10],
            'resolved': (f.get('resolutiondate') or '')[:10],
            'logged': f.get('timespent') or 0,
            'custom': {label: cf_value(f, fid, ftype) for label, fid, ftype in cfg},
        })
    projects.append({
        'key': key, 'name': name,
        'customCfg': [{'label': c[0], 'type': c[2]} for c in cfg],
        'issues': issues,
    })
    print(f'{key}: {len(issues)} issues')

data = {'fetchFrom': f'{datetime.date.today().year}-01-01',
        'generated': datetime.date.today().isoformat(), 'projects': projects}
json.dump(data, open(os.path.join(OUT, 'support_data.json'), 'w', encoding='utf-8'), ensure_ascii=False)
print('OK -> support_data.json')
