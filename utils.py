import random


def random_item[T](items: dict[any, T]) -> T:
    return random.choice(list(items.values()))
