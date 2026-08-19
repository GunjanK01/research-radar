# Research Radar — Project Brief

## Context
Take-home assignment for **Full Stack / Platform Engineer** role, ANRF AI PMU (IIIT Hyderabad),
for the "Master Platform for Indian Research and Innovation" initiative (Anumapi), secondary
loading on Saral AI integration.

- Received: Aug 6, 2026, ~4pm
- Window given: 10–14 days → hard deadline **Aug 20, 4pm**
- Target submission: **Aug 19, morning** (buffer before hard cutoff)
- Applicant status: fresher, applied with SOP/cover letter despite 3+ yrs stated requirement

## Why this task matters for the role
JD explicitly frames the role as **systems design / platform-building, not GenAI research**:
> "Where GenAI features are needed (search ranking, summarisation), integrate existing models
> and APIs cleanly — depth in LLM internals is not the focus."

Good-to-haves called out directly: search infrastructure / **vector search**, working with
scholarly metadata, LLM/embedding API integration. This brief and the architecture doc are
built to demonstrate exactly those things.

## Scope decisions (locked)
| Area | Decision | Why |
|---|---|---|
| Data source | OpenAlex API | Free, no key, richer metadata than arXiv |
| Topics | 2 (to be finalized) | e.g. computer vision, NLP |
| Part 3 AI feature | **Find similar papers** (not summarize, not reviewer suggestion) | Matches "vector search" / "systems problem wearing an AI hat" — see DECISIONS_LOG |
| Embedding approach | sentence-transformers (`all-MiniLM-L6-v2`), local, no API key | Zero external AI dependency at runtime; robust for evaluator's `docker compose up` |
| Similarity storage/query | Postgres + pgvector | Directly demonstrates the JD's vector search good-to-have |
| Keyword search | Postgres full-text search (`tsvector`) | Avoids over-scoping with Elasticsearch; "do not gold plate" |
| Backend | FastAPI + Alembic migrations | Matches JD stack explicitly |
| Frontend | Next.js | Matches JD stack explicitly |
| Bonus (deploy/CI/CD/auth) | **Skipped** | Not in the scored evaluation order; time better spent on core quality |

## Evaluation order (their stated priority — build and polish in this order)
1. Does it run end-to-end (`docker compose up`, <10 min)
2. Data modelling and API design
3. Code quality and structure
4. AI feature — sensible approach, honest about limitations
5. Frontend usability
6. README and communication

## Non-negotiable traps to avoid
- No raw data dumps committed to repo (ingestion script only, data lives in Postgres)
- No hand-created tables — every table via Alembic migration
- Debounced search input on frontend
- No single giant "final commit" — commit per logical phase
- Model weights baked into Docker image at **build time**, not downloaded at request time
- Explain every assumption in the README, not in a pre-approval email

## Deliverables
- Public (or access-granted private) GitHub repo
- 2–5 min screen recording walking through the app + one design decision
- README: setup, design decisions, tradeoffs, "what's next with more time"
