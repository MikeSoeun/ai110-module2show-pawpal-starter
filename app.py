from datetime import date

import streamlit as st

from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.caption("A pet care planning assistant: add pets, schedule care tasks, and see today's plan.")

# --- Application "memory": keep one Owner alive across reruns ---
if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan")

owner = st.session_state.owner
scheduler = Scheduler(owner)

# --- Owner ---
st.subheader("Owner")
owner.name = st.text_input("Owner name", value=owner.name)

st.divider()

# --- Add a pet ---
st.subheader("Add a Pet")
with st.form("add_pet_form", clear_on_submit=True):
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    if st.form_submit_button("Add pet"):
        if not pet_name.strip():
            st.error("Please enter a pet name.")
        elif owner.get_pet(pet_name):
            st.error(f"{pet_name} is already added.")
        else:
            owner.add_pet(Pet(pet_name.strip(), species))
            st.success(f"Added {pet_name}!")

if owner.pets:
    st.write("Your pets: " + ", ".join(f"{p.name} ({p.species})" for p in owner.pets))
else:
    st.info("No pets yet. Add one above.")

st.divider()

# --- Schedule a task ---
st.subheader("Schedule a Task")
if owner.pets:
    with st.form("add_task_form", clear_on_submit=True):
        pet_choice = st.selectbox("Pet", [p.name for p in owner.pets])
        task_title = st.text_input("Task", value="Morning walk")
        col1, col2 = st.columns(2)
        with col1:
            task_time = st.time_input("Time", value=None)
            duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        with col2:
            priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
            frequency = st.selectbox("Repeats", ["once", "daily", "weekly"])
        if st.form_submit_button("Add task"):
            if task_time is None or not task_title.strip():
                st.error("Please enter a task name and a time.")
            else:
                pet = owner.get_pet(pet_choice)
                pet.add_task(
                    Task(
                        description=task_title.strip(),
                        time=task_time.strftime("%H:%M"),
                        duration_minutes=int(duration),
                        priority=priority,
                        frequency=frequency,
                    )
                )
                st.success(f"Scheduled '{task_title}' for {pet_choice} at {task_time:%H:%M}.")
else:
    st.caption("Add a pet first to schedule tasks.")

st.divider()

# --- Today's schedule ---
st.subheader(f"Today's Schedule ({date.today():%A, %b %d})")

# Show the message saved by "Complete task" before the rerun
if "message" in st.session_state:
    st.success(st.session_state.pop("message"))

# Conflict warnings come first so the owner sees them right away
for warning in scheduler.detect_conflicts():
    st.warning(f"⚠️ {warning}. Consider moving one of these tasks.")

pet_filter = st.selectbox("Show tasks for", ["All pets"] + [p.name for p in owner.pets])
hide_done = st.checkbox("Hide completed tasks")

todays = scheduler.get_todays_schedule()
if pet_filter != "All pets":
    todays = [(p, t) for p, t in todays if p.name == pet_filter]
if hide_done:
    todays = [(p, t) for p, t in todays if not t.completed]

if todays:
    st.table(
        [
            {
                "Time": t.time,
                "Pet": p.name,
                "Task": t.description,
                "Minutes": t.duration_minutes,
                "Priority": t.priority,
                "Repeats": t.frequency,
                "Status": "✅ done" if t.completed else "⏳ to do",
            }
            for p, t in todays
        ]
    )

    # Mark a task complete (recurring tasks schedule their next occurrence)
    open_tasks = [(p, t) for p, t in todays if not t.completed]
    if open_tasks:
        labels = [f"{t.time} - {p.name}: {t.description}" for p, t in open_tasks]
        choice = st.selectbox("Mark a task complete", labels)
        if st.button("Complete task"):
            pet, task = open_tasks[labels.index(choice)]
            new_task = scheduler.mark_task_complete(pet, task)
            if new_task:
                st.session_state.message = f"Done! Next '{task.description}' scheduled for {new_task.due_date:%a %b %d}."
            else:
                st.session_state.message = f"Done! '{task.description}' completed."
            st.rerun()  # refresh so the table shows the new status
    else:
        st.success("All of today's tasks are complete! 🎉")
else:
    st.info("No tasks scheduled for today.")
