"""Streamlit UI — RAJA Intelligent Product Content Pipeline demo."""

from __future__ import annotations

import asyncio
import json
from typing import Any

import streamlit as st

from demo_data import SMART_QUERY_EXAMPLES
from pipeline import ProductContentPipeline, STEPS

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="RAJA × Microsoft Foundry — Product Content Pipeline",
    page_icon="📦",
    layout="wide",
)

# ---------------------------------------------------------------------------
# State initialisation
# ---------------------------------------------------------------------------
if "pipeline_result" not in st.session_state:
    st.session_state.pipeline_result = None
    st.session_state.trace = None

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/Microsoft_logo.svg/512px-Microsoft_logo.svg.png", width=160)
    st.markdown("## RAJA × Microsoft Foundry")
    st.caption("Intelligent Product Content Pipeline")
    st.divider()
    st.markdown("### Smart Query Examples")
    for i, q in enumerate(SMART_QUERY_EXAMPLES):
        if st.button(q, key=f"example_{i}", use_container_width=True):
            st.session_state["query_input"] = q
    st.divider()
    st.markdown(
        "**Architecture:** 8 specialised agents orchestrated in a "
        "sequential + parallel workflow pattern (Agent Framework)."
    )
    st.markdown(
        "**Grounding:** Foundry IQ multi-source retrieval with citations."
    )

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.title("📦 Intelligent Product Content Pipeline")
st.markdown(
    "Transform raw product data into **enriched, SEO-ready, multilingual content** "
    "in seconds — grounded on enterprise data, with full traceability."
)

# ---------------------------------------------------------------------------
# Query input
# ---------------------------------------------------------------------------
query = st.text_input(
    "Enter a product query or select an example from the sidebar:",
    key="query_input",
    placeholder="e.g. Show me the recycled single-wall carton 300 x 200 x 150 active for France and Germany",
)

col_run, col_clear = st.columns([1, 1])
with col_run:
    run_btn = st.button("🚀 Run Pipeline", type="primary", disabled=not query, use_container_width=True)
with col_clear:
    if st.button("🗑️ Clear Results", use_container_width=True):
        st.session_state.pipeline_result = None
        st.session_state.trace = None
        st.rerun()

# ---------------------------------------------------------------------------
# Pipeline execution
# ---------------------------------------------------------------------------

STEP_ICONS = {
    "smart_query_intake": "🔍",
    "foundry_iq_retrieval": "📚",
    "normalization": "⚙️",
    "product_enrichment": "✏️",
    "seo": "📈",
    "multilingual": "🌍",
    "quality_compliance": "✅",
    "publication": "📤",
}


def _run_pipeline(user_query: str) -> tuple[dict[str, Any], dict]:
    """Execute the pipeline synchronously (called from Streamlit)."""
    pipeline = ProductContentPipeline()

    step_results: dict[str, Any] = {}

    def on_step(key: str, status: str, data: dict | None = None) -> None:
        if data:
            step_results[key] = data

    loop = asyncio.new_event_loop()
    try:
        ctx, tracer = loop.run_until_complete(
            pipeline.run(user_query, on_step=on_step)
        )
    finally:
        loop.close()

    return ctx, tracer.summary()


if run_btn and query:
    with st.status("Running pipeline…", expanded=True) as status_ui:
        for key, label in STEPS:
            st.write(f"{STEP_ICONS.get(key, '•')} {label}…")

        ctx, trace = _run_pipeline(query)
        st.session_state.pipeline_result = ctx
        st.session_state.trace = trace

        errors = [k for k in ctx if isinstance(ctx[k], dict) and "error" in ctx[k]]
        if errors:
            status_ui.update(label="Pipeline completed with errors", state="error")
        else:
            status_ui.update(label="Pipeline complete!", state="complete")

# ---------------------------------------------------------------------------
# Results display
# ---------------------------------------------------------------------------
ctx = st.session_state.pipeline_result
trace = st.session_state.trace

if ctx:
    st.divider()

    # --- Pipeline flow visualisation ---
    cols = st.columns(len(STEPS))
    for i, (key, label) in enumerate(STEPS):
        with cols[i]:
            icon = STEP_ICONS.get(key, "•")
            has_error = isinstance(ctx.get(key), dict) and "error" in ctx.get(key, {})
            color = "red" if has_error else "green"
            st.markdown(f":{color}[{icon}]  \n**{label}**")

    st.divider()

    # --- Tabs for detailed results ---
    tabs = st.tabs([
        "📋 Enrichment",
        "📈 SEO",
        "🌍 Multilingual",
        "✅ Quality",
        "📤 Publication",
        "🔍 Trace & Monitoring",
        "🗂️ Full JSON",
    ])

    # -- Enrichment --------------------------------------------------------
    with tabs[0]:
        enrichment = ctx.get("enrichment", {})
        if "error" in enrichment:
            st.error(enrichment["error"])
        else:
            st.subheader("Short Description")
            st.info(enrichment.get("short_description", "N/A"))

            st.subheader("Long Description")
            st.write(enrichment.get("long_description", "N/A"))

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Customer Benefits")
                for b in enrichment.get("customer_benefits", []):
                    st.markdown(f"- {b}")

                st.subheader("Industry Applications")
                for a in enrichment.get("industry_applications", []):
                    st.markdown(f"- {a}")

            with col2:
                st.subheader("Recommended Use Cases")
                for u in enrichment.get("recommended_use_cases", []):
                    st.markdown(f"- {u}")

                st.subheader("Cross-Sell / Up-Sell")
                for c in enrichment.get("cross_sell_suggestions", []):
                    st.markdown(f"- {c}")
                upsell = enrichment.get("upsell_suggestion")
                if upsell:
                    st.markdown(f"**Up-sell:** {upsell}")

    # -- SEO ---------------------------------------------------------------
    with tabs[1]:
        seo = ctx.get("seo", {})
        if "error" in seo:
            st.error(seo["error"])
        else:
            st.subheader("H1")
            st.code(seo.get("h1", "N/A"))
            st.subheader("H2 List")
            for h in seo.get("h2_list", []):
                st.markdown(f"- {h}")
            st.subheader("Meta Description")
            meta = seo.get("meta_description", "N/A")
            st.info(f"{meta}  \n*({len(meta)} chars)*")
            st.subheader("Keywords")
            st.write(f"**Primary:** {seo.get('primary_keyword', 'N/A')}")
            st.write(f"**Secondary:** {', '.join(seo.get('secondary_keywords', []))}")
            notes = seo.get("seo_notes")
            if notes:
                st.caption(notes)

    # -- Multilingual ------------------------------------------------------
    with tabs[2]:
        ml = ctx.get("multilingual", {})
        if "error" in ml:
            st.error(ml["error"])
        else:
            lang_tabs = st.tabs(["🇬🇧 English", "🇩🇪 German", "🇪🇸 Spanish", "🇮🇹 Italian"])
            for lt, code in zip(lang_tabs, ["en", "de", "es", "it"]):
                with lt:
                    lang_data = ml.get(code, {})
                    st.markdown(f"**Short:** {lang_data.get('short_description', 'N/A')}")
                    st.markdown(f"**Long:** {lang_data.get('long_description', 'N/A')}")
                    benefits = lang_data.get("customer_benefits", [])
                    if benefits:
                        st.markdown("**Benefits:**")
                        for b in benefits:
                            st.markdown(f"- {b}")
                    st.markdown(f"**Meta:** {lang_data.get('meta_description', 'N/A')}")
            flags = ml.get("translation_flags", [])
            if flags:
                st.warning("Translation flags:")
                for f in flags:
                    st.write(f"⚠️ **{f.get('field')}** ({f.get('language')}): {f.get('issue')}")

    # -- Quality -----------------------------------------------------------
    with tabs[3]:
        quality = ctx.get("quality", {})
        if "error" in quality:
            st.error(quality["error"])
        else:
            status = quality.get("status", "unknown")
            if status == "approved":
                st.success(f"Status: **{status.upper()}**")
            else:
                st.warning(f"Status: **{status.upper()}**")

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Confidence Score", f"{quality.get('overall_confidence_score', 'N/A')}/100")
            with col2:
                st.metric("Citation Coverage", f"{quality.get('citation_coverage_score', 'N/A')}/100")

            st.subheader("Checks Passed")
            for c in quality.get("checks_passed", []):
                st.markdown(f"✅ {c}")

            flags = quality.get("flags", [])
            if flags:
                st.subheader("Flags")
                for f in flags:
                    st.warning(
                        f"**{f.get('field', '?')}** ({f.get('language', '—')}): "
                        f"{f.get('issue', '?')}  \n"
                        f"*Recommendation:* {f.get('recommendation', '—')}"
                    )

    # -- Publication -------------------------------------------------------
    with tabs[4]:
        pub = ctx.get("publication", {})
        if "error" in pub:
            st.error(pub["error"])
        else:
            pub_tabs = st.tabs(["PIM / CMS JSON", "Marketplace", "CRM Short", "Catalog Text"])
            with pub_tabs[0]:
                st.json(pub.get("ecommerce_json", {}))
            with pub_tabs[1]:
                st.json(pub.get("marketplace_ready", {}))
            with pub_tabs[2]:
                st.text(pub.get("crm_short", "N/A"))
            with pub_tabs[3]:
                st.text(pub.get("catalog_text_block", "N/A"))

    # -- Trace & Monitoring ------------------------------------------------
    with tabs[5]:
        if trace:
            st.subheader("Pipeline Trace")
            st.caption(f"Run ID: `{trace['run_id']}`")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Latency", f"{trace['total_latency_ms']:.0f} ms")
            with col2:
                st.metric("Total Tokens", trace["total_tokens"])
            with col3:
                st.metric("Agents", len(trace["spans"]))

            st.subheader("Per-Agent Breakdown")
            for s in trace["spans"]:
                icon = STEP_ICONS.get(s["agent"], "•")
                status_icon = "✅" if s["status"] == "ok" else "❌"
                with st.expander(f"{icon} {s['agent']} — {s['latency_ms']:.0f} ms {status_icon}"):
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Latency", f"{s['latency_ms']:.0f} ms")
                    c2.metric("Tokens", s["tokens"])
                    c3.metric("Status", s["status"])
                    if s["flags"]:
                        st.warning(f"Flags: {', '.join(s['flags'])}")

            # Latency chart
            st.subheader("Latency Distribution")
            import pandas as pd

            df = pd.DataFrame(trace["spans"])
            st.bar_chart(df.set_index("agent")["latency_ms"])
        else:
            st.info("Run the pipeline to see trace data.")

    # -- Full JSON ---------------------------------------------------------
    with tabs[6]:
        st.json(ctx)
