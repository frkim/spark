"""CLI entry point — run the RAJA product content pipeline from the terminal."""

from __future__ import annotations

import asyncio
import json
import sys

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.syntax import Syntax

from demo_data import SMART_QUERY_EXAMPLES
from pipeline import ProductContentPipeline, STEPS

console = Console()


def _print_banner() -> None:
    console.print(
        Panel(
            "[bold blue]Microsoft Foundry × RAJA[/]\n"
            "[dim]Intelligent Product Content Pipeline[/]",
            border_style="blue",
        )
    )


def _pick_query() -> str:
    console.print("\n[bold]Smart query examples:[/]")
    for i, q in enumerate(SMART_QUERY_EXAMPLES, 1):
        console.print(f"  [cyan]{i}.[/] {q}")
    console.print(f"  [cyan]{len(SMART_QUERY_EXAMPLES)+1}.[/] Enter a custom query\n")

    choice = console.input("[bold]Choose a query (number): [/]").strip()
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(SMART_QUERY_EXAMPLES):
            return SMART_QUERY_EXAMPLES[idx]
    except ValueError:
        pass
    return console.input("[bold]Enter your query: [/]").strip()


async def _run(query: str) -> None:
    pipeline = ProductContentPipeline()

    step_status: dict[str, str] = {}
    step_data: dict[str, dict] = {}

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        tasks: dict[str, object] = {}
        for key, label in STEPS:
            tasks[key] = progress.add_task(f"[dim]{label}[/]", total=None)

        def on_step(key: str, status: str, data: dict | None = None) -> None:
            step_status[key] = status
            if data:
                step_data[key] = data
            label = dict(STEPS).get(key, key)
            if status == "running":
                progress.update(tasks[key], description=f"[yellow]⟳ {label}[/]")
            else:
                progress.update(tasks[key], description=f"[green]✓ {label}[/]", completed=1, total=1)

        ctx, tracer = await pipeline.run(query, on_step=on_step)

    # -- Results -----------------------------------------------------------
    console.print()

    # Enrichment summary
    enrichment = ctx.get("enrichment", {})
    if enrichment and "error" not in enrichment:
        console.print(Panel("[bold]Product Enrichment[/]", border_style="green"))
        console.print(f"[bold]Short description:[/] {enrichment.get('short_description', 'N/A')}")
        console.print(f"\n[bold]Long description:[/]\n{enrichment.get('long_description', 'N/A')}")
        benefits = enrichment.get("customer_benefits", [])
        if benefits:
            console.print("\n[bold]Customer benefits:[/]")
            for b in benefits:
                console.print(f"  • {b}")

    # SEO summary
    seo = ctx.get("seo", {})
    if seo and "error" not in seo:
        console.print(Panel("[bold]SEO Metadata[/]", border_style="cyan"))
        console.print(f"[bold]H1:[/] {seo.get('h1', 'N/A')}")
        console.print(f"[bold]Meta:[/] {seo.get('meta_description', 'N/A')}")
        console.print(f"[bold]Keywords:[/] {', '.join(seo.get('secondary_keywords', []))}")

    # Quality summary
    quality = ctx.get("quality", {})
    if quality and "error" not in quality:
        console.print(Panel("[bold]Quality & Compliance[/]", border_style="magenta"))
        status_color = "green" if quality.get("status") == "approved" else "red"
        console.print(f"[bold]Status:[/] [{status_color}]{quality.get('status', 'N/A')}[/]")
        console.print(f"[bold]Confidence:[/] {quality.get('overall_confidence_score', 'N/A')}/100")
        console.print(f"[bold]Citation coverage:[/] {quality.get('citation_coverage_score', 'N/A')}/100")
        flags = quality.get("flags", [])
        if flags:
            console.print("[bold]Flags:[/]")
            for f in flags:
                console.print(f"  ⚠ {f.get('field', '?')} ({f.get('language', '?')}): {f.get('issue', '?')}")

    # Trace summary
    trace = tracer.summary()
    console.print(Panel("[bold]Pipeline Trace[/]", border_style="blue"))
    table = Table(show_header=True, header_style="bold")
    table.add_column("Agent")
    table.add_column("Latency", justify="right")
    table.add_column("Tokens", justify="right")
    table.add_column("Status")
    for s in trace["spans"]:
        table.add_row(
            s["agent"],
            f"{s['latency_ms']:.0f} ms",
            str(s["tokens"]),
            f"[green]{s['status']}[/]" if s["status"] == "ok" else f"[red]{s['status']}[/]",
        )
    console.print(table)
    console.print(f"\n[bold]Total:[/] {trace['total_latency_ms']:.0f} ms | {trace['total_tokens']} tokens | run_id: {trace['run_id']}")

    # Full JSON output
    console.print(Panel("[bold]Publication Output (PIM JSON)[/]", border_style="green"))
    pub = ctx.get("publication", {}).get("ecommerce_json", ctx.get("publication", {}))
    console.print(Syntax(json.dumps(pub, indent=2, ensure_ascii=False), "json", theme="monokai"))


def main() -> None:
    _print_banner()
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = _pick_query()

    if not query:
        console.print("[red]No query provided. Exiting.[/]")
        return

    console.print(f"\n[bold]Query:[/] {query}\n")
    asyncio.run(_run(query))


if __name__ == "__main__":
    main()
