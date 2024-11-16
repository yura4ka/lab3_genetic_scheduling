import pandas as pd
from pathlib import Path

from .Group import Group
from .Classroom import Classroom
from .Teacher import Teacher
from .Subject import Subject
from .TeacherSubject import TeacherSubject
from .Class import Class


class Database:
    def __init__(self, path: str):
        root = Path(path)
        self.__populate_groups(root)
        self.__populate_classrooms(root)
        self.__populate_teachers(root)
        self.__populate_subjects(root)
        self.__populate_teacher_subjects(root)
        self.__populate_classes(root)

    def get_group_by_class_id(self, class_id: int):
        return self.classes[class_id].group

    def get_subject_by_class_id(self, class_id: int):
        return self.classes[class_id].subject

    def __populate_groups(self, path: Path):
        groups = pd.read_csv(path / "groups.csv", encoding="utf-8")
        groups = [
            Group(id, name, student_count) for id, name, student_count in groups.values
        ]
        self.groups = {group.id: group for group in groups}

    def __populate_classrooms(self, path: Path):
        classrooms = pd.read_csv(path / "classrooms.csv", encoding="utf-8")
        classrooms = [
            Classroom(id, name, capacity) for id, name, capacity in classrooms.values
        ]
        self.classrooms = {classroom.id: classroom for classroom in classrooms}

    def __populate_teachers(self, path: Path):
        teachers = pd.read_csv(path / "teachers.csv", encoding="utf-8")
        teachers = [Teacher(id, name) for id, name in teachers.values]
        self.teachers = {teacher.id: teacher for teacher in teachers}

    def __populate_subjects(self, path: Path):
        subjects = pd.read_csv(path / "subjects.csv", encoding="utf-8")
        subjects = [Subject(id, name) for id, name in subjects.values]
        self.subjects = {subject.id: subject for subject in subjects}

    def __populate_teacher_subjects(self, path: Path):
        teacher_subjects = pd.read_csv(path / "teacher_subjects.csv", encoding="utf-8")
        teacher_subjects = [TeacherSubject(*v) for v in teacher_subjects.values]
        self.teacher_subjects = {ts.id: ts for ts in teacher_subjects}

        for ts in teacher_subjects:
            self.teachers[ts.teacher_id].subjects.append(ts)
            self.subjects[ts.subject_id].teachers.append(ts)

    def __populate_classes(self, path: Path):
        classes = pd.read_csv(path / "classes.csv", encoding="utf-8")
        classes = [
            Class(
                id,
                self.groups[group_id],
                self.subjects[subject_id],
                hours_per_week,
                type,
            )
            for id, group_id, subject_id, hours_per_week, type in classes.values
        ]
        self.classes = {c.id: c for c in classes}
