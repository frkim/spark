
# Microsoft Foundry × RAJA — Intelligent Product Content Pipeline

**Author:** François-Xavier Kim, Solution Engineer, Microsoft France
**Date:** April 2026
**Classification:** Microsoft Confidential — For RAJA Use Only

---

## Table of Contents

1. [Scenario Overview](#scenario-overview)
2. [Agentic Architecture](#agentic-architecture)
3. [Full Demo Script](#full-demo-script)
4. [Technical Architecture Description](#technical-architecture-description)
5. [Agent Prompt Designs](#agent-prompt-designs)
6. [Sample Raw IQ Product Sheet](#sample-raw-iq-product-sheet)
7. [Example Output](#example-output)

---

## Scenario Overview

A RAJA product manager uploads or selects a **raw product sheet** from IQ.

The sheet is incomplete, technical, and not ready for e-commerce.

Microsoft Foundry orchestrates a set of specialized agents that transform this raw input into a **fully enriched product sheet** — in under 30 seconds.

**Key business value:**
- Eliminates 20–45 minutes of manual work per product record
- Scales to thousands of SKUs per day
- Delivers SEO-optimized, multilingual content consistently
- Human review only for flagged exceptions

---

## Agentic Architecture

| # | Agent | Role |
|---|---|---|
| 1 | IQ Extraction Agent | Pulls structured attributes from IQ (dimensions, material, weight, category, compliance) |
| 2 | Normalization Agent | Harmonizes units, labels, categories, and RAJA naming conventions |
| 3 | Product Enrichment Agent | Generates descriptions, benefits, use cases, cross-sell, up-sell |
| 4 | SEO Agent | Creates meta descriptions, keywords, H1/H2 structure |
| 5 | Multilingual Agent | Produces EN/DE/ES/IT versions with cultural adaptation |
| 6 | Quality & Compliance Agent | Checks accuracy, tone, forbidden claims, RAJA guidelines |
| 7 | Publication Agent | Formats output for e-commerce, CRM, marketplaces, catalog PDFs |

**Pipeline flow:**

```
[Raw IQ Record]
      │
      ▼
IQ Extraction Agent
      │
      ▼
Normalization Agent
      │
      ▼
Product Enrichment Agent
      │
    ┌─┴───────────────┐
    ▼                 ▼
SEO Agent     Multilingual Agent
(parallel)    EN / DE / ES / IT
    └─────────┬───────┘
              ▼
Quality & Compliance Agent
              │
              ▼ (approved)
     Publication Agent
              │
    ┌─────────┼─────────┬──────────┐
    ▼         ▼         ▼          ▼
PIM JSON  Marketplace  CRM      Catalog
          Ready        Short    PDF Block
```

---

## Full Demo Script

**Audience:** RAJA product/digital team + decision-makers
**Duration:** ~20 minutes live demo

---

### Opening (2 min)

> "Thank you for having us today. What I want to show you is not a concept — it's a working pipeline built on Microsoft Foundry that addresses a problem every product team in your industry faces: turning raw technical data into high-quality, market-ready product content, at scale, across languages.
>
> We've built this specifically around your context — a large catalog, multiple markets, strong editorial standards, and constant update pressure.
>
> Let me walk you through it live."

---

### Step 1 — Load a Raw IQ Product (2 min)

*Show the raw IQ product sheet on screen*

> "This is what comes out of IQ today — a raw product record. Dimensions, SKU, material, weight. It's accurate, but it's not usable for e-commerce, marketplaces, or your catalog without significant manual work.
>
> A product manager today would spend 20 to 45 minutes enriching a single record like this. Multiply that by your catalog size, and you understand the bottleneck.
>
> What Foundry does is orchestrate a chain of specialized agents that handle this entire transformation — automatically, in under 30 seconds."

---

### Step 2 — Extraction & Normalization (3 min)

*Trigger the pipeline. Show the Extraction Agent output.*

> "The first agent — the IQ Extraction Agent — reads the raw record and pulls out every structured attribute: dimensions in normalized units, material classification, weight, category, compliance flags.
>
> The Normalization Agent then maps these to RAJA's internal taxonomy. Units are standardized. Categories are aligned. Labels follow your naming conventions — not the supplier's.
>
> What you're seeing here is clean, structured JSON. This is the foundation everything else builds on."

---

### Step 3 — Product Enrichment (4 min)

*Show the Enrichment Agent output.*

> "This is where the business value becomes visible.
>
> The Product Enrichment Agent generates a short description, a long description, customer benefits, recommended use cases, and cross-sell and up-sell suggestions — all grounded in the structured data we just extracted.
>
> Notice what it does NOT do: it doesn't hallucinate specifications. Every claim traces back to a verified attribute.
>
> This is enterprise-grade content generation — controlled, traceable, auditable."

---

### Step 4 — SEO Optimization (2 min)

*Show SEO Agent output.*

> "The SEO Agent takes the enriched content and adds the layer your digital team would otherwise handle manually: meta description, keyword set, H1 and H2 structure, search-optimized phrasing.
>
> This runs on every single product in the pipeline — not just the high-priority SKUs."

---

### Step 5 — Multilingual Expansion (3 min)

*Show the four language tabs: EN / DE / ES / IT.*

> "One click. Four markets.
>
> The Multilingual Agent doesn't just translate — it adapts. Tone, register, and phrasing are adjusted for each market. German buyers expect precision and technical detail. Spanish content leans warmer. Italian copy is typically more descriptive.
>
> This is not Google Translate. It's culturally adapted content, generated in seconds."

---

### Step 6 — Quality & Compliance (2 min)

*Show the Quality Agent report.*

> "Before anything is published, the Quality and Compliance Agent runs a full check: factual consistency against the source attributes, tone of voice alignment with RAJA's editorial guidelines, and a scan for forbidden claims.
>
> Any flag is surfaced here, with a specific recommendation. The product manager reviews only the exceptions — not every record."

---

### Step 7 — Publication (2 min)

*Show the multi-format output panel.*

> "The final output is not a single document. It's a structured payload ready for each channel:
>
> - E-commerce JSON for your PIM or website
> - A marketplace-ready version for Amazon, Cdiscount, or others
> - A short CRM version for sales team use
> - A catalog text block formatted for print or PDF generation
>
> One source. Multiple formats. Zero reformatting work."

---

### Closing (1 min)

> "What you've just seen is a pipeline that runs in under 30 seconds per product. At your catalog scale, that translates to thousands of enriched, SEO-optimized, multilingual product records per day — with full auditability and human review only where it's needed.
>
> Microsoft Foundry makes this orchestration possible. The agents are configurable to your specific rules, your taxonomy, your markets.
>
> We'd love to scope a proof of concept around a real subset of your catalog. What product family would be the most valuable to start with?"

---

## Technical Architecture Description

### Key Architectural Principles

| Principle | Detail |
|---|---|
| Orchestrator | Microsoft Foundry manages agent sequencing, retries, and state |
| Parallelism | SEO and Multilingual agents run concurrently after Enrichment |
| Grounding | Every agent receives normalized JSON as its source of truth |
| Auditability | Each agent step produces a versioned output stored in Foundry |
| Human-in-the-loop | Quality Agent flags exceptions; only flagged records require human review |
| Configurability | Taxonomy, tone rules, and forbidden terms are RAJA-specific config files |
| Output adapters | Publication Agent formats to target system schemas (PIM, marketplace, CRM) |

### Stage-by-Stage Description

**Stage 1 — IQ Extraction Agent**
Reads the raw IQ product record and extracts all structured attributes into a normalized JSON object: SKU, dimensions, weight, material, color, category, compliance flags.

**Stage 2 — Normalization Agent**
Maps extracted attributes to RAJA's internal taxonomy. Standardizes units (all dimensions to mm, all weights to grams). Aligns category codes to RAJA's e-commerce structure. Flags any mapping assumptions for human review.

**Stage 3 — Product Enrichment Agent**
Generates commercial content grounded entirely in the normalized data. Every claim is traceable to a source attribute. Produces: short description, long description, customer benefits, use cases, industry applications, cross-sell and up-sell suggestions.

**Stage 4A — SEO Agent (parallel)**
Generates H1, H2s, meta description, primary keyword, and secondary keywords optimized for B2B packaging and logistics searches.

**Stage 4B — Multilingual Agent (parallel)**
Produces culturally adapted translations in German, Spanish, and Italian. Register and tone are adapted per market — not literal translation.

**Stage 5 — Quality & Compliance Agent**
Validates all content: factual consistency, tone of voice, forbidden claims, length targets, cross-language consistency. Outputs approved/flagged status with specific recommendations.

**Stage 6 — Publication Agent**
Formats approved content into four output schemas ready for downstream systems.

---

## Agent Prompt Designs

### Agent 1 — IQ Extraction Agent

```
You are a product data extraction specialist for RAJA Group.

Your input is a raw product record from the IQ catalog system.
Your task is to extract and return a structured JSON object containing all identifiable attributes.

Always extract the following fields when present:
- sku (string)
- product_label (string, original)
- dimensions_mm (object: length, width, height)
- weight_g (integer)
- material (string)
- color (string)
- category_raw (string, as found in source)
- compliance_flags (array of strings)
- supplier_ref (string, if present)

Rules:
- Do not infer values not present in the source.
- If a field is absent, set its value to null.
- Do not reformat or interpret — extract only.
- Return valid JSON only. No commentary.
```

---

### Agent 2 — Normalization Agent

```
You are a product data normalization specialist for RAJA Group.

Your input is a JSON object extracted from a raw IQ product record.
Your task is to normalize this data according to RAJA's internal standards.

Apply the following normalizations:
- Convert all dimensions to millimeters (mm).
- Convert all weights to grams (g).
- Map category_raw to the closest RAJA catalog category using the provided taxonomy.
- Standardize material names to RAJA's approved material vocabulary.
- Normalize color names to RAJA's color palette labels.
- Expand compliance_flags to full RAJA compliance tags.

Return the normalized JSON with added fields:
- raja_category (string)
- normalization_notes (array)

Rules:
- Flag any field where normalization required an assumption.
- Do not enrich or generate new content — normalize only.
- Return valid JSON only.
```

---

### Agent 3 — Product Enrichment Agent

```
You are a senior product content writer for RAJA Group, specializing in packaging and logistics products.

Your input is a normalized product JSON.
Generate complete, accurate, and commercially compelling product content.

Generate:
- short_description (max 30 words)
- long_description (80–120 words)
- customer_benefits (array of 4–5 bullets, max 12 words each)
- recommended_use_cases (array of 3–5 strings)
- industry_applications (array of 3 industries)
- cross_sell_suggestions (array of 2–3 product types)
- upsell_suggestion (string)

Rules:
- Every claim must be grounded in the input JSON.
- Tone: professional, clear, practical. No superlatives or marketing clichés.
- Do not mention competitor products or brands.
- Do not make regulatory claims unless a compliance_flag supports them.
- Return valid JSON only.
```

---

### Agent 4 — SEO Agent

```
You are an e-commerce SEO specialist for RAJA Group.

Your input is enriched product content in JSON.
Generate SEO metadata optimized for B2B packaging and logistics searches.

Generate:
- h1 (max 60 characters, keyword-rich)
- h2_list (array of 2–3 strings)
- meta_description (140–160 characters, benefit-led)
- primary_keyword (string)
- secondary_keywords (array of 4–6 strings)
- seo_notes (string)

Rules:
- Prioritize B2B buyer search terms.
- Avoid keyword stuffing. Optimize for intent.
- Meta description must be a complete, natural sentence.
- Return valid JSON only.
```

---

### Agent 5 — Multilingual Agent

```
You are a multilingual product content specialist for RAJA Group.

Your input is enriched product content in English.
Produce culturally adapted translations in: German (de), Spanish (es), Italian (it).

For each language, adapt: short_description, long_description, customer_benefits, meta_description.

Register guidelines:
- German: precise, technical, formal register
- Spanish: clear, professional, slightly warmer register
- Italian: descriptive, commercial, relationship-oriented register

Rules:
- Do not translate specifications — keep dimensions, weights, SKU as-is.
- Preserve RAJA brand tone: professional, practical, reliable.
- Flag any untranslatable term.
- Return JSON with keys: "de", "es", "it".
```

---

### Agent 6 — Quality & Compliance Agent

```
You are a content quality and compliance reviewer for RAJA Group.

Your input is fully enriched, multilingual product content in JSON.
Validate all content against RAJA's editorial and compliance standards.

Run these checks:
1. Factual consistency — claims must match normalized source JSON
2. Tone of voice — professional, no unverifiable superlatives
3. Forbidden claims — flag environmental/safety claims without compliance_flag support
4. Length compliance — verify field length targets are met
5. Cross-language consistency — no new claims introduced in translations

Return:
- status: "approved" | "flagged"
- checks_passed (array)
- flags (array: field, language, issue, recommendation)
- overall_confidence_score (0–100)

Be conservative. Flag uncertainty. Do not rewrite — flag and recommend only.
```

---

### Agent 7 — Publication Agent

```
You are a product content publication specialist for RAJA Group.

Your input is approved, multilingual product content in JSON.
Format it into the required schemas for each publication channel.

Generate:
1. ecommerce_json — full structured record for PIM/CMS
2. marketplace_ready — flat JSON (product_label max 200 chars, short_description max 150 chars)
3. crm_short — plain text paragraph, max 60 words, English only
4. catalog_text_block — plain text with H1, short description, benefit bullets, dimensions, SKU

Rules:
- Do not add content not in the input.
- Respect all field length limits.
- Return all four formats in one JSON object.
```

---

## Sample Raw IQ Product Sheet

*This is the "before" state shown at the start of the demo.*

| Field | Value |
|---|---|
| SKU | RAJA-12345 |
| Supplier Ref | SB-300-200-150-K |
| Short Label | Crt simple cannelure brun rec 300x200x150 |
| Category (IQ) | CTN-SW-BR |
| Dimensions | 300 × 200 × 150 mm |
| Weight | 380 g |
| Material | Carton ondulé simple cannelure |
| Color | Brun |
| Compliance | Recyclé |
| Certification | — |
| Long Description | *(empty)* |
| Benefits | *(empty)* |
| SEO | *(empty)* |
| Languages | FR only |
| Publication Status | Draft |
| Last Modified | 2026-03-12 |
| Modified By | Import automatique IQ |

**What is missing:**
- No commercial description
- No customer benefits or use cases
- No SEO content
- No English, German, Spanish, or Italian versions
- Category code is internal — not mapped to e-commerce taxonomy
- Label is technical shorthand, not publishable copy

> *This is the gap Foundry closes in under 30 seconds.*

---

## Example Output

### Short Description

Durable single-wall cardboard box ideal for shipping lightweight to medium-weight products. Made from 100% recycled material.

### Long Description

This single-wall cardboard box is designed for efficient and secure shipping of lightweight to medium-weight items. Its recycled cardboard structure ensures both strength and sustainability. Easy to assemble and compatible with standard carriers, it fits seamlessly into RAJA's logistics workflows.

### Customer Benefits

- Reliable protection for everyday shipments
- Quick and easy assembly
- Eco-friendly recycled material
- Optimized dimensions to reduce empty space

### SEO

| Field | Value |
|---|---|
| H1 | Single-Wall Cardboard Box 300×200×150 mm |
| Meta | Single-wall cardboard box 300×200×150 mm — ideal for secure and sustainable shipping. |
| Primary keyword | cardboard box |
| Secondary keywords | shipping box, single-wall packaging, recycled packaging, box 300x200, e-commerce box |

---

*End of document*
