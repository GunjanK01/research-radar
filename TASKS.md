# Tasks Checklist

Mapped to phases in ARCHITECTURE.md. Check off as you go — this is the quick-scan companion
to SESSION_HANDOFF.md's narrative summary.

## Phase 0 — Setup
- [x] Repo initialized, `.gitignore` added
- [x] Folder structure scaffolded (backend/, frontend/)
- [x] Postgres + pgvector running locally
- [x] 2 OpenAlex topics finalized (DECISIONS_LOG D005) — Large Language Models + Computer Vision

## Phase 1 — Schema + migrations
- [x] `papers`, `authors`, `topics`, join tables designed
- [x] Alembic initialized
- [x] First migration applied (tested upgrade + downgrade against real Postgres+pgvector)
- [x] Commit made (branch: phase-1-schema-migrations, not yet merged to main)

## Phase 2 — Ingestion
- [ ] OpenAlex fetch script written
- [ ] Idempotent upsert logic (on openalex_work_id)
- [ ] 300–500 papers loaded across 2 topics
- [ ] Re-run tested for idempotency
- [ ] Commit made

## Phase 3 — Backend API
- [ ] `GET /papers` — pagination
- [ ] `GET /papers` — keyword search (title/abstract)
- [ ] `GET /papers` — filters (year, topic, author)
- [ ] `GET /papers/{id}` — full detail with authors/metadata
- [ ] Tests for both endpoints
- [ ] Commit made

## Phase 4 — Dockerize
- [ ] Backend Dockerfile (model baked in at build time)
- [ ] Frontend Dockerfile
- [ ] docker-compose.yml wiring db/backend/frontend
- [ ] Clean-clone `docker compose up` validated end-to-end, timed (<10 min)
- [ ] Commit made

## Phase 5 — AI feature (similar papers)
- [ ] Embeddings generated for all abstracts
- [ ] `vector` column populated via pgvector
- [ ] `GET /papers/{id}/similar` implemented
- [ ] Verified results look sensible for a few sample papers
- [ ] Commit made

## Phase 6 — Frontend
- [ ] Search page: box + filters + pagination
- [ ] Debounced search input
- [ ] Detail page: metadata + authors
- [ ] Similar papers shown on detail page
- [ ] Empty states handled
- [ ] Loading states handled
- [ ] API error states handled
- [ ] Commit(s) made

## Phase 7 — Polish & submission
- [ ] README written (setup, decisions, tradeoffs, next steps)
- [ ] Git history reviewed for meaningful commit messages
- [ ] Screen recording (2–5 min) done
- [ ] Repo visibility/access confirmed (public or access granted)
- [ ] Final submission sent
