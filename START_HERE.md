# Start here (study copy for teammates)

This zip is a **study copy** of our hackathon project: the IT Ticket Analysis & Resolution Assistant.
All code changes are made centrally from one laptop, so **don't edit files in this copy**. Use it to understand
your part well enough to explain it and answer judge questions.

## 1. Read in this order

| # | File | What you get | Time |
|---|---|---|---|
| 1 | [docs/PROJECT_CONTEXT.md](docs/PROJECT_CONTEXT.md) | Everything: functionality → architecture → code level → setup | 45 min |
| 2 | Your role's section in Part 3 of that file | The files and functions you own | 30 min |
| 3 | [docs/WORKED_EXAMPLES.md](docs/WORKED_EXAMPLES.md) | Six real tickets with their full output | 15 min |
| 4 | [EVALUATION.md](EVALUATION.md) | The numbers judges will ask about | 10 min |
| 5 | [learning/DEMO_GUIDE.md](learning/DEMO_GUIDE.md) | How we present | 15 min |
| 6 | `learning/pages/*.html` (double-click to open) | RAG study guide with 170 judge questions, code walkthrough, HLD questions | as needed |

## 2. Study with Claude

Open this folder in Claude Code (or upload the files you need to a Claude chat) and paste **the prompt for your role**.
Each prompt asks Claude to explain, not to change anything.

### Everyone: first message

```
Read START_HERE.md, PROMPT.md and docs/PROJECT_CONTEXT.md. This is a study copy: do not edit, create or delete
any files. Explain the project to me in three levels: (1) what it does for an IT analyst, in plain words;
(2) the architecture: the 6 pipeline steps and why each technology was chosen; (3) which files implement each
step. Use simple language and everyday analogies. Then wait for my questions.
```

### Role 1: Data, classifier, evaluation

```
I am Role 1 (data, classifier, evaluation). Study copy: do not edit files.
Walk me through, file by file and with line numbers: data/generate.py (how the 1,800 tickets and their noise
are made), data/kb/articles.json (structure of a KB article), app/taxonomy.py (labels and the priority rules),
app/baseline.py (TF-IDF + logistic regression in simple terms), app/build_index.py (what the index build does
step by step), eval/run_eval.py and EVALUATION.md (every metric: Recall@5, Precision@5, MRR, macro-F1,
calibration, what each number means and how it is computed).
Then quiz me with 15 judge questions on my part, one at a time, and correct my answers.
```

### Role 2: Retrieval and privacy

```
I am Role 2 (retrieval and privacy). Study copy: do not edit files.
Walk me through, with line numbers: app/redact.py (each pattern it masks and why error codes are kept),
app/embeddings.py (what an embedding is, the multilingual model, normalisation), app/retriever.py
(search_tickets, search_kb, _semantic_candidates with ChromaDB, BM25, _hybrid scoring
0.6·semantic + 0.3·BM25 + 0.1·metadata, the keyword_only guard, duplicates, filters, the reranker and why it is off),
and the retrieval numbers in EVALUATION.md (BM25 vs semantic vs hybrid, keyword traps).
Explain cosine similarity, BM25 and HNSW with simple analogies.
Then quiz me with 15 judge questions on my part, one at a time, and correct my answers.
```

### Role 3: LLM and trust layer

```
I am Role 3 (LLM and trust layer). Study copy: do not edit files.
Walk me through, with line numbers: app/pipeline.py Pipeline.analyze step by step, app/llm_provider.py
(Groq → Gemini failover, rate limits), app/llm.py (the SYSTEM prompt rule by rule, prompt-injection fencing,
JSON parsing, the repair retry, the disk cache), app/validator.py (how every quote is checked word for word,
and the Unicode hyphen bug we fixed), app/confidence.py (the three signals, the 0.35/0.40/0.25 weights,
every rule for OK / NEEDS_REVIEW / ESCALATE, including the weak-evidence rule), and degraded mode.
Then quiz me with 15 judge questions on my part, one at a time, and correct my answers.
```

### Role 4: API, UI, audit

```
I am Role 4 (API, UI, audit). Study copy: do not edit files.
Walk me through, with line numbers: app/schema.py (TicketIn, AnalysisResult and every field the UI shows),
app/api.py (each endpoint, its inputs and outputs), app/db.py (the audit tables, what is stored, the CSV export),
ui/app.py (the 3 tabs, the API client and its in-process fallback, the feedback buttons), scripts/ (check_env,
prewarm_cache, worked_examples), and how this maps to the brief's FR-06 and FR-08.
Also explain how this would be deployed and scaled in production and how it would plug into ServiceNow.
Then quiz me with 15 judge questions on my part, one at a time, and correct my answers.
```

## 3. Optional: run it on your laptop

Running it helps you see your part working, but it is not required for studying.
Follow [docs/PROJECT_CONTEXT.md](docs/PROJECT_CONTEXT.md) Part 4. In short:

1. Create a virtual environment and `pip install -r requirements.txt` (~2 GB download).
2. `copy .env.example .env` (Linux/macOS: `cp`). The zip has **no API keys**; add your own free Groq/Gemini keys,
   or leave them empty: the app then runs in degraded mode (no LLM), which is enough to explore.
3. Start the API and the UI (commands in Part 4). The index is already built, so skip `build_index`.

The search index and cached demo answers are included in `data/`, so the demo tickets answer instantly.
If anything in `data/` fails to load on your machine, `python -m app.build_index` rebuilds it in about 30 seconds.
