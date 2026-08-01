from app.services.search_service import search_trusted_sources
claim = "UPI payments have been banned across India"
results = search_trusted_sources(claim)
print("=" * 80)
print(f"Found {len(results)} results")
print("=" * 80)
for i, result in enumerate(results, start=1):
    print(f"\nResult {i}")
    print("Title :", result["title"])
    print("URL   :", result["url"])
    print("Score :", result["score"])
    print("Content:")
    print(result["content"])
    print("-" * 80)