"""Comparison demo: Heuristic vs Groq API retrieval.

Shows how the two retrieval modes perform on the same queries.
Requires: .env file with GROQ_API_KEY
"""

import time
import os
from tabulate import tabulate
from src.ai.retriever import PetCareRetriever, GroqEnhancedRetriever

# Sample queries to test
QUERIES = [
    "dog morning exercise routine",
    "cat feeding schedule",
    "senior pet health care",
    "medication for pets",
    "puppy socialization tips",
]


def format_results(results):
    """Format retrieval results for display."""
    if not results:
        return "No results"
    return "\n".join([
        f"  • {r.title} (relevance: {r.relevance_score:.0%})"
        for r in results
    ])


def compare_retrievers():
    """Compare heuristic and Groq API retrievers."""
    print("\n" + "=" * 80)
    print("RETRIEVAL COMPARISON: Heuristic vs Groq API")
    print("=" * 80 + "\n")

    # Initialize retrievers
    heuristic = PetCareRetriever("knowledge_base.json")
    groq = GroqEnhancedRetriever("knowledge_base.json", use_api=True)

    heuristic_mode = "Heuristic (keyword-based)"
    groq_mode = groq.get_mode()

    print(f"Heuristic Mode: {heuristic_mode}")
    print(f"Groq Mode:      {groq_mode}\n")

    # Test each query
    for i, query in enumerate(QUERIES, 1):
        print(f"\n{'-' * 80}")
        print(f"Query {i}: {query}")
        print(f"{'-' * 80}\n")

        # Heuristic retrieval
        start = time.time()
        heuristic_results = heuristic.retrieve(query, top_k=3)
        heuristic_time = time.time() - start

        # Groq API retrieval
        start = time.time()
        groq_results = groq.retrieve(query, top_k=3)
        groq_time = time.time() - start

        # Display results
        results_table = [
            ["Heuristic (ms)", f"{heuristic_time * 1000:.1f}"],
            ["Groq API (ms)", f"{groq_time * 1000:.1f}"],
            ["Speed", f"{heuristic_time / groq_time:.1f}x faster" if groq_time > 0 else "N/A"],
        ]

        print(tabulate(results_table, headers=["Mode", "Time"], tablefmt="grid"))

        # Show results
        print(f"\n[HEURISTIC RESULTS]")
        print(format_results(heuristic_results))

        print(f"\n[GROQ API RESULTS]")
        print(format_results(groq_results))

        # Compare document overlap
        heuristic_docs = {r.title for r in heuristic_results}
        groq_docs = {r.title for r in groq_results}
        overlap = heuristic_docs & groq_docs

        print(f"\n[COMPARISON]")
        print(f"  • Heuristic returned: {len(heuristic_docs)} unique documents")
        print(f"  • Groq API returned:  {len(groq_docs)} unique documents")
        print(f"  • Overlap: {len(overlap)} documents in both")
        if overlap:
            print(f"  • Overlapping: {', '.join(list(overlap)[:2])}..." if len(overlap) > 2 else f"  • Overlapping: {', '.join(overlap)}")


def test_fallback():
    """Test API fallback to heuristic when API fails."""
    print(f"\n\n{'=' * 80}")
    print("FALLBACK TEST: API Failure Recovery")
    print(f"{'=' * 80}\n")

    # Create retriever with API disabled (simulates API unavailable)
    groq = GroqEnhancedRetriever("knowledge_base.json", use_api=False)

    query = "dog exercise and training"
    print(f"Query: {query}")
    print(f"Mode: {groq.get_mode()}\n")

    results = groq.retrieve(query, top_k=3)

    print("Results (using heuristic fallback):")
    print(format_results(results))


def suggestions():
    """Print usage suggestions."""
    print(f"\n\n{'=' * 80}")
    print("USAGE SUGGESTIONS")
    print(f"{'=' * 80}\n")

    suggestions_text = """
1. USE HEURISTIC MODE FOR:
   • Quick queries (no API latency)
   • Development/testing (no API key needed)
   • Simple keyword-based searches
   • Production environments with API fallback

2. USE GROQ API MODE FOR:
   • Semantic understanding needed
   • Complex queries with context
   • Improved relevance ranking
   • Comparing with heuristic baseline

3. SETUP FOR GROQ API:
   • Get free key: https://console.groq.com
   • Copy .env.example to .env
   • Add your GROQ_API_KEY to .env
   • Ensure .env is in .gitignore (never commit!)

4. IN YOUR CODE:

   # Heuristic only (fast, no API)
   from src.ai.integrator import AISchedulingIntegrator
   integrator = AISchedulingIntegrator(retriever_mode="heuristic")

   # Groq API with fallback
   integrator = AISchedulingIntegrator(retriever_mode="groq")

5. HYBRID APPROACH:
   • Run heuristic for speed
   • Fall back to Groq for edge cases
   • Compare results for A/B testing
   • Track which mode performs better
"""

    print(suggestions_text)


if __name__ == "__main__":
    # Check if Groq API key is available
    if not os.getenv("GROQ_API_KEY") or os.getenv("GROQ_API_KEY") == "your_key_here":
        print("\n[!] Groq API key not found in .env")
        print("    The comparison will still run with fallback to heuristic.\n")

    try:
        compare_retrievers()
        test_fallback()
        suggestions()
    except Exception as e:
        print(f"\n[ERROR] {e}")
        print("\nMake sure:")
        print("  1. .env file exists with GROQ_API_KEY")
        print("  2. groq package installed: pip install groq")
        print("  3. python-dotenv installed: pip install python-dotenv")
