# Learning pack: Teammate B (RAG Core)

Everything you need to learn and present your part of the **IT Ticket Analysis & Resolution Assistant**
(HCLTech *Future Ready AI Engineer* hackathon). It works offline and doesn't depend on any Claude account.

## Study in this order

| # | Open | What it gives you | Time |
|---|---|---|---|
| 1 | [pages/3-system-architecture-overview.html](pages/3-system-architecture-overview.html) | The whole system on one page: components, who owns what, the request flow | 15 min |
| 2 | [pages/1-rag-study-guide-170-questions.html](pages/1-rag-study-guide-170-questions.html) | RAG from zero in 13 steps, topics judges ask (LLM basics, chunking types, Flat/IVF/HNSW, evals, guardrails), and **170 judge questions** with quiz mode | 2–3 h |
| 3 | [pages/2-rag-code-walkthrough.html](pages/2-rag-code-walkthrough.html) | One real ticket followed through **your code**, file by file and line by line, with real outputs and the hand-offs to A and C | 1 h |
| 3b | [pages/4-system-design-hld-questions.html](pages/4-system-design-hld-questions.html) | System design (HLD) prep: why each technology, today vs production architecture, capacity maths, rate limiting, security layers, and **71 panel questions** with quiz mode | 1–2 h |
| 4 | [DEMO_GUIDE.md](DEMO_GUIDE.md) | How to present to the panel: checklist, the 7-minute run sheet, what to say, the demo 6 "caught a wrong citation" story, troubleshooting | 30 min + practice |
| 5 | [../docs/ARCHITECTURE.md](../docs/ARCHITECTURE.md) | The detailed design contract (schemas, confidence rules, retrieval design, fallbacks) | reference |
| 6 | [../EVALUATION.md](../EVALUATION.md) | The numbers you quote to judges | 10 min |
| 7 | [../docs/PLAYBOOK.md](../docs/PLAYBOOK.md) | If the brief on the day is **not** IT tickets: how the same chassis maps to every sample brief | 20 min |

Open the `.html` files by double-clicking them; they open in your browser. The diagrams need internet the first time;
without it they show as text. Quiz progress ("I know this") is saved in your browser.

## Your files (Teammate B)

| Step | File | What it does |
|---|---|---|
| 1 | `app/redact.py` | Masks emails, phones, IPs, IDs, passwords before search, LLM and storage |
| 3 | `app/embeddings.py` | Turns text into 384-number meaning vectors (multilingual MiniLM) |
| 4–5 | `app/retriever.py` | Hybrid search: ChromaDB (meaning) + BM25 (keywords), `0.6·cos + 0.3·bm25 + 0.1·meta`, filters |
| 6–7 | `app/llm.py` | Prompt with rules, evidence and injection fencing; JSON parse; one repair retry; disk cache |
| 7 | `app/llm_provider.py` | Free LLM chain Groq → Gemini, wait-and-retry on 429/503 |
| 8 | `app/validator.py` | Code checks: cited IDs were retrieved, quotes are word for word, labels are allowed |
| 9 | `app/confidence.py` | `0.35·LLM + 0.40·retrieval + 0.25·agreement` → OK / NEEDS_REVIEW / ESCALATE |
| all | `app/pipeline.py` | `Pipeline.analyze()`: runs steps 1–9; the one function C's API calls |

Tests for your part: `tests/test_core.py` and `tests/test_pipeline.py`.

## Run the app (Windows, in `D:\HACKATHON`)

First time on a new laptop:
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```
Then put your Groq and Gemini keys in `.env` (see DEMO_GUIDE.md → "API keys"), and build the index:
```bash
.venv\Scripts\python.exe -m app.build_index
```
Every time (two terminals):
```bash
.venv\Scripts\python.exe -m uvicorn app.api:app --port 8000
```
```bash
.venv\Scripts\python.exe -m streamlit run ui/app.py
```
Open http://localhost:8501. Check everything works: `.venv\Scripts\python.exe -m pytest -q` (29 tests).

## Other things in this folder

- `briefs/`: the sample problem statements from other colleges (UC1–UC5, DS UC2–5, Banking, Hospital, Library) and the earlier slide deck.
- `claude-memory/`: the notes Claude kept about this project, so a new Claude account can read them.
- `../PROMPT.md`: paste it into a new Claude chat to give it the full context.
