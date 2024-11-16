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
            class_id=self.class_id,
            classroom_id=self.classroom_id,
            teacher_id=self.teacher_id,
            day=self.day,
            slot=self.slot,
        )
