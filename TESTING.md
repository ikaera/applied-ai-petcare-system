# petcare Testing Guide

## Overview

This guide provides detailed instructions for testing the petcare Streamlit application to ensure all features work correctly and the user experience is clear and intuitive.

---

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Launching the Application](#launching-the-application)
- [Feature Testing](#feature-testing)
  - [Test 1: Profile Setup](#test-1-profile-setup)
  - [Test 2: Add a Pet](#test-2-add-a-pet)
  - [Test 3: Add Tasks](#test-3-add-tasks)
  - [Test 4: Task Overview](#test-4-task-overview---multiple-views)
  - [Test 5: Mark Tasks Complete](#test-5-mark-tasks-complete)
  - [Test 6: Detect Conflicts](#test-6-detect-scheduling-conflicts)
  - [Test 7: Find Available Slot](#test-7-find-next-available-slot)
  - [Test 8: Generate Daily Plan](#test-8-generate-daily-plan)
  - [Test 9: Data Persistence](#test-9-data-persistence)
- [Edge Cases & Stress Tests](#edge-cases--stress-tests)
- [User Experience Checks](#user-experience-checks)
- [Testing Checklist](#testing-checklist)
- [Common Issues & Troubleshooting](#common-issues--troubleshooting)
- [Manual Testing Report Template](#manual-testing-report-template)

---

## Prerequisites

Before testing, ensure you have:

1. **Python 3.8+** installed
2. **Required dependencies installed:**
   ```bash
   pip install streamlit
   ```
3. **Project files present:**
   - `app.py` (Streamlit application)
   - `pawpal_system.py` (core logic)
   - `formatting.py` (display helpers)

---

## Launching the Application

### Step 1: Start the Streamlit App

Open a terminal in the project directory and run:

```bash
streamlit run app.py
```

**Expected Result:**
- Streamlit opens automatically in your default browser (usually `http://localhost:8501`)
- The petcare title and introduction appear
- Page layout is clean with clear sections

### Step 2: Verify Initial State

**Check these elements:**
- ✅ Title: "🐾 petcare"
- ✅ Introduction text explaining the app's features
- ✅ Profile section with name and available time inputs
- ✅ All sections have helpful descriptions and icons

---

## Feature Testing

### Test 1: Profile Setup

**Test Step:** Set up your user profile

1. In the "📝 Your Profile" section:
   - Change "Your name" field to `TestUser`
   - Set "Available time today" to `90` minutes
   
2. Scroll down and verify the values are used (they'll appear in generated plans)

**Expected Results:**
- ✅ Name field accepts any text
- ✅ Time field accepts values between 1-600 minutes
- ✅ No errors on input
- ✅ Values persist as you interact with other parts of the app

---

### Test 2: Add a Pet

**Test Step:** Add your first pet

1. In the "🐶 Manage Your Pets" section:
   - Enter "Max" in the pet name field
   - Select "dog" from the Species dropdown
   - Click "➕ Add Pet"

2. Verify the pet appears in the table below

**Expected Results:**
- ✅ Success message appears: "✅ Max added!"
- ✅ Pet appears in the "Your Pets" table
- ✅ Table shows: Name=Max, Species=Dog
- ✅ Input fields reset to default values

**Test Step:** Add a second pet

1. Enter "Whiskers" in the pet name field
2. Select "cat" from Species dropdown
3. Click "➕ Add Pet"

**Expected Results:**
- ✅ Both pets appear in the table (Max and Whiskers)
- ✅ Success message appears for Whiskers
- ✅ Data persists (file `data.json` is created)

---

### Test 3: Add Tasks

**Test Step:** Add tasks for the first pet

1. In the "✅ Add Care Tasks" section:
   - "Which pet is this task for?" → Select "Max"
   - Task title → "Morning Walk"
   - Priority level → "high"
   - Category → "walk"
   - Duration → 30 minutes
   - Scheduled time → 08:00
   - Frequency → "daily"
   - Click "➕ Add Task"

2. Verify task appears under "Tasks for Max"

**Expected Results:**
- ✅ Success message: "✅ Task 'Morning Walk' added for Max!"
- ✅ Task displays with full details:
   - Status: ⬜ (uncompleted)
   - Time: ⏰ 08:00
   - Title: Morning Walk
   - Category: 🚶 walk
   - Priority: 🔴 HIGH
   - Duration: ⏱️ 30m
   - Frequency: 🔄 daily
   - A "✓ Done" button on the right

**Test Step:** Add more tasks to test variety

Add these tasks to explore different combinations:

**Task 2 - Feeding (High Priority):**
- Pet: Max
- Title: Lunch Feeding
- Priority: high
- Category: feeding
- Duration: 15 minutes
- Time: 12:00
- Frequency: daily

**Task 3 - Medication (Medium Priority):**
- Pet: Whiskers
- Title: Allergy Medication
- Priority: medium
- Category: meds
- Duration: 5 minutes
- Time: 14:00
- Frequency: daily

**Task 4 - Enrichment (Low Priority):**
- Pet: Whiskers
- Title: Playtime
- Priority: low
- Category: enrichment
- Duration: 20 minutes
- Time: 18:00
- Frequency: once

**Expected Results:**
- ✅ All tasks appear in their respective pet's task list
- ✅ All display correct icons and formatting
- ✅ No errors occur

---

### Test 4: Task Overview - Multiple Views

**Test Step:** View "📊 Task Overview" section

Verify three metrics appear:
- **Total Tasks:** Should show 4
- **Completed:** Should show 0
- **Pending:** Should show 4

**Test Step:** Click the "⏰ By Time" tab

**Expected Results:**
- ✅ Tasks display in a table sorted by time (earliest first)
- ✅ Order should be: 08:00, 12:00, 14:00, 18:00
- ✅ Table has columns: Status, Time, Task, Category, Priority
- ✅ All icons display correctly (✅ or ⬜, ⏰, 🚶, 🔴/🟡/🟢, etc.)

**Test Step:** Click the "🔴 By Priority" tab

**Expected Results:**
- ✅ Tasks sorted by priority (high → medium → low), then by time
- ✅ Order should be: Morning Walk (08:00), Lunch Feeding (12:00), Allergy Medication (14:00), Playtime (18:00)
- ✅ Table columns in different order: Status, Priority, Time, Task, Category

**Test Step:** Click the "🔍 Filter" tab

1. Leave "Pet" as "All" and "Status" as "All"
2. Verify all 4 tasks appear

3. Change "Pet" to "Max"
4. Verify only 2 tasks appear (Morning Walk, Lunch Feeding)

5. Change "Pet" back to "All"
6. Change "Status" to "Completed"
7. Verify 0 tasks appear (message: "👆 No tasks match your filter.")

8. Change "Status" to "Pending"
9. Verify all 4 tasks appear again

**Expected Results:**
- ✅ Filtering works correctly for both pet and status
- ✅ Appropriate messages show when no results
- ✅ Data is displayed in a clean table

---

### Test 5: Mark Tasks Complete

**Test Step:** Complete a task

1. Scroll back to "Tasks for Max" section
2. Next to "Morning Walk" task, click the "✓ Done" button

**Expected Results:**
- ✅ Success message appears: "✅ Next occurrence scheduled for [today's date]"
- ✅ "Morning Walk" task in the list now shows ✅ (completed) instead of ⬜
- ✅ A new "Morning Walk" task is created for tomorrow (since it's daily)
- ✅ Metrics update: Completed=1, Pending=4 (total=5 now)

**Test Step:** Complete a non-recurring task

1. Find "Playtime" (frequency: once)
2. Click "✓ Done"

**Expected Results:**
- ✅ Task shows as ✅ (completed)
- ✅ No new task is created (it's a one-time task)
- ✅ Metrics update: Pending should decrease by 1

---

### Test 6: Detect Scheduling Conflicts

**Test Step:** Add conflicting tasks

Add a task that overlaps with an existing task:

1. Add a task for Max:
   - Title: "Grooming Session"
   - Priority: high
   - Category: grooming
   - Duration: 45 minutes
   - Time: 08:00 (same as Morning Walk!)
   - Frequency: once

2. Scroll to "⚙️ Schedule Actions" section
3. Click "🔍 Detect Conflicts" button

**Expected Results:**
- ✅ A warning appears indicating the conflict
- ✅ Warning mentions both tasks and their times
- ✅ Example: "⚠️ Conflict: Morning Walk (08:00, 30m) overlaps with Grooming Session (08:00, 45m)"

**Test Step:** Remove conflict and verify

1. Go back and complete the "Grooming Session" task (mark it done)
2. Click "🔍 Detect Conflicts" again

**Expected Results:**
- ✅ Success message appears: "✅ No conflicts detected."

---

### Test 7: Find Next Available Slot

**Test Step:** Find available time

1. Scroll to "⚙️ Schedule Actions"
2. In "Find Available Time" column:
   - Set "Task duration (minutes)" to `45`
   - Click "🕒 Find Next Slot"

**Expected Results:**
- ✅ A success message shows the next available time
- ✅ Example: "Next available: 13:45" (or similar, depending on scheduled tasks)
- ✅ The time slot is long enough for the requested duration

**Test Step:** Request more time than available

1. Set duration to `600` minutes (10 hours)
2. Click "🕒 Find Next Slot"

**Expected Results:**
- ✅ A warning appears: "No slots available today."

---

### Test 8: Generate Daily Plan

**Test Step:** Generate an optimized schedule

1. Scroll to "⚙️ Schedule Actions"
2. Click "📅 Generate Plan" button

**Expected Results:**
- ✅ A plan is generated showing which tasks fit in the available 90 minutes
- ✅ **Included tasks** (✅) show tasks that fit in the time budget, sorted by priority
- ✅ **Skipped tasks** (⏭️) show tasks that don't fit, with a reason
- ✅ Total duration of included tasks ≤ available minutes
- ✅ High-priority tasks are included first

**Example Output:**
```
✅ 🚶 Max: Morning Walk (🔴 HIGH, 30m)
✅ 🍖 Max: Lunch Feeding (🔴 HIGH, 15m)
⏭️ 💊 Whiskers: Allergy Medication (🟡 MEDIUM, 5m)
⏭️ 🎾 Whiskers: Playtime (🟢 LOW, 20m)
```

---

### Test 9: Data Persistence

**Test Step:** Verify data saves and loads

1. Complete the test scenario above (add pets and tasks)
2. Close the browser tab
3. Relaunch the app: `streamlit run app.py`
4. Refresh the browser or wait for it to reload

**Expected Results:**
- ✅ A toast notification appears: "✅ Loaded saved data from data.json."
- ✅ All pets are still visible in the "Your Pets" table
- ✅ All tasks are still visible with correct status (completed/pending)
- ✅ Metrics show correct totals

---

## Edge Cases & Stress Tests

### Test 10: Boundary Values

**Test Step:** Enter extreme values

1. Set "Available time" to 1 minute
2. Try to add a task with 500 minutes duration
3. Click "Generate Plan"

**Expected Results:**
- ✅ App doesn't crash
- ✅ Plan shows no tasks fit (or warning about time limit)

**Test Step:** Create many pets and tasks

1. Add 5+ pets
2. Add 10+ tasks across various pets
3. Try filtering, sorting, and generating plans

**Expected Results:**
- ✅ No performance issues
- ✅ All features still work correctly
- ✅ UI remains responsive

### Test 11: Special Characters

**Test Step:** Enter special characters in fields

1. Pet name: "Max-O'Reilly 🐕"
2. Task title: "Lunch! (must do) @ 12:00"

**Expected Results:**
- ✅ Special characters display correctly
- ✅ No encoding errors
- ✅ Data saves and loads properly

---

## User Experience Checks

### Check 1: Visual Clarity

Verify these UI elements are present and clear:

- ✅ All sections have descriptive headers with icons
- ✅ Help text appears on hover for input fields
- ✅ Success/warning/info messages are color-coded
- ✅ Emojis are used consistently throughout
- ✅ Tables are well-formatted and easy to read
- ✅ No text overlaps or layout issues
- ✅ Buttons are clearly labeled with action icons

### Check 2: User Guidance

Verify users understand what to do:

- ✅ Profile section explains what to input
- ✅ Pet section clearly shows how to add pets
- ✅ Task section has helpful descriptions for each field
- ✅ Action buttons explain their purpose (Detect Conflicts, Find Slot, Generate Plan)
- ✅ Empty states show encouraging messages (👆 prompts)
- ✅ Success messages confirm actions

### Check 3: Navigation

Verify users can easily navigate:

- ✅ Sections are clearly separated with dividers
- ✅ Logical flow: Profile → Pets → Tasks → Overview → Actions
- ✅ Tabs in "Task Overview" are easy to switch between
- ✅ No dead-ends or confusing navigation

---

## Testing Checklist

Use this checklist to verify all features are working:

### Setup & Launch
- [ ] App launches without errors
- [ ] Initial UI renders cleanly
- [ ] All sections are visible and organized

### Pet Management
- [ ] Can add a pet
- [ ] Pet appears in table
- [ ] Can add multiple pets
- [ ] All pet info displays correctly

### Task Management
- [ ] Can add a task to a pet
- [ ] Task displays with all details (time, priority, category, duration, frequency)
- [ ] Can add multiple tasks
- [ ] Tasks display for correct pets

### Task Overview
- [ ] Metrics show correct counts
- [ ] "By Time" tab sorts correctly
- [ ] "By Priority" tab sorts correctly
- [ ] "Filter" tab filters by pet
- [ ] "Filter" tab filters by status

### Task Completion
- [ ] Can mark a task complete
- [ ] Completed task shows ✅
- [ ] Recurring task creates next occurrence
- [ ] One-time task doesn't create new occurrence
- [ ] Metrics update correctly

### Schedule Features
- [ ] Conflict detection works
- [ ] No false positives for non-overlapping tasks
- [ ] Find available slot returns correct time
- [ ] Plan generation includes high-priority tasks first
- [ ] Plan respects time budget
- [ ] Plan explains why tasks are included/skipped

### Data
- [ ] Data saves to `data.json`
- [ ] Data loads on app restart
- [ ] Toast notification appears on load

### UX & Clarity
- [ ] All buttons have clear labels
- [ ] Help text appears for inputs
- [ ] Success/warning messages are helpful
- [ ] Empty states show guidance
- [ ] Layout is clean and organized
- [ ] No errors in browser console

---

## Common Issues & Troubleshooting

### Issue: App doesn't launch

**Solution:**
```bash
# Ensure Streamlit is installed
pip install --upgrade streamlit

# Try running with explicit port
streamlit run app.py --server.port 8501
```

### Issue: `data.json` not loading

**Solution:**
- Verify `data.json` exists in the project directory
- Check file permissions
- Try deleting `data.json` and recreating it
- Check that JSON is valid (use a JSON validator)

### Issue: Tasks don't appear after adding

**Solution:**
- Verify you selected a pet before adding tasks
- Check browser console for JavaScript errors
- Try refreshing the page
- Check if `data.json` was created/updated

### Issue: Performance is slow

**Solution:**
- Clear browser cache
- Reduce number of tasks (remove old data from `data.json`)
- Restart Streamlit server
- Check system resources

---

## Manual Testing Report Template

When testing, fill out this template:

```
Date: _______________
Tester: _______________
Environment: Python ___ | Streamlit ___

PASS/FAIL Summary:
- Profile Setup: [ ] PASS [ ] FAIL
- Pet Management: [ ] PASS [ ] FAIL
- Task Management: [ ] PASS [ ] FAIL
- Task Overview: [ ] PASS [ ] FAIL
- Task Completion: [ ] PASS [ ] FAIL
- Conflict Detection: [ ] PASS [ ] FAIL
- Find Available Slot: [ ] PASS [ ] FAIL
- Generate Plan: [ ] PASS [ ] FAIL
- Data Persistence: [ ] PASS [ ] FAIL
- UX & Clarity: [ ] PASS [ ] FAIL

Issues Found:
1. _______________________________________________
2. _______________________________________________
3. _______________________________________________

Notes:
___________________________________________________
___________________________________________________
```

---

## Conclusion

When all tests in this guide pass successfully, the petcare application is ready for use. The app should provide a clear, intuitive interface for managing pet care tasks with smart scheduling features.

For issues or questions, review the CLAUDE.md file for project context.
