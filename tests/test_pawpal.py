"""Tests for the PawPal+ logic layer."""

from datetime import date, timedelta

from pawpal_system import Owner, Pet, Task, Scheduler


def make_scheduler():
    """Build an owner with two pets and return (scheduler, dog, cat)."""
    owner = Owner("Jordan")
    dog = Pet("Mochi", "dog")
    cat = Pet("Luna", "cat")
    owner.add_pet(dog)
    owner.add_pet(cat)
    return Scheduler(owner), dog, cat


def test_mark_complete_changes_status():
    task = Task("Walk", "07:00")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_adding_task_increases_pet_task_count():
    pet = Pet("Mochi", "dog")
    assert len(pet.tasks) == 0
    pet.add_task(Task("Walk", "07:00"))
    assert len(pet.tasks) == 1


def test_sort_by_time_returns_chronological_order():
    scheduler, dog, cat = make_scheduler()
    dog.add_task(Task("Evening walk", "18:00"))
    cat.add_task(Task("Feeding", "08:00"))
    dog.add_task(Task("Morning walk", "07:30"))
    times = [task.time for _, task in scheduler.get_todays_schedule()]
    assert times == ["07:30", "08:00", "18:00"]


def test_filter_by_pet_name():
    scheduler, dog, cat = make_scheduler()
    dog.add_task(Task("Walk", "07:00"))
    cat.add_task(Task("Feeding", "08:00"))
    result = scheduler.filter_tasks(pet_name="Luna")
    assert len(result) == 1
    assert result[0][1].description == "Feeding"


def test_filter_by_completion_status():
    scheduler, dog, _ = make_scheduler()
    done = Task("Walk", "07:00")
    done.mark_complete()
    dog.add_task(done)
    dog.add_task(Task("Feeding", "08:00"))
    result = scheduler.filter_tasks(completed=False)
    assert [task.description for _, task in result] == ["Feeding"]


def test_completing_daily_task_creates_next_day_task():
    scheduler, dog, _ = make_scheduler()
    today = date.today()
    walk = Task("Walk", "07:00", frequency="daily", due_date=today)
    dog.add_task(walk)
    new_task = scheduler.mark_task_complete(dog, walk)
    assert walk.completed is True
    assert new_task.due_date == today + timedelta(days=1)
    assert new_task.completed is False
    assert len(dog.tasks) == 2


def test_completing_weekly_task_creates_task_one_week_later():
    scheduler, dog, _ = make_scheduler()
    today = date.today()
    bath = Task("Bath", "10:00", frequency="weekly", due_date=today)
    dog.add_task(bath)
    new_task = scheduler.mark_task_complete(dog, bath)
    assert new_task.due_date == today + timedelta(weeks=1)


def test_completing_one_time_task_creates_nothing():
    scheduler, dog, _ = make_scheduler()
    vet = Task("Vet visit", "15:00", frequency="once")
    dog.add_task(vet)
    assert scheduler.mark_task_complete(dog, vet) is None
    assert len(dog.tasks) == 1


def test_detect_conflicts_flags_same_time():
    scheduler, dog, cat = make_scheduler()
    dog.add_task(Task("Pill", "08:00"))
    cat.add_task(Task("Feeding", "08:00"))
    warnings = scheduler.detect_conflicts()
    assert len(warnings) == 1
    assert "08:00" in warnings[0]


def test_no_conflicts_when_times_differ():
    scheduler, dog, cat = make_scheduler()
    dog.add_task(Task("Walk", "07:00"))
    cat.add_task(Task("Feeding", "08:00"))
    assert scheduler.detect_conflicts() == []


def test_pet_with_no_tasks_gives_empty_schedule():
    scheduler, _, _ = make_scheduler()
    assert scheduler.get_todays_schedule() == []
