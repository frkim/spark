# SPARK — Smart Product Augmentation & Representation Kit

## Microsoft Foundry × RAJA — Intelligent Product Content Pipeline

A demo application that transforms raw product data into **enriched, SEO-ready, multilingual content** in seconds, using an 8-agent pipeline powered by Azure OpenAI.

## Architecture

```
User Query
    │
    ▼
Smart Query Intake Agent       ← resolves SKU / product family
    │
    ▼
Foundry IQ Retrieval Agent     ← multi-source evidence retrieval
    │
    ▼
Normalization Agent            ← units, taxonomy, vocabulary
    │
    ▼
Product Enrichment Agent       ← descriptions, benefits, use cases
    │
    ├──────────────┐
    ▼              ▼
SEO Agent    Multilingual Agent   ← parallel execution
    │              │
    └──────┬───────┘
           ▼
Quality & Compliance Agent     ← validation, citations, flags
           │
           ▼
Publication Agent              ← PIM, marketplace, CRM, catalog
```

## Prerequisites

- **Python 3.11+**
- An **Azure OpenAI** resource with a `gpt-4o` deployment

## Setup

### Option A — Using `uv` (recommended)

```bash
# Install uv if not already installed
# Windows:
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
# macOS/Linux:
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create venv and install dependencies
uv venv
uv pip install -r requirements.txt

# Or install from pyproject.toml
uv pip install -e .
```

### Option B — Using `pip`

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### Configure environment

Copy `.env.example` to `.env` and fill in your Azure OpenAI credentials:

```bash
cp .env.example .env
```

Edit `.env`:

```ini
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_API_VERSION=2024-12-01-preview
AZURE_OPENAI_MODEL=gpt-4o
```

## Running

### Streamlit UI (demo mode)

```bash
streamlit run app.py
```

Opens a browser with the full interactive pipeline UI including:
- Smart query input with examples
- Step-by-step pipeline execution
- Enrichment, SEO, multilingual, quality, and publication tabs
- Trace & monitoring dashboard

### CLI

```bash
# Interactive mode (choose from examples)
python main.py

# Direct query
python main.py "Show me the recycled single-wall carton 300 x 200 x 150 active for France and Germany"
```

## Project Structure

```
├── app.py                 # Streamlit UI
├── main.py                # CLI entry point
├── config.py              # Settings from .env
├── demo_data.py           # Realistic multi-source product data
├── pipeline.py            # 8-agent orchestrator (sequential + parallel)
├── observability.py       # Trace spans & run metadata
├── agents/
│   ├── base.py            # Base agent (Azure OpenAI wrapper)
│   ├── query_intake.py    # Agent 1 — Smart Query Intake
│   ├── retrieval.py       # Agent 2 — Foundry IQ Retrieval
│   ├── normalization.py   # Agent 3 — Normalization
│   ├── enrichment.py      # Agent 4 — Product Enrichment
│   ├── seo.py             # Agent 5 — SEO
│   ├── multilingual.py    # Agent 6 — Multilingual (EN/DE/ES/IT)
│   ├── quality.py         # Agent 7 — Quality & Compliance
│   └── publication.py     # Agent 8 — Publication
├── pyproject.toml
├── requirements.txt
├── .env.example
└── docs/
    └── demo_specification.md
```

## Key Design Decisions

| Decision | Rationale |
|---|---|
| Azure OpenAI via `openai` SDK | Reliable, well-documented, works with API key auth |
| Agent-per-step architecture | Mirrors Microsoft Agent Framework SequentialBuilder + ConcurrentBuilder patterns |
| Parallel SEO + Multilingual | Demonstrates concurrent execution (Agent Framework ConcurrentBuilder) |
| JSON contracts between agents | Each agent receives structured context and returns JSON |
| Embedded demo data | Simulates Foundry IQ grounding without requiring IQ setup |
| Streamlit UI | Fast to iterate, impressive for demos, no frontend build step |
| OpenTelemetry-ready tracing | Built-in trace spans; extend with OTLP exporters for production |

## Smart Query Examples

- *"Show me the recycled single-wall carton 300 x 200 x 150 currently active for France and Germany."*
- *"Find the RAJA shipping box mapped from supplier ref SB-300-200-150-K and show the source documents behind it."*
- *"Which product record supports a recyclable claim and is ready for marketplace publication?"*
- *"Why did the system map CTN-SW-BR to the RAJA single-wall shipping carton category?"*
