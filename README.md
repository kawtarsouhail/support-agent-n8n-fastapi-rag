# Agent de triage support client avec RAG

Agent IA qui classe les messages clients, cherche une réponse dans une base
de connaissances (RAG), décide de répondre automatiquement ou d'escalader
vers un humain — avec validation et alertes en temps réel.

### Workflow Scenarios

#### 1. Réponse automatique depuis la FAQ

Lorsque la question du client concerne un sujet couvert par notre FAQ, n8n récupère les informations pertinentes et génère directement une réponse au client.

![Workflow — Réponse automatique depuis la FAQ](docs/workflow1.png)

#### 2. Escalade vers le support humain

Lorsque le message du client est identifié comme urgent, n8n déclenche une escalade directe vers le support humain afin qu'un membre de l'équipe puisse prendre en charge la demande.

![Workflow — Escalade vers le support humain](docs/workflow2.png)

#### 3. Question hors sujet

Lorsque la question du client n'a aucun rapport avec l'activité de l'entreprise, le système l'identifie comme une demande hors sujet et applique le traitement prévu pour ce type de message.

![Workflow — Question hors sujet](docs/workflow3.png)


## Stack
- n8n (orchestration)
- FastAPI + sentence-transformers (micro-service RAG)
- PostgreSQL + pgvector, hébergé sur Supabase (base vectorielle + logs)
- Groq (Llama 3.3) — classification et génération
- Telegram Bot API (escalade et validation humaine)

## Résultats
| action            | count |
| ----------------- | ----- |
| escalade_urgence  | 1     |
| escalade_hors_faq | 2     |
| reponse_directe   | 3     |

## Installation
1. `cd python && pip install -r requirements.txt`
2. Copier `.env.example` en `.env`, remplir les vraies valeurs
3. `python3 ingest.py`
4. `python3 -m uvicorn main:app --port 8000`
5. `cd n8n && docker compose up -d`
6. Importer `n8n/workflow.json` dans n8n, reconnecter les credentials

## Limites connues
- FAQ volontairement réduite (~20 entrées) pour rester démonstratif
- Pas d'authentification utilisateur (usage interne)
