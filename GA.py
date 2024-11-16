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
        mutation_probability=0.1,
    ):
        self.db = db
        self.elite_size = elite_size
        self.tournament_size = tournament_size
        self.mutation_probability = mutation_probability

    def __call__(self, *, population_size=100, max_generations=500):
        population = [Schedule(self.db) for _ in range(population_size)]
        population.sort(key=lambda s: s.calculate_fitness(), reverse=True)
        i = 0

        while i < max_generations and population[0].fitness < 0.999:
            print(f"Generation {i}: best fitness: {population[0].fitness}")
            population = self.__crossover_population(population)
            population = self.__mutate_population(population)
            population.sort(key=lambda s: s.calculate_fitness(), reverse=True)
            i += 1

        return population[0 : self.elite_size]

    def __tournament_selection(
        self, population: list[Schedule], num_offspring
    ) -> list[Schedule]:
        result = []
        while len(result) < num_offspring:
            tournament = random.sample(population, self.tournament_size)
            tournament.sort(key=lambda s: s.fitness, reverse=True)
            result.append(tournament[0])
        return result

    def __crossover_population(self, population: list[Schedule]):
        crossover = []
        for i in range(self.elite_size):
            crossover.append(population[i])

        size = len(population) - self.elite_size
        selection = self.__tournament_selection(population, size)

        for i in range(0, size if size % 2 == 0 else size - 1, 2):
            parent1 = selection[i]
            parent2 = selection[i + 1]
            child1, child2 = self.__crossover(parent1, parent2)
            crossover.append(child1)
            crossover.append(child2)

        if size % 2 != 0:
            crossover.append(selection[-1])

        return crossover

    def __crossover(
        self, parent1: Schedule, parent2: Schedule
    ) -> tuple[Schedule, Schedule]:
        child1, child2 = Schedule(self.db), Schedule(self.db)

        for i in range(len(parent1.lessons)):
            if random.random() < 0.5:
                child1.lessons[i] = parent1.lessons[i].copy()
                child2.lessons[i] = parent2.lessons[i].copy()
            else:
                child1.lessons[i] = parent2.lessons[i].copy()
                child2.lessons[i] = parent1.lessons[i].copy()

        return child1, child2

    def __mutate_population(self, population: list[Schedule]):
        for i in range(self.elite_size, len(population)):
            population[i] = self.__mutate(population[i])
        return population

    def __mutate(self, schedule: Schedule):
        random_schedule = Schedule(self.db)
        for i in range(len(schedule.lessons)):
            if random.random() >= self.mutation_probability:
                random_schedule.lessons[i] = schedule.lessons[i].copy()

        return random_schedule
