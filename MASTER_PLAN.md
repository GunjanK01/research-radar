# Research Radar — Master Plan

One-stop overview of the entire project: what it is, why it's built this way, and how it
gets executed. (Companion docs — PROJECT_BRIEF.md, ARCHITECTURE.md, DECISIONS_LOG.md,
SESSION_HANDOFF.md, TASKS.md — go deeper on each piece; this is the map that ties them together.)

---

## 1. What this is

A take-home assignment ("Research Radar") for the **Full Stack / Platform Engineer** role at
ANRF AI PMU, IIIT Hyderabad — for the Master Platform for Indian Research and Innovation
(Anumapi), with Saral AI as secondary loading.

**In one line:** a research paper search tool — pull real papers into Postgres, expose a
search/filter API, put a usable Next.js UI on top, and add one AI feature (semantic
"find similar papers") that shows platform engineering depth rather than just LLM prompting.

**Applicant context:** fresher, applied with SOP against a 3+ yrs JD, got the assessment
anyway — this project is the chance to prove capability outweighs years-on-paper.

## 2. Timeline
- Assignment received: Aug 6, 2026, 4pm
- Window: 10–14 days → hard deadline **Aug 20, 4pm**
- Target: submit **Aug 19 morning**, leaving buffer before the hard cutoff
- Working days: Aug 15 (today) through Aug 19

## 3. What we're building — the four pieces

| Piece | What it does | Why it's graded on |
|---|---|---|
| **Ingestion** | Idempotent script pulling 300–500 papers from OpenAlex across 2 topics into Postgres | Re-runnable without duplicates; no raw data committed to repo |
| **Backend API** | FastAPI service: search/filter/paginate papers, get full paper detail, get similar papers | Data modelling (schema) + API design quality |
| **Frontend** | Next.js: search page (debounced, filtered, paginated) + detail page (metadata + similar papers) | Usable without instructions, not visual polish |
| **AI feature** | Embedding-based "find 5 similar papers," powered by local sentence-transformers + pgvector, zero external API key | Sensible approach, honest about limitations, ties directly to JD's "vector search" skill |

All four pieces come up together with a single `docker compose up`, in under 10 minutes,
from a clean clone — this is the first thing the evaluator checks, and everything else is
secondary to getting this right.

## 4. Why it's built this way (the throughline)

The JD is explicit that this role is **systems/platform engineering, not GenAI research**:
LLM/embedding integration matters, but "depth in LLM internals is not the focus." Every major
technical choice below traces back to that one sentence:

- **Similarity search over summarization** — a real data/systems problem (embeddings,
  vector storage, indexed similarity query), not a thin prompt-and-display wrapper.
- **Local embeddings (sentence-transformers), not an LLM API** — removes any external
  dependency from the Docker demo; the evaluator's clone-and-run never depends on an API key
  or a third-party service being up.
- **Postgres full-text search over Elasticsearch** — the assignment explicitly rewards scope
  control; a 4th service for 300–500 rows would be over-engineering, not impressive engineering.
- **No bonus features (deploy/CI/CD/auth)** — not in the scored evaluation order; time goes
  into the six things that are.

## 5. Stack, at a glance
Next.js (frontend) · FastAPI (backend) · PostgreSQL + pgvector (data + vectors) · Alembic
(migrations) · sentence-transformers `all-MiniLM-L6-v2` (embeddings, local) · Docker Compose
(orchestration). Full detail, folder structure, and data models are in ARCHITECTURE.md.

## 6. Execution roadmap
```
Phase 0  Setup                → repo, folders, Postgres+pgvector running locally
Phase 1  Schema + migrations  → papers/authors/topics tables, Alembic
Phase 2  Ingestion            → OpenAlex script, idempotent upsert, 300-500 papers
Phase 3  Backend API          → search/filter/paginate, detail endpoint, tests
Phase 4  Dockerize            → do this EARLY (day 3, not day 5) — riskiest step for a
                                 Docker newcomer, needs slack time
Phase 5  AI feature           → embeddings generated, pgvector column, /similar endpoint
Phase 6  Frontend             → search + detail pages, debounce, empty/loading/error states
Phase 7  Polish + submission  → README, git log cleanup, screen recording
```
Suggested day mapping (flexible, not rigid):
Aug 15 → Phase 0–1 · Aug 16 → Phase 2–3 · Aug 17 → Phase 4 · Aug 18 → Phase 5–6 · Aug 19 → Phase 6–7

## 7. What "done and good" looks like
Mapped directly to how they say they'll evaluate, in order:
1. **Runs end-to-end** — clean clone, `docker compose up`, works within 10 min, no manual steps
2. **Data modelling + API design** — schema reflects real relationships (papers↔authors↔topics),
   not a flat table; endpoints follow REST conventions cleanly
3. **Code quality** — organized by concern (models/schemas/routers/services), not one big file
4. **AI feature** — similarity results look sensible on spot-checked papers, README is upfront
   about what it does and doesn't do well (e.g. no reranking, no citation-graph awareness)
5. **Frontend usability** — a stranger could search, filter, and open a paper with zero guidance
6. **README + communication** — decisions and tradeoffs explained, not just a setup guide

## 8. What we're explicitly NOT doing (and why that's fine)
- Deployment / live URL — bonus only, not in the scored list
- CI/CD, auth, caching — bonus only
- Elasticsearch/Typesense — disproportionate for corpus size, scope-control risk
- Full test coverage — spec asks for "a few tests where they matter most," not exhaustive suites
- Reviewer suggestion / summarize-and-simplify features — one feature done well beats three
  done halfway (spec's own words)

## 9. Where things stand right now
See **SESSION_HANDOFF.md** for the live status and **TASKS.md** for the checklist. As of this
writing: planning complete, Phase 0 about to start, two OpenAlex topics still need to be
finalized (DECISIONS_LOG D005).
