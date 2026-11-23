---
name: hcl-hackathon-context
description: "User is prepping the HCLTech \"IT Ticket Analysis & Resolution Assistant\" 6-hr hackathon (3-person team, all code built in Claude chat, each teammate pushes own branch)"
metadata:
  node_type: memory
  type: project
  originSessionId: 5a213079-a64d-4ec6-aff0-afb8f0f3d758
  modified: 2026-11-10T20:19:22.587Z
---

User's team (3 people) will build the HCLTech Future Ready AI Engineer hackathon use case (D:\HACKATHON\problem.docx): 6 hrs, 1 hr architecture. All code is written in one Claude chat; each teammate pushes their own branch to GitHub with their own author identity.

Chosen stack (2026-11-10): Streamlit + FastAPI, LLM-centric RAG, synthetic data as backup. The team has NO paid LLM key, so the LLM is a free API-key chain (Groq → Gemini) through the OpenAI-compatible client. The user does NOT want an offline/local LLM (no Ollama; the laptop has 7.8 GB RAM). Vector store is ChromaDB plus BM25. The contract is in docs/ARCHITECTURE.md.

**Status 2026-11-11:** The full UC1 app is built in D:\HACKATHON (app/, ui/app.py, eval/, tests/, data/generate.py, README.md, EVALUATION.md). 26 tests pass, and the UI and API were verified in the browser in degraded mode. Still open:
- The live LLM path is untested because no Groq or Gemini key is in .env yet.
- There is no git repo or branch split yet.

Reference: a friend's selected team's repo https://github.com/HarshithaPanchaneni/HCL_Tech used a HuggingFace dataset (1,800 tickets, columns Category/Subcategory/Text, 18 subcategories, partly Italian, NO resolution text or priority) plus a 30-article curated KB as the resolution source.

The real brief isn't known in advance. Sample briefs are in C:\Users\LOVII\Downloads\New folder (AI UC1/2/4/5, Banking, Hospital, Library, DS UC2–5). docs/PLAYBOOK.md maps every brief onto one reusable chassis with archetypes A–E.

The user is Teammate B (RAG core) and is new to RAG, so explain concepts simply. Their study guide with 170 judge Q&A: https://claude.ai/artifact/KB8tyG1QApCcrq8QCUR9xQ

**Why:** The real dataset probably has no resolutions, so the plan needs a curated KB and multilingual embeddings.
**How to apply:** Use the repo as a reference for ideas only, never copy its code (plagiarism risk). Aim to beat it on evaluation rigor (theirs: 7 test tickets, confidence stuck at 0.5, relevance defined only at category level).
