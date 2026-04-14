
# Microsoft Foundry × RAJA — Intelligent Product Content Pipeline

**Author:** François-Xavier Kim, Solution Engineer, Microsoft France
**Date:** April 2026
**Classification:** Microsoft Confidential — For RAJA Use Only

---

## Table of Contents

1. [Scenario Overview](#scenario-overview)
2. [Solution Stack](#solution-stack)
3. [Agentic Architecture](#agentic-architecture)
4. [Multi-Source Grounding with Foundry IQ](#multi-source-grounding-with-foundry-iq)
5. [Full Demo Script](#full-demo-script)
6. [Technical Architecture Description](#technical-architecture-description)
7. [Tracing and Monitoring](#tracing-and-monitoring)
8. [Agent Prompt Designs](#agent-prompt-designs)
9. [Realistic Demo Data](#realistic-demo-data)
10. [Example Output](#example-output)
11. [Appendix — Sample Reference Links](#appendix--sample-reference-links)

---

## Scenario Overview

A RAJA product manager uploads, selects, or queries a **raw product record** using a smart search experience backed by Foundry IQ.

The starting data is fragmented across systems: IQ exports, supplier documents, RAJA taxonomy files, compliance references, and existing catalog content.

Microsoft Foundry orchestrates a set of specialized agents that transform this raw input into a **fully enriched product sheet** in under 30 seconds, while preserving traceability to the underlying business data.

**Key business value:**
- Eliminates 20–45 minutes of manual work per product record
- Scales to thousands of SKUs per day
- Delivers SEO-optimized, multilingual content consistently
- Grounds generated content on real enterprise data rather than free-form generation
- Requires human review only for flagged exceptions

---

## Solution Stack

| Layer | Technology | Role in the demo |
|---|---|---|
| Agent orchestration | Microsoft Agent Framework | Builds the multi-step workflow and parallel branches |
| Implementation language | Python | Primary implementation language for the workflow and tool adapters |
| Agent runtime | Microsoft Foundry Agent Services | Hosts the orchestrated agents and workflow endpoints |
| Data grounding | Foundry IQ | Connects and indexes multiple enterprise data sources for retrieval and smart query |
| Model and workflow platform | Microsoft Foundry | Manages models, orchestration context, evaluation, state, and operational governance |
| Observability | Tracing + monitoring via OpenTelemetry and Azure Monitor / Application Insights | Captures run traces, latency, failures, and business KPIs |

**Implementation positioning:**

- The end-to-end flow is implemented in **Python** using **Microsoft Agent Framework** workflow orchestration patterns.
- The agents are deployed and operated through **Microsoft Foundry Agent Services**.
- **Foundry IQ** provides the grounded retrieval layer across product, compliance, taxonomy, and supplier content.
- **Microsoft Foundry** provides the enterprise control plane for models, workflow execution, evaluation, and operational governance.

---

## Agentic Architecture

| # | Agent | Role | Runtime pattern |
|---|---|---|---|
| 1 | Smart Query Intake Agent | Accepts a product lookup or natural-language query and resolves the target SKU/product family | Agent Framework entry agent |
| 2 | Foundry IQ Retrieval Agent | Retrieves the best evidence from IQ and connected sources with citations | Foundry IQ grounded retrieval |
| 3 | Normalization Agent | Harmonizes units, labels, categories, and RAJA naming conventions | Python transformation/tool agent |
| 4 | Product Enrichment Agent | Generates descriptions, benefits, use cases, cross-sell, and up-sell | Hosted content generation agent |
| 5 | SEO Agent | Creates meta descriptions, keywords, H1/H2 structure | Parallel branch |
| 6 | Multilingual Agent | Produces EN/DE/ES/IT versions with cultural adaptation | Parallel branch |
| 7 | Quality & Compliance Agent | Checks accuracy, tone, forbidden claims, RAJA guidelines, and citation coverage | Validation agent |
| 8 | Publication Agent | Formats output for e-commerce, CRM, marketplaces, and catalog PDFs | Output adapter agent |

**Workflow flow implemented with Agent Framework:**

```text
[User / Product Manager]
       |
       v
Smart Query Intake Agent
       |
       v
Foundry IQ Retrieval Agent
   (IQ + supplier PDF + taxonomy + compliance + catalog history)
       |
       v
Normalization Agent
       |
       v
Product Enrichment Agent
       |
    +--+-------------------+
    |                      |
    v                      v
  SEO Agent           Multilingual Agent
  (parallel)          EN / DE / ES / IT
    +----------+-----------+
             |
             v
    Quality & Compliance Agent
             |
             v
       Publication Agent
             |
    +----------+----------+-----------+
    |                     |           |
    v                     v           v
 PIM / CMS JSON      Marketplace     CRM / Catalog
               payload         outputs
```

**Why this architecture is credible in a demo:**

- It shows **Agent Framework** as the orchestration layer, not just prompt chaining.
- It shows **Foundry IQ** as the grounding layer across multiple enterprise sources.
- It shows **Foundry Agent Services** as the runtime and operating model.
- It shows **parallel execution** for SEO and multilingual tasks, which is visible and business-relevant.
- It shows **auditability** by keeping citations, trace IDs, and quality flags attached to each generated record.

---

## Multi-Source Grounding with Foundry IQ

The demo should avoid the impression that the system only reads one IQ row. The stronger story is that **Foundry IQ unifies several enterprise data sources** and lets the workflow query them through one grounded retrieval layer.

### Data sources connected to Foundry IQ

| Source | Example content | Why it matters |
|---|---|---|
| IQ product export | SKU, dimensions, weight, supplier ref, raw category | Primary operational source |
| Supplier technical sheet | Load limits, material composition, assembly notes | Adds technical evidence |
| RAJA taxonomy reference | Internal category mapping, approved labels, material vocabulary | Normalization authority |
| Compliance and sustainability reference | Recycling claims, restricted wording, certification status | Controls allowed claims |
| Existing RAJA catalog content | Tone examples, legacy descriptions, related products | Supports consistent style and cross-sell |
| ERP / stock feed | Availability, lead time, packaging unit, market activation | Adds go-to-market context |

### Smart query examples for the live demo

Use one of these queries before running the enrichment pipeline:

- "Show me the recycled single-wall carton 300 x 200 x 150 currently active for France and Germany."
- "Find the RAJA shipping box mapped from supplier ref SB-300-200-150-K and show the source documents behind it."
- "Which product record supports a recyclable claim and is ready for marketplace publication?"
- "Why did the system map CTN-SW-BR to the RAJA single-wall shipping carton category?"

### Expected smart query response behavior

The Smart Query Intake Agent should return:

- the matched SKU or ranked candidate list
- the source documents used by Foundry IQ
- the confidence of the match
- the product family/category selected for downstream enrichment
- a traceable explanation of the category mapping when requested

This makes the demo more credible because the user does not have to start from a single hand-picked record. The workflow can begin from a realistic business question and then pivot into enrichment.

---

## Full Demo Script

**Audience:** RAJA product/digital team + decision-makers  
**Duration:** ~20 minutes live demo

---

### Opening (2 min)

> "What I want to show you is not a concept deck. It is a Python workflow built with Microsoft Agent Framework, running on Microsoft Foundry Agent Services, and grounded on your enterprise data through Foundry IQ.
>
> The business problem is familiar: your teams start with fragmented product data and need to produce complete, publishable content across channels and languages, quickly and consistently.
>
> The point of this demo is to show how Microsoft Foundry turns that into an operational pipeline with grounding, tracing, and quality control built in."

---

### Step 1 — Smart Query Across Enterprise Sources (3 min)

*Show the smart query interface and ask a business-style question.*

> "Instead of opening a single raw IQ row, we start with a smart query. The user can search in business language: for example, 'show me the recycled single-wall carton 300 by 200 by 150 active for France and Germany.'
>
> Foundry IQ searches across several sources at once: the IQ export, supplier technical documents, RAJA taxonomy references, compliance rules, and existing catalog material.
>
> The system returns the best matching SKU, the documents used as evidence, and the confidence of the match. That means the pipeline starts from grounded retrieval, not from a manually prepared demo file."

---

### Step 2 — Retrieval, Extraction, and Normalization (3 min)

*Show Foundry IQ evidence, then the normalized payload.*

> "The first runtime step uses Foundry IQ to retrieve the relevant evidence for the selected product. We can see the raw IQ row, the supplier sheet, the taxonomy entry, and the allowed compliance wording.
>
> The Normalization Agent then converts this into one clean JSON contract: dimensions in millimeters, weight in grams, approved material naming, normalized color, and RAJA category mapping.
>
> This is implemented in Python as a deterministic Agent Framework step. It is not creative generation. It is structured transformation with explicit notes when an assumption had to be made."

---

### Step 3 — Product Enrichment (4 min)

*Show the Enrichment Agent output and supporting citations.*

> "Once the data is normalized, the Product Enrichment Agent generates the commercial layer: short description, long description, customer benefits, use cases, industry applications, cross-sell, and up-sell.
>
> The important point is that the content is grounded. Each meaningful claim can be traced back to a source attribute or a supporting document retrieved by Foundry IQ.
>
> This is what makes the output enterprise-ready. We are not asking the model to invent product facts. We are asking it to express verified facts in a publishable way."

---

### Step 4 — Parallel SEO and Multilingual Generation (3 min)

*Show both branches running in parallel.*

> "At this point the Agent Framework workflow forks into two parallel branches.
>
> The SEO Agent creates the H1, H2 structure, meta description, and keyword set for B2B search intent. At the same time, the Multilingual Agent creates adapted versions for English, German, Spanish, and Italian.
>
> That concurrency matters in practice. It reduces end-to-end latency while keeping each specialization isolated and measurable."

---

### Step 5 — Quality, Compliance, and Citation Coverage (2 min)

*Show the validation report.*

> "Before anything is published, the Quality and Compliance Agent checks factual consistency, tone, forbidden claims, target lengths, and cross-language consistency.
>
> We also score citation coverage. If a product description contains a claim that cannot be linked back to a trusted source, it is flagged.
>
> That changes the review model completely. Product managers review the exceptions, not every product."

---

### Step 6 — Publication Output (2 min)

*Show the multi-format output panel.*

> "The final output is delivered in the formats your downstream teams actually need: structured PIM JSON, marketplace-ready payload, CRM short copy, and catalog text.
>
> One grounded workflow produces all of them. No copy-paste, no reformatting loop, and no hidden loss of traceability between systems."

---

### Step 7 — Tracing and Monitoring View (2 min)

*Show the trace view or monitoring dashboard.*

> "Because this runs on Foundry Agent Services, we can inspect the execution itself. Here is the trace for this product run: each agent step, how long it took, which documents were retrieved, where flags were raised, and what the final status was.
>
> On top of that, monitoring shows us the operational KPIs: latency, failure rate, citation coverage, and approval rate. This is what turns a nice demo into an operating model."

---

### Closing (1 min)

> "What you have just seen is a grounded, traceable product content pipeline implemented in Python with Agent Framework, executed on Microsoft Foundry Agent Services, and connected to multiple enterprise data sources through Foundry IQ.
>
> At catalog scale, this means thousands of enriched, SEO-ready, multilingual product records per day, with operational visibility and human review focused only where risk is detected.
>
> The logical next step would be a proof of concept on a real product family, using your own source systems and editorial rules."

---

## Technical Architecture Description

### Key Architectural Principles

| Principle | Detail |
|---|---|
| Orchestrator | Agent Framework coordinates the workflow, branching, retries, and hand-off contracts |
| Runtime | Foundry Agent Services hosts the agents and exposes the workflow endpoint |
| Grounding | Foundry IQ retrieves evidence from multiple enterprise sources before generation |
| Deterministic core | Normalization and mapping steps are deterministic Python components where possible |
| Parallelism | SEO and Multilingual agents run concurrently after enrichment |
| Auditability | Each step emits a versioned payload, source citations, confidence, and trace identifiers |
| Human-in-the-loop | Quality Agent flags only the records that need review |
| Configurability | Taxonomy, tone rules, forbidden claims, and market policies are RAJA-managed configs |
| Observability | OpenTelemetry traces and Azure Monitor / Application Insights metrics support operations |

### Suggested Python implementation shape

| Component | Responsibility |
|---|---|
| `query_intake_agent.py` | Accepts user query or selected SKU and initializes workflow context |
| `foundry_iq_adapter.py` | Queries Foundry IQ and returns ranked documents plus source metadata |
| `normalization_agent.py` | Applies unit conversion, taxonomy mapping, and vocabulary normalization |
| `enrichment_agent.py` | Generates grounded commercial content |
| `seo_agent.py` | Generates SEO assets |
| `multilingual_agent.py` | Produces EN/DE/ES/IT localized variants |
| `quality_agent.py` | Checks compliance, evidence coverage, and translation consistency |
| `publication_agent.py` | Emits target-channel payloads |
| `observability.py` | Standardizes trace IDs, run metadata, and custom metrics |

### Stage-by-stage description

**Stage 0 — Smart Query Intake Agent**  
Accepts a natural-language request or a direct SKU. Resolves the target product, market scope, and requested output mode.

**Stage 1 — Foundry IQ Retrieval Agent**  
Retrieves the most relevant evidence from IQ exports, supplier sheets, RAJA taxonomy files, compliance references, catalog history, and ERP/stock data. Returns citations and document metadata.

**Stage 2 — Normalization Agent**  
Maps extracted attributes to RAJA's internal taxonomy. Standardizes units, approved material names, color labels, market availability, and compliance tags. Flags any mapping assumption.

**Stage 3 — Product Enrichment Agent**  
Generates commercial content grounded in the normalized record and retrieved evidence. Every material claim should remain traceable.

**Stage 4A — SEO Agent (parallel)**  
Generates H1, H2s, meta description, primary keyword, and secondary keywords optimized for B2B packaging and logistics searches.

**Stage 4B — Multilingual Agent (parallel)**  
Produces culturally adapted versions in English, German, Spanish, and Italian, while preserving product facts and compliance constraints.

**Stage 5 — Quality & Compliance Agent**  
Validates factual consistency, tone, claim eligibility, field lengths, and cross-language drift. Also checks citation completeness and flags unsupported statements.

**Stage 6 — Publication Agent**  
Formats approved content into target schemas for PIM/CMS, marketplaces, CRM, and print/catalog use.

### Performance target for the demo

| Step | Target latency |
|---|---|
| Smart query + retrieval | 3–6 seconds |
| Normalization | less than 1 second |
| Enrichment | 5–8 seconds |
| SEO + multilingual in parallel | 5–8 seconds |
| Quality + publication | 2–4 seconds |
| Total | 15–27 seconds |

---

## Tracing and Monitoring

The demo should explicitly show that the workflow is observable in production terms, not only visually impressive.

### Tracing design

Each workflow run should generate and preserve:

- `run_id`
- `product_id` / `sku`
- `user_query`
- `source_document_ids`
- `agent_step_name`
- `latency_ms`
- `model_name`
- `prompt_version`
- `quality_status`
- `citation_coverage_score`

Each agent step should emit a trace span with:

- input contract summary
- retrieved documents and ranking
- token usage and latency
- output schema version
- validation flags
- retry count if applicable

### Monitoring dashboard KPIs

| KPI | Why it matters |
|---|---|
| End-to-end latency | Demonstrates operational viability |
| Per-agent latency | Identifies bottlenecks in retrieval, enrichment, or translation |
| Success / failure rate | Tracks workflow health |
| Approval rate | Measures business-ready output quality |
| Flag rate by agent | Shows where exceptions are coming from |
| Citation coverage | Confirms grounded generation |
| Source freshness | Ensures decisions are based on current data |
| Translation drift rate | Detects unsupported claims introduced by localization |

### Operational tooling

| Need | Tooling approach |
|---|---|
| Distributed traces | OpenTelemetry traces emitted by the Python workflow |
| Request and dependency performance | Azure Monitor / Application Insights |
| Run-level dashboards | Workbook or dashboard combining trace, latency, and quality KPIs |
| Alerting | Alerts on latency spikes, rising flag rates, or failed retrievals |
| Audit trail | Persist run metadata, citations, and output versions per SKU |

### Suggested demo moment

After showing the final generated content, switch to a monitoring view and say:

> "This is the operational trace for the exact run you just watched. We can see which sources were retrieved, how long each agent took, whether any retries occurred, and whether the final content was fully grounded. That is the difference between a generative feature and an enterprise process."

---

## Agent Prompt Designs

### Shared workflow contract

Every agent should receive:

- `run_id`
- `sku`
- `market_scope`
- `normalized_product_json`
- `retrieved_sources`
- `prompt_version`

Every agent should return:

- `output`
- `citations`
- `confidence`
- `flags`
- `trace_metadata`

### Agent 1 — Smart Query Intake Agent

```text
You are the smart query intake specialist for RAJA Group.

Your input is either:
- a natural-language business query from a product manager, or
- a direct SKU / supplier reference.

Your task is to identify the intended product or product family and prepare the workflow context.

Return:
- query_type
- resolved_sku or candidate_skus
- market_scope
- user_intent
- retrieval_query
- clarification_needed (boolean)

Rules:
- Prefer exact SKU and supplier reference matches when available.
- If multiple candidates are plausible, return a ranked list.
- Do not invent product identifiers.
- Return valid JSON only.
```

---

### Agent 2 — Foundry IQ Retrieval Agent

```text
You are a grounded retrieval specialist for RAJA Group.

Your input is a resolved product context and a retrieval query.
Your task is to retrieve the most relevant evidence from Foundry IQ.

Search across these source types:
- IQ product exports
- supplier technical sheets
- RAJA taxonomy references
- compliance and sustainability references
- existing catalog content
- ERP or stock feeds

Return:
- retrieved_sources (array with source_id, source_type, excerpt, confidence)
- extracted_attributes
- missing_critical_fields
- retrieval_notes

Rules:
- Prioritize trusted internal sources over stylistic examples.
- Preserve source identifiers for downstream citations.
- Do not generate product content.
- Return valid JSON only.
```

---

### Agent 3 — Normalization Agent

```text
You are a product data normalization specialist for RAJA Group.

Your input is retrieved evidence and extracted product attributes.
Your task is to normalize the data according to RAJA's internal standards.

Apply the following normalizations:
- Convert all dimensions to millimeters (mm).
- Convert all weights to grams (g).
- Map raw categories to the closest RAJA catalog category using the provided taxonomy.
- Standardize material names to RAJA's approved material vocabulary.
- Normalize color names to RAJA's color palette labels.
- Expand compliance fields to approved RAJA compliance tags.

Return:
- normalized_product_json
- normalization_notes
- assumptions
- citations

Rules:
- Flag every assumption explicitly.
- Do not enrich or generate commercial copy.
- Return valid JSON only.
```

---

### Agent 4 — Product Enrichment Agent

```text
You are a senior product content writer for RAJA Group, specializing in packaging and logistics products.

Your input is a normalized product JSON plus grounded source excerpts.
Generate complete, accurate, and commercially useful product content.

Generate:
- short_description (max 30 words)
- long_description (80-120 words)
- customer_benefits (array of 4-5 bullets, max 12 words each)
- recommended_use_cases (array of 3-5 strings)
- industry_applications (array of 3 industries)
- cross_sell_suggestions (array of 2-3 product types)
- upsell_suggestion (string)

Rules:
- Every meaningful claim must be supported by input data or cited source evidence.
- Tone: professional, clear, practical.
- No superlatives, no invented specifications, no unsupported compliance claims.
- Return valid JSON only.
```

---

### Agent 5 — SEO Agent

```text
You are an e-commerce SEO specialist for RAJA Group.

Your input is enriched product content in JSON.
Generate SEO metadata optimized for B2B packaging and logistics searches.

Generate:
- h1 (max 60 characters)
- h2_list (array of 2-3 strings)
- meta_description (140-160 characters)
- primary_keyword (string)
- secondary_keywords (array of 4-6 strings)
- seo_notes (string)

Rules:
- Optimize for B2B buyer intent.
- Avoid keyword stuffing.
- Keep wording aligned with validated product facts.
- Return valid JSON only.
```

---

### Agent 6 — Multilingual Agent

```text
You are a multilingual product content specialist for RAJA Group.

Your input is validated English product content in JSON.
Produce culturally adapted versions in English, German, Spanish, and Italian.

For each language, adapt:
- short_description
- long_description
- customer_benefits
- meta_description

Register guidelines:
- English: concise, clear, B2B practical
- German: precise, technical, formal
- Spanish: clear, professional, slightly warmer
- Italian: descriptive, commercial, relationship-oriented

Rules:
- Do not translate specifications incorrectly.
- Preserve SKU, dimensions, weights, and supported claims.
- Flag any untranslatable or risky term.
- Return valid JSON only.
```

---

### Agent 7 — Quality & Compliance Agent

```text
You are a content quality and compliance reviewer for RAJA Group.

Your input is fully enriched, multilingual product content in JSON with citations.
Validate all content against RAJA's editorial and compliance standards.

Run these checks:
1. Factual consistency
2. Tone of voice
3. Forbidden or unsupported claims
4. Length compliance
5. Cross-language consistency
6. Citation coverage

Return:
- status: approved | flagged
- checks_passed
- flags (array: field, language, issue, recommendation)
- overall_confidence_score (0-100)
- citation_coverage_score (0-100)

Be conservative. Flag uncertainty. Do not rewrite; flag and recommend only.
```

---

### Agent 8 — Publication Agent

```text
You are a product content publication specialist for RAJA Group.

Your input is approved, multilingual product content in JSON.
Format it into the required schemas for each publication channel.

Generate:
1. ecommerce_json — full structured record for PIM/CMS
2. marketplace_ready — flat JSON
3. crm_short — plain text paragraph, max 60 words, English only
4. catalog_text_block — plain text with H1, short description, benefit bullets, dimensions, SKU

Rules:
- Do not add content not in the input.
- Respect field length limits.
- Preserve run_id and citation references for audit purposes.
- Return all four formats in one JSON object.
```

---

## Realistic Demo Data

The demo will be stronger if it uses a realistic multi-source product record rather than a single synthetic row.

### Primary product used in the demo

| Field | Value |
|---|---|
| SKU | RAJA-FR-SW-302015-R |
| Supplier Ref | SB-300-200-150-K |
| Short Label (IQ) | Crt simple cannelure brun rec 300x200x150 |
| Category (IQ) | CTN-SW-BR |
| Dimensions | 300 x 200 x 150 mm |
| Weight | 382 g |
| Material | Carton ondule simple cannelure, 70% recycle |
| Color | Brun |
| Pack Quantity | 25 |
| Market Availability | FR, BE, ES, IT, DE |
| Compliance | Recycle, FSC mix pending verification |
| Publication Status | Draft |
| Last Modified | 2026-03-12 |
| Modified By | Import automatique IQ |

### Additional source snippets indexed in Foundry IQ

**Supplier technical sheet excerpt**

> Product code SB-300-200-150-K. Single-wall corrugated shipping carton. Internal dimensions 300 x 200 x 150 mm. Recommended for light to medium goods. Brown kraft finish. Supplied flat for storage efficiency.

**RAJA taxonomy reference**

| Raw Category | RAJA Category | Approved Label |
|---|---|---|
| CTN-SW-BR | Shipping > Cartons > Single-wall | Single-wall cardboard shipping box |

**Compliance reference**

| Claim | Allowed? | Condition |
|---|---|---|
| Recycled material | Yes | If supplier declaration exists |
| FSC certified | No | Only if valid certificate ID is present |
| Recyclable | Yes | Allowed for corrugated cardboard |

**ERP / stock feed excerpt**

| SKU | Available Stock | Lead Time | Market Status |
|---|---|---|---|
| RAJA-FR-SW-302015-R | 4,850 | 48 hours | Active |

### Demo smart query examples using this data

- "Find the recycled single-wall box 300 x 200 x 150 and show me the sources behind the recyclable claim."
- "Which RAJA box matches supplier ref SB-300-200-150-K and is active in Germany?"
- "Why is this product flagged for FSC wording but approved for recyclable wording?"

### What is missing before enrichment

- No commercial long description
- No customer benefits or use cases
- No SEO content
- No English, German, Spanish, or Italian content package
- Raw category code not yet mapped to the e-commerce taxonomy presented to business users
- Compliance wording not yet filtered for allowed versus disallowed claims

> *This is the gap the grounded workflow closes in under 30 seconds.*

---

## Example Output

### Short Description

Single-wall cardboard shipping box for light to medium goods, with recycled material content and dimensions suited to standard e-commerce and logistics workflows.

### Long Description

This single-wall cardboard shipping box is designed for the efficient dispatch of light to medium-weight items. Its 300 x 200 x 150 mm format supports standard packing operations while limiting unnecessary empty space. The brown corrugated construction is easy to store flat, quick to assemble, and suitable for day-to-day shipping workflows. Based on the available source data, the product can be described as recyclable and containing recycled material, while certification claims remain controlled by compliance rules.

### Customer Benefits

- Reliable everyday protection for shipped items
- Fast assembly in packing operations
- Flat storage saves warehouse space
- Format helps reduce void fill needs
- Suitable for standard parcel workflows

### SEO

| Field | Value |
|---|---|
| H1 | Single-Wall Cardboard Shipping Box 300 x 200 x 150 mm |
| Meta | Single-wall cardboard shipping box with recycled material content, designed for efficient and reliable everyday parcel dispatch. |
| Primary keyword | single-wall cardboard shipping box |
| Secondary keywords | corrugated shipping box, recycled cardboard box, carton 300 x 200 x 150, ecommerce shipping carton, brown parcel box |

### Quality and grounding summary

| Check | Result |
|---|---|
| Factual consistency | Passed |
| Unsupported claims | FSC wording flagged and removed |
| Citation coverage | 92/100 |
| Translation drift | No critical issue detected |
| Publication status | Approved with compliance notes |

---

## Appendix — Sample Reference Links

### Agent Framework

- https://github.com/microsoft/agent-framework/tree/main/python/packages/foundry/agent_framework_foundry
- https://github.com/microsoft/agent-framework/tree/main/python/samples/03-workflows/orchestrations
- https://github.com/microsoft/agent-framework/tree/main/python/samples
- https://github.com/microsoft/agent-framework/tree/main/python/samples/02-agents/devui

### Suggested talking point for the appendix

These links are useful to support the implementation story during follow-up discussions. They show that the demo aligns with current Agent Framework Python patterns for Foundry integration, workflow orchestration, general samples, and local developer UI experiences.

---

*End of document*
- Normalize color names to RAJA's color palette labels.
- Expand compliance fields to approved RAJA compliance tags.

Return:
- normalized_product_json
- normalization_notes
- assumptions
- citations

Rules:
- Flag every assumption explicitly.
- Do not enrich or generate commercial copy.
- Return valid JSON only.
```

---

### Agent 4 — Product Enrichment Agent

```text
You are a senior product content writer for RAJA Group, specializing in packaging and logistics products.

Your input is a normalized product JSON plus grounded source excerpts.
Generate complete, accurate, and commercially useful product content.

Generate:
- short_description (max 30 words)
- long_description (80-120 words)
- customer_benefits (array of 4-5 bullets, max 12 words each)
- recommended_use_cases (array of 3-5 strings)
- industry_applications (array of 3 industries)
- cross_sell_suggestions (array of 2-3 product types)
- upsell_suggestion (string)

Rules:
- Every meaningful claim must be supported by input data or cited source evidence.
- Tone: professional, clear, practical.
- No superlatives, no invented specifications, no unsupported compliance claims.
- Return valid JSON only.
```

---

### Agent 5 — SEO Agent

```text
You are an e-commerce SEO specialist for RAJA Group.

Your input is enriched product content in JSON.
Generate SEO metadata optimized for B2B packaging and logistics searches.

Generate:
- h1 (max 60 characters)
- h2_list (array of 2-3 strings)
- meta_description (140-160 characters)
- primary_keyword (string)
- secondary_keywords (array of 4-6 strings)
- seo_notes (string)

Rules:
- Optimize for B2B buyer intent.
- Avoid keyword stuffing.
- Keep wording aligned with validated product facts.
- Return valid JSON only.
```

---

### Agent 6 — Multilingual Agent

```text
You are a multilingual product content specialist for RAJA Group.

Your input is validated English product content in JSON.
Produce culturally adapted versions in English, German, Spanish, and Italian.

For each language, adapt:
- short_description
- long_description
- customer_benefits
- meta_description

Register guidelines:
- English: concise, clear, B2B practical
- German: precise, technical, formal
- Spanish: clear, professional, slightly warmer
- Italian: descriptive, commercial, relationship-oriented

Rules:
- Do not translate specifications incorrectly.
- Preserve SKU, dimensions, weights, and supported claims.
- Flag any untranslatable or risky term.
- Return valid JSON only.
```

---

### Agent 7 — Quality & Compliance Agent

```text
You are a content quality and compliance reviewer for RAJA Group.

Your input is fully enriched, multilingual product content in JSON with citations.
Validate all content against RAJA's editorial and compliance standards.

Run these checks:
1. Factual consistency
2. Tone of voice
3. Forbidden or unsupported claims
4. Length compliance
5. Cross-language consistency
6. Citation coverage

Return:
- status: approved | flagged
- checks_passed
- flags (array: field, language, issue, recommendation)
- overall_confidence_score (0-100)
- citation_coverage_score (0-100)

Be conservative. Flag uncertainty. Do not rewrite; flag and recommend only.
```

---

### Agent 8 — Publication Agent

```text
You are a product content publication specialist for RAJA Group.

Your input is approved, multilingual product content in JSON.
Format it into the required schemas for each publication channel.

Generate:
1. ecommerce_json — full structured record for PIM/CMS
2. marketplace_ready — flat JSON
3. crm_short — plain text paragraph, max 60 words, English only
4. catalog_text_block — plain text with H1, short description, benefit bullets, dimensions, SKU

Rules:
- Do not add content not in the input.
- Respect field length limits.
- Preserve run_id and citation references for audit purposes.
- Return all four formats in one JSON object.
```

---

## Realistic Demo Data

The demo will be stronger if it uses a realistic multi-source product record rather than a single synthetic row.

### Primary product used in the demo

| Field | Value |
|---|---|
| SKU | RAJA-FR-SW-302015-R |
| Supplier Ref | SB-300-200-150-K |
| Short Label (IQ) | Crt simple cannelure brun rec 300x200x150 |
| Category (IQ) | CTN-SW-BR |
| Dimensions | 300 x 200 x 150 mm |
| Weight | 382 g |
| Material | Carton ondule simple cannelure, 70% recycle |
| Color | Brun |
| Pack Quantity | 25 |
| Market Availability | FR, BE, ES, IT, DE |
| Compliance | Recycle, FSC mix pending verification |
| Publication Status | Draft |
| Last Modified | 2026-03-12 |
| Modified By | Import automatique IQ |

### Additional source snippets indexed in Foundry IQ

**Supplier technical sheet excerpt**

> Product code SB-300-200-150-K. Single-wall corrugated shipping carton. Internal dimensions 300 x 200 x 150 mm. Recommended for light to medium goods. Brown kraft finish. Supplied flat for storage efficiency.

**RAJA taxonomy reference**

| Raw Category | RAJA Category | Approved Label |
|---|---|---|
| CTN-SW-BR | Shipping > Cartons > Single-wall | Single-wall cardboard shipping box |

**Compliance reference**

| Claim | Allowed? | Condition |
|---|---|---|
| Recycled material | Yes | If supplier declaration exists |
| FSC certified | No | Only if valid certificate ID is present |
| Recyclable | Yes | Allowed for corrugated cardboard |

**ERP / stock feed excerpt**

| SKU | Available Stock | Lead Time | Market Status |
|---|---|---|---|
| RAJA-FR-SW-302015-R | 4,850 | 48 hours | Active |

### Demo smart query examples using this data

- "Find the recycled single-wall box 300 x 200 x 150 and show me the sources behind the recyclable claim."
- "Which RAJA box matches supplier ref SB-300-200-150-K and is active in Germany?"
- "Why is this product flagged for FSC wording but approved for recyclable wording?"

### What is missing before enrichment

- No commercial long description
- No customer benefits or use cases
- No SEO content
- No English, German, Spanish, or Italian content package
- Raw category code not yet mapped to the e-commerce taxonomy presented to business users
- Compliance wording not yet filtered for allowed versus disallowed claims

> *This is the gap the grounded workflow closes in under 30 seconds.*

---

## Example Output

### Short Description

Single-wall cardboard shipping box for light to medium goods, with recycled material content and dimensions suited to standard e-commerce and logistics workflows.

### Long Description

This single-wall cardboard shipping box is designed for the efficient dispatch of light to medium-weight items. Its 300 x 200 x 150 mm format supports standard packing operations while limiting unnecessary empty space. The brown corrugated construction is easy to store flat, quick to assemble, and suitable for day-to-day shipping workflows. Based on the available source data, the product can be described as recyclable and containing recycled material, while certification claims remain controlled by compliance rules.

### Customer Benefits

- Reliable everyday protection for shipped items
- Fast assembly in packing operations
- Flat storage saves warehouse space
- Format helps reduce void fill needs
- Suitable for standard parcel workflows

### SEO

| Field | Value |
|---|---|
| H1 | Single-Wall Cardboard Shipping Box 300 x 200 x 150 mm |
| Meta | Single-wall cardboard shipping box with recycled material content, designed for efficient and reliable everyday parcel dispatch. |
| Primary keyword | single-wall cardboard shipping box |
| Secondary keywords | corrugated shipping box, recycled cardboard box, carton 300 x 200 x 150, ecommerce shipping carton, brown parcel box |

### Quality and grounding summary

| Check | Result |
|---|---|
| Factual consistency | Passed |
| Unsupported claims | FSC wording flagged and removed |
| Citation coverage | 92/100 |
| Translation drift | No critical issue detected |
| Publication status | Approved with compliance notes |

---

## Appendix — Sample Reference Links

### Agent Framework

- https://github.com/microsoft/agent-framework/tree/main/python/packages/foundry/agent_framework_foundry
- https://github.com/microsoft/agent-framework/tree/main/python/samples/03-workflows/orchestrations
- https://github.com/microsoft/agent-framework/tree/main/python/samples
- https://github.com/microsoft/agent-framework/tree/main/python/samples/02-agents/devui

### Suggested talking point for the appendix

These links are useful to support the implementation story during follow-up discussions. They show that the demo aligns with current Agent Framework Python patterns for Foundry integration, workflow orchestration, general samples, and local developer UI experiences.

---

*End of document*
