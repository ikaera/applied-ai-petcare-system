"""A/B Testing: Compare heuristic vs Groq API retrieval results.

Tests both modes on real scheduling scenarios and compares:
- Document relevance
- Validation outcomes
- Confidence scores
- Performance metrics
"""

import time
from tabulate import tabulate
from src.ai.integrator import AISchedulingIntegrator
from pawpal_system import Owner, Pet, Task, Scheduler


def create_test_scenario(name: str) -> Owner:
    """Create a test scenario with pets and tasks."""
    owner = Owner(name=name, available_minutes=120)

    # Dog
    dog = Pet(name="Mochi", species="dog")
    dog.add_task(Task("Morning walk", 30, "high", "walk"))
    dog.add_task(Task("Feeding", 10, "high", "feeding"))
    dog.add_task(Task("Training", 20, "medium", "enrichment"))

    # Cat
    cat = Pet(name="Whiskers", species="cat")
    cat.add_task(Task("Feeding", 5, "high", "feeding"))
    cat.add_task(Task("Grooming", 15, "medium", "grooming"))

    owner.add_pet(dog)
    owner.add_pet(cat)

    return owner


def run_ab_test():
    """Run A/B test comparing both retrieval modes."""

    print("\n" + "=" * 100)
    print("A/B TESTING: Heuristic vs Groq API Retrieval")
    print("=" * 100 + "\n")

    # Create test scenario
    owner = create_test_scenario("TestOwner")

    # Generate base plan
    scheduler = Scheduler()
    base_plan = scheduler.generate_plan(owner)

    pet_species_map = {pet.name: pet.species for pet in owner.pets}

    # Test both modes
    results = {}

    for mode in ["heuristic", "groq"]:
        print(f"\n[Running {mode.upper()} mode...]")

        start_time = time.time()
        integrator = AISchedulingIntegrator(
            knowledge_base_path="knowledge_base.json",
            retriever_mode=mode
        )
        enhanced_plan = integrator.enhance_plan(base_plan, pet_species_map)
        elapsed = time.time() - start_time

        # Calculate metrics
        total_items = len([i for i in enhanced_plan if i.planned_item.included])
        valid_items = len([i for i in enhanced_plan
                          if i.planned_item.included
                          and i.validation_result
                          and i.validation_result.is_valid])

        avg_retrieval_score = 0
        retrieval_count = 0
        for item in enhanced_plan:
            if item.retrieval_results:
                avg_retrieval_score += sum(r.relevance_score for r in item.retrieval_results) / len(item.retrieval_results)
                retrieval_count += 1

        if retrieval_count > 0:
            avg_retrieval_score /= retrieval_count

        avg_confidence = 0
        confidence_count = 0
        for item in enhanced_plan:
            if item.validation_result:
                avg_confidence += item.validation_result.confidence_score
                confidence_count += 1

        if confidence_count > 0:
            avg_confidence /= confidence_count

        results[mode] = {
            "time": elapsed,
            "total_items": total_items,
            "valid_items": valid_items,
            "valid_rate": (valid_items / total_items * 100) if total_items > 0 else 0,
            "avg_retrieval_score": avg_retrieval_score,
            "avg_confidence": avg_confidence,
            "retriever_mode": integrator.get_retriever_mode(),
        }

    # Display comparison
    print("\n" + "=" * 100)
    print("RESULTS COMPARISON")
    print("=" * 100 + "\n")

    comparison_table = [
        ["Metric", "Heuristic", "Groq API", "Difference"],
        ["Time (ms)",
         f"{results['heuristic']['time']*1000:.2f}",
         f"{results['groq']['time']*1000:.2f}",
         f"{(results['groq']['time'] - results['heuristic']['time'])*1000:+.2f}"],
        ["Items Scheduled",
         results['heuristic']['total_items'],
         results['groq']['total_items'],
         f"{results['groq']['total_items'] - results['heuristic']['total_items']:+d}"],
        ["Items Valid",
         results['heuristic']['valid_items'],
         results['groq']['valid_items'],
         f"{results['groq']['valid_items'] - results['heuristic']['valid_items']:+d}"],
        ["Validation Rate",
         f"{results['heuristic']['valid_rate']:.1f}%",
         f"{results['groq']['valid_rate']:.1f}%",
         f"{results['groq']['valid_rate'] - results['heuristic']['valid_rate']:+.1f}%"],
        ["Avg Retrieval Score",
         f"{results['heuristic']['avg_retrieval_score']:.2f}",
         f"{results['groq']['avg_retrieval_score']:.2f}",
         f"{results['groq']['avg_retrieval_score'] - results['heuristic']['avg_retrieval_score']:+.2f}"],
        ["Avg Confidence",
         f"{results['heuristic']['avg_confidence']:.2f}",
         f"{results['groq']['avg_confidence']:.2f}",
         f"{results['groq']['avg_confidence'] - results['heuristic']['avg_confidence']:+.2f}"],
    ]

    print(tabulate(comparison_table, headers="firstrow", tablefmt="grid"))

    # Interpretation
    print("\n" + "=" * 100)
    print("INTERPRETATION")
    print("=" * 100 + "\n")

    heuristic_faster = results['heuristic']['time'] < results['groq']['time']
    print(f"1. SPEED:")
    if heuristic_faster:
        speed_diff = (results['groq']['time'] / results['heuristic']['time'] - 1) * 100
        print(f"   Heuristic is {speed_diff:.0f}% faster")
        print(f"   (Good for: High-throughput scenarios, real-time responses)\n")
    else:
        print(f"   Times are comparable\n")

    print(f"2. VALIDITY:")
    heuristic_valid = results['heuristic']['valid_rate']
    groq_valid = results['groq']['valid_rate']
    if abs(heuristic_valid - groq_valid) < 5:
        print(f"   Both modes have similar validation rates")
    elif groq_valid > heuristic_valid:
        print(f"   Groq API has {groq_valid - heuristic_valid:.1f}% better validation")
        print(f"   (Better semantic understanding)\n")
    else:
        print(f"   Heuristic has {heuristic_valid - groq_valid:.1f}% better validation\n")

    print(f"3. RETRIEVAL QUALITY:")
    heuristic_retrieval = results['heuristic']['avg_retrieval_score']
    groq_retrieval = results['groq']['avg_retrieval_score']
    print(f"   Heuristic: {heuristic_retrieval:.2f}")
    print(f"   Groq API:  {groq_retrieval:.2f}")
    if abs(heuristic_retrieval - groq_retrieval) < 0.1:
        print(f"   (Similar relevance scores)\n")
    else:
        better = "Groq API" if groq_retrieval > heuristic_retrieval else "Heuristic"
        print(f"   ({better} returns more relevant documents)\n")

    # Recommendations
    print("=" * 100)
    print("RECOMMENDATIONS")
    print("=" * 100 + "\n")

    if heuristic_faster:
        print("[HEURISTIC MODE]")
        print("  Use when:")
        print("    - Speed is critical")
        print("    - No API key available")
        print("    - Running tests/development")
        print("    - Simple keyword-based queries")
        print()

    print("[GROQ API MODE]")
    print("  Use when:")
    print("    - Semantic understanding needed")
    print("    - Complex multi-word queries")
    print("    - Production with fallback desired")
    print("    - Want AI-powered ranking")
    print()

    print("[HYBRID APPROACH]")
    print("  Try both and compare:")
    print("    - Use heuristic for fast initial results")
    print("    - Fall back to Groq for complex cases")
    print("    - Compare results for quality assurance")
    print("    - Track which mode performs better over time")


if __name__ == "__main__":
    try:
        run_ab_test()
    except Exception as e:
        print(f"\n[ERROR] {e}")
        print("\nDependencies needed:")
        print("  pip install groq python-dotenv tabulate")
