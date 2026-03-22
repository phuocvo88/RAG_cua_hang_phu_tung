# RAG Motorcycle Parts Shop - Architecture Overview

**Version:** 1.0
**Last Updated:** March 9, 2026
**Status:** Active Development

---

## 🏗️ System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                             │
│  ┌──────────────────────┐       ┌──────────────────────────┐   │
│  │   Next.js Frontend   │       │   Mobile App (Future)    │   │
│  │   - Chat Interface   │       │   - iOS/Android          │   │
│  │   - Product Display  │       │   - React Native         │   │
│  └──────────┬───────────┘       └──────────┬───────────────┘   │
└─────────────┼──────────────────────────────┼───────────────────┘
              │                              │
              │  HTTP/REST API               │
              │                              │
┌─────────────┼──────────────────────────────┼───────────────────┐
│             │      APPLICATION LAYER       │                   │
│  ┌──────────▼──────────────────────────────▼──────────┐       │
│  │            FastAPI Backend Server                   │       │
│  │  ┌────────────────────────────────────────────┐    │       │
│  │  │         /api/chat Endpoint                 │    │       │
│  │  │  - Request validation (Pydantic)           │    │       │
│  │  │  - CORS middleware                         │    │       │
│  │  │  - Error handling                          │    │       │
│  │  └────────────────┬───────────────────────────┘    │       │
│  └───────────────────┼────────────────────────────────┘       │
└────────────────────────┼──────────────────────────────────────┘
                        │
┌────────────────────────┼──────────────────────────────────────┐
│                        │   RAG ENGINE LAYER                    │
│  ┌────────────────────▼───────────────────────────────────┐  │
│  │              query_rag_system()                        │  │
│  │  ┌──────────────────────────────────────────────────┐ │  │
│  │  │  1. Keyword Extraction                           │ │  │
│  │  │     - extract_keywords_from_query()              │ │  │
│  │  │     - Vietnamese stopword filtering              │ │  │
│  │  └──────────────────────────────────────────────────┘ │  │
│  │  ┌──────────────────────────────────────────────────┐ │  │
│  │  │  2. SQL Search (Structured Data)                 │ │  │
│  │  │     - search_sql_by_keyword()                    │ │  │
│  │  │     - Multi-field search                         │ │  │
│  │  └──────────────────────────────────────────────────┘ │  │
│  │  ┌──────────────────────────────────────────────────┐ │  │
│  │  │  3. Vector Search (Unstructured Knowledge)       │ │  │
│  │  │     - search_knowledge()                         │ │  │
│  │  │     - LlamaIndex retriever                       │ │  │
│  │  └──────────────────────────────────────────────────┘ │  │
│  │  ┌──────────────────────────────────────────────────┐ │  │
│  │  │  4. Context Fusion & Prompt Building             │ │  │
│  │  │     - Combine SQL + Vector results               │ │  │
│  │  │     - System instruction template                │ │  │
│  │  └──────────────────────────────────────────────────┘ │  │
│  │  ┌──────────────────────────────────────────────────┐ │  │
│  │  │  5. LLM Inference                                │ │  │
│  │  │     - Google Gemini (primary)                    │ │  │
│  │  │     - Claude (fallback)                          │ │  │
│  │  └──────────────────────────────────────────────────┘ │  │
│  └────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────┘
                        │
┌────────────────────────┼──────────────────────────────────────┐
│                        │      DATA LAYER                       │
│  ┌─────────────────────▼──────────────┐  ┌──────────────────┐ │
│  │     SQLite Database                │  │   Vector Store   │ │
│  │  ┌──────────────────────────────┐  │  │  (LlamaIndex)    │ │
│  │  │  products Table              │  │  │                  │ │
│  │  │  - sku, name, brand          │  │  │  Knowledge Base  │ │
│  │  │  - category, price           │  │  │  - Compatibility │ │
│  │  │  - in_stock, promotion       │  │  │  - Guides        │ │
│  │  │  - warranty, notes           │  │  │  - Tips          │ │
│  │  └──────────────────────────────┘  │  │                  │ │
│  └─────────────────────────────────────┘  └──────────────────┘ │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │            Embedding Model (Local)                      │  │
│  │  - HuggingFace: sentence-transformers/all-MiniLM-L6-v2 │  │
│  │  - Runs locally (no API cost)                          │  │
│  └─────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────┐
│                      EXTERNAL SERVICES                          │
│  ┌──────────────────────┐       ┌──────────────────────────┐  │
│  │   Google Gemini API  │       │   Anthropic Claude API   │  │
│  │   - gemini-2.5-flash │       │   - claude-3-5-sonnet    │  │
│  │   - Primary LLM      │       │   - Fallback LLM         │  │
│  └──────────────────────┘       └──────────────────────────┘  │
└────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Data Flow

### Request Processing Flow

```
1. User Query
   └─> "Tim phuoc cho xe Yamaha NVX"

2. API Endpoint (/api/chat)
   └─> Validate request (Pydantic)
   └─> Extract message: "Tim phuoc cho xe Yamaha NVX"

3. RAG Engine (query_rag_system)
   │
   ├─> 3a. Keyword Extraction
   │   └─> Keywords: ["Tim phuoc cho xe Yamaha NVX", "phuoc", "yamaha", "nvx"]
   │
   ├─> 3b. SQL Search
   │   └─> Query: SELECT * FROM products WHERE name LIKE '%phuoc%'
   │   └─> Result: "YM-002: Phuoc binh dau NVX, 3,200,000 VND, KM: 10%"
   │
   ├─> 3c. Vector Search
   │   └─> Embed query: [0.12, -0.45, 0.78, ...]
   │   └─> Similarity search in knowledge base
   │   └─> Result: "Phuoc NVX tuong thich voi NVX 125/155..."
   │
   ├─> 3d. Context Fusion
   │   └─> Combine: SQL results + Vector knowledge
   │   └─> Build prompt with system instruction
   │
   └─> 3e. LLM Inference (Gemini)
       └─> Generate Vietnamese response
       └─> "Phuoc binh dau NVX [Yamaha] - YM-002..."

4. API Response
   └─> Return JSON: {"reply": "Phuoc binh dau NVX...", "source": "..."}

5. Frontend Display
   └─> Render message in chat interface
```

---

## 🧩 Component Details

### 1. Frontend Layer (Planned)

**Technology:** Next.js 14 + React + Tailwind CSS

**Components:**
```
src/
├── app/
│   ├── page.tsx              # Main chat page
│   ├── layout.tsx            # Root layout
│   └── api/                  # API routes (optional)
├── components/
│   ├── ChatInterface.tsx     # Main chat component
│   ├── MessageList.tsx       # Message display
│   ├── MessageInput.tsx      # User input field
│   ├── ProductCard.tsx       # Product display
│   └── LoadingSpinner.tsx    # Loading state
├── lib/
│   └── api.ts                # Backend API client
└── styles/
    └── globals.css           # Global styles
```

**Features:**
- Real-time message rendering
- Auto-scroll to latest message
- Loading states
- Error handling
- Responsive design (mobile/desktop)

---

### 2. Backend API Layer

**Technology:** FastAPI + Pydantic + Python 3.11

**File Structure:**
```
backend/
├── main.py                   # FastAPI server
├── rag_engine.py             # RAG core logic
├── models.py                 # Pydantic models (future)
├── database/
│   ├── store.db              # SQLite database
│   └── storage/              # Vector store
└── utils/
    └── logger.py             # Logging (future)
```

**API Endpoints:**
```python
GET  /                        # Health check
POST /api/chat                # Main chat endpoint
  Request:  {"message": "string"}
  Response: {"reply": "string", "source": "string"}

# Future endpoints
GET  /api/products            # List all products
GET  /api/products/{sku}      # Get product details
GET  /api/categories          # List categories
```

**CORS Configuration:**
```python
allow_origins = ["http://localhost:3000"]  # Next.js dev server
allow_methods = ["GET", "POST"]
allow_headers = ["*"]
```

---

### 3. RAG Engine Layer

**Core Functions:**

#### 3.1 Keyword Extraction
```python
def extract_keywords_from_query(query: str) -> list:
    """
    Input:  "Tim phuoc cho xe Yamaha NVX"
    Output: ["Tim phuoc cho xe Yamaha NVX", "phuoc", "yamaha", "nvx"]

    Algorithm:
    1. Normalize to lowercase
    2. Split by whitespace
    3. Filter stopwords (cho, toi, ve, etc.)
    4. Filter short words (len < 3)
    5. Return top 5 keywords
    """
```

#### 3.2 SQL Search
```python
def search_sql_by_keyword(keyword: str, limit: int = 10) -> str:
    """
    Input:  keyword="phuoc", limit=10
    Output: Formatted product list

    SQL Query:
    SELECT sku, name, brand, category, price, in_stock,
           promotion, warranty, notes
    FROM products
    WHERE name LIKE '%phuoc%'
       OR sku LIKE '%phuoc%'
       OR category LIKE '%phuoc%'
       OR brand LIKE '%phuoc%'
       OR notes LIKE '%phuoc%'
    ORDER BY in_stock DESC, price ASC
    LIMIT 10
    """
```

#### 3.3 Vector Search
```python
def search_knowledge(query: str) -> str:
    """
    Input:  "phuoc NVX"
    Output: Retrieved knowledge text

    Process:
    1. Load index from storage
    2. Create retriever (top_k=3)
    3. Embed query using HuggingFace model
    4. Retrieve top 3 similar documents
    5. Concatenate text results
    """
```

#### 3.4 LLM Inference
```python
def query_rag_system(user_query: str, provider: str = "google") -> str:
    """
    Input:  user_query="Tim phuoc NVX", provider="google"
    Output: AI-generated Vietnamese response

    Providers:
    - "google": Gemini 2.5 Flash (default)
    - "anthropic": Claude 3.5 Sonnet (fallback)

    Prompt Template:
    System: "Ban la tro ly tu van phu tung..."
    User: "Cau hoi: {user_query}
           Du lieu SQL: {sql_context}
           Kien thuc: {knowledge_context}"
    """
```

---

### 4. Data Layer

#### 4.1 SQLite Database

**Schema:**
```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sku TEXT UNIQUE NOT NULL,           -- HD-001, YM-002
    name TEXT NOT NULL,                  -- "Phuoc binh dau NVX"
    brand TEXT,                          -- "Yamaha", "Honda"
    category TEXT,                       -- "He thong treo"
    price INTEGER NOT NULL,              -- 3200000 (VND)
    in_stock BOOLEAN NOT NULL,           -- TRUE/FALSE
    promotion TEXT,                      -- "Giam 10%", "Free lap"
    warranty TEXT,                       -- "12 thang", "6 thang"
    min_quantity INTEGER,                -- 1, 2, 5
    notes TEXT                           -- Technical details
);

-- Indexes for performance
CREATE INDEX idx_name ON products(name);
CREATE INDEX idx_brand ON products(brand);
CREATE INDEX idx_category ON products(category);
CREATE INDEX idx_sku ON products(sku);
```

**Sample Data:**
```
sku: YM-002
name: Phuoc binh dau NVX
brand: Yamaha
category: He thong treo
price: 3200000
in_stock: TRUE
promotion: Giam 10%
warranty: 12 thang
min_quantity: 1
notes: Phu hop cho NVX 125 va NVX 155, cong nghe piston kep
```

#### 4.2 Vector Database

**Storage Format:** LlamaIndex SimpleVectorStore (JSON)

**Files:**
```
database/storage/
├── docstore.json              # Document metadata
├── index_store.json           # Index configuration
├── vector_store.json          # Vector embeddings
└── graph_store.json           # Graph relationships
```

**Knowledge Documents:**
```python
[
    "Kính chiếu hậu xe Honda Airblade đời 2018 hoàn toàn có thể
     dùng cho xe Honda Airblade 2020 hoặc 2021 vì chúng dùng chung
     1 loại ngàm vặn chân 10 ly răng thuận...",

    "Lốp xe số kích thước 90/90-14 có thể gắn vừa cho cả bánh sau
     xe Honda Airblade các đời từ 2013 đến 2022 và bánh sau xe
     Honda Vision...",

    # ... more knowledge entries
]
```

**Embedding Model:**
- Model: `sentence-transformers/all-MiniLM-L6-v2`
- Dimensions: 384
- Runtime: Local (no API call)
- Speed: ~100ms per query

---

## 🔧 Technology Stack

### Backend
| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Framework** | FastAPI | 0.109.2 | REST API server |
| **Language** | Python | 3.11+ | Backend logic |
| **RAG Framework** | LlamaIndex | 0.10.15 | RAG orchestration |
| **Database** | SQLite | 3.x | Product data storage |
| **Vector DB** | LlamaIndex SimpleVectorStore | - | Knowledge embeddings |
| **Embeddings** | HuggingFace Transformers | - | Local embedding model |
| **LLM (Primary)** | Google Gemini | 2.5 Flash | Response generation |
| **LLM (Secondary)** | Anthropic Claude | 3.5 Sonnet | Fallback LLM |
| **Validation** | Pydantic | 2.6.1 | Request/response models |
| **Server** | Uvicorn | 0.27.1 | ASGI server |

### Frontend (Planned)
| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Framework** | Next.js | 14.x | React framework |
| **UI Library** | React | 18.x | Component library |
| **Styling** | Tailwind CSS | 3.x | Utility-first CSS |
| **HTTP Client** | Axios / Fetch | - | API communication |
| **State** | React Hooks | - | Local state management |

### Development Tools
| Tool | Purpose |
|------|---------|
| **Git** | Version control |
| **VSCode** | IDE |
| **Python venv** | Virtual environment |
| **pip** | Package management |
| **npm/yarn** | Frontend package management |

---

## 🔐 Security & Configuration

### API Key Management

**Current Approach (Development):**
```python
# API keys read from local files (temporary)
GOOGLE_API_KEY: F:/side_projects/keys/Google key/RAG_cua_hang_phu_tung.txt
ANTHROPIC_API_KEY: F:/side_projects/keys/Claude key/ragkt.txt
```

**Planned Approach (Production):**
```python
# Use environment variables
GOOGLE_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
DATABASE_URL=sqlite:///./database/store.db
```

**.env file:**
```bash
# LLM API Keys
GOOGLE_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here

# Database
DATABASE_URL=sqlite:///./database/store.db

# Server
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=http://localhost:3000

# LlamaIndex
VECTOR_STORE_PATH=./database/storage
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

### CORS Configuration
```python
# Development
allow_origins = ["http://localhost:3000", "http://127.0.0.1:3000"]

# Production
allow_origins = ["https://your-frontend-domain.com"]
```

---

## 📊 Performance Considerations

### Response Time Breakdown
```
Total: ~2-3 seconds

1. Keyword Extraction:     ~50ms
2. SQL Query:              ~100ms
3. Vector Search:          ~200ms
4. Context Building:       ~50ms
5. LLM Inference:          ~1.5s (Gemini)
6. Response Formatting:    ~50ms
```

### Optimization Strategies

#### Implemented
- ✅ Local embeddings (no API latency)
- ✅ SQL indexing on key fields
- ✅ Result limit (top 10 products)
- ✅ Efficient keyword filtering

#### Planned
- 🔵 Query result caching (Redis)
- 🔵 Database connection pooling
- 🔵 Async LLM calls
- 🔵 Frontend lazy loading
- 🔵 CDN for static assets

---

## 🧪 Testing Architecture

### Test Layers

```
┌─────────────────────────────────────────┐
│        End-to-End Tests (Future)        │
│  - Full user flow testing               │
│  - Frontend + Backend integration       │
└─────────────────────────────────────────┘
                  ▲
┌─────────────────────────────────────────┐
│      Integration Tests (Current)        │
│  - test_comprehensive.py (8 scenarios)  │
│  - API endpoint testing                 │
└─────────────────────────────────────────┘
                  ▲
┌─────────────────────────────────────────┐
│        Unit Tests (Planned)             │
│  - Keyword extraction tests             │
│  - SQL query tests                      │
│  - Vector search tests                  │
└─────────────────────────────────────────┘
```

### Current Test Coverage
```python
# test_comprehensive.py
1. Product name search       ✅
2. Brand + price filter      ✅
3. Vehicle + part type       ✅
4. Stock availability check  ✅
5. SKU code lookup           ✅
6. Price inquiry             ✅
7. Product comparison        ✅
8. Promotion search          ✅
```

---

## 🚀 Deployment Architecture (Planned)

### Development Environment
```
Local Machine:
- Backend: http://localhost:8000
- Frontend: http://localhost:3000
- Database: SQLite (local file)
```

### Production Environment (Target)
```
┌─────────────────────────────────────────────┐
│             CDN (Cloudflare)                │
│  - Static assets                            │
│  - Frontend caching                         │
└─────────────┬───────────────────────────────┘
              │
┌─────────────▼───────────────────────────────┐
│      Frontend (Vercel/Netlify)              │
│  - Next.js SSR                              │
│  - Auto-scaling                             │
└─────────────┬───────────────────────────────┘
              │
              │  HTTPS
              │
┌─────────────▼───────────────────────────────┐
│   Backend (Railway/Render/DigitalOcean)     │
│  - FastAPI container                        │
│  - Auto-scaling                             │
│  - Health checks                            │
└─────────────┬───────────────────────────────┘
              │
┌─────────────▼───────────────────────────────┐
│       Database (Persistent Storage)         │
│  - SQLite → PostgreSQL (scalability)        │
│  - Vector Store (mounted volume)            │
└─────────────────────────────────────────────┘
```

---

## 📦 Scalability Considerations

### Current Limitations
- **Database:** SQLite (single-file, not ideal for high concurrency)
- **Vector Store:** In-memory loading (RAM intensive)
- **LLM Calls:** Synchronous (blocking)

### Scaling Plan

#### Phase 1: Optimize Current Stack
- Add query caching (Redis)
- Optimize SQL indexes
- Implement connection pooling

#### Phase 2: Upgrade Components
- Migrate SQLite → PostgreSQL
- Use dedicated vector DB (Qdrant/Pinecone)
- Async LLM calls with queue

#### Phase 3: Horizontal Scaling
- Load balancer for API servers
- Read replicas for database
- Distributed caching

---

## 🔍 Monitoring & Observability (Planned)

### Metrics to Track
```
Application Metrics:
- Request count (/api/chat)
- Response time (p50, p95, p99)
- Error rate
- Cache hit rate

Business Metrics:
- Daily active users
- Queries per user
- Product search frequency
- Conversion rate (query → product view)

Infrastructure Metrics:
- CPU usage
- Memory usage
- Database connections
- API rate limits
```

### Logging Strategy
```python
# Structured logging (JSON)
{
  "timestamp": "2026-03-09T20:00:00Z",
  "level": "INFO",
  "service": "rag-engine",
  "query": "Tim phuoc NVX",
  "keywords": ["phuoc", "nvx"],
  "sql_results": 1,
  "vector_results": 3,
  "llm_provider": "google",
  "response_time_ms": 2345
}
```

---

## 📚 References

### Documentation
- [LlamaIndex Docs](https://docs.llamaindex.ai/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Google Gemini API](https://ai.google.dev/)
- [Anthropic Claude API](https://docs.anthropic.com/)

### Project Files
- [Implementation Plan](../implementation_plan.md)
- [Milestone 01](./MILESTONE_01_PRODUCT_IMPORT.md)
- [Project Timeline](./PROJECT_TIMELINE.md)

---

*Last Updated: March 9, 2026*
*Architecture Version: 1.0*
