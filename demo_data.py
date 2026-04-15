"""Realistic demo data from multiple enterprise sources — simulates Foundry IQ grounding."""

# ---------------------------------------------------------------------------
# Primary product record (IQ export)
# ---------------------------------------------------------------------------
IQ_PRODUCT_EXPORT = {
    "sku": "RAJA-FR-SW-302015-R",
    "supplier_ref": "SB-300-200-150-K",
    "short_label": "Crt simple cannelure brun rec 300x200x150",
    "category_code": "CTN-SW-BR",
    "dimensions_mm": {"length": 300, "width": 200, "height": 150},
    "weight_g": 382,
    "material_raw": "Carton ondulé simple cannelure, 70 % recyclé",
    "color_raw": "Brun",
    "pack_quantity": 25,
    "market_availability": ["FR", "BE", "ES", "IT", "DE"],
    "compliance_raw": "Recyclé, FSC mix pending verification",
    "publication_status": "Draft",
    "last_modified": "2026-03-12",
    "modified_by": "Import automatique IQ",
}

# ---------------------------------------------------------------------------
# Supplier technical sheet
# ---------------------------------------------------------------------------
SUPPLIER_TECHNICAL_SHEET = {
    "source_id": "SUPPLIER-TECH-SB300",
    "source_type": "supplier_technical_sheet",
    "supplier_ref": "SB-300-200-150-K",
    "excerpt": (
        "Product code SB-300-200-150-K. Single-wall corrugated shipping carton. "
        "Internal dimensions 300 x 200 x 150 mm. Recommended for light to medium "
        "goods. Brown kraft finish. Supplied flat for storage efficiency."
    ),
}

# ---------------------------------------------------------------------------
# RAJA taxonomy reference
# ---------------------------------------------------------------------------
TAXONOMY_REFERENCE = {
    "source_id": "TAXONOMY-CTN-SW-BR",
    "source_type": "raja_taxonomy",
    "mappings": [
        {
            "raw_category": "CTN-SW-BR",
            "raja_category": "Shipping > Cartons > Single-wall",
            "approved_label": "Single-wall cardboard shipping box",
        }
    ],
}

# ---------------------------------------------------------------------------
# Compliance & sustainability reference
# ---------------------------------------------------------------------------
COMPLIANCE_REFERENCE = {
    "source_id": "COMPLIANCE-REF-2026",
    "source_type": "compliance_reference",
    "rules": [
        {
            "claim": "Recycled material",
            "allowed": True,
            "condition": "If supplier declaration exists",
        },
        {
            "claim": "FSC certified",
            "allowed": False,
            "condition": "Only if valid certificate ID is present",
        },
        {
            "claim": "Recyclable",
            "allowed": True,
            "condition": "Allowed for corrugated cardboard",
        },
    ],
}

# ---------------------------------------------------------------------------
# ERP / stock feed
# ---------------------------------------------------------------------------
ERP_STOCK_FEED = {
    "source_id": "ERP-STOCK-2026Q2",
    "source_type": "erp_stock_feed",
    "sku": "RAJA-FR-SW-302015-R",
    "available_stock": 4850,
    "lead_time": "48 hours",
    "market_status": "Active",
}

# ---------------------------------------------------------------------------
# Existing RAJA catalog content (legacy)
# ---------------------------------------------------------------------------
CATALOG_HISTORY = {
    "source_id": "CATALOG-LEGACY-CTN-SW",
    "source_type": "catalog_history",
    "excerpt": (
        "RAJA shipping cartons provide reliable everyday protection for dispatched "
        "items. Assembled quickly, stored flat, and suitable for standard parcel "
        "workflows across e-commerce and logistics operations."
    ),
}

# ---------------------------------------------------------------------------
# All sources combined (used by retrieval agent)
# ---------------------------------------------------------------------------
ALL_SOURCES = [
    {
        "source_id": IQ_PRODUCT_EXPORT["sku"],
        "source_type": "iq_product_export",
        "data": IQ_PRODUCT_EXPORT,
    },
    SUPPLIER_TECHNICAL_SHEET,
    TAXONOMY_REFERENCE,
    COMPLIANCE_REFERENCE,
    ERP_STOCK_FEED,
    CATALOG_HISTORY,
]

# ---------------------------------------------------------------------------
# Known product catalog (for smart query resolution)
# ---------------------------------------------------------------------------
PRODUCT_CATALOG = [
    {
        "sku": "RAJA-FR-SW-302015-R",
        "supplier_ref": "SB-300-200-150-K",
        "short_label": "Crt simple cannelure brun rec 300x200x150",
        "category_code": "CTN-SW-BR",
        "dimensions": "300 x 200 x 150 mm",
        "material": "Single-wall corrugated, 70% recycled",
        "markets": ["FR", "BE", "ES", "IT", "DE"],
        "status": "Active",
    },
    {
        "sku": "RAJA-FR-DW-604040-N",
        "supplier_ref": "DB-600-400-400-K",
        "short_label": "Crt double cannelure brun 600x400x400",
        "category_code": "CTN-DW-BR",
        "dimensions": "600 x 400 x 400 mm",
        "material": "Double-wall corrugated",
        "markets": ["FR", "DE"],
        "status": "Active",
    },
    {
        "sku": "RAJA-FR-SW-200150100-W",
        "supplier_ref": "SB-200-150-100-W",
        "short_label": "Crt simple cannelure blanc 200x150x100",
        "category_code": "CTN-SW-WH",
        "dimensions": "200 x 150 x 100 mm",
        "material": "Single-wall corrugated, white",
        "markets": ["FR", "BE"],
        "status": "Draft",
    },
]

# ---------------------------------------------------------------------------
# Smart query examples
# ---------------------------------------------------------------------------
SMART_QUERY_EXAMPLES = [
    "Enrich the recycled single-wall carton 300×200×150 with full descriptions, benefits, and SEO-ready content for France and Germany.",
    "Generate multilingual product content for supplier ref SB-300-200-150-K and prepare it for marketplace publication.",
    "Create e-commerce descriptions, cross-sell suggestions, and compliance-validated content for the double-wall carton 600×400×400.",
    "Produce SEO metadata and translated product sheets for the white single-wall box 200×150×100, targeting the French and Belgian markets.",
]
