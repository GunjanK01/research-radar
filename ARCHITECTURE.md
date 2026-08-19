# Research Radar — Architecture & Execution Plan

## Stack
| Layer | Choice | Notes |
|---|---|---|
| Frontend | Next.js (App Router), TypeScript | Search page + detail page |
| Backend | FastAPI (Python) | REST API, async |
| DB | PostgreSQL 16 + `pgvector` extension | Relational data + embeddings in one place |
| Migrations | Alembic | No hand-created tables |
| Embeddings | sentence-transformers `all-MiniLM-L6-v2` | Local, no API key, baked into image at build |
| Ingestion source | OpenAlex API | Free, no key |
| Containerization | Docker + Docker Compose | 3 services: db, backend, frontend |
| Hosting | None (local `docker compose up` only) — bonus, skipped | Time budget prioritizes core |

## Phased execution plan

### Phase 0 — Setup (today)
- Repo init, `.gitignore`, base folder structure
- Postgres + pgvector running (locally first, Docker later) to de-risk early
- Confirm 2 topics for OpenAlex query

### Phase 1 — Schema + migrations
- Design `papers`, `authors`, `topics`, join tables
- Alembic init, first migration
- Commit: "Initial schema and migrations"

### Phase 2 — Ingestion
- OpenAlex fetch script, idempotent upsert (on OpenAlex work ID)
- 300–500 papers across 2 topics
- Commit: "OpenAlex ingestion script"

### Phase 3 — Backend API
- `GET /papers` — pagination, keyword search (tsvector), filters (year/topic/author)
- `GET /papers/{id}` — full detail
- Basic tests on these two endpoints
- Commit: "Papers API with search, filters, pagination"

### Phase 4 — Dockerize (do this early, not last)
- Dockerfile (backend), Dockerfile (frontend), docker-compose.yml
- Bake sentence-transformers model into backend image at build time
- Validate full `docker compose up` from a clean clone
- Commit: "Docker Compose setup"

### Phase 5 — AI feature: similar papers
- Generate embeddings for all abstracts on ingestion
- Store as `vector` column via pgvector
- `GET /papers/{id}/similar` — cosine distance top 5
- Commit: "Similarity search via pgvector embeddings"

### Phase 6 — Frontend
- Search page: box, filters, pagination, debounced input
- Detail page: metadata + similar papers list
- Empty / loading / error states throughout
- Commit(s): "Search page", "Detail page + similar papers UI", "Loading/empty/error states"

### Phase 7 — Polish & submission
- README (setup, decisions, tradeoffs, next steps)
- Final pass on git history / commit messages
- Screen recording
- Commit: "README and final polish"

## Folder structure
```
research-radar/
├── docker-compose.yml
├── README.md
├── PROJECT_BRIEF.md
├── DECISIONS_LOG.md
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── alembic/
│   │   ├── versions/
│   │   └── env.py
│   ├── alembic.ini
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── db.py
│   │   ├── models/          # SQLAlchemy models
│   │   │   ├── paper.py
│   │   │   ├── author.py
│   │   │   └── topic.py
│   │   ├── schemas/         # Pydantic response/request models
│   │   ├── routers/
│   │   │   └── papers.py
│   │   ├── services/
│   │   │   ├── search.py
│   │   │   └── similarity.py
│   │   └── ml/
│   │       └── embeddings.py
│   ├── scripts/
│   │   └── ingest_openalex.py
│   └── tests/
│       └── test_papers_api.py
└── frontend/
    ├── Dockerfile
    ├── package.json
    ├── app/
    │   ├── page.tsx              # search page
    │   └── papers/[id]/page.tsx  # detail page
    ├── components/
    │   ├── SearchBar.tsx
    │   ├── FilterPanel.tsx
    │   ├── PaperCard.tsx
    │   └── SimilarPapers.tsx
    └── lib/
        └── api.ts
```

## Core data models
```
authors
  id (pk)
  openalex_author_id (unique)
  name

topics
  id (pk)
  name (unique)

papers
  id (pk)
  openalex_work_id (unique)   -- idempotency key
  title
  abstract
  year
  embedding (vector(384))     -- all-MiniLM-L6-v2 output dim
  created_at

paper_authors  (join table)
  paper_id (fk)
  author_id (fk)
  author_position

paper_topics  (join table)
  paper_id (fk)
  topic_id (fk)
```
Indexes: full-text index on `papers.title || papers.abstract`; ivfflat/hnsw index on `embedding`
for pgvector similarity performance; index on `papers.year`.

## Key flows
**Search flow:** frontend debounces input → `GET /papers?q=&year=&topic=&author=&page=` →
Postgres full-text query + filters → paginated JSON → rendered as result cards.

**Detail flow:** frontend loads `/papers/{id}` → full metadata + authors → in parallel,
`/papers/{id}/similar` → 5 nearest neighbors by embedding cosine distance → rendered below.

**Ingestion flow (offline, run before submission):** script queries OpenAlex for 2 topics →
upserts into `papers`/`authors`/`topics` on natural keys → generates embedding per abstract →
writes to `embedding` column. Re-running is safe (upsert, not insert).
