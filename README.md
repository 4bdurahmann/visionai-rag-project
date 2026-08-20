# VisionAI Medical RAG

Cited question-answering over a clinical guideline, built for the AI Hackathon
2026. The system retrieves evidence chunks from a local vector store, gates
out-of-scope questions, and generates natural-language answers with inline
`【N】` citations — then scores each answer for **faithfulness** (are claims
supported by the sources?) and **citation accuracy** (do the citations resolve
to sections that actually back the claims?).

The demo asks questions about the USPSTF 2020 recommendation on *Behavioral
Counseling to Promote a Healthy Diet and Physical Activity for CVD Prevention*
(JAMA 2020;324(20):2069-2075).

**By Abdul-Rahman Gamal & Hossam Ibrahim — VISION AI TEAM.**

---

## Repository layout

```
visionai-rag-project/
├── VisionAI_FastAPI/          # Python backend (FastAPI + RAG pipeline)
│   ├── src/
│   │   ├── controllers/       # API request/response Pydantic models
│   │   ├── core/              # config / .env loader
│   │   ├── modules/           # retrieval, gating, LLM generation, scoring
│   │   ├── Routes/            # FastAPI routers (/health, /query, /query/score)
│   │   ├── data/              # source documents + eval artifacts
│   │   ├── assets/            # original source PDF
│   │   └── main.py            # FastAPI app entry point
│   ├── requirements.txt
│   ├── .env.example           # copy to .env and fill in LLM keys
│   └── LICENSE
├── VisionAI_React/            # React frontend (React Router + Vite + Tailwind)
│   ├── app/                   # pages, components, data types
│   ├── vite.config.ts
│   └── package.json
└── README.md
```

## Backend

### Quick start

```bash
# 1. environment
cd VisionAI_FastAPI
cp .env.example .env            # add at least one LLM key (see below)

# 2. dependencies
python -m venv rag && source rag/bin/activate
pip install -r requirements.txt

# 3. build the index (one-time)
cd src
python -m modules.embed.parse2embed --org USPSTF \
    --doc-title "USPSTF 2020 behavioral counseling recommendation"
python -m modules.chroma_db.chroma_db

# 4. ask questions (inside src/)
python -m modules.llm.query_chroma "What is the letter grade of this recommendation?"

# 5. run the HTTP API
#    from VisionAI_FastAPI/:
rag/bin/python -m uvicorn --app-dir src main:app --host 0.0.0.0 --port 8000
#    ...or from inside src/:
cd src && ../rag/bin/python -m uvicorn main:app --host 0.0.0.0 --port 8000

curl -X POST http://localhost:8000/query \
     -H 'Content-Type: application/json' \
     -d '{"query":"How much physical activity should the counseling aim for?","k":5}'
```

### LLM providers

The answering/judging models run through whichever provider key is present.
Auto-selection order: **OpenRouter → Gemini → Alibaba/Qwen → Groq → OpenAI**.
Force one with `LLM_PROVIDER` in `.env` (e.g. `LLM_PROVIDER=groq`). If Groq
hits its daily token cap (429), requests automatically fail over to the next
provider.

| Key prefix | Provider | Get a key |
|---|---|---|
| `sk-or-v1-` | OpenRouter (many models, incl. free `:free`) | https://openrouter.ai/keys |
| `AIza...` | Google Gemini (free tier) | https://aistudio.google.com/apikey |
| `sk-ws-` | Alibaba Cloud Model Studio / Qwen | Alibaba Model Studio console |
| `gsk_` | Groq | https://console.groq.com/keys |
| `sk-proj-` | OpenAI | https://platform.openai.com/api-keys |

Model overrides: `OPENROUTER_MODEL`, `GEMINI_MODEL`, `OPENROUTER_JUDGE_MODEL`,
etc. Use e.g. `OPENROUTER_MODEL=meta-llama/llama-3.3-70b-instruct:free` for a
zero-cost option.

### How an answer is built

1. **Retrieve** — embed the question with a local PubMedBERT model
   (`NeuML/pubmedbert-base-embeddings`) and search 37 indexed chunks via hybrid
   BM25 + vector reranking (RRF fusion).
2. **Gate** — three layers decide if the corpus confidently covers the question:
   vector-similarity floor, BM25-fusion floor, and a grade gate for
   decision-style questions. Out-of-scope input gets a refusal instead of a
   hallucinated answer.
3. **Answer** — the LLM writes a concise, cited answer over the retrieved
   excerpts (`【N】` markers map back to sources with section + page). Markers
   are then re-attributed to the best-matching chunk for precision.
4. **Score** — each answer is decomposed into atomic claims which are judged
   against the evidence (faithfulness) and each citation is checked for
   correct placement, section/page provenance, and true support (citation
   accuracy). A deterministic embedding tiebreak keeps single flaky LLM
   verdicts from sinking good citations.

### API

- `GET /health` — service + index status
- `POST /query` — body `{"query", "k", "strategy", "use_llm", "score"}`;
  returns the answer, retrieved hits, and a `quality` report
  (`faithfulness`, `citation_accuracy`, `unsupported_claims`, `bad_citations`).
  With `"score": false` the answer returns immediately with a `request_id`;
  call `POST /query/score` with `{"request_id"}` to fetch the quality report
  asynchronously. A trailing slash (`POST /query/`) is accepted.

### Evaluation

```bash
# run from src/ (commands assume the venv is active, or prefix rag/bin/python)
cd src
python -m modules.llm.evaluate_accuracy --k 3 --strategy hybrid

# LLM-judged correctness (uses the configured LLM)
python -m modules.llm.evaluate_accuracy --k 3 --strategy hybrid --judge llm

# refusal-quality grading on hard red-team cases
python -m modules.llm.refusal_quality
```

Latest run: **13/14 · 92.9%** (accuracy_results.json). Q&A run
transcripts can be kept in `VisionAI_FastAPI/history/` (optional, gitignored).

## Frontend

### Quick start

```bash
cd VisionAI_React
yarn install
yarn dev            # http://localhost:5173
```

The live demo lives at `/clinical-rag`. By default it calls the backend at
`http://127.0.0.1:8000`; point it at another API with the `VITE_API_URL`
environment variable at build time:

```bash
VITE_API_URL=https://your-backend.example.com yarn build
```

### Commands

```bash
yarn dev         # dev server with HMR
yarn build       # production build (client + server)
yarn typecheck   # react-router typegen + tsc
yarn start       # serve the built app (node)
```

## License

MIT — see `VisionAI_FastAPI/LICENSE`.