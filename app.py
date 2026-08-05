import os
from datetime import date, time

import streamlit as st

from formatting import CATEGORY_EMOJIS, category_label, priority_label, status_emoji
from pawpal_system import Task, Pet, Owner, Scheduler

DATA_FILE = "data.json"

st.set_page_config(page_title="petcare - Pet Care Manager", page_icon="🐾", layout="wide")

st.title("🐾 petcare")
st.markdown("**Your intelligent pet care task manager**")

with st.expander("ℹ️ About petcare", expanded=False):
    st.markdown(
        """
        **petcare** is your personal pet care assistant that helps you:

        - 📋 **Track all tasks** - walks, feeding, meds, enrichment, grooming, and more
        - ⏰ **Schedule intelligently** - assign priorities and specific times
        - 🔔 **Avoid conflicts** - automatically detect overlapping tasks
        - 📅 **Optimize daily plans** - fit the most important tasks in your available time
        - 💾 **Save automatically** - all your pet data persists between sessions

        **Perfect for:** Pet owners with one or multiple pets who want to stay organized!
        """
    )

scheduler = Scheduler()

st.divider()

st.subheader("📝 Your Profile & Settings")
st.markdown("**Setup Information**")
st.markdown("Tell us about yourself so we can personalize your pet care plan.")

col1, col2, col3 = st.columns([2, 2, 1])
with col1:
    owner_name = st.text_input(
        "Your name",
        value="Jordan",
        help="Enter your name to personalize your pet care plan"
    )
with col2:
    available_minutes = st.number_input(
        "Available time today (minutes)",
        min_value=1,
        max_value=600,
        value=60,
        help="Total minutes you can dedicate to pet care tasks today"
    )
with col3:
    st.markdown("**Actions**")
    if st.button("🗑️ Clear All Data", help="⚠️ This will delete all pets and tasks permanently!"):
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
        if "owner" in st.session_state:
            del st.session_state.owner
        st.success("✅ All data cleared! Starting fresh...")
        st.rerun()

# Create the Owner once per session; reused on every rerun instead of being
# rebuilt from scratch each time Streamlit reruns the script. If a data.json
# from a previous run exists, load it so pets/tasks persist across restarts.
if "owner" not in st.session_state:
    if os.path.exists(DATA_FILE):
        st.session_state.owner = Owner.load_from_json(DATA_FILE)
        st.toast(f"Loaded saved data from {DATA_FILE}.")
    else:
        st.session_state.owner = Owner(name=owner_name, available_minutes=available_minutes)

owner = st.session_state.owner

st.divider()
st.subheader("🐶 Manage Your Pets")
st.markdown("Add your pets to start creating care tasks. You can manage tasks for multiple pets.")

pet_col1, pet_col2, pet_col3 = st.columns([2, 1.5, 1])
with pet_col1:
    pet_name = st.text_input("Pet name", value="Mochi", help="Enter your pet's name")
with pet_col2:
    species = st.selectbox("Species", ["dog", "cat", "other"], help="Select your pet's species")
with pet_col3:
    st.write("")  # spacing
    if st.button("➕ Add Pet", use_container_width=True):
        owner.add_pet(Pet(name=pet_name, species=species))
        owner.save_to_json(DATA_FILE)
        st.success(f"✅ {pet_name} added!")
        st.rerun()

if owner.pets:
    st.markdown("**Your Pets:**")
    pets_data = [{"name": p.name, "species": p.species.capitalize()} for p in owner.pets]
    st.dataframe(pets_data, use_container_width=True, hide_index=True)
else:
    st.info("👆 Add a pet above to get started!")

st.divider()
st.subheader("✅ Add Care Tasks")
st.markdown("Create tasks for your pets with priority levels, scheduled times, and frequencies.")

if owner.pets:
    pet_names = [p.name for p in owner.pets]
    selected_pet_name = st.selectbox("Which pet is this task for?", pet_names, help="Select the pet this task is for")
    pet = next(p for p in owner.pets if p.name == selected_pet_name)

    task_col1, task_col2, task_col3 = st.columns(3)
    with task_col1:
        task_title = st.text_input("Task title", value="Morning walk", help="e.g., Morning walk, Lunch feeding, Brush coat")
    with task_col2:
        priority = st.selectbox(
            "Priority level",
            ["low", "medium", "high"],
            index=2,
            help="🔴 High=urgent, 🟡 Medium=important, 🟢 Low=optional"
        )
    with task_col3:
        category = st.selectbox(
            "Category",
            list(CATEGORY_EMOJIS.keys()),
            index=0,
            help="Type of care activity"
        )

    task_col4, task_col5, task_col6 = st.columns(3)
    with task_col4:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20, help="How long this task takes")
    with task_col5:
        scheduled_time = st.time_input("Scheduled time", value=time(9, 0), help="What time should this task be done?")
    with task_col6:
        frequency = st.selectbox("Frequency", ["once", "daily", "weekly"], index=0, help="Is this a one-time or recurring task?")

    if st.button("➕ Add Task", use_container_width=True):
        pet.add_task(
            Task(
                title=task_title,
                duration_minutes=int(duration),
                priority=priority,
                category=category,
                frequency=frequency,
                scheduled_time=scheduled_time.strftime("%H:%M"),
            )
        )
        owner.save_to_json(DATA_FILE)
        st.success(f"✅ Task '{task_title}' added for {pet.name}!")
        st.rerun()

    if pet.tasks:
        st.markdown(f"**Tasks for {pet.name}:** ({len(pet.tasks)} total)")

        # Create scrollable container for tasks
        with st.container(border=True):
            st.markdown("**Active Tasks** (scroll down to see all)")

            # Custom CSS for scrollable container
            st.markdown(
                """
                <style>
                .task-container {
                    max-height: 400px;
                    overflow-y: auto;
                    border: 1px solid #e0e0e0;
                    padding: 10px;
                    border-radius: 5px;
                }
                </style>
                """,
                unsafe_allow_html=True,
            )

            for idx, task in enumerate(pet.tasks):
                t_col1, t_col2 = st.columns([5, 1])
                with t_col1:
                    status = status_emoji(task.completed)
                    time_str = f"⏰ {task.scheduled_time}"
                    category_str = category_label(task.category)
                    priority_str = priority_label(task.priority)
                    duration_str = f"⏱️ {task.duration_minutes}m"
                    freq_str = f"🔄 {task.frequency}"

                    # Color code by completion status
                    if task.completed:
                        st.write(
                            f"{status} ~~**{task.title}**~~ — {time_str} | {category_str} | {priority_str} | {duration_str} | {freq_str}"
                        )
                    else:
                        st.write(
                            f"{status} **{task.title}** — {time_str} | {category_str} | {priority_str} | {duration_str} | {freq_str}"
                        )
                with t_col2:
                    if not task.completed:
                        if st.button("✓ Done", key=f"complete-{pet.name}-{id(task)}", use_container_width=True):
                            next_task = pet.complete_task(task)
                            owner.save_to_json(DATA_FILE)
                            if next_task is not None:
                                st.toast(f"✅ Next occurrence scheduled for {next_task.due_date}")
                            st.rerun()
                    else:
                        st.write("✓")
    else:
        st.info(f"👆 No tasks yet for {pet.name}. Add one above to get started!")
else:
    st.info("👆 Add a pet first, then you can add tasks!")

st.divider()
st.subheader("📊 Task Overview")

all_tasks = [task for _, task in owner.get_all_tasks()]

if all_tasks:
    overview_col1, overview_col2, overview_col3 = st.columns(3)
    with overview_col1:
        st.metric("Total Tasks", len(all_tasks))
    with overview_col2:
        completed = sum(1 for t in all_tasks if t.completed)
        st.metric("Completed", completed)
    with overview_col3:
        pending = len(all_tasks) - completed
        st.metric("Pending", pending)

    st.divider()

    tab1, tab2, tab3 = st.tabs(["⏰ By Time", "🔴 By Priority", "🔍 Filter"])

    with tab1:
        st.caption("Tasks ordered by scheduled time (earliest first)")
        sorted_tasks = scheduler.sort_by_time(all_tasks)
        st.dataframe(
            [
                {
                    "Status": status_emoji(t.completed),
                    "Time": t.scheduled_time,
                    "Task": t.title,
                    "Category": category_label(t.category),
                    "Priority": priority_label(t.priority),
                }
                for t in sorted_tasks
            ],
            use_container_width=True,
            hide_index=True,
        )

    with tab2:
        st.caption("Tasks ordered by priority (highest first), then by time")
        priority_sorted_tasks = scheduler.sort_by_priority_then_time(all_tasks)
        st.dataframe(
            [
                {
                    "Status": status_emoji(t.completed),
                    "Priority": priority_label(t.priority),
                    "Time": t.scheduled_time,
                    "Task": t.title,
                    "Category": category_label(t.category),
                }
                for t in priority_sorted_tasks
            ],
            use_container_width=True,
            hide_index=True,
        )

    with tab3:
        st.caption("Filter tasks by pet and completion status")
        filter_col1, filter_col2 = st.columns(2)
        with filter_col1:
            pet_filter = st.selectbox("Pet", ["All"] + [p.name for p in owner.pets], help="Filter by pet")
        with filter_col2:
            status_filter = st.selectbox("Status", ["All", "Pending", "Completed"], help="Filter by completion status")

        filtered = owner.get_all_tasks()
        filtered = scheduler.filter_tasks(
            filtered,
            pet_name=None if pet_filter == "All" else pet_filter,
            completed=None if status_filter == "All" else status_filter == "Completed",
        )
        if filtered:
            st.dataframe(
                [
                    {
                        "Status": status_emoji(task.completed),
                        "Pet": pet.name,
                        "Time": task.scheduled_time,
                        "Task": task.title,
                        "Priority": priority_label(task.priority),
                    }
                    for pet, task in filtered
                ],
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("👆 No tasks match your filter.")
else:
    st.info("📭 No tasks yet. Add a pet and some tasks to get started!")

st.divider()
st.subheader("⚙️ Schedule Actions")

action_col1, action_col2, action_col3 = st.columns(3)

with action_col1:
    st.markdown("**Check for Conflicts**")
    st.caption("Detect overlapping tasks")
    if st.button("🔍 Detect Conflicts", use_container_width=True):
        conflicts = scheduler.detect_conflicts(owner)
        if conflicts:
            for warning in conflicts:
                st.warning(f"⚠️ {warning}")
        else:
            st.success("✅ No conflicts detected.")

with action_col2:
    st.markdown("**Find Available Time**")
    st.caption("Find the next open time slot")
    slot_duration = st.number_input("Task duration (minutes)", min_value=1, max_value=240, value=20, key="slot_duration")
    if st.button("🕒 Find Next Slot", use_container_width=True):
        slot = scheduler.find_next_available_slot(owner, due_date=date.today(), duration_minutes=int(slot_duration))
        if slot:
            st.success(f"Next available: {slot}")
        else:
            st.warning("No slots available today.")

with action_col3:
    st.markdown("**Generate Daily Plan**")
    st.caption("Create optimized schedule")
    if st.button("📅 Generate Plan", use_container_width=True):
        plan = scheduler.generate_plan(owner)
        if not plan:
            st.info("No pending tasks to schedule.")
        else:
            for item in plan:
                message = (
                    f"{category_label(item.task.category)} {item.pet_name}: {item.task.title} "
                    f"({priority_label(item.task.priority)}, {item.task.duration_minutes} min)"
                )
                if item.included:
                    st.success(f"✅ {message}")
                else:
                    st.warning(f"⏭️ {message}")
                st.caption(f"Reason: {item.reason}")

st.divider()

# Help and Testing Section
with st.expander("📖 Help & Testing Guide", expanded=False):
    st.markdown("## How to Use petcare")

    col_help1, col_help2 = st.columns(2)

    with col_help1:
        st.markdown("### Getting Started")
        st.markdown(
            """
            1. **Enter your info** - Your name and available time (e.g., 60 min)
            2. **Add a pet** - Click "➕ Add Pet" with your pet's name and species
            3. **Add tasks** - Create care tasks with times and priorities
            4. **View tasks** - Use tabs to sort by time or priority
            5. **Mark complete** - Click "✓ Done" when finished
            6. **Generate plan** - Click "📅 Generate Plan" to see optimized schedule
            """
        )

    with col_help2:
        st.markdown("### Tips for Best Results")
        st.markdown(
            """
            ✨ **Pro Tips:**
            - Set realistic available time (include breaks!)
            - Use high priority for urgent tasks (vet visits, meds)
            - Schedule recurring tasks for habits (daily feeding)
            - Review conflicts before finalizing schedule
            - Check available slots before adding new tasks

            🔑 **Key Features:**
            - **Conflicts** - Detects overlapping tasks
            - **Slot Finder** - Shows gaps in your schedule
            - **Smart Plan** - Fits high-priority tasks first
            """
        )

    st.markdown("---")
    st.markdown("### Testing the App")

    test_col1, test_col2 = st.columns(2)

    with test_col1:
        st.markdown("**Quick Test (5 minutes):**")
        st.markdown(
            """
            1. Create a pet: "Max" (dog)
            2. Add 2 tasks:
               - "Morning Walk" 08:00, 30min, High
               - "Lunch" 12:00, 15min, High
            3. Click "Generate Plan"
            4. Check results fit in available time
            """
        )

    with test_col2:
        st.markdown("**Full Test (15 minutes):**")
        st.markdown(
            """
            1. Add 2+ pets with different species
            2. Add 5-10 tasks with mixed priorities
            3. Try each tab: Time, Priority, Filter
            4. Test conflict detection
            5. Create overlapping tasks, then fix them
            6. Close and reopen - verify data saves
            """
        )

    st.markdown("---")
    st.markdown("### Priority Colors")
    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1:
        st.markdown("🔴 **HIGH** - Urgent, must do (vet, meds)")
    with col_p2:
        st.markdown("🟡 **MEDIUM** - Important, schedule soon")
    with col_p3:
        st.markdown("🟢 **LOW** - Optional, nice to have")

    st.markdown("### Task Categories")
    st.markdown(
        """
        - 🚶 **Walk** - Exercise and bathroom breaks
        - 🍖 **Feeding** - Meals and treats
        - 💊 **Meds** - Medications and supplements
        - 🎾 **Enrichment** - Play and mental stimulation
        - 🧼 **Grooming** - Bathing, brushing, nail care
        """
    )
