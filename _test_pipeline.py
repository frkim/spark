import asyncio, json

async def test():
    from pipeline import ProductContentPipeline
    pipeline = ProductContentPipeline(mode='azure')
    ctx, tracer = await pipeline.run('Rouleau de film etirable pre-etire RAJA')

    # Check each step
    steps = ['intake', 'retrieval', 'normalization', 'enrichment', 'seo', 'multilingual', 'quality', 'publication']
    for s in steps:
        data = ctx.get(s, {})
        if 'error' in data:
            print(f'  {s}: ERROR - {data["error"]}')
        else:
            print(f'  {s}: OK ({len(json.dumps(data))} chars)')

    # Print tracer summary
    summary = tracer.summary()
    for span in summary.get('spans', []):
        print(f'  {span["agent"]:30s} {span["latency_ms"]:>8.0f}ms  {span.get("tokens_total",0):>6} tokens  {span["status"]}')
    print(f'  TOTAL: {summary["total_latency_ms"]:.0f}ms  {summary["total_tokens"]} tokens')

asyncio.run(test())
