# PawPal+ (Module 2 Project)

**PawPal+** is a Streamlit app that helps a busy pet owner plan care tasks for their pets. It keeps track of walks, feeding, meds, grooming and other tasks, builds a sorted daily schedule, warns about time conflicts, and automatically reschedules recurring tasks.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

## ✨ Features

- **Multiple pets per owner.** Each pet keeps its own list of care tasks.
- **Sorting by time.** Today's schedule is listed in chronological order, regardless of the order tasks were added.
- **Filtering.** View tasks for a single pet, or only tasks that still need to be done.
- **Daily and weekly recurrence.** Completing a recurring task automatically creates the next one (tomorrow, or one week later).
- **Conflict warnings.** If two unfinished tasks are scheduled at the same time, the app shows a warning instead of crashing.
- **Persistent session.** The Streamlit app keeps your owner, pets and tasks in `st.session_state`, so data survives button clicks.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Run

```bash
python main.py          # CLI demo
streamlit run app.py    # Streamlit app
python -m pytest        # tests
```

## 🏗️ System Design

The logic lives in `pawpal_system.py` and is made of four classes:

| Class | Responsibility |
|-------|----------------|
| `Task` (dataclass) | One care activity: description, time (`HH:MM`), duration, priority, frequency, due date, completion status |
| `Pet` (dataclass) | A pet's name, species and its list of tasks |
| `Owner` | Holds multiple pets and gives access to all their tasks |
| `Scheduler` | The "brain": sorts, filters, completes, and checks tasks for conflicts across all pets |

UML diagrams (Mermaid): `diagrams/uml_draft.mmd` (Phase 1 draft) and `diagrams/uml_final.mmd` (final design).

## 🖥️ Sample Output

Output of `python main.py`:

```
======================================================================
Today's Schedule for Jordan
======================================================================
  Sun 10/11 07:30  Mochi    Morning walk        30 min  [high] [daily] [todo]
  Sun 10/11 08:00  Mochi    Heartworm pill       5 min  [medium] [once] [todo]
  Sun 10/11 08:00  Luna     Feeding             10 min  [high] [daily] [todo]
  Sun 10/11 12:00  Luna     Brush fur           15 min  [low] [weekly] [todo]
  Sun 10/11 18:00  Mochi    Evening walk        30 min  [high] [daily] [todo]

Conflict check:
  WARNING: Conflict at 08:00: Mochi: Heartworm pill, Luna: Feeding

Only Mochi's tasks:
  Sun 10/11 07:30  Mochi    Morning walk        30 min  [high] [daily] [todo]
  Sun 10/11 08:00  Mochi    Heartworm pill       5 min  [medium] [once] [todo]
  Sun 10/11 18:00  Mochi    Evening walk        30 min  [high] [daily] [todo]

Completed 'Morning walk'. Next one scheduled for 2026-10-12.

Incomplete tasks (all pets, all days):
  Sun 10/11 08:00  Mochi    Heartworm pill       5 min  [medium] [once] [todo]
  Sun 10/11 08:00  Luna     Feeding             10 min  [high] [daily] [todo]
  Sun 10/11 12:00  Luna     Brush fur           15 min  [low] [weekly] [todo]
  Sun 10/11 18:00  Mochi    Evening walk        30 min  [high] [daily] [todo]
  Mon 10/12 07:30  Mochi    Morning walk        30 min  [high] [daily] [todo]
```

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()`, `Scheduler.get_todays_schedule()` | Uses `sorted()` with a lambda key of `(due_date, time)`. `"HH:MM"` strings with leading zeros sort correctly as text. |
| Filtering | `Scheduler.filter_tasks(pet_name=..., completed=...)` | Filter by pet name (case-insensitive), by completion status, or both. |
| Conflict handling | `Scheduler.detect_conflicts()` | Groups today's unfinished tasks by exact time and returns a warning string for any time with 2+ tasks. Returns a list of messages, never raises an error. |
| Recurring tasks | `Task.next_occurrence()`, `Scheduler.mark_task_complete()` | Marking a `daily` task complete adds a copy due `due_date + timedelta(days=1)`; `weekly` uses `timedelta(weeks=1)`; `once` creates nothing. |

## 🧪 Testing PawPal+

```bash
python -m pytest
```

The tests in `tests/test_pawpal.py` cover:

- **Task basics:** `mark_complete()` changes status; adding a task increases a pet's task count
- **Sorting:** tasks added out of order come back in chronological order
- **Filtering:** by pet name and by completion status
- **Recurrence:** daily → next day, weekly → one week later, one-time → no new task
- **Conflict detection:** same-time tasks are flagged; different times are not
- **Edge case:** an owner whose pets have no tasks gets an empty schedule

Sample test output:

```
=================================================================================== test session starts ====================================================================================
platform win32 -- Python 3.13.7, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\Miko\ai110-module2show-pawpal-starter
plugins: anyio-4.15.1
collected 11 items

tests\test_pawpal.py ...........                                                                                                                                                      [100%]

==================================================================================== 11 passed in 0.06s ====================================================================================
```

**Confidence level:** ⭐⭐⭐⭐ (4/5). All core behaviors are tested and pass. Conflict detection only checks exact time matches, so overlapping durations (e.g. a 30-minute walk at 07:30 and a task at 07:45) are not caught yet.

## 📸 Demo Walkthrough

1. **Start the app** with `streamlit run app.py`. Enter the owner's name at the top.
2. **Add pets.** In "Add a Pet", type a name (e.g. Mochi), choose a species, and click **Add pet**. Repeat for a second pet (e.g. Luna the cat). The pet list updates right away.
3. **Schedule tasks.** In "Schedule a Task", pick a pet, enter a task name, time, duration, priority, and whether it repeats (once / daily / weekly), then click **Add task**.
4. **View today's schedule.** The "Today's Schedule" table shows every task for today, sorted by time across all pets. Use **Show tasks for** to filter to one pet, or **Hide completed tasks** to see only what's left.
5. **See conflict warnings.** If two unfinished tasks share the same time (e.g. Mochi's pill and Luna's feeding at 08:00), a yellow warning appears above the table suggesting you move one.
6. **Complete a task.** Choose a task under **Mark a task complete** and click **Complete task**. Its status changes to ✅ done. If it was a daily or weekly task, a message confirms when the next one is scheduled.

**CLI demo:** the same scheduler behaviors (sorting, pet filter, conflict warning, daily recurrence) from `python main.py`:

```
======================================================================
Today's Schedule for Jordan
======================================================================
  Sun 10/11 07:30  Mochi    Morning walk        30 min  [high] [daily] [todo]
  Sun 10/11 08:00  Mochi    Heartworm pill       5 min  [medium] [once] [todo]
  Sun 10/11 08:00  Luna     Feeding             10 min  [high] [daily] [todo]
  Sun 10/11 12:00  Luna     Brush fur           15 min  [low] [weekly] [todo]
  Sun 10/11 18:00  Mochi    Evening walk        30 min  [high] [daily] [todo]

Conflict check:
  WARNING: Conflict at 08:00: Mochi: Heartworm pill, Luna: Feeding

Only Mochi's tasks:
  Sun 10/11 07:30  Mochi    Morning walk        30 min  [high] [daily] [todo]
  Sun 10/11 08:00  Mochi    Heartworm pill       5 min  [medium] [once] [todo]
  Sun 10/11 18:00  Mochi    Evening walk        30 min  [high] [daily] [todo]

Completed 'Morning walk'. Next one scheduled for 2026-10-12.

Incomplete tasks (all pets, all days):
  Sun 10/11 08:00  Mochi    Heartworm pill       5 min  [medium] [once] [todo]
  Sun 10/11 08:00  Luna     Feeding             10 min  [high] [daily] [todo]
  Sun 10/11 12:00  Luna     Brush fur           15 min  [low] [weekly] [todo]
  Sun 10/11 18:00  Mochi    Evening walk        30 min  [high] [daily] [todo]
  Mon 10/12 07:30  Mochi    Morning walk        30 min  [high] [daily] [todo]
```
