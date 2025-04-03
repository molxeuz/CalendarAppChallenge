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
class Evento:
    """Clase que representa un evento en el calendario."""
    titulo: str
    descripcion: str
    fecha: date
    inicio: time
    fin: time
    id: str = field(default_factory=generar_id_unico)
    recordatorios: list[Recordatorio] = field(default_factory=list)

    def agregar_recordatorio(self, fecha_hora: datetime, tipo: str = Recordatorio.EMAIL):
        self.recordatorios.append(Recordatorio(fecha_hora, tipo))

    def eliminar_recordatorio(self, indice: int):
        if 0 <= indice < len(self.recordatorios):
            self.recordatorios.pop(indice)
        else:
            error_recordatorio_no_encontrado()

    def __str__(self):
        return f"ID: {self.id}\nTítulo: {self.titulo}\nDescripción: {self.descripcion}\nHora: {self.inicio} - {self.fin}"

# TODO: Implement Day class here


# TODO: Implement Calendar class here
