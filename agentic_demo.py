"""Demo: Agentic planner with multi-step reasoning and error logging."""

import sys
import json

if sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

from tabulate import tabulate
from formatting import category_label, priority_label
from pawpal_system import Task, Pet, Owner
from src.ai.agentic_planner import AgenticSchedulePlanner

# Create owner and pets
owner = Owner(name="Jordan", available_minutes=90)

mochi = Pet(name="Mochi", species="dog")
mochi.add_task(Task("Morning walk", 30, "high", "walk", scheduled_time="08:00"))
mochi.add_task(Task("Breakfast", 10, "high", "feeding", scheduled_time="08:30"))
mochi.add_task(Task("Evening meds", 5, "high", "meds", scheduled_time="19:00"))
mochi.add_task(Task("Play fetch", 20, "low", "enrichment", scheduled_time="17:00"))

whiskers = Pet(name="Whiskers", species="cat")
whiskers.add_task(Task("Feeding", 10, "high", "feeding", scheduled_time="08:00"))
whiskers.add_task(Task("Litter box cleaning", 10, "medium", "grooming", scheduled_time="12:00"))
whiskers.add_task(Task("Brushing", 15, "low", "grooming", scheduled_time="20:00"))

owner.add_pet(mochi)
owner.add_pet(whiskers)

# Initialize agentic planner
print("\n" + "=" * 100)
print("AGENTIC SCHEDULE PLANNER - MULTI-STEP REASONING DEMO")
print("=" * 100 + "\n")

planner = AgenticSchedulePlanner()

# Run agentic planning
print(f"Planning schedule for {owner.name} ({owner.available_minutes} min available)\n")
result = planner.plan_schedule(owner)

print("=" * 100)
print("MULTI-STEP REASONING TRACES")
print("=" * 100 + "\n")

# Display each reasoning step
for i, trace in enumerate(result.reasoning_traces, 1):
    step_name = trace.step.value.replace("_", " ").title()
    confidence_pct = f"{trace.confidence * 100:.0f}%"

    print(f"\nStep {i}: {step_name}")
    print(f"Confidence: {confidence_pct}")
    print(f"Description: {trace.description}")

    if trace.findings:
        print(f"\nFindings:")
        for finding in trace.findings:
            print(f"  • {finding}")

    if trace.decisions:
        print(f"\nDecisions:")
        for decision in trace.decisions:
            print(f"  → {decision}")

    if trace.errors:
        print(f"\nErrors ({len(trace.errors)}):")
        for error in trace.errors:
            print(f"  ! {error.error_type}: {error.message}")

    print("-" * 100)

# Display final plan
print("\n" + "=" * 100)
print("GENERATED SCHEDULE")
print("=" * 100 + "\n")

plan_rows = []
for item in result.plan:
    status = "✓ INCLUDE" if item.included else "✗ SKIP"
    plan_rows.append([
        status,
        item.pet_name,
        item.task.title,
        category_label(item.task.category),
        priority_label(item.task.priority),
        f"{item.task.duration_minutes}m",
        item.reason[:50] + "..." if len(item.reason) > 50 else item.reason,
    ])

headers = ["Status", "Pet", "Task", "Category", "Priority", "Duration", "Reason"]
print(tabulate(plan_rows, headers=headers, tablefmt="grid"))

# Display metrics
print("\n" + "=" * 100)
print("PLANNING RESULTS & METRICS")
print("=" * 100 + "\n")

included = len([item for item in result.plan if item.included])
total = len(result.plan)

print(f"Plan Viability: {'VIABLE' if result.is_viable else 'NOT VIABLE'}")
print(f"Overall Confidence: {result.total_confidence:.1%}")
print(f"Tasks Scheduled: {included}/{total}")
print(f"\n{result.summary}\n")

# Display error summary
if result.errors:
    print(f"Errors Logged: {len(result.errors)}")
    error_summary = planner.error_logger.get_summary()
    print(f"  By Step: {error_summary.get('errors_by_step', {})}")
    print(f"  By Type: {error_summary.get('error_types', {})}")
else:
    print("No errors logged - plan generation successful!")

# Export reasoning log
print("\n" + "=" * 100)
print("EXPORTING REASONING LOG")
print("=" * 100 + "\n")

log_file = planner.export_reasoning_log("reasoning_traces.json")
print(f"Reasoning traces exported to: {log_file}")

# Show snippet of exported log
with open(log_file) as f:
    log_data = json.load(f)
    print(f"\nLog contains {len(log_data['traces'])} reasoning traces")
    print(f"First trace step: {log_data['traces'][0]['step']}")

print("\n" + "=" * 100)
print("DEMO COMPLETE")
print("=" * 100 + "\n")
