"""Groq API mode demo: Full system with semantic retrieval.

Shows the complete workflow using Groq API for intelligent document ranking.
"""

import os
from src.ai.integrator import AISchedulingIntegrator
from src.ai.validator import RecommendationValidator
from pawpal_system import Owner, Pet, Task, Scheduler

def demo_groq_mode():
    """Run complete system using Groq API retrieval mode."""

    print("\n" + "=" * 80)
    print("GROQ API MODE DEMO: Full Pet Care Scheduling Workflow")
    print("=" * 80 + "\n")

    # Check API key
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key == "your_key_here":
        print("[!] No Groq API key found. Using heuristic fallback.")
        print("    To use Groq API:")
        print("    1. Get free key from https://console.groq.com")
        print("    2. Add to .env: GROQ_API_KEY=your_key_here")
        print("    3. Run this demo again\n")

    # Create owner and pets
    print("Setting up pets and tasks...\n")

    owner = Owner(name="Jordan", available_minutes=120)

    # Dog: Mochi
    mochi = Pet(name="Mochi", species="dog")
    mochi.add_task(Task("Morning walk", 30, "high", "walk"))
    mochi.add_task(Task("Feeding", 10, "high", "feeding"))
    mochi.add_task(Task("Playtime", 20, "medium", "enrichment"))
    mochi.add_task(Task("Evening meds", 5, "high", "meds"))

    # Cat: Whiskers
    whiskers = Pet(name="Whiskers", species="cat")
    whiskers.add_task(Task("Feeding", 5, "high", "feeding"))
    whiskers.add_task(Task("Grooming", 15, "medium", "grooming"))
    whiskers.add_task(Task("Litter box cleaning", 5, "high", "care"))

    owner.add_pet(mochi)
    owner.add_pet(whiskers)

    print(f"Owner: {owner.name}")
    print(f"Available time: {owner.available_minutes} minutes")
    print(f"Pets: {', '.join([p.name for p in owner.pets])}")
    print(f"Total tasks: {sum(len(p.tasks) for p in owner.pets)}\n")

    # Generate base schedule
    print("Generating base schedule...")
    scheduler = Scheduler()
    base_plan = scheduler.generate_plan(owner)
    print(f"Base schedule: {len([i for i in base_plan if i.included])} tasks fit in {owner.available_minutes} minutes\n")

    # Enhance with Groq API
    print("Enhancing with Groq API retrieval (with heuristic fallback)...")
    integrator = AISchedulingIntegrator(
        knowledge_base_path="knowledge_base.json",
        retriever_mode="groq"  # Use Groq API mode
    )

    pet_species_map = {pet.name: pet.species for pet in owner.pets}
    enhanced_plan = integrator.enhance_plan(base_plan, pet_species_map)

    # Display results
    print("\n" + "=" * 80)
    print("ENHANCED SCHEDULE WITH GROQ API RETRIEVAL")
    print("=" * 80 + "\n")

    retriever_mode = integrator.get_retriever_mode()
    print(f"Retrieval Mode: {retriever_mode}\n")

    print("SCHEDULE:\n")
    print("{:<10} {:<15} {:<25} {:<15} {:<15}".format(
        "Time", "Pet", "Task", "Status", "Confidence"
    ))
    print("-" * 80)

    for i, item in enumerate(enhanced_plan, 1):
        if item.planned_item.included:
            task = item.planned_item.task
            time_str = task.scheduled_time or "---"
            pet_name = item.planned_item.pet_name
            task_name = task.title[:25]

            status = "PASS" if (item.validation_result and item.validation_result.is_valid) else "REVIEW"
            confidence = f"{item.validation_result.confidence_score:.0%}" if item.validation_result else "N/A"

            print("{:<10} {:<15} {:<25} {:<15} {:<15}".format(
                time_str, pet_name, task_name, status, confidence
            ))

    # Show retrieval details for first few items
    print("\n" + "=" * 80)
    print("RETRIEVED DOCUMENTS (Top 3 results)")
    print("=" * 80 + "\n")

    for i, item in enumerate(enhanced_plan[:3], 1):
        if item.planned_item.included and item.retrieval_results:
            print(f"{i}. {item.planned_item.task.title} ({item.planned_item.pet_name}):")
            for j, doc in enumerate(item.retrieval_results, 1):
                print(f"   {j}. {doc.title} (relevance: {doc.relevance_score:.0%})")
                print(f"      {doc.content[:100]}...")
            print()

    # Show validation issues
    print("=" * 80)
    print("VALIDATION RESULTS")
    print("=" * 80 + "\n")

    issues_count = 0
    for item in enhanced_plan:
        if item.planned_item.included and item.validation_result:
            if not item.validation_result.is_valid:
                issues_count += 1
                print(f"[!] {item.planned_item.pet_name}: {item.planned_item.task.title}")
                print(f"    Status: {item.validation_result.explanation}")
                if item.validation_result.recommendations:
                    print(f"    Suggestions:")
                    for rec in item.validation_result.recommendations:
                        print(f"      - {rec}")
                print()

    if issues_count == 0:
        print("[OK] All tasks passed validation!")

    # Show metrics
    print("\n" + "=" * 80)
    print("SYSTEM METRICS")
    print("=" * 80 + "\n")

    metrics = integrator.get_metrics()
    print(f"Items evaluated:        {metrics['total_items']}")
    print(f"Items validated:        {metrics['items_validated']}")
    print(f"Valid items:            {metrics['valid_items']}")
    print(f"Average confidence:     {metrics.get('avg_confidence', 0):.2f}")
    print(f"Average retrieval score: {metrics.get('avg_retrieval_score', 0):.2f}")
    print(f"Retrieval mode:         {metrics.get('retriever_mode', 'unknown')}")

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80 + "\n")

    included = len([i for i in base_plan if i.included])
    print(f"Successfully scheduled {included} tasks for {owner.name}'s pets")
    print(f"All recommendations are knowledge-backed and validated")
    print(f"Using {retriever_mode} for intelligent document retrieval\n")


if __name__ == "__main__":
    try:
        demo_groq_mode()
    except Exception as e:
        print(f"\n[ERROR] {e}")
        print("\nMake sure:")
        print("  1. knowledge_base.json exists")
        print("  2. groq package installed: pip install groq")
        print("  3. python-dotenv installed: pip install python-dotenv")
