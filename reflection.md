# PawPal+ Project Reflection

## 1. System Design

**Core user actions**

After reading the scenario, I identified three core actions that a user should be able to perform in order to stay on top of their pet's care. First, the user should be able to add a pet with its name and species. Second, the user should be able to schedule a care task for that pet, such as a walk or a feeding, along with a time, how long it takes, its priority, and whether it repeats daily or weekly. Lastly, the user should be able to see today's schedule for all of their pets in time order, which includes being warned about conflicts and being able to mark a task as done.

**a. Initial design**

My initial UML design (`diagrams/uml_draft.mmd`) was made up of four classes, which were Task, Pet, Owner, and Scheduler. The Task class represents a single care activity and holds the description, the time in `HH:MM` format, the duration, the priority, the frequency, and whether or not it has been completed. The Pet class holds the pet's name, its species, and its own list of tasks, which allows each pet to keep track of what needs to be done for it. The Owner class holds a list of pets and is able to return all of the tasks across every pet. Additionally, the Scheduler class acts as the "brain" of the system, which takes in an Owner and organizes all of the tasks into a schedule. In regard to the relationships, an Owner has many Pets, a Pet has many Tasks, and the Scheduler reads the tasks through the Owner. I used Python dataclasses for Task and Pet since they mostly hold data, which kept the code clean and simple.

**b. Design changes**

My design did change during implementation, mainly in order to support the features that were added later on. First, I added a `due_date` to the Task class, since recurring tasks need to know which day they are for, otherwise tomorrow's walk would look exactly the same as today's walk. Furthermore, I changed `get_all_tasks()` so that it returns pairs of a pet and its task instead of just the tasks, which allows the schedule to show which pet each task belongs to without having the Task class store its pet. I also added `filter_tasks()`, `mark_task_complete()`, `detect_conflicts()`, and `next_occurrence()` in Phase 4. I placed `mark_task_complete()` in the Scheduler rather than in the Task class, since creating the next occurrence means adding a new task to the pet's list, which a Task cannot do on its own. Overall, the final diagram in `diagrams/uml_final.mmd` reflects these changes.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers the time of day, the date, whether or not a task has been completed, and how often a task repeats. Each task also stores its priority and duration, which are shown in the schedule so that the owner can decide what matters most. I decided that time mattered the most, since pet care such as feeding and medication usually happens at set times, and a schedule that is in the right order is the most useful thing for a busy owner. Conflicts were the next most important, since having two things scheduled at once is a real problem that the owner needs to be aware of in order to fix it.

**b. Tradeoffs**

One tradeoff that my scheduler makes is that it only checks for tasks that are scheduled at the exact same time, rather than checking for overlapping durations. For example, a 30-minute walk at 07:30 and a feeding at 07:45 do overlap, but the scheduler will not show a warning for them. I believe this tradeoff is reasonable for this scenario, since most pet tasks are short and owners usually schedule them on round times. Additionally, checking for exact matches is simple to read, easy to test, and only returns a warning message rather than crashing the program. Checking for overlaps would require converting the times into minutes and comparing every pair of tasks, which adds more complexity for a small benefit at this stage.

---

## 3. AI Collaboration

**a. How you used AI**

I used Claude as my AI coding assistant for this project, all within one chat rather than separate chat sessions for each phase. I gave it the assignment instructions along with the starter files from my repo, and it was able to read and write files directly in my project folder, which was the most effective feature since many of the changes had to touch multiple files at once, such as the recurring tasks needing changes to both `pawpal_system.py` and `main.py`. It helped with drafting the UML diagrams, writing the class skeleton with dataclasses, implementing the Scheduler methods, connecting `app.py` to the logic through `st.session_state`, writing the pytest tests, and filling in the README. The most helpful thing I did was ask it to check its work against the assignment steps, which is how we found that the class skeleton had not been committed as its own step and that the Demo Walkthrough was missing the CLI output. Although I did not use separate chat sessions, I presume that doing so would have helped keep each phase more focused, since one long chat made it harder to tell which phase we were working on at times.

**b. Judgment and verification**

One moment where I did not accept things as they were was with my commits. At first, I told the AI to skip the multiple commits and that I wanted to do one single commit for the whole project. However, after reviewing the Phase 1 steps again, I noticed that the skeleton commit was its own step, so I changed my mind and had the AI create a skeleton version of `pawpal_system.py` first. I committed that on its own with the message "chore: add class skeletons from UML", and then the AI put the full code back for my second commit. Additionally, I asked it to always ask me before saving or committing anything to my repo, in order to keep control over what goes into my project. In regard to verifying the code, I ran `python -m pytest` on my own computer, where all 11 tests passed, and I ran the Streamlit app with `python -m streamlit run app.py` in order to try adding pets, scheduling tasks, and seeing the conflict warning myself. All in all, being the "lead architect" meant that the AI could write the code quickly, but I still had to make the decisions, follow the assignment, and check that everything actually worked.

---

## 4. Testing and Verification

**a. What you tested**

I tested marking a task as complete, adding tasks to a pet, sorting tasks into chronological order, filtering tasks by pet and by completion status, daily, weekly, and one-time recurrence, conflict detection for tasks at the same time and at different times, and the edge case of a schedule that has no tasks. These tests were important since they cover the behaviors that the whole app depends on. If the sorting or the recurrence were wrong, the owner would either see the schedule in the wrong order or miss a feeding the next day, which defeats the purpose of the app.

**b. Confidence**

I would give my scheduler a confidence level of 4 out of 5, since all of the core behaviors are tested and all 11 tests passed. However, it is not perfect, since the conflict detection only checks for exact time matches. If I had more time, I would test overlapping durations, tasks that go past midnight, invalid time inputs such as "7:5", completing the same recurring task twice, and two pets that share the same name.

---

## 5. Reflection

**a. What went well**

The part of this project that I am most satisfied with is how the classes are separated. All of the logic lives in `pawpal_system.py`, which allowed it to be tested in the terminal first before connecting it to the Streamlit app, and `app.py` only calls those methods. Additionally, seeing the recurring tasks work was satisfying, since completing a daily walk right away schedules the next one for tomorrow.

**b. What you would improve**

If I had another iteration, I would add conflict detection that checks overlapping durations, allow the user to edit or delete tasks in the app, sort by priority when two tasks share the same time, and save the data to a file so that it does not disappear once the app is closed. Furthermore, I would split my commits into smaller steps as I go, rather than making most of the changes in one commit at the end.

**c. Key takeaway**

The key takeaway from this project is that designing the system first, by starting with the UML, then the skeleton, and then the logic, made working with AI much more useful, since it had a clear structure to follow. In conclusion, AI is a powerful tool that can write code fast, but it is still up to me to follow the requirements, make the design decisions, and verify that the work is correct before turning it in.
