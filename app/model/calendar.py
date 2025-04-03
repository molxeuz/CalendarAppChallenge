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
class Day:
    """Clase que representa un día en el calendario con espacios de tiempo."""
    def __init__(self, date_: date):
        self.date_ = date_
        self.slots = {}
        self._init_slots()

    def _init_slots(self):
        """Inicializa los slots de tiempo con intervalos de 15 minutos."""
        current_time = time(0, 0)
        while current_time < time(23, 45):
            self.slots[current_time] = None
            next_time = (datetime.combine(date.today(), current_time) + timedelta(minutes=15)).time()
            current_time = next_time

    def add_event(self, event_id: str, start_at: time, end_at: time):
        """Añade un evento a los espacios de tiempo disponibles."""
        slots_to_fill = [slot for slot in self.slots if start_at <= slot < end_at]

        if any(self.slots[slot] is not None for slot in slots_to_fill):
            slot_not_available_error()
            return

        for slot in slots_to_fill:
            self.slots[slot] = event_id

    def delete_event(self, event_id: str):
        """Elimina un evento de los espacios de tiempo."""
        deleted = False
        for slot, saved_id in self.slots.items():
            if saved_id == event_id:
                self.slots[slot] = None
                deleted = True
        if not deleted:
            event_not_found_error()

    def update_event(self, event_id: str, start_at: time, end_at: time):
        """Actualiza un evento cambiando su horario."""
        self.delete_event(event_id)
        self.add_event(event_id, start_at, end_at)

# TODO: Implement Calendar class here
