from GA import GA
from models.Database import Database


def main():
    db = Database("./data")

    ga = GA(db)
    populations = ga()

    db.print_classrooms()
    db.print_teachers()
    db.print_groups()
    populations[0].print()
    print("\n")
    populations[0].calculate_fitness(print_conflicts=True)


if __name__ == "__main__":
    main()
