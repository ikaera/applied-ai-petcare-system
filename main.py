"""PawPal+ with RAG and validation demo."""

import os
import sys
from datetime import timedelta

# Windows consoles default to a cp1252 codepage that can't encode emoji;
# force UTF-8 so the formatted output below prints correctly everywhere.
if sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

from tabulate import tabulate

from formatting import category_label, priority_label
from pawpal_system import Task, Pet, Owner, Scheduler
from src.ai.integrator import AISchedulingIntegrator

# Owner has 90 minutes available today
owner = Owner(name="Jordan", available_minutes=90)

mochi = Pet(name="Mochi", species="dog")
mochi.add_task(Task("Morning walk", 30, "high", "walk", scheduled_time="08:00"))
mochi.add_task(Task("Evening meds", 5, "high", "meds", scheduled_time="19:30"))
mochi.add_task(Task("Breakfast", 10, "high", "feeding", scheduled_time="08:30"))
mochi.add_task(Task("Fetch in the yard", 40, "low", "enrichment", scheduled_time="17:00"))

whiskers = Pet(name="Whiskers", species="cat")
whiskers.add_task(Task("Brushing", 15, "low", "grooming", scheduled_time="20:00"))
whiskers.add_task(Task("Feeding", 10, "high", "feeding", scheduled_time="08:15"))
whiskers.add_task(Task("Litter box cleaning", 10, "medium", "grooming", scheduled_time="12:00"))
whiskers.add_task(Task("Weekly grooming", 30, "medium", "grooming", frequency="weekly", scheduled_time="10:00"))

owner.add_pet(mochi)
owner.add_pet(whiskers)

# Generate base schedule
scheduler = Scheduler()
plan = scheduler.generate_plan(owner)

# Enhance with RAG + validation
ai_integrator = AISchedulingIntegrator()
pet_species_map = {pet.name: pet.species for pet in owner.pets}
enhanced_plan = ai_integrator.enhance_plan(plan, pet_species_map)

print(f"Today's Schedule for {owner.name} ({owner.available_minutes} min available)\n")
print("=" * 100)

schedule_rows = []
for item in enhanced_plan:
    planned = item.planned_item
    task = planned.task
    retrieval_status = f"📚 {len(item.retrieval_results)} docs" if item.retrieval_results else "—"
    validation = "✓" if item.validation_result and item.validation_result.is_valid else "⚠"

    schedule_rows.append([
        "✅" if planned.included else "⏭️",
        planned.pet_name,
        task.title,
        category_label(task.category),
        priority_label(task.priority),
        f"{task.duration_minutes}m",
        retrieval_status,
        validation,
    ])

headers = ["Status", "Pet", "Task", "Category", "Priority", "Time", "References", "Valid"]
print(tabulate(schedule_rows, headers=headers, tablefmt="grid"))

print("\n" + "=" * 100)
print("\nDETAILED RECOMMENDATIONS WITH RAG & VALIDATION:\n")

for i, item in enumerate(enhanced_plan, 1):
    planned = item.planned_item
    task = planned.task

    if planned.included:
        print(f"\n{i}. ✅ {task.title} ({task.duration_minutes}m)")
        print(f"   Pet: {planned.pet_name} | Category: {task.category} | Priority: {task.priority}")
        print(f"   Reason: {planned.reason}")

        # Show retrieval results
        if item.retrieval_results:
            print(f"   📚 Retrieved {len(item.retrieval_results)} relevant documents:")
            for j, result in enumerate(item.retrieval_results[:2], 1):
                print(f"      {j}. {result.title} (relevance: {result.relevance_score:.0%})")
                print(f"         → {result.content[:100]}...")

        # Show validation result
        if item.validation_result:
            print(f"   {item.get_validation_summary()}")
            if item.validation_result.recommendations:
                print(f"   Suggestions: {', '.join(item.validation_result.recommendations)}")

print("\n" + "=" * 100)
print("\nSYSTEM RELIABILITY METRICS:\n")
metrics = ai_integrator.get_metrics()
print(f"Total items evaluated: {metrics['total_items']}")
print(f"Items validated: {metrics['items_validated']}")
print(f"Valid recommendations: {metrics['valid_items']}")
print(f"Validation success rate: {metrics.get('validation_success_rate', 0):.1%}")
print(f"Average confidence score: {metrics['avg_confidence']:.2f}")
print(f"Average retrieval score: {metrics['avg_retrieval_score']:.2f}")
print("\n" + "=" * 100)

# --- Sorting demo: tasks were added out of order above; sort_by_time fixes that. ---
all_tasks = [task for _, task in owner.get_all_tasks()]
print("\nAll tasks sorted by scheduled time:\n")
time_sorted_rows = [
    [task.scheduled_time, task.title, category_label(task.category), priority_label(task.priority)]
    for task in scheduler.sort_by_time(all_tasks)
]
print(tabulate(time_sorted_rows, headers=["Time", "Task", "Category", "Priority"]))

# --- Priority scheduling demo: sort by priority first, ties broken by scheduled time. ---
print("\nAll tasks sorted by priority, then by time:\n")
priority_sorted_rows = [
    [priority_label(task.priority), task.scheduled_time, task.title, category_label(task.category)]
    for task in scheduler.sort_by_priority_then_time(all_tasks)
]
print(tabulate(priority_sorted_rows, headers=["Priority", "Time", "Task", "Category"]))

# --- Filtering demo: only Mochi's tasks, then only incomplete tasks. ---
print("\nFiltered: Mochi's tasks only:\n")
for pet, task in scheduler.filter_tasks(owner.get_all_tasks(), pet_name="Mochi"):
    print(f"{pet.name}: {task.title}")

print("\nFiltered: incomplete tasks only:\n")
for pet, task in scheduler.filter_tasks(owner.get_all_tasks(), completed=False):
    print(f"{pet.name}: {task.title}")

# --- Recurring task demo: completing a daily task should spawn tomorrow's occurrence. ---
morning_walk = next(t for t in mochi.tasks if t.title == "Morning walk")
print(f"\nCompleting '{morning_walk.title}' (due {morning_walk.due_date}, frequency={morning_walk.frequency})")
next_occurrence = mochi.complete_task(morning_walk)
print(f"✅ Completed: {morning_walk.completed}")
print(f"🔁 Next occurrence created for {next_occurrence.due_date} (completed={next_occurrence.completed})")

# --- Conflict detection demo: two tasks (different pets) scheduled at the same time. ---
whiskers.add_task(Task("Play session", 15, "medium", "enrichment", scheduled_time="08:30"))

print("\nChecking for scheduling conflicts:\n")
conflicts = scheduler.detect_conflicts(owner)
if conflicts:
    for warning in conflicts:
        print(f"⚠️  {warning}")
else:
    print("✅ No conflicts found.")

# --- Next available slot demo: find room for a new 20-minute task on Mochi's busy day. ---
print("\nFinding next available 20-minute slot for Mochi today:\n")
slot = scheduler.find_next_available_slot(owner, due_date=morning_walk.due_date, duration_minutes=20)
if slot:
    print(f"🕒 Next available slot: {slot}")
else:
    print("🕒 No slot available today.")

# --- Weekly rescheduling demo: next week's "Weekly grooming" would land at the same
#     time as a vet visit whiskers already has booked, so it gets nudged to a free slot. ---
weekly_grooming = next(t for t in whiskers.tasks if t.title == "Weekly grooming")
next_week = weekly_grooming.due_date + timedelta(weeks=1)
whiskers.add_task(Task("Vet checkup", 20, "high", "meds", scheduled_time="10:15", due_date=next_week))

print(f"\nRescheduling '{weekly_grooming.title}' for next week (conflicts with a vet checkup at 10:15):\n")
rescheduled = scheduler.reschedule_weekly_task(owner, weekly_grooming)
if rescheduled:
    print(f"🔁 Moved to {rescheduled.due_date} at {rescheduled.scheduled_time} (originally 10:00).")
else:
    print("🔁 No open slot found within the search window.")

# --- Persistence demo: save the owner's full state to JSON, then reload it. ---
demo_file = "demo_data.json"
owner.save_to_json(demo_file)
print(f"\n💾 Saved {owner.name}'s data to {demo_file}.")

reloaded_owner = Owner.load_from_json(demo_file)
print(f"💾 Reloaded owner '{reloaded_owner.name}' with {len(reloaded_owner.pets)} pets "
      f"and {len(reloaded_owner.get_all_tasks())} total tasks.")

os.remove(demo_file)
