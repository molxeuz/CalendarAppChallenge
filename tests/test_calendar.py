from datetime import datetime, time, date, timedelta
import pytest
import inspect

import app.model.calendar

module_members = [item[0] for item in inspect.getmembers(app.model.calendar)]
reminder_defined = "Reminder" in module_members
event_defined = "Event" in module_members
calendar_defined = "Calendar" in module_members
day_defined = "Day" in module_members

if reminder_defined:
    from app.model.calendar import Reminder

if event_defined:
    from app.model.calendar import Event

if calendar_defined:
    from app.model.calendar import Calendar

if day_defined:
    from app.model.calendar import Day


base_date = datetime.now().date() + timedelta(days=5)


@pytest.fixture()
def reminder_with_email():
    date_time = datetime(base_date.year, base_date.month, base_date.day, 12, 0)
    return Reminder(date_time, Reminder.EMAIL)


@pytest.fixture()
def reminder_with_system():
    date_time = datetime(base_date.year, base_date.month, base_date.day, 12, 0)
    return Reminder(date_time, Reminder.SYSTEM)


class TestReminder:
    @pytest.mark.skipif(not reminder_defined, reason="Reminder class not defined")
    def test_reminder_class_decorated_with_dataclass(self, reminder_with_email):
        assert hasattr(reminder_with_email, "__dataclass_params__")

    @pytest.mark.skipif(not reminder_defined, reason="Reminder class not defined")
    @pytest.mark.parametrize(
        "constant_name, constant_value", [("EMAIL", "email"), ("SYSTEM", "system")]
    )
    def test_reminder_class_has_constants_with_value(self, reminder_with_email, constant_name, constant_value):
        assert hasattr(reminder_with_email, constant_name)
        assert getattr(reminder_with_email, constant_name) == constant_value

    @pytest.mark.skipif(not reminder_defined, reason="Reminder class not defined")
    @pytest.mark.parametrize(
        "attribute_name, attribute_type",
        [("date_time", datetime), ("type", str)]
    )
    def test_reminder_class_has_attributes(self, reminder_with_email, attribute_name, attribute_type):
        assert hasattr(reminder_with_email, attribute_name)
        assert isinstance(getattr(reminder_with_email, attribute_name), attribute_type)

    @pytest.mark.skipif(not reminder_defined, reason="Reminder class not defined")
    def test_reminder_class_has_str_method(self, reminder_with_email):
        assert hasattr(reminder_with_email, "__str__")
        assert callable(getattr(reminder_with_email, "__str__"))
        assert isinstance(reminder_with_email.__str__(), str)

    @pytest.mark.skipif(not reminder_defined, reason="Reminder class not defined")
    def test_reminder_str_method_output(self, reminder_with_email):
        assert str(reminder_with_email) == f"Reminder on {base_date.year}-{base_date.month:02d}-{base_date.day:02d} 12:00:00 of type email"


@pytest.fixture()
def event_without_reminders():
    return Event("Event title",
                 "Event description",
                 base_date,
                 time(10, 0),
                 time(11, 0))


@pytest.fixture()
def event_with_reminders():
    event = Event("Event title",
                  "Event description",
                  base_date,
                  time(10, 0),
                  time(11, 0))
    event.add_reminder(datetime(base_date.year, base_date.month, base_date.day, 9, 0), Reminder.EMAIL)
    event.add_reminder(datetime(base_date.year, base_date.month, base_date.day, 8, 0), Reminder.SYSTEM)
    return event


class TestEvent:

    @pytest.mark.skipif(not event_defined, reason="Event class not defined")
    def test_event_class_decorated_with_dataclass(self, event_without_reminders):
        assert hasattr(event_without_reminders, "__dataclass_params__")

    @pytest.mark.skipif(not event_defined, reason="Event class not defined")
    @pytest.mark.parametrize(
        "attribute_name, attribute_type",
        [("title", str), ("description", str), ("date_", date),
         ("start_at", time), ("end_at", time), ("id", str), ("reminders", list)]
    )
    def test_event_class_has_attributes(self, event_without_reminders, attribute_name, attribute_type):
        assert hasattr(event_without_reminders, attribute_name)
        assert isinstance(getattr(event_without_reminders, attribute_name), attribute_type)

    @pytest.mark.skipif(not event_defined, reason="Event class not defined")
    @pytest.mark.parametrize(
        "attribute_name, expected_value",
        [("title", "Event title"), ("description", "Event description"),
         ("date_", base_date),
         ("start_at", time(10, 0)),
         ("end_at", time(11, 0)),
         ("id", None),
         ("reminders", [])]
    )
    def test_event_class_initializes_attributes(self, event_without_reminders, attribute_name, expected_value):
        if expected_value is not None:
            assert getattr(event_without_reminders, attribute_name) == expected_value
        else:
            assert getattr(event_without_reminders, attribute_name)

    @pytest.mark.skipif(not event_defined, reason="Event class not defined")
    @pytest.mark.parametrize(
        "method_name, expected_return_type, args",
        [("add_reminder", None, (datetime(base_date.year, base_date.month, base_date.day, 9, 0), "email")),
         ("delete_reminder", None, (0,)),
         ("__str__", str, ())]
    )
    def test_event_class_has_methods(self, event_without_reminders, method_name, expected_return_type, args):
        assert hasattr(event_without_reminders, method_name)
        method = getattr(event_without_reminders, method_name)
        assert callable(method)
        if expected_return_type:
            assert isinstance(method(*args), expected_return_type)

    @pytest.mark.skipif(not reminder_defined, reason="Reminder class not defined")
    def test_add_reminder_method_functionality(self, event_without_reminders):
        event_without_reminders.add_reminder(datetime(base_date.year, base_date.month, base_date.day, 9, 0), Reminder.EMAIL)
        assert len(event_without_reminders.reminders) == 1
        assert event_without_reminders.reminders[0].type == Reminder.EMAIL
        assert event_without_reminders.reminders[0].date_time == datetime(base_date.year, base_date.month, base_date.day, 9, 0)

    @pytest.mark.skipif(not reminder_defined, reason="Reminder class not defined")
    def test_delete_reminder_method_functionality(self, event_with_reminders):
        event_with_reminders.delete_reminder(0)
        assert len(event_with_reminders.reminders) == 1
        assert event_with_reminders.reminders[0].type == Reminder.SYSTEM
        assert event_with_reminders.reminders[0].date_time == datetime(base_date.year, base_date.month, base_date.day, 8, 0)

    @pytest.mark.skipif(not reminder_defined, reason="Reminder class not defined")
    def test_delete_reminder_method_calls_reminder_not_found_error(self, event_without_reminders):
        with pytest.raises(ValueError):
            event_without_reminders.delete_reminder(0)

    @pytest.mark.skipif(not event_defined, reason="Event class not defined")
    def test_event_class_str_method_output(self, event_without_reminders):
        event_str = str(event_without_reminders)
        assert f"ID: {event_without_reminders.id}" in event_str
        assert f"Event title: {event_without_reminders.title}" in event_str
        assert f"Description: {event_without_reminders.description}" in event_str
        assert f"Time: {event_without_reminders.start_at} - {event_without_reminders.end_at}" in event_str


@pytest.fixture()
def day():
    return Day(base_date)


@pytest.fixture()
def day_with_event():
    day = Day(base_date)
    day.add_event("event_id", time(10, 0), time(11, 0))
    return day


class TestDay:

    @pytest.mark.skipif(not day_defined, reason="Day class not defined")
    def test_day_class_is_not_marked_as_dataclass(self):
        assert not hasattr(Day, "__dataclass_params__")

    @pytest.mark.skipif(not day_defined, reason="Day class not defined")
    @pytest.mark.parametrize(
        "attribute_name, attribute_type",
        [("date_", date), ("slots", dict)]
    )
    def test_day_class_has_attributes(self, day, attribute_name, attribute_type):
        assert hasattr(day, attribute_name)
        assert isinstance(getattr(day, attribute_name), attribute_type)

    @pytest.mark.skipif(not day_defined, reason="Day class not defined")
    @pytest.mark.parametrize(
        "method_name, expected_return_type, args",
        [("__init__", None, (base_date)),
         ("_init_slots", None, ()),
         ("add_event", None, ("event_id", time(10, 0), time(11, 0))),
         ("delete_event", None, ("event_id",)),
         ("update_event", None, ("event_id", time(10, 0), time(11, 0)))]
    )
    def test_day_class_has_methods(self, day, method_name, expected_return_type, args):
        assert hasattr(day, method_name)
        method = getattr(day, method_name)
        assert callable(method)
        if expected_return_type:
            assert isinstance(method(*args), expected_return_type)

    @pytest.mark.skipif(not day_defined, reason="Day class not defined")
    @pytest.mark.parametrize(
        "attribute_name, expected_value",
        [("date_", base_date),
         ("slots", {time(hour, minute): None for hour in range(24) for minute in range(0, 60, 15)})
         ]
    )
    def test_day_class_initializes_attributes(self, day, attribute_name, expected_value):
        assert getattr(day, attribute_name) == expected_value

    @pytest.mark.skipif(not day_defined, reason="Day class not defined")
    def test_add_event_method_functionality(self, day):
        day.add_event("event_id", time(10, 0), time(11, 0))
        assert day.slots[time(10, 0)] == "event_id"
        assert day.slots[time(10, 15)] == "event_id"
        assert day.slots[time(10, 30)] == "event_id"
        assert day.slots[time(10, 45)] == "event_id"
        assert day.slots[time(11, 0)] is None

    @pytest.mark.skipif(not day_defined, reason="Day class not defined")
    def test_add_event_calls_slot_not_available_error(self, day_with_event):
        with pytest.raises(ValueError):
            day_with_event.add_event("event_id", time(10, 0), time(11, 0))


@pytest.fixture()
def empty_calendar():
    return Calendar()


@pytest.fixture()
def calendar_with_events():
    calendar = Calendar()
    event = Event("Event 1",
                  "Event 1 description",
                  base_date,
                  time(10, 0),
                  time(11, 0),
                  id="event_id")
    calendar.events["event_id"] = event

    calendar.add_event("Event 2",
                       "Event 2 description",
                       base_date,
                       time(12, 0),
                       time(13, 0))
    calendar.add_event("Event 3",
                       "Event 3 description",
                       base_date,
                       time(14, 0),
                       time(15, 0))
    return calendar


@pytest.fixture()
def calendar_with_some_slots_available():
    calendar = Calendar()
    calendar.add_event("Event 1",
                       "Event 1 description",
                       base_date,
                       time(0, 0),
                       time(12, 0))

    calendar.add_event("Event 2",
                       "Event 2 description",
                       base_date,
                       time(13, 0),
                       time(23, 59))

    return calendar


class TestCalendar:
    @pytest.mark.skipif(not calendar_defined, reason="Calendar class not defined")
    def test_calendar_class_is_not_marked_as_dataclass(self, empty_calendar):
        assert not hasattr(empty_calendar, "__dataclass_params__")

    @pytest.mark.skipif(not calendar_defined, reason="Calendar class not defined")
    @pytest.mark.parametrize(
        "attribute_name, attribute_type",
        [("days", dict), ("events", dict)]
    )
    def test_calendar_class_has_attributes(self, empty_calendar, attribute_name, attribute_type):
        assert hasattr(empty_calendar, attribute_name)
        assert isinstance(getattr(empty_calendar, attribute_name), attribute_type)

    @pytest.mark.skipif(not calendar_defined, reason="Calendar class not defined")
    @pytest.mark.parametrize(
        "method_name, expected_return_type, args",
        [("add_event", str, ("Event 1", "Event 1 description", base_date, time(10, 0), time(11, 0))),
         ("update_event", None, ("event_id", "Event 1", "Event 1 description", base_date, time(10, 0), time(11, 0))),
         ("delete_event", None, ("event_id",)),
         ("find_events", dict, (base_date, base_date + timedelta(days=1))),
         ("add_reminder", None, ("event_id", datetime(base_date.year, base_date.month, base_date.day, 9, 0), "email")),
         ("delete_reminder", None, ("event_id", 0)),
         ("list_reminders", list, ("event_id",)),
         ("find_available_slots", list, (base_date,)),
         ("__init__", None, ())]
    )
    def test_calendar_class_has_methods(self, calendar_with_events, method_name, expected_return_type, args):
        assert hasattr(calendar_with_events, method_name)
        method = getattr(calendar_with_events, method_name)
        assert callable(method)
        if expected_return_type:
            assert isinstance(method(*args), expected_return_type)

    @pytest.mark.skipif(not calendar_defined, reason="Calendar class not defined")
    @pytest.mark.parametrize(
        "attribute_name, expected_value",
        [("days", {}),
         ("events", {})]
    )
    def test_calendar_class_initializes_attributes(self, empty_calendar, attribute_name, expected_value):
        assert getattr(empty_calendar, attribute_name) == expected_value

    @pytest.mark.skipif(not calendar_defined, reason="Calendar class not defined")
    def test_add_event_method_adds_the_event_to_the_event_dict(self, empty_calendar):
        event_id = empty_calendar.add_event("Event 1", "Event 1 description", base_date, time(10, 0), time(11, 0))
        assert len(empty_calendar.events) == 1
        assert event_id in empty_calendar.events
        assert empty_calendar.events[event_id].title == "Event 1"
        assert empty_calendar.events[event_id].description == "Event 1 description"
        assert empty_calendar.events[event_id].date_ == base_date
        assert empty_calendar.events[event_id].start_at == time(10, 0)
        assert empty_calendar.events[event_id].end_at == time(11, 0)

    @pytest.mark.skipif(not calendar_defined, reason="Calendar class not defined")
    def test_add_event_method_returns_event_id(self, empty_calendar):
        event_id = empty_calendar.add_event("Event 1", "Event 1 description", base_date, time(10, 0), time(11, 0)
        )
        assert event_id

    @pytest.mark.skipif(not calendar_defined, reason="Calendar class not defined")
    def test_add_event_method_calls_date_lower_than_today_error(self, empty_calendar):
        with pytest.raises(ValueError):
            empty_calendar.add_event("Event 1", "Event 1 description", date(2020, 5, 1), time(10, 0), time(11, 0))

    @pytest.mark.skipif(not calendar_defined, reason="Calendar class not defined")
    def test_add_event_method_creates_day_object_in_days_dict(self, empty_calendar):
        empty_calendar.add_event("Event 1", "Event 1 description", base_date, time(10, 0), time(11, 0))
        assert base_date in empty_calendar.days

    @pytest.mark.skipif(not calendar_defined, reason="Calendar class not defined")
    def test_add_event_method_calls_add_event_on_day_object(self, empty_calendar):
        event_id = empty_calendar.add_event("Event 1", "Event 1 description", base_date, time(10, 0), time(11, 0))
        assert event_id in empty_calendar.days[base_date].slots.values()

    @pytest.mark.skipif(not calendar_defined, reason="Calendar class not defined")
    def test_add_reminder_method_functionality(self, calendar_with_events):
        calendar_with_events.add_reminder("event_id", datetime(base_date.year, base_date.month, base_date.day, 9, 0), Reminder.EMAIL)
        assert len(calendar_with_events.events["event_id"].reminders) == 1
        assert calendar_with_events.events["event_id"].reminders[0].type == Reminder.EMAIL
        assert calendar_with_events.events["event_id"].reminders[0].date_time == datetime(base_date.year, base_date.month, base_date.day, 9, 0)

    @pytest.mark.skipif(not calendar_defined, reason="Calendar class not defined")
    def test_add_reminder_method_calls_event_not_found_error(self, calendar_with_events):
        with pytest.raises(ValueError):
            calendar_with_events.add_reminder("event_id_not_found", datetime(base_date.year, base_date.month, base_date.day, 9, 0), Reminder.EMAIL)

    @pytest.mark.skipif(not calendar_defined, reason="Calendar class not defined")
    def test_find_available_slots_method_functionality(self, calendar_with_some_slots_available):
        available_slots = calendar_with_some_slots_available.find_available_slots(base_date)
        assert len(available_slots) == 4
        assert available_slots[0] == time(12, 0)
        assert available_slots[1] == time(12, 15)
        assert available_slots[2] == time(12, 30)
        assert available_slots[3] == time(12, 45)
