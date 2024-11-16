import random
from models.Database import Database
from models.Schedule import Schedule


class GA:
    def __init__(
        self,
        db: Database,
        *,
        elite_size=5,
        tournament_size=3,
        mutation_probability=0.01,
    ):
        self.db = db
        self.elite_size = elite_size
        self.tournament_size = tournament_size
        self.mutation_probability = mutation_probability

    def __call__(self, *, population_size=100, max_generations=1000, threshold=0.999):
        population = [Schedule(self.db) for _ in range(population_size)]
        population.sort(key=lambda s: s.calculate_fitness(), reverse=True)
        i = 0

        while i < max_generations and population[0].fitness < threshold:
            print(
                f"Generation {i}: best fitness: {population[0].fitness}, conflicts: {population[0].number_of_conflicts}"
            )
            population = self.__crossover_population(population)
            population = self.__mutate_population(population)
            population.sort(key=lambda s: s.calculate_fitness(), reverse=True)
            i += 1

        print(
            f"RESULT -- Generation {i}: fitness: {population[0].fitness}, conflicts: {population[0].number_of_conflicts}"
        )
        return population[0 : self.elite_size]

    def __tournament_selection(self, population: list[Schedule]) -> list[Schedule]:
        return sorted(
            [random.choice(population) for _ in range(self.tournament_size)],
            key=lambda s: s.fitness,
            reverse=True,
        )

    def __crossover_population(self, population: list[Schedule]):
        crossover = []
        for i in range(self.elite_size):
            crossover.append(population[i])

        for i in range(self.elite_size, len(population)):
            parent1 = self.__tournament_selection(population)[0]
            parent2 = self.__tournament_selection(population)[0]
            crossover.append(self.__crossover(parent1, parent2))

        return crossover

    def __crossover(self, parent1: Schedule, parent2: Schedule) -> Schedule:
        child = Schedule(self.db)

        for i in range(len(child.lessons)):
            if random.random() < 0.5:
                child.lessons[i] = parent1.lessons[i].copy()
            else:
                child.lessons[i] = parent2.lessons[i].copy()

        return child

    def __mutate_population(self, population: list[Schedule]):
        for i in range(self.elite_size, len(population)):
            population[i] = self.__mutate(population[i])
        return population

    def __mutate(self, schedule: Schedule):
        random_schedule = Schedule(self.db)
        for i in range(len(schedule.lessons)):
            if random.random() <= self.mutation_probability:
                schedule.lessons[i] = random_schedule.lessons[i]

        return schedule
