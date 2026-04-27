# Project Analysis: RAG Cửa Hàng Phụ Tùng

## Overview

A Retrieval-Augmented Generation (RAG) chatbot for a motorbike parts store. Staff can query an AI assistant to look up products, prices, and compatibility. The system combines SQL search (structured product data) with a Vector DB (unstructured knowledge) to generate accurate answers via Google Gemini or Anthropic Claude.

**Stack:** FastAPI (Python) + Next.js (TypeScript) + SQLite + LlamaIndex Vector DB + Google Gemini LLM

**Hosting:** Render (backend) + Vercel (frontend)

---

## Implementation Phases

### Phase 0 — Core RAG System (Mar 20, 2026)
**Commit:** `8c4c926` — Initial commit

Built the foundational system from scratch:

- **Backend** (FastAPI):
  - `main.py` — REST API with `/api/chat` endpoint
  - `rag_engine.py` — RAG pipeline: SQL search → Vector search → LLM answer
  - `store.db` — SQLite with 50 seed products
  - `import_products.py` — CSV importer script
  - `seed_data.py` — Initial data seeder
- **Frontend** (Next.js):
  - Chat UI with message history and loading states
  - Hardcoded to `localhost:8000`
- **Embedding:** HuggingFace `sentence-transformers/all-MiniLM-L6-v2` (local, no API key)
- **LLM:** Google Gemini (primary) + Anthropic Claude (fallback)
- **RAG Flow:**
  1. Extract keywords from user query
  2. SQL LIKE search across product name, SKU, brand, category, notes
  3. Vector similarity search for knowledge/compatibility info
  4. Combine both contexts into a prompt → LLM generates answer

---

### Phase 1 — Knowledge Feedback Loop (Mar 22, 2026)
**PR #1:** `feature/knowledge_feedback_loop` → `cf2c865`

Added a full staff correction workflow so the AI learns from mistakes:

- **New API endpoints:**
  - `POST /api/knowledge/feedback` — Staff submits correction for a wrong AI answer
  - `GET /api/admin/knowledge/pending` — Admin lists pending feedback items
  - `POST /api/admin/knowledge/{id}/approve` — Approve → inserts knowledge into Vector DB
  - `POST /api/admin/knowledge/{id}/reject` — Reject with notes
- **Admin UI:** `/admin/knowledge-review` page for reviewing pending feedback
- **Frontend:** "Góp ý / Cập nhật" button on each AI response opens a correction modal
- **Database:** New `knowledge_feedbacks` table with status workflow (`pending` → `approved`/`rejected`)
- **Dynamic learning:** Approved corrections are inserted into the live LlamaIndex Vector DB

---

### Phase 2 — Project Structure Reorganization (Mar 22, 2026)
**Commits:** `86b5223`, `db273d8`

- Moved documentation into requirement-specific folders
- Restored and cleaned up the main `README.md`

---

### Phase 3 — Gradle Build Tool (PR #2, Mar 25, 2026)
**Commits:** `d08fa98` → `1758abd`

- Added Gradle as a unified build system (`build.gradle`, `gradlew`)
- Single command to start both backend and frontend
- Added `REQ-03` documentation

---

### Phase 4 — Cross-Platform Compatibility (PR #3, Mar 25, 2026)
**Commits:** `bd126b3` → `ce5265d`

- Setup scripts (`setup.sh`, `gradlew`) updated to run correctly on Linux, Mac, and Windows
- Path and shell differences handled

---

### Phase 5 — Free Hosting Deployment (Apr 10, 2026)
**Commits:** `211bc85` → `73efdce` (5 commits)

Migrated from local-only to cloud deployment on Render + Vercel:

| Commit | Change |
|--------|--------|
| `211bc85` | Add `Procfile` for Render, replace `localhost:8000` with `NEXT_PUBLIC_API_URL` env var |
| `b0b5c74` | Skip ESLint during Vercel production build |
| `af8b1d4` | Fix Render port binding — read `PORT` from environment |
| `2393952` | Replace HuggingFace/PyTorch embedding with lightweight Gemini REST API embedding (fixes Render 512MB OOM crash); make vector search fault-tolerant |
| `73efdce` | Trigger Vercel rebuild to bake in `NEXT_PUBLIC_API_URL` value |

**Key architectural change in this phase:**

Before (local):
```python
embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
```

After (deployed):
```python
class GeminiDirectEmbedding(BaseEmbedding):
    def _embed(self, text: str) -> List[float]:
        # Calls Google REST API directly — no PyTorch, no 2GB model download
        url = f"https://generativelanguage.googleapis.com/v1beta/models/embedding-001:embedContent?key={self.api_key}"
        ...
```

---

---

### Phase 6 — Production Bug Fixes (Apr 27, 2026)
**Commits:** `2ea4341`, `94553f5`

Diagnosed and fixed two bugs causing the deployed AI to answer incorrectly while local worked fine.

#### Bug 1 — Deployed Database Had Only 50 Products

**Root cause:** The `store.db` in git was created by `seed_data.py` with only 50 hardcoded products. Locally, `import_products.py` had been run against `products.csv` (933 products) but neither the updated DB nor the CSV was ever committed. Render deployed the old 50-product DB → SQL search found almost nothing → AI gave wrong or generic answers.

**Diagnosis:**
```
State                   | Products | Source
------------------------|----------|-----------------------------
git / Render (deployed) | 50       | seed_data.py (Mar 20)
Local machine           | 891      | import_products.py + products.csv
```

**Fix applied (`2ea4341`):**
- Fixed a crash in `import_products.py`: `SL_Toi_Thieu` column stores floats like `"5.0"` but the script called `int()` directly → changed to `int(float(...))`
- Ran the importer locally → `store.db` grew from 36 KB (50 products) to 151 KB (891 products)
- Committed updated `store.db` and full `products.csv` to git
- Updated `backend/Procfile` to auto-import on every Render deploy:
  ```
  web: python import_products.py && python main.py
  ```
- Added `frontend/vercel.json` with explicit Next.js build config

#### Bug 2 — Keyword Extraction Cut Off SKUs and Matched Wrong Products

**Root cause:** Two bugs in `extract_keywords_from_query` in `rag_engine.py`:

1. **`[:5]` hard limit**: The full query string was inserted at index 0, pushing all actual keywords down. For a query like *"giá và tên của sản phẩm HD-008"*, the word `hd-008` ended up at index 6 — silently dropped. The SQL loop never tried it.

2. **Missing accented stopwords**: Common Vietnamese question words with accents (`giá`, `sản`, `phẩm`, `của`, `tên`) were not in the stopwords set (which only had unaccented forms). These survived filtering, were tried first in the SQL LIKE loop, accidentally matched unrelated products (e.g. the SIM product), and caused the loop to `break` early with a wrong result.

**Example of the failure:**

| Query | Keywords tried (old) | First SQL match |
|---|---|---|
| "giá và tên của sản phẩm HD-008" | `[full_query, 'giá', 'tên', 'của', 'sản']` | wrong product via `'sản'` |
| "Rùa đen bóng có gon Future Neo 2005" | `[full_query, 'sản', 'phẩm', 'giá', 'của']` | wrong product via `'sản'` |

**Fix applied (`94553f5`):**
- Added accented Vietnamese filler/question words to the stopwords set
- Removed the `[:5]` cap entirely
- Removed the full query from the keyword list (it never matches a LIKE search usefully)
- Sorted keywords by **length descending** — longer words (SKUs, model names) are tried first

**Example after fix:**

| Query | Keywords tried (new) | First SQL match |
|---|---|---|
| "giá và tên của sản phẩm HD-008" | `['hd-008']` | HD-008 → Ma phanh truoc PCX, 180,000 VND ✓ |
| "Rùa đen bóng có gon Future Neo 2005" | `['future', 'bóng', '2005', 'rùa', ...]` | Future Neo products → SKU `83600KYL700ZD`, 85,000 VND ✓ |

**Code change summary:**

```python
# Before
stopwords = { 'cho', 'toi', ... }  # unaccented only
keywords.insert(0, query.strip())   # full query at index 0
return keywords[:5]                 # SKUs at position 6+ silently dropped

# After
stopwords = { 'cho', 'toi', ..., 'và', 'của', 'sản', 'phẩm', 'giá', 'tên', ... }
keywords.sort(key=len, reverse=True)  # longest (most specific) first
return keywords if keywords else [query.strip()]  # no cap, no full-query pollution
```

#### Environment Variable Config (already in place, confirmed)

`NEXT_PUBLIC_API_URL` was already set correctly in Vercel dashboard (`https://rag-cua-hang-phu-tung.onrender.com`) for All Environments before the Phase 5 rebuild. No action needed.

Render environment variables required:
```
GOOGLE_API_KEY=<set in Render dashboard>
ANTHROPIC_API_KEY=<set in Render dashboard, optional>
PORT=<set automatically by Render>
```

---

## Architecture Diagram

```
[User Browser]
     │
     ▼
[Vercel — Next.js Frontend]
  - Chat UI
  - Feedback modal
  - Admin review page
     │
     │ NEXT_PUBLIC_API_URL (must be set at build time)
     ▼
[Render — FastAPI Backend]
  - /api/chat
  - /api/knowledge/feedback
  - /api/admin/knowledge/*
     │
     ├──► [SQLite store.db]
     │      Products table (50 seeded / 933 from CSV)
     │      knowledge_feedbacks table
     │
     ├──► [LlamaIndex Vector DB]
     │      ./database/storage/*.json
     │      Embedding: Gemini REST API
     │
     └──► [Google Gemini API]
            LLM: gemini-2.5-flash-lite
            Embedding: embedding-001
```

---

*Generated: 2026-04-26 | Updated: 2026-04-27*
