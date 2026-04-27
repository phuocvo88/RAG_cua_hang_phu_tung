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

## Bug: AI Answers Correctly Locally but Not on Vercel/Render

### Root Cause 1 — Deployed Database Has Only 50 Products

The `store.db` committed to git was created during Phase 0 seeding with only **50 products**. Locally, `import_products.py` was run against `products.csv` which has **933 products** — but neither the updated `store.db` nor the new `products.csv` was committed.

```
State                  | Products | Source
-----------------------|----------|---------------------------
git / Render (deployed)| 50       | seed_data.py (Mar 20)
Local machine          | 933+     | import_products.py + products.csv
```

When Render deploys, it uses the git version of `store.db`. SQL search finds almost nothing → AI has no product data → answers are generic or wrong.

**Evidence:**
```bash
# What's in git
git ls-files backend/database/
# → backend/database/store.db  (36KB, 50 products)

# Local products.csv
wc -l products.csv
# → 934 lines (header + 933 products)  ← modified, NOT committed
```

### Root Cause 2 — `NEXT_PUBLIC_API_URL` Not Baked In at Build Time

Next.js embeds `NEXT_PUBLIC_*` environment variables **at build time**, not at runtime. If Vercel built the frontend before the env var was configured in the Vercel dashboard, the variable is `undefined` and the code falls back to:

```typescript
const response = await fetch(
  `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/chat`
);
```

From the browser on Vercel, `http://localhost:8000` is unreachable — requests fail silently or throw a network error. The AI is never actually called.

The commit `73efdce` ("Trigger Vercel rebuild to apply NEXT_PUBLIC_API_URL env var") confirms this was discovered, but a rebuild only works if the env var was already set in the Vercel dashboard before that build.

---

## Fixes Required

### Fix 1 — Sync the Product Database

**Option A — Commit the updated database (quick fix):**
```bash
# Run the importer locally first if not done yet
cd backend && python import_products.py

# Then commit both the DB and the CSV
git add backend/database/store.db products.csv
git commit -m "Update product catalog: import 933 products from CSV"
git push
```

**Option B — Auto-import on startup (recommended for production):**

Edit `backend/Procfile`:
```
web: python import_products.py && python main.py
```

This ensures the DB is always populated from the CSV on each Render deploy, even if the DB file gets reset.

### Fix 2 — Verify Vercel Environment Variable

1. Go to Vercel dashboard → Project → **Settings** → **Environment Variables**
2. Confirm `NEXT_PUBLIC_API_URL` is set to your Render backend URL:
   ```
   NEXT_PUBLIC_API_URL=https://your-app-name.onrender.com
   ```
3. **Redeploy** (not just rebuild) from the Vercel dashboard to bake the value in

### Fix 3 — Verify Render Environment Variables

Confirm these are set in Render dashboard → Environment:
```
GOOGLE_API_KEY=your_google_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key  (if using Claude)
PORT=8000  (Render sets this automatically)
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

*Generated: 2026-04-26*
