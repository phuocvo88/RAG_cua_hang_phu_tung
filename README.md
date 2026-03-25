# RAG Chatbot Cửa Hàng Phụ Tùng Xe Máy

AI-powered chatbot for auto parts store using RAG (Retrieval-Augmented Generation) with knowledge feedback loop.

## 🎯 Features

### Core Chatbot
- **Intelligent Product Search:** Natural language queries for parts search
- **RAG-powered Responses:** Combines SQL database and vector knowledge base
- **Multi-LLM Support:** Google Gemini and Anthropic Claude
- **Vietnamese Language:** Fully optimized for Vietnamese queries

### Knowledge Feedback Loop ✨ NEW
- **Staff Feedback:** Submit corrections directly from chat interface
- **Admin Dashboard:** Review and approve/reject feedback submissions
- **Dynamic Learning:** Approved knowledge automatically added to vector database
- **Audit Trail:** Track all feedback submissions and reviews

## 🏗️ Architecture

```
Frontend (Next.js) ←→ Backend (FastAPI) ←→ Databases
                                          ├─ SQLite (Products)
                                          └─ Vector DB (Knowledge)
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+ (or let Gradle download it)
- Java 17+ (for Gradle build tool)
- Git

### Installation Methods

#### Option 1: Using Gradle (Recommended)

Gradle automates the entire build process for both backend and frontend.

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd RAG_cua_hang_phu_tung
   ```

2. **Setup everything with one command:**
   ```bash
   # Windows
   .\gradlew-fixed.bat buildAll

   # Linux/Mac
   ./gradlew buildAll
   ```

3. **Configure API Keys:**
   - Create `.env` file in backend directory
   - Add your API keys:
     ```
     GOOGLE_API_KEY=your_google_key
     ANTHROPIC_API_KEY=your_anthropic_key
     ```

4. **Run the application:**
   ```bash
   # Windows
   .\gradlew-fixed.bat runAll

   # Linux/Mac
   ./gradlew runAll
   ```

See [Gradle Usage Guide](other_information/Gradle%20Usage%20Guide.md) for detailed Gradle commands.

#### Option 2: Manual Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd RAG_cua_hang_phu_tung
   ```

2. **Setup Backend:**
   ```bash
   cd backend
   python -m venv venv
   venv/Scripts/activate  # On Windows
   # source venv/bin/activate  # On Linux/Mac
   pip install -r requirements.txt
   ```

3. **Setup Frontend:**
   ```bash
   cd frontend
   npm install
   ```

4. **Initialize Database:**
   ```bash
   cd backend
   python create_feedback_table.py
   ```

5. **Configure API Keys:**
   - Create `.env` file in backend directory
   - Add your API keys:
     ```
     GOOGLE_API_KEY=your_google_key
     ANTHROPIC_API_KEY=your_anthropic_key
     ```

### Run the Application

**Terminal 1 - Backend:**
```bash
cd backend
venv/Scripts/python.exe main.py
```
Backend runs at: http://localhost:8000

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```
Frontend runs at: http://localhost:3000

## 📖 Usage

### Chat Interface
1. Open http://localhost:3000
2. Type your question (e.g., "Giá phanh trước SH 2023?")
3. Get AI-powered response
4. Click "Góp ý / Cập nhật" if information is incorrect

### Admin Dashboard
1. Open http://localhost:3000/admin/knowledge-review
2. Review pending feedback submissions
3. Approve or reject each submission
4. Approved knowledge is automatically added to the system

## 🧪 Testing

### Run Integration Tests
```bash
cd backend
python test_knowledge_feedback.py
```

### Manual Testing
See [QUICKSTART.md](QUICKSTART.md) for detailed testing workflow.

## 📁 Project Structure

```
RAG_cua_hang_phu_tung/
├── backend/
│   ├── main.py                    # FastAPI application
│   ├── rag_engine.py              # RAG logic and LLM integration
│   ├── create_feedback_table.py   # Database migration
│   ├── test_knowledge_feedback.py # Integration tests
│   ├── database/
│   │   ├── store.db               # SQLite database
│   │   └── storage/               # Vector DB storage
│   └── requirements.txt           # Python dependencies
├── frontend/
│   ├── src/
│   │   └── app/
│   │       ├── page.tsx           # Chat interface
│   │       └── admin/
│   │           └── knowledge-review/
│   │               └── page.tsx   # Admin dashboard
│   ├── package.json               # Node dependencies
│   └── tailwind.config.ts         # Tailwind config
├── task.md                        # Original task list
├── QUICKSTART.md                  # Quick start guide
├── KNOWLEDGE_FEEDBACK_IMPLEMENTATION.md  # Detailed docs
└── README.md                      # This file
```

## 🔧 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/chat` | Chat with AI |
| `POST` | `/api/knowledge/feedback` | Submit feedback |
| `GET` | `/api/admin/knowledge/pending` | Get feedbacks by status |
| `POST` | `/api/admin/knowledge/{id}/approve` | Approve feedback |
| `POST` | `/api/admin/knowledge/{id}/reject` | Reject feedback |

API documentation: http://localhost:8000/docs (when backend is running)

## 🗄️ Database Schema

### Products Table
- Product information, prices, stock status
- SKU codes, categories, brands

### Knowledge Feedbacks Table
- User queries and AI responses
- Corrected knowledge from staff
- Approval status and reviewer info

## 🛠️ Technology Stack

### Backend
- **FastAPI:** High-performance API framework
- **LlamaIndex:** Vector database and RAG orchestration
- **SQLite:** Relational database for products
- **Google Gemini:** Primary LLM
- **Anthropic Claude:** Alternative LLM
- **HuggingFace:** Local embeddings (sentence-transformers)

### Frontend
- **Next.js 14:** React framework with App Router
- **TypeScript:** Type-safe JavaScript
- **Tailwind CSS:** Utility-first styling
- **React Hooks:** Modern state management

## 📚 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Get started in 5 minutes
- **[Gradle Usage Guide](other_information/Gradle%20Usage%20Guide.md)** - Complete Gradle build tool guide
- **[KNOWLEDGE_FEEDBACK_IMPLEMENTATION.md](KNOWLEDGE_FEEDBACK_IMPLEMENTATION.md)** - Detailed implementation guide
- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Project summary and statistics

## 🔐 Security Notes

**Current implementation is for development only.**

For production deployment:
- Add authentication/authorization
- Implement rate limiting
- Configure proper CORS origins
- Use environment variables for secrets
- Enable HTTPS
- Add input validation and sanitization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

[Add your license here]

## 👥 Authors

[Add author information]

## 🙏 Acknowledgments

- LlamaIndex for RAG framework
- Google Gemini and Anthropic Claude for LLM capabilities
- FastAPI and Next.js communities

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check the documentation in the docs folder

## 🗺️ Roadmap

- [x] Basic RAG chatbot
- [x] Knowledge feedback loop
- [ ] User authentication
- [ ] Email notifications
- [ ] Analytics dashboard
- [ ] Mobile app
- [ ] Multi-language support

---

**Status:** ✅ Production Ready (with security enhancements)

**Last Updated:** March 21, 2026
