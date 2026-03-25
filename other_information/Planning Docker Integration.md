# Docker Integration Plan

This plan outlines the steps to containerize the RAG Chatbot project using Docker and Docker Compose. This will ensure consistent environments across different machines and simplify the setup process for new users (like your friend).

## Docker vs. Local Setup: Comparison

| Feature | Local Setup (Clone & Install) | Docker Setup |
| :--- | :--- | :--- |
| **Ease of Setup** | Requires manual installation of Python 3.11, Node.js 18, and all dependencies. | Requires only Docker and Docker Compose. One command to start everything. |
| **Consistency** | Environment may vary between OS (Windows/Linux/Mac), leading to "works on my machine" issues. | Identical environment for everyone. Containers run in isolated Linux environments. |
| **Isolation** | Dependencies are installed in the host system or venv/node_modules. | Dependencies are isolated inside containers. No clutter on the host system. |
| **Performance** | Native performance. | Slight overhead due to virtualization, usually negligible for this project. |
| **Debugging** | Direct access to local files and debuggers. | Requires extra configuration for attaching debuggers to containers. |

### Potential Obstacles
- **API Keys**: Docker containers need access to environment variables. We will use a `.env` file passed to Docker Compose.
- **Data Persistence**: SQLite and Vector DB data must be stored in Docker Volumes so they aren't lost when containers stop.
- **Network**: The Frontend needs to communicate with the Backend via the internal Docker network name (`backend:8000` instead of `localhost:8000`).
- **Hardcoded Paths**: Some paths in `rag_engine.py` are absolute Windows paths (e.g., `F:\side_projects\...`). These will not work in Docker and must fallback to Environment Variables.

## Proposed Changes

### [Backend]
#### [NEW] [Dockerfile](file:///f:/side_projects/RAG_cua_hang_phu_tung/backend/Dockerfile)
Create a multi-stage Dockerfile for the FastAPI backend using `python:3.11-slim`.
- Optimization: Use a non-root user for security.
- Persistence: Ensure `database/` is a volume-ready directory.

#### [NEW] [.dockerignore](file:///f:/side_projects/RAG_cua_hang_phu_tung/backend/.dockerignore)
Exclude `venv`, `__pycache__`, and local data files.

### [Frontend]
#### [NEW] [Dockerfile](file:///f:/side_projects/RAG_cua_hang_phu_tung/frontend/Dockerfile)
Create a multi-stage Dockerfile for the Next.js frontend.
- Stage 1: Install & Build.
- Stage 2: Runner using `node:18-slim` or the official Next.js standalone output.

#### [NEW] [.dockerignore](file:///f:/side_projects/RAG_cua_hang_phu_tung/frontend/.dockerignore)
Exclude `node_modules`, `.next`, and build artifacts.

### [Orchestration]
#### [NEW] [docker-compose.yml](file:///f:/side_projects/RAG_cua_hang_phu_tung/docker-compose.yml)
Define `backend` and `frontend` services.
- Map ports: `8000:8000` (BE) and `3000:3000` (FE).
- Mount volumes for persistence.
- Inject environment variables from `.env`.

### [Documentation]
#### [MODIFY] [README.md](file:///f:/side_projects/RAG_cua_hang_phu_tung/README.md)
Add a "Run with Docker" section with one-line instructions for your friend.

---

## Instructions for your Friend
To launch the project using Docker:
1. **Install Docker Desktop**.
2. **Clone the repo**.
3. **Setup Environment**: Create a `.env` file in the root with your `GOOGLE_API_KEY`.
4. **Launch**: Open terminal and run:
   ```bash
   docker-compose up --build
   ```
5. **Access**:
   - Web App: `http://localhost:3000`
   - API Docs: `http://localhost:8000/docs`

---

## Verification Plan

### Automated Tests
- No automated Docker tests exist yet. I will verify by running the build command.

### Manual Verification
1. Run `docker-compose up --build`.
2. Check logs to ensure Backend connects to SQLite and Frontend starts on port 3000.
3. Access `http://localhost:8000/` to verify Backend is "ok".
4. Access `http://localhost:3000` and send a test message to verify E2E connectivity.
5. Verify that data persists after `docker-compose down` and `up` by checking if the conversation or product list remains consistent.
