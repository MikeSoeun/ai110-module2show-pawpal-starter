# PawPal+ Project Reflection

## 1. System Design

**Core user actions**

1. Add a pet (name and species) to their profile.
2. Schedule a care task for a pet, with a time, duration, priority, and whether it repeats (once, daily, or weekly).
3. See today's schedule for all pets in time order, with warnings about conflicts, and mark tasks as done.

**a. Initial design**

My initial UML (`diagrams/uml_draft.mmd`) had four classes:

- **Task**: one care activity. Holds the description, time (`HH:MM`), duration, priority, frequency, and whether it's completed. It can mark itself complete.
- **Pet**: a pet's name, species, and its own list of tasks. It can add tasks.
- **Owner**: holds a list of pets and can return all tasks across every pet.
- **Scheduler**: the "brain". It takes an Owner and organizes the tasks (sorting them into today's schedule).

The relationships are: an Owner has many Pets, a Pet has many Tasks, and the Scheduler reads tasks through the Owner. I used Python dataclasses for Task and Pet because they mostly hold data.

**b. Design changes**

Yes, the design changed in a few ways while I implemented it:

- **Added `due_date` to Task.** Recurring tasks need to know *which day* they're for. Without a date, "the next daily walk" would look identical to today's walk.
- **`get_all_tasks()` returns (pet, task) pairs instead of just tasks.** The schedule needs to show which pet each task belongs to, and a Task doesn't store its pet. Returning pairs kept Task simple instead of adding a back-reference to Pet.
- **Added `filter_tasks()`, `mark_task_complete()`, `detect_conflicts()`, and `next_occurrence()`.** These came in Phase 4. `mark_task_complete()` lives in the Scheduler (not Task) because creating the next task means adding it to the pet's list, and a Task alone can't do that.

The final diagram is in `diagrams/uml_final.mmd`.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- The scheduler considers **time of day** (tasks are ordered by `HH:MM`), **date** (only today's tasks show in today's schedule), **completion status**, and **frequency** (daily/weekly tasks come back automatically). Each task also stores **priority** and **duration**, which are shown so the owner can decide what matters most.
- I decided **time** mattered most, because pet care like feeding and meds happens at set times. A schedule that's in the right order is the most useful thing for a busy owner. Conflicts were next most important, since two things at once is a real problem the owner needs to notice.

**b. Tradeoffs**

- My conflict detection only checks for tasks at the **exact same time**. It doesn't check overlapping durations. For example, a 30-minute walk at 07:30 and feeding at 07:45 actually overlap, but no warning is shown.
- This is reasonable for this scenario because most pet tasks are short and an owner usually schedules them on round times. Exact matching is simple to read, easy to test, and never crashes. It only returns warning messages. Checking overlaps would mean converting times to minutes and comparing every pair of tasks, which adds complexity for a small benefit at this stage.

---

## 3. AI Collaboration

**a. How you used AI**

- I used Claude as an AI coding assistant across all phases: brainstorming the four classes and drafting the Mermaid UML, generating the class skeleton with dataclasses, implementing the Scheduler methods, wiring `app.py` to the logic using `st.session_state`, writing pytest tests, and drafting docs.
- The most helpful prompts were specific ones that named the file and method, such as "how should the Scheduler retrieve all tasks from the Owner's pets?" and "how do I sort `HH:MM` strings with a lambda key?"

**b. Judgment and verification**

- For sorting, one option was to convert each `HH:MM` string into a `datetime.time` object before sorting. I kept the simpler version that sorts the strings directly, because zero-padded `HH:MM` strings already sort correctly as text, and the Streamlit time picker always produces zero-padded times. It's easier to read and has the same result.
- I verified suggestions by running `python main.py` to see the output, and by running `python -m pytest`. For example, the tests confirmed that completing a daily task creates a new task dated exactly one day later and that one-time tasks don't create anything.

---

## 4. Testing and Verification

**a. What you tested**

- Marking a task complete, adding tasks to a pet, sorting tasks into chronological order, filtering by pet and by completion status, daily/weekly/one-time recurrence, conflict detection (same time flagged, different times not flagged), and the edge case of a schedule with no tasks.
- These were important because they're the behaviors the app depends on. If sorting or recurrence were wrong, the owner would see a wrong schedule or miss a feeding the next day.

**b. Confidence**

- I'm fairly confident (4/5). All the core behaviors have tests and they pass.
- Next I would test: overlapping durations (not just exact times), tasks spanning midnight, invalid time strings like `"7:5"`, completing the same recurring task twice, and two pets with the same name.

---

## 5. Reflection

**a. What went well**

- I'm most satisfied with how the classes are separated. All the logic is in `pawpal_system.py`, so it could be tested from the terminal first, and `app.py` only calls those methods. Recurring tasks were also satisfying to see work: completing a daily walk immediately shows tomorrow's walk.

**b. What you would improve**

- I would add overlap-based conflict detection using durations, let the user edit or delete tasks in the UI, sort by priority when times tie, and save data to a file so it lasts after the app closes.

**c. Key takeaway**

- Designing the system first (UML, then skeleton, then logic) made the AI's help much more useful, because I could give it a clear structure to follow. As the "lead architect," my job was to decide what the classes should be responsible for and to check the AI's code against the tests, instead of just accepting whatever it generated.
