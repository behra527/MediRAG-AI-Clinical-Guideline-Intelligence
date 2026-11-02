# MediRAG AI v2 — Clinical Guideline Research

A local educational PDF-RAG app with FastAPI, React/Vite, ChromaDB, local sentence-transformer embeddings and OpenRouter.

## Windows setup (IMPORTANT)
1. Extract ZIP completely. Open the **MediRAG_AI_v2** folder.
2. Copy `.env.example` to `.env` **in the project root**, not in `backend` or `frontend`.
3. Edit `.env`: set `OPENROUTER_API_KEY` to your real key and `OPENROUTER_MODEL` to a model enabled on your OpenRouter account. Never share or commit the key.
4. Double-click `START_BACKEND.bat`. Wait for `Uvicorn running on http://127.0.0.1:8000`. First install and embedding model download can take time.
5. Check http://127.0.0.1:8000/api/health in browser. It should show `status: ok`.
6. Double-click `START_FRONTEND.bat`. Open http://127.0.0.1:5173 .
7. Upload a **text-searchable PDF** (not a scanned image), choose it, then ask a question.

### Manual commands (PowerShell)
Backend (from PROJECT ROOT):
```
cd backend
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```
Frontend (in ANOTHER terminal, from PROJECT ROOT):
```
cd frontend
npm install
npm run dev
```

### Why "Failed to fetch" happened
Previously the browser called `http://localhost:8000` directly. If the backend was not running or the origin differed, fetch could fail. v2 routes browser requests through Vite `/api` proxy to `127.0.0.1:8000`, and displays a clearer error when the API is unavailable. **Both servers still must be running.**

### API health checks
- http://127.0.0.1:8000/api/health — backend status
- http://127.0.0.1:8000/docs — Swagger API docs
- http://127.0.0.1:5173 — frontend

### Project functionality
PDF ingestion → overlapping chunks → sentence-transformer embeddings → persistent ChromaDB → similarity retrieval → OpenRouter LLM answer with sources. Compare mode also requests a baseline answer without retrieval. The evaluation page supports manual review.

### Troubleshooting
- `API disconnected`: start backend and visit `/api/health`; check backend terminal for errors.
- `OpenRouter returned HTTP 401`: invalid API key; `402`: insufficient credits; `404`: invalid/unavailable model; `429`: rate limit.
- `No extractable text`: use a searchable PDF; scanned PDFs need OCR.
- Model download errors: allow first-time Hugging Face model download and check network.
- If your browser is on another device, proxy host and network settings must be changed.

### Safety
Educational research only. Not medical advice. Do not upload patient-identifiable information. Verify all claims against official guideline. This is a local prototype, not a production medical system.
