# VisionAI Medical RAG

Cited question-answering over a clinical guideline. The system retrieves
evidence chunks from a local vector store, gates out-of-scope questions, and
generates natural-language answers with inline `【N】` citations — then scores
each answer for **faithfulness** (are claims supported by the sources?) and
**citation accuracy** (do the citations resolve to sections that actually back
the claims?).

Built around the USPSTF 2020 recommendation on *Behavioral Counseling to
Promote a Healthy Diet and Physical Activity for CVD Prevention*
(JAMA 2020;324(20):2069-2075).

Structure follows a clean three-tier layout (`src/`):

```
VISIONAI/
├── src/
│   ├── controllers/      # API request/response Pydantic models
│   │   ├── queryControllers.py    # QueryRequest
│   │   ├── hitControllers.py      # HitModel (retrieved source)
│   │   └── responseControllers.py # QueryResponse + QualityReport
│   ├── core/
│   │   └── config.py      # .env loader, project metadata, model name
│   ├── modules/           # domain libraries
│   │   ├── chroma_db/     # vector store layer
│   │   │   ├── retrieval.py   # hybrid BM25+vector retrieval (RRF fusion)
│   │   │   ├── gate.py        # confidence / out-of-scope disclaimer gates
│   │   │   ├── grade.py       # recommendation-grade (A/B/C/D/I) extraction
│   │   │   ├── chroma_db.py   # index embedded chunks into Chroma
│   │   │   └── chroma_data/   # built index (gitignored)
│   │   ├── embed/
│   │   │   ├── parse2embed.py          # chunk + embed the JSON source
│   │   │   └── chunk_size_experiment.py# P@5 sweep over chunk size/overlap
│   │   ├── llm/
│   │   │   ├── llm.py            # multi-provider prompts, generation, scoring
│   │   │   ├── query_chroma.py   # interactive Q&A in the terminal
│   │   │   ├── evaluate_accuracy.py # accuracy vs ground-truth eval set
│   │   │   ├── refusal_quality.py   # grades refusal messages (3-point rubric)
│   │   │   └── classify_question.py # labels question categories
│   │   └── engine.py       # lazy singletons: embedding model, Chroma, retriever
│   │   └── pipeline.py     # shared query pipeline (retrieve → gate → answer → score)
│   ├── Routes/
│   │   ├── QueryRoute.py   # FastAPI router: /health, /query (+ lifespan)
│   │   └── RootRoute.py    # root route with project metadata
│   ├── data/               # source documents + eval artifacts (partly gitignored)
│   ├── assets/             # original source PDF
│   └── main.py             # FastAPI app entry point
├── requirements.txt
├── .env.example            # copy to .env and fill in LLM keys
├── LICENSE
└── output.txt              # sample Q&A transcript
```

## Quick start

```bash
# 1. environment
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

# 5. run the HTTP API from the project root
rag/bin/python -m uvicorn --app-dir src main:app --host 0.0.0.0 --port 8000

#    ...or without --app-dir, from inside src/
cd src && ../rag/bin/python -m uvicorn main:app --host 0.0.0.0 --port 8000

#    (the venv's activate scripts already point at VisionAI_FastAPI/rag,
#     so `source rag/bin/activate && python` also works)

curl -X POST http://localhost:8000/query \
     -H 'Content-Type: application/json' \
     -d '{"query":"How much physical activity should the counseling aim for?","k":5}'
```

## LLM providers

The answering/judging models run through whichever provider key is present.
Auto-selection order: **OpenRouter → Gemini → Alibaba/Qwen → Groq → OpenAI**.
Force one with `LLM_PROVIDER` in `.env`. If Groq hits its daily token cap
(429), requests automatically fail over to the next provider.

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

## How an answer is built

1. **Retrieve** — embed the question with a local PubMedBERT model
   (`NeuML/pubmedbert-base-embeddings`) and search 37 indexed chunks via hybrid
   BM25 + vector reranking (RRF fusion).
2. **Gate** — three layers decide if the corpus confidently covers the question:
   vector-similarity floor, BM25-fusion floor, and a grade gate for
   decision-style questions. Out-of-scope input gets a refusal instead of a
   hallucinated answer.
3. **Answer** — the LLM writes a concise, cited answer over the retrieved
   excerpts (`【N】` markers map back to sources with section + page).
4. **Score** — each answer is decomposed into atomic claims which are judged
   against the evidence (faithfulness) and each citation is checked for
   correct placement in-range + section/page provenance + true support
   (citation accuracy).

## API

- `GET /health` — service + index status
- `POST /query` — body `{"query", "k", "strategy", "use_llm"}`; returns the
  answer, retrieved hits, and a `quality` report
  (`faithfulness`, `citation_accuracy`, `unsupported_claims`, `bad_citations`).
  A trailing slash (`POST /query/`) is accepted without redirecting.

## Evaluation

```bash
# run from src/ (commands assume the venv is active, or prefix rag/bin/python)
cd src
python -m modules.llm.evaluate_accuracy --k 3 --strategy hybrid

# LLM-judged correctness (uses the configured LLM)
python -m modules.llm.evaluate_accuracy --k 3 --strategy hybrid --judge llm

# refusal-quality grading on hard red-team cases
python -m modules.llm.refusal_quality
```

Latest run (per-question faithfulness / citation accuracy): see
`output.txt` for a sample transcript. The eval reports are written to
`src/data/accuracy_results.json`.