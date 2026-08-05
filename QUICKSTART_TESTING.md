# petcare Quick Start Testing Guide

A quick reference for testing the app in under 5 minutes.

---

## 1. Launch the App (1 minute)

```bash
cd "path/to/applied-ai-petcare-system"
streamlit run app.py
```

**Expected:** App opens at `http://localhost:8501` with clean UI and clear sections.

---

## 2. Setup Profile & Pet (1 minute)

### Profile Section
- Keep name as "Jordan"
- Keep available time as "60 minutes"

### Pet Section
- Enter pet name: `Max`
- Select species: `dog`
- Click "➕ Add Pet"

**Expected:** 
- ✅ Success message: "✅ Max added!"
- ✅ Pet appears in table below

---

## 3. Add Test Tasks (2 minutes)

### Task 1: Morning Walk
- Pet: Max
- Title: Morning Walk
- Priority: high
- Category: walk
- Duration: 30 min
- Time: 08:00
- Frequency: once
- Click "➕ Add Task"

### Task 2: Lunch
- Pet: Max
- Title: Lunch Feeding
- Priority: high
- Category: feeding
- Duration: 15 min
- Time: 12:00
- Frequency: once
- Click "➕ Add Task"

**Expected:**
- ✅ Both tasks appear under "Tasks for Max"
- ✅ Tasks show all details with icons

---

## 4. Verify Features (1 minute)

### 📊 Task Overview Section

Click tabs and verify:
- **"⏰ By Time" tab** - Tasks ordered 08:00 → 12:00
- **"🔴 By Priority" tab** - Both high priority tasks shown
- **"🔍 Filter" tab** - Can filter by pet (shows Max) or status

**Expected:** All tabs work, tables display correctly with proper formatting

### ⚙️ Schedule Actions Section

1. Click "🔍 Detect Conflicts" → Should say "✅ No conflicts detected."
2. Click "🕒 Find Next Slot" (with 20 min duration) → Should show available time
3. Click "📅 Generate Plan" → Should show both tasks fit in 60 minutes

**Expected:** All three buttons work and show results

---

## 5. Test Data Persistence (30 seconds)

1. Close the browser tab
2. Reopen: `http://localhost:8501`
3. Check if toast says "Loaded saved data from data.json"
4. Verify pets and tasks are still there

**Expected:** 
- ✅ Data loads automatically
- ✅ Toast notification appears
- ✅ All pets and tasks preserved

---

## Success Criteria ✅

If all of the following are true, the app is working correctly:

- [ ] App launches without errors
- [ ] Profile section accepts input
- [ ] Can add pets and they appear in table
- [ ] Can add tasks and they display with icons
- [ ] Task overview metrics show correct counts
- [ ] All three tabs in task overview work
- [ ] Filter works correctly
- [ ] Detect Conflicts button works
- [ ] Find Next Slot button works
- [ ] Generate Plan button works and respects time budget
- [ ] Data persists after refresh/restart
- [ ] UI is clean and organized with no overlapping text
- [ ] All buttons, icons, and formatting display correctly

---

## Troubleshooting

### App won't launch
```bash
pip install --upgrade streamlit
streamlit run app.py --server.port 8501
```

### Data not loading
- Delete `data.json` and restart
- Check file is in the correct directory

### Tasks don't appear
- Verify you added a pet first
- Check browser console (F12) for errors

### Performance is slow
- Clear browser cache
- Restart Streamlit server

---

## Full Testing Docs

For comprehensive testing with all features and edge cases, see:
- **TESTING.md** - Complete test scenarios and verification steps
- **IMPROVEMENTS.md** - Details of all UI/UX improvements made

---

## Important Files

- **app.py** - The improved Streamlit application
- **pawpal_system.py** - Core business logic (unchanged)
- **formatting.py** - Display helpers (unchanged)
- **data.json** - Auto-generated data file (created on first use)

---

## Quick Feature Overview

| Feature | How to Test | Expected Result |
|---------|-----------|-----------------|
| Add Pet | Enter name, select species, click button | Pet appears in table |
| Add Task | Fill form, click button | Task appears with full details |
| Mark Done | Click "✓ Done" on task | Task shows ✅, next occurrence created if recurring |
| Sort by Time | Click "By Time" tab | Tasks ordered earliest→latest |
| Sort by Priority | Click "By Priority" tab | High priority first |
| Filter | Select pet and status | Shows only matching tasks |
| Detect Conflicts | Click button | Shows warnings if overlapping |
| Find Slot | Enter duration, click button | Shows next available time |
| Generate Plan | Click button | Shows which tasks fit in available time |
| Persist Data | Restart app | Data loads automatically |

---

## Notes for Testing

- The app loads demo values (Jordan, 60 min, Mochi, etc.) but these are just defaults
- Everything is customizable - try different values
- Data.json stores everything in JSON format - you can view/edit it if needed
- The app is designed to work with multiple pets at once
- Recurring tasks (daily/weekly) create new tasks automatically when marked complete

---

**Time to complete testing: ~5 minutes**

If everything works, petcare is ready to use! 🎉
