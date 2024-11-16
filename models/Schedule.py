from math import floor
import random

from utils import random_item

from .Database import Database
from .Class import Class
from .ScheduleLesson import ScheduleLesson


class Schedule:
    lessons: list[ScheduleLesson]

    def __init__(self, db: Database):
        self.lessons = []
        self.db = db
        for cl in db.classes.values():
            for _ in range(floor(cl.hours_per_week / 2)):
                classroom = random_item(db.classrooms).id
                teacher = self.__select_random_teacher(cl)
                day = random.randint(1, 5)
                slot = random.randint(1, 4)
                self.lessons.append(
                    ScheduleLesson(cl.id, int(classroom), teacher, day, slot)
                )
        self.max_conflicts = 3 * len(self.lessons) * (len(self.lessons) - 1) / 2
        self.max_weak_violations = 2 * len(self.lessons)
        self.max_windows = (len(self.db.teachers) + len(self.db.groups)) * 2 * 5

    def get_timetable(self):
        timetable: list[list[list[ScheduleLesson]]] = [
            [[] for _ in range(4)] for _ in range(5)
        ]
        for lesson in self.lessons:
            timetable[lesson.day - 1][lesson.slot - 1].append(lesson)
        return timetable

    def calculate_fitness(self):
        number_of_conflicts = 0
        weak_violations = 0
        for i in range(len(self.lessons)):
            lesson1 = self.lessons[i]
            if self.__check_capacity_violation(lesson1):
                weak_violations += 1
            if self.__check_wrong_teacher_violation(lesson1):
                weak_violations += 1
            for j in range(i + 1, len(self.lessons)):
                lesson2 = self.lessons[j]
                if lesson1.day == lesson2.day and lesson1.slot == lesson2.slot:
                    if lesson1.classroom_id == lesson2.classroom_id:
                        number_of_conflicts += 1
                    if lesson1.teacher_id == lesson2.teacher_id:
                        number_of_conflicts += 1
                    if lesson1.class_id == lesson2.class_id:
                        number_of_conflicts += 1

        w1 = self.__calculate_student_windows()
        w2 = self.__calculate_teacher_windows()
        windows = w1 + w2

        conflicts_score = number_of_conflicts / self.max_conflicts
        weak_violations_score = weak_violations / self.max_weak_violations
        windows_score = windows / self.max_windows

        if number_of_conflicts:
            self.fitness = -(
                0.7 * conflicts_score
                + 0.2 * weak_violations_score
                + 0.1 * windows_score
            )
        else:
            self.fitness = 1 - (0.666 * weak_violations_score + 0.333 * windows_score)

        return self.fitness

    def __check_capacity_violation(self, lesson: ScheduleLesson):
        return (
            self.db.classrooms[lesson.classroom_id].capacity
            < self.db.get_group_by_class_id(lesson.class_id).student_count
        )

    def __check_wrong_teacher_violation(self, lesson: ScheduleLesson):
        teacher = self.db.teachers.get(lesson.teacher_id)
        if not teacher:
            return True

        return not any(
            s.type == self.db.classes[lesson.class_id].type
            and s.subject_id == self.db.get_subject_by_class_id(lesson.class_id).id
            for s in self.db.teachers.get(lesson.teacher_id).subjects
        )

    def __calculate_student_windows(self):
        result = 0
        timetable = self.get_timetable()
        for g in self.db.groups.values():
            for day in timetable:
                prev_lesson = -1
                for i, slot in enumerate(day):
                    for lesson in slot:
                        if self.db.get_group_by_class_id(lesson.class_id).id == g.id:
                            if prev_lesson != -1 and i - prev_lesson > 1:
                                result += i - prev_lesson
                            prev_lesson = i
        return result

    def __calculate_teacher_windows(self):
        result = 0
        timetable = self.get_timetable()
        for t in self.db.teachers.values():
            for day in timetable:
                prev_lesson = -1
                for i, slot in enumerate(day):
                    for lesson in slot:
                        if lesson.teacher_id == t.id:
                            if prev_lesson != -1 and i - prev_lesson > 1:
                                result += i - prev_lesson
                            prev_lesson = i
        return result

    def __select_random_teacher(self, cl: Class):
        teachers = self.db.subjects[cl.subject.id].teachers
        filtered_teachers = [t for t in teachers if t.type == cl.type]
        return (
            random.choice(filtered_teachers).id
            if filtered_teachers
            else random.choice(teachers).id
            if teachers
            else random_item(self.db.teachers).id
        )
