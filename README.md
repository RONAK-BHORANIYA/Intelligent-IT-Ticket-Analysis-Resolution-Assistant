# IT Ticket Analysis & Resolution Assistant

An evidence-first assistant for service-desk analysts. For a new ticket it **classifies** it (category,
subcategory, priority), finds **similar past tickets**, recommends **ranked resolution steps backed by quoted
evidence**, and decides with an honest **confidence score** whether to recommend, ask for review, or **escalate**.
All feedback and analyses are **audited** in SQLite and can be exported.

Built for the HCLTech *Future Ready AI Engineer* hackathon. Full design: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).
Results: [EVALUATION.md](EVALUATION.md). Worked examples (input → classification → similar cases → resolution → evidence):
[docs/WORKED_EXAMPLES.md](docs/WORKED_EXAMPLES.md), regenerate with `python scripts/worked_examples.py`.

## How it works

```
ticket ─► redact PII ─► baseline classifier ─► hybrid retrieval ─► LLM (JSON) ─► validator ─► confidence gate ─► result
                         (TF-IDF+LogReg)        ChromaDB + BM25     Groq→Gemini   code checks   OK / REVIEW / ESCALATE
```

| Step | File | What it does |
|---|---|---|
| Redact | `app/redact.py` | Masks emails, phones, IPs, IDs, secrets **before** indexing, LLM calls, storage and export |
| Baseline | `app/baseline.py` | TF-IDF + logistic regression: fallback labels, agreement signal, evaluation comparison |
| Retrieve | `app/retriever.py` | `0.6·cosine + 0.3·BM25 + 0.1·metadata` over ChromaDB (HNSW, cosine) and BM25; filters by category, app, environment, status, group, dates |
| Reason | `app/llm.py`, `app/llm_provider.py` | One JSON-mode call to free Groq (Llama 3.3 70B), failover to Gemini; Pydantic validation + one repair retry; disk cache |
| Validate | `app/validator.py` | Cited ids must be retrieved; excerpts must be verbatim; labels must be in the taxonomy |
| Gate | `app/confidence.py` | `0.35·LLM + 0.40·retrieval + 0.25·agreement`; P1, dropped claims or knowledge gaps force review/escalation |
| API / UI | `app/api.py`, `ui/app.py` | FastAPI + Streamlit; feedback buttons; audit export |

## Run it (Windows)

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env            # add your free GROQ_API_KEY / GEMINI_API_KEY (optional)
python -m app.build_index         # generates synthetic data if needed, builds ChromaDB + BM25 (~30 s)
uvicorn app.api:app --port 8000   # API docs: http://127.0.0.1:8000/docs
streamlit run ui/app.py           # UI: http://localhost:8501 (works even if the API is not running)
```

Optional: `python scripts/prewarm_cache.py` (cache the demo tickets), `python -m eval.run_eval --llm 30`
(evaluation with an LLM sample), `pytest -q` (29 tests, no network needed).

## API

| Method | Path | Purpose |
|---|---|---|
| POST | `/analyze?use_llm=true` | Full analysis of a `TicketIn` → `AnalysisResult` |
| GET | `/search?q=&mode=hybrid\|semantic\|bm25&category=&application=&status=&date_from=` | Search history and KB |
| POST | `/feedback` | Useful / incorrect / unresolved on a classification, similar ticket or resolution path |
| GET | `/audit/export?format=csv\|json` | Analyses joined with feedback (already redacted) |
| GET | `/health`, `/taxonomy`, `/analyses`, `/stats`, `/kb/{id}` | Status, labels, recent analyses, dashboard |

## Assumptions

- **Data:** no dataset was supplied in advance, so `data/generate.py` creates 1,800 synthetic tickets (26
  subcategories in 8 categories, ~25% with distracting sentences, 4% vague, 3% mislabelled, 6% Italian/Spanish, 30% with personal
  data to redact). 20% are held out and never indexed. Real datasets plug in through the loader.
- **Resolutions** come from a curated 36-article KB (`data/kb/articles.json`); past tickets are supporting evidence.
- **Priority** is rarely labelled, so rules set a floor (outage / all users / prod down → P1, many users or blocked →
  P2, single user → P3, how-to → P4) and the LLM may only raise it.
- **Free-tier LLMs** may use submitted data under their terms, which is another reason everything is redacted first.
- Out of scope: auto-closing tickets, remediation actions, ITSM write-back, real RBAC.
 
