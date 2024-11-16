from dataclasses import dataclass


@dataclass
class ScheduleLesson:
    class_id: int
    classroom_id: int
    teacher_id: int
    day: int
    slot: int

    def copy(self):
        return ScheduleLesson(
            self.class_id, self.classroom_id, self.teacher_id, self.day, self.slot
        )
