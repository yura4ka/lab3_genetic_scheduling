from .Group import Group
from .Subject import Subject


class Class:
    def __init__(
        self, id: int, group: Group, subject: Subject, hours_per_week: int, type: str
    ):
        self.id = id
        self.group = group
        self.subject = subject
        self.hours_per_week = hours_per_week
        self.type = type
