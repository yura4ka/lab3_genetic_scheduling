from .TeacherSubject import TeacherSubject


class Subject:
    teachers: list[TeacherSubject]

    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
        self.teachers = []
