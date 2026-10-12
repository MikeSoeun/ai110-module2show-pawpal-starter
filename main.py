"""CLI demo for PawPal+: builds an owner with pets and tasks, then prints the schedule."""

from pawpal_system import Owner, Pet, Task, Scheduler

# Set up an owner with two pets
owner = Owner("Jordan")
mochi = Pet("Mochi", "dog")
luna = Pet("Luna", "cat")
owner.add_pet(mochi)
owner.add_pet(luna)

# Tasks are added out of order on purpose to show sorting
mochi.add_task(Task("Evening walk", "18:00", 30, "high", "daily"))
mochi.add_task(Task("Morning walk", "07:30", 30, "high", "daily"))
luna.add_task(Task("Feeding", "08:00", 10, "high", "daily"))
luna.add_task(Task("Brush fur", "12:00", 15, "low", "weekly"))
mochi.add_task(Task("Heartworm pill", "08:00", 5, "medium", "once"))  # same time as Luna's feeding

scheduler = Scheduler(owner)

print("=" * 70)
print(f"Today's Schedule for {owner.name}")
print("=" * 70)
print(scheduler.format_schedule(scheduler.get_todays_schedule()))

print("\nConflict check:")
warnings = scheduler.detect_conflicts()
if warnings:
    for warning in warnings:
        print(f"  WARNING: {warning}")
else:
    print("  No conflicts.")

print("\nOnly Mochi's tasks:")
print(scheduler.format_schedule(scheduler.sort_by_time(scheduler.filter_tasks(pet_name="Mochi"))))

# Complete a daily task -> next day's copy is created automatically
morning_walk = mochi.tasks[1]
next_task = scheduler.mark_task_complete(mochi, morning_walk)
print(f"\nCompleted '{morning_walk.description}'. Next one scheduled for {next_task.due_date}.")

print("\nIncomplete tasks (all pets, all days):")
print(scheduler.format_schedule(scheduler.sort_by_time(scheduler.filter_tasks(completed=False))))
