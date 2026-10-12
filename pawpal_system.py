"""PawPal+ logic layer: Task, Pet, Owner, and Scheduler classes."""

from dataclasses import dataclass, field


@dataclass
class Task:
    """A single pet care activity."""

    description: str
    time: str  # "HH:MM" (24-hour)
    duration_minutes: int = 15
    priority: str = "medium"  # "low", "medium", or "high"
    frequency: str = "once"  # "once", "daily", or "weekly"
    completed: bool = False

    def mark_complete(self):
        """Mark this task as done."""
        pass


@dataclass
class Pet:
    """A pet and its list of care tasks."""

    name: str
    species: str
    tasks: list = field(default_factory=list)

    def add_task(self, task):
        """Add a task to this pet."""
        pass


class Owner:
    """A pet owner who manages one or more pets."""

    def __init__(self, name):
        """Create an owner with no pets."""
        self.name = name
        self.pets = []

    def add_pet(self, pet):
        """Add a pet to this owner."""
        pass

    def get_all_tasks(self):
        """Return every task across all pets."""
        pass


class Scheduler:
    """The 'brain' that retrieves, organizes, and manages tasks across an owner's pets."""

    def __init__(self, owner):
        """Create a scheduler for the given owner."""
        self.owner = owner

    def sort_by_time(self, tasks):
        """Return tasks sorted by time."""
        pass

    def get_todays_schedule(self):
        """Return today's tasks sorted by time."""
        pass
