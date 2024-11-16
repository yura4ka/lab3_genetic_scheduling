from pprint import pprint
from GA import GA
from models.Database import Database


def main():
    db = Database("./data")

    ga = GA(db)
    populations = ga()

    t = populations[0].get_timetable()
    for i, d in enumerate(t):
        print(f"\n===========Day {i}===========")
        for j, s in enumerate(d):
            print(f"\n==========Lesson {j} ({len(s)} lessons)==========")
            for lesson in s:
                pprint(lesson)


if __name__ == "__main__":
    main()
