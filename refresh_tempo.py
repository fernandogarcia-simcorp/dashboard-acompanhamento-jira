# -*- coding: utf-8 -*-
"""
Puxa as horas reais do app Tempo (api.tempo.io v4) e grava em tempo_hours.json,
que o build_dashboard_data.py consome para alimentar o dashboard.

NUNCA coloque o token no codigo. O script le de variaveis de ambiente:

  TEMPO_TOKEN     (obrigatorio)  -> token de API do Tempo (Settings > API Integration)
  JIRA_EMAIL      (opcional)     -> seu e-mail Atlassian
  JIRA_API_TOKEN  (opcional)     -> token de API do Jira (id.atlassian.com/manage/api-tokens)

Como definir (PowerShell, sessao atual):
  $env:TEMPO_TOKEN = "xxxx"
  $env:JIRA_EMAIL = "fernando.garcia@simconsultas.com.br"
  $env:JIRA_API_TOKEN = "yyyy"
Ou persistente (abra um NOVO terminal depois):
  setx TEMPO_TOKEN "xxxx"

Uso:
  python refresh_tempo.py                 # periodo padrao: 2026-04-01 ate hoje
  python refresh_tempo.py 2026-04-01 2026-06-30

- Com JIRA_EMAIL + JIRA_API_TOKEN: resolve chave/responsavel/resumo, filtra SCUPOKR
  e grava tempo_hours.json pronto para o dashboard.
- Sem credenciais Jira: grava tempo_worklogs_raw.json (ids nao resolvidos) para o
  Claude enriquecer via MCP. Recomendado fornecer as credenciais Jira.
"""
import os, sys, json, base64, datetime, urllib.request, urllib.parse, urllib.error

OUT = os.path.dirname(os.path.abspath(__file__))
PROJECT_PREFIX = "SCUPOKR-"
JIRA_CLOUD = "simconsultas.atlassian.net"

TEMPO_TOKEN = os.environ.get("TEMPO_TOKEN")
JIRA_EMAIL = os.environ.get("JIRA_EMAIL")
JIRA_API_TOKEN = os.environ.get("JIRA_API_TOKEN")

def die(msg):
    print("ERRO: " + msg)
    sys.exit(1)

if not TEMPO_TOKEN:
    die("variavel de ambiente TEMPO_TOKEN nao definida. Veja o cabecalho deste arquivo.")

# periodo
today = datetime.date.today()
arg_from = sys.argv[1] if len(sys.argv) > 1 else "2026-04-01"
arg_to = sys.argv[2] if len(sys.argv) > 2 else today.isoformat()

def http_get(url, headers):
    req = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")[:300]
        die(f"HTTP {e.code} em {url}\n{body}")
    except urllib.error.URLError as e:
        die(f"falha de rede: {e}")

# ---------------- 1) Tempo: buscar worklogs ----------------
def fetch_tempo():
    headers = {"Authorization": "Bearer " + TEMPO_TOKEN, "Accept": "application/json"}
    base = "https://api.tempo.io/4/worklogs"
    params = {"from": arg_from, "to": arg_to, "limit": "1000", "offset": "0"}
    url = base + "?" + urllib.parse.urlencode(params)
    out = []
    while url:
        data = http_get(url, headers)
        for w in data.get("results", []):
            out.append({
                "tempoWorklogId": w.get("tempoWorklogId"),
                "issueId": (w.get("issue") or {}).get("id"),
                "seconds": w.get("timeSpentSeconds", 0),
                "billableSeconds": w.get("billableSeconds"),
                "accountId": (w.get("author") or {}).get("accountId"),
                "started": w.get("startDate"),
                "description": (w.get("description") or "").strip(),
            })
        url = (data.get("metadata") or {}).get("next")
    return out

print(f"Buscando worklogs do Tempo de {arg_from} a {arg_to} ...")
raw = fetch_tempo()
print(f"  {len(raw)} worklogs recebidos do Tempo.")

# ---------------- 2) Jira (opcional): resolver chave/nome/resumo ----------------
def jira_auth_header():
    tok = base64.b64encode(f"{JIRA_EMAIL}:{JIRA_API_TOKEN}".encode()).decode()
    return {"Authorization": "Basic " + tok, "Accept": "application/json"}

if JIRA_EMAIL and JIRA_API_TOKEN:
    jh = jira_auth_header()
    # 2a) issue id -> {key, summary, status, assignee}
    issue_ids = sorted({str(w["issueId"]) for w in raw if w["issueId"]})
    issue_map = {}
    print(f"Resolvendo {len(issue_ids)} issues no Jira ...")
    for iid in issue_ids:
        u = f"https://{JIRA_CLOUD}/rest/api/3/issue/{iid}?fields=key,summary,status,assignee"
        d = http_get(u, jh)
        f = d.get("fields", {})
        issue_map[iid] = {
            "key": d.get("key"),
            "summary": f.get("summary", ""),
            "status": (f.get("status") or {}).get("name", ""),
            "assignee": ((f.get("assignee") or {}) or {}).get("displayName", "Nao atribuido"),
        }
    # 2b) accountId -> displayName (em lote)
    acc_ids = sorted({w["accountId"] for w in raw if w["accountId"]})
    name_map = {}
    for i in range(0, len(acc_ids), 90):
        chunk = acc_ids[i:i+90]
        qs = "&".join("accountId=" + urllib.parse.quote(a) for a in chunk)
        u = f"https://{JIRA_CLOUD}/rest/api/3/user/bulk?{qs}&maxResults=90"
        d = http_get(u, jh)
        for usr in d.get("values", []):
            name_map[usr.get("accountId")] = usr.get("displayName")

    worklogs = []
    for w in raw:
        info = issue_map.get(str(w["issueId"]), {})
        key = info.get("key", "")
        if not key.startswith(PROJECT_PREFIX):
            continue  # mantem so o projeto SCUPOKR
        worklogs.append({
            "key": key,
            "summary": info.get("summary", ""),
            "status": info.get("status", ""),
            "assignee": info.get("assignee", ""),
            "seconds": w["seconds"],
            "person": name_map.get(w["accountId"], info.get("assignee", "Desconhecido")),
            "started": w["started"],
            "comment": w["description"],
            "synced": True,
        })
    payload = {
        "source": "tempo-api-v4",
        "range": {"from": arg_from, "to": arg_to},
        "generated": today.isoformat(),
        "worklogs": worklogs,
    }
    json.dump(payload, open(os.path.join(OUT, "tempo_hours.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    tot = sum(w["seconds"] for w in worklogs)
    print(f"OK -> tempo_hours.json | {len(worklogs)} worklogs SCUPOKR | total {tot/3600:.1f}h")
    print("Agora rode:  python build_dashboard_data.py && python generate_dashboard.py")
else:
    json.dump({"source": "tempo-api-v4", "range": {"from": arg_from, "to": arg_to},
               "generated": today.isoformat(), "raw": raw},
              open(os.path.join(OUT, "tempo_worklogs_raw.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("OK -> tempo_worklogs_raw.json (ids nao resolvidos).")
    print("Sem JIRA_EMAIL/JIRA_API_TOKEN: defina-os para resolver chaves/nomes,")
    print("ou peca ao Claude para enriquecer este arquivo via MCP do Jira.")
