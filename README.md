# EvidenceLens

An explainable multimodal evidence-retrieval system for assessing the
credibility of social media video content — instead of predicting
fake/real, it gathers and presents verifiable evidence from video,
audio, text, and trusted knowledge sources.

See `docs/architecture.md` for the system design and `docs/roadmap.md`
for the build plan.

## Structure

- `backend/` — FastAPI service (pipeline, API)
- `frontend/` — React + Vite UI
- `datasets/` — benchmark examples for evaluation
- `knowledge_base/` — trusted-source ingestion/corpus
- `models/` — local model weights/checkpoints (gitignored)
- `docs/` — architecture, API, roadmap, evaluation, limitations
- `scripts/` — one-off utility/ingestion scripts
- `tests/` — unit/integration tests

## Getting started

```bash
# backend
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# frontend
cd frontend
npm install
npm run dev
```
