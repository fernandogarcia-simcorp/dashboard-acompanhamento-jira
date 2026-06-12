# SCUPDATA · OKR — Dashboard automático (Amplify + GitHub Actions + e-mail)

Dashboard estático publicado no **AWS Amplify**, atualizado **toda segunda 08:30** por um
**GitHub Actions** que puxa Jira + Tempo, regenera o HTML, faz commit (dispara o deploy)
e envia o **resumo semanal por e-mail** (SMTP).

```
GitHub Actions (cron seg 08:30 BRT)
   └─ refresh_all.py ── Jira REST (SCUPOKR, SDE, SDS) + Tempo  → dashboard.html / index.html
   └─ git commit index.html  ─────────────────────────────────→ Amplify faz deploy
   └─ send_email.py ── SMTP (O365/Gmail) ─────────────────────→ resumo + link p/ a equipe
```

## Componentes
| Arquivo | Papel |
|---|---|
| `refresh_all.py` | Busca os 3 projetos na API REST do Jira + roda Tempo e os builds. Ponto único de atualização. |
| `refresh_tempo.py` | Puxa as horas reais do app Tempo (`api.tempo.io`). |
| `build_support_data.py` | Agrega SDE/SDS no período → `support_data.json`. |
| `build_dashboard_data.py` | Consolida SCUPOKR + suporte + horas + alertas → `dashboard_data.json`. |
| `generate_dashboard.py` | Renderiza `dashboard.html` **e** `index.html` (Design System SIMCORP). |
| `send_email.py` | Monta e envia o resumo semanal (use `--dry-run` p/ preview). |
| `.github/workflows/weekly.yml` | Agenda + orquestração. |
| `amplify.yml` | Build spec (site estático). |

---

## Pré-requisitos (gerar uma vez)
1. **Token de API do Jira** — https://id.atlassian.com/manage/api-tokens
2. **Token do Tempo** — Tempo → Settings → API Integration (com permissão *View Worklogs* de alcance total).
3. **Conta de envio de e-mail + senha de app**:
   - **Office 365**: `smtp.office365.com` / porta `587`. Requer *app password* (MFA) habilitado para a conta.
   - **Gmail**: `smtp.gmail.com` / `587` + senha de app (https://myaccount.google.com/apppasswords).

---

## Passo 1 — Repositório no GitHub
```bash
git init           # (já inicializado neste diretório)
git add .
git commit -m "dashboard SCUPDATA-OKR"
git branch -M main
git remote add origin https://github.com/<org>/<repo>.git
git push -u origin main
```

## Passo 2 — Conectar o AWS Amplify
1. AWS Console → **Amplify** → **Create new app** → **Host web app**.
2. Fonte: **GitHub** → autorize → selecione o repositório e o branch `main`.
3. O Amplify detecta o `amplify.yml`. Confirme e **Deploy**.
4. Ao final, copie a URL pública (ex.: `https://main.xxxxxxxx.amplifyapp.com`).

> A partir daí, **todo push** no `main` (inclusive os do robô semanal) dispara um novo deploy.

## Passo 3 — Secrets e variáveis no GitHub
Repo → **Settings → Secrets and variables → Actions**.

**Secrets** (criptografados):
| Nome | Valor |
|---|---|
| `JIRA_EMAIL` | seu e-mail Atlassian |
| `JIRA_API_TOKEN` | token do Jira |
| `TEMPO_TOKEN` | token do Tempo |
| `SMTP_HOST` | `smtp.office365.com` (ou `smtp.gmail.com`) |
| `SMTP_PORT` | `587` |
| `SMTP_USER` | conta de envio |
| `SMTP_PASS` | senha de app |
| `MAIL_FROM` | remetente (pode ser igual ao `SMTP_USER`) |
| `MAIL_TO` | destinatários separados por vírgula |

**Variables** (não-secretos):
| Nome | Valor |
|---|---|
| `DASHBOARD_URL` | a URL do Amplify do Passo 2 |
| `DASH_PERIOD_START` | (opcional) início do período de SDE/SDS — default `2026-04-01` |

## Passo 4 — Testar agora (sem esperar a segunda)
Repo → aba **Actions** → workflow **"Dashboard Semanal"** → **Run workflow**.
Confira: o dashboard é atualizado/commitado, o Amplify redeploya e o e-mail chega.

## Agenda
Cron `30 11 * * 1` = **segunda-feira 08:30** America/Sao_Paulo (11:30 UTC).
Para mudar dia/hora, edite o `cron` em `.github/workflows/weekly.yml` (sempre em UTC).

---

## Atualização manual (local)
Com as variáveis de ambiente definidas (`JIRA_EMAIL`, `JIRA_API_TOKEN`, `TEMPO_TOKEN`):
```powershell
python refresh_all.py            # puxa tudo e regenera dashboard.html/index.html
python send_email.py --dry-run   # gera email_preview.html (não envia)
```

## Observações
- **Período SDE/SDS**: só entram itens criados **ou** movimentados desde `DASH_PERIOD_START`. O SCUPOKR é mostrado completo.
- **Horas**: vêm do Tempo (autor real). Se o token do Tempo não enxergar todos os worklogs, o build complementa com o worklog nativo do Jira e o dashboard avisa.
- **Sem servidor ligado**: tudo roda no GitHub Actions sob demanda/cron. O Amplify só hospeda os arquivos estáticos versionados.
- O `dashboard_data.json`, `raw/` e demais intermediários são gerados no CI (estão no `.gitignore`); apenas `index.html`/`dashboard.html`/logo são versionados para o deploy inicial.
