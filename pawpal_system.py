"""PawPal+ logic layer: Task, Pet, Owner, and Scheduler classes."""

from dataclasses import dataclass, field
from datetime import date, timedelta


@dataclass
class Task:
    """A single pet care activity."""

    description: str
    time: str  # "HH:MM" (24-hour)
    duration_minutes: int = 15
    priority: str = "medium"  # "low", "medium", or "high"
    frequency: str = "once"  # "once", "daily", or "weekly"
    due_date: date = field(default_factory=date.today)
    completed: bool = False

    def mark_complete(self):
        """Mark this task as done."""
        self.completed = True

    def next_occurrence(self):
        """Return a new Task for the next daily/weekly occurrence, or None for one-time tasks."""
        if self.frequency == "daily":
            next_date = self.due_date + timedelta(days=1)
        elif self.frequency == "weekly":
            next_date = self.due_date + timedelta(weeks=1)
        else:
            return None
        return Task(
            description=self.description,
            time=self.time,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            frequency=self.frequency,
            due_date=next_date,
        )


@dataclass
class Pet:
    """A pet and its list of care tasks."""

    name: str
    species: str
    tasks: list = field(default_factory=list)

    def add_task(self, task):
        """Add a task to this pet."""
        self.tasks.append(task)

    def remove_task(self, task):
        """Remove a task from this pet."""
        self.tasks.remove(task)


class Owner:
    """A pet owner who manages one or more pets."""

    def __init__(self, name):
        """Create an owner with no pets."""
        self.name = name
        self.pets = []

    def add_pet(self, pet):
        """Add a pet to this owner."""
        self.pets.append(pet)

    def get_pet(self, name):
        """Return the pet with the given name, or None if not found."""
        for pet in self.pets:
            if pet.name.lower() == name.lower():
                return pet
        return None

    def get_all_tasks(self):
        """Return a list of (pet, task) pairs for every task across all pets."""
        pairs = []
        for pet in self.pets:
            for task in pet.tasks:
                pairs.append((pet, task))
        return pairs


class Scheduler:
    """The 'brain' that retrieves, organizes, and manages tasks across an owner's pets."""

    def __init__(self, owner):
        """Create a scheduler for the given owner."""
        self.owner = owner

    def sort_by_time(self, pairs):
        """Return (pet, task) pairs sorted by due date, then by "HH:MM" time."""
        return sorted(pairs, key=lambda pair: (pair[1].due_date, pair[1].time))

    def filter_tasks(self, pet_name=None, completed=None):
        """Return (pet, task) pairs matching a pet name and/or completion status."""
        result = []
        for pet, task in self.owner.get_all_tasks():
            if pet_name is not None and pet.name.lower() != pet_name.lower():
                continue
            if completed is not None and task.completed != completed:
                continue
            result.append((pet, task))
        return result

    def get_todays_schedule(self, day=None):
        """Return today's tasks (all pets), sorted by time."""
        if day is None:
            day = date.today()
        todays = [(pet, task) for pet, task in self.owner.get_all_tasks() if task.due_date == day]
        return self.sort_by_time(todays)

    def mark_task_complete(self, pet, task):
        """Complete a task; if it recurs, add the next occurrence to the pet and return it."""
        task.mark_complete()
        new_task = task.next_occurrence()
        if new_task is not None:
            pet.add_task(new_task)
        return new_task

    def detect_conflicts(self, day=None):
        """Return warning messages for incomplete tasks scheduled at the exact same date and time."""
        if day is None:
            day = date.today()
        seen = {}  # time -> list of "Pet: task" labels
        for pet, task in self.get_todays_schedule(day):
            if task.completed:
                continue
            seen.setdefault(task.time, []).append(f"{pet.name}: {task.description}")
        warnings = []
        for time, labels in seen.items():
            if len(labels) > 1:
                warnings.append(f"Conflict at {time}: " + ", ".join(labels))
        return warnings

    def format_schedule(self, pairs):
        """Return a readable multi-line string for a list of (pet, task) pairs."""
        if not pairs:
            return "  (no tasks)"
        lines = []
        for pet, task in pairs:
            status = "done" if task.completed else "todo"
            lines.append(
                f"  {task.due_date:%a %m/%d} {task.time}  {pet.name:<8} {task.description:<18} "
                f"{task.duration_minutes:>3} min  [{task.priority}] [{task.frequency}] [{status}]"
            )
        return "\n".join(lines)
