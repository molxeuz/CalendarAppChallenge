from dataclasses import dataclass, field
from datetime import datetime, date, time
from typing import ClassVar

from app.services.util import generate_unique_id, date_lower_than_today_error, event_not_found_error, \
    reminder_not_found_error, slot_not_available_error


# TODO: Implement Reminder class here
@dataclass
class Reminder:
    """Clase que representa un recordatorio para un evento."""
    EMAIL = "email"
    SYSTEM = "system"

    date_time: datetime
    type: str = EMAIL

    def __str__(self):
        return f"Reminder on {self.date_time} of type {self.type}"

# TODO: Implement Event class here
@dataclass
class Event:
    """Clase que representa un evento en el calendario."""
    title: str
    description: str
    date_: date
    start_at: time
    end_at: time
    id: str = field(default_factory=generate_unique_id)
    reminders: list[Reminder] = field(default_factory=list)

    def add_reminder(self, date_time: datetime, type_: str = Reminder.EMAIL):
        self.reminders.append(Reminder(date_time, type_))

    def delete_reminder(self, reminder_index: int):
        if 0 <= reminder_index < len(self.reminders):
            self.reminders.pop(reminder_index)
        else:
            reminder_not_found_error()

    def __str__(self):
        return f"ID: {self.id}\nEvent title: {self.title}\nDescription: {self.description}\nTime: {self.start_at} - {self.end_at}"

# TODO: Implement Day class here


# TODO: Implement Calendar class here
