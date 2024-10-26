counter = {}


def increment_count(id: int):
    counter[id] = counter.get(id, 0) + 1


def get_count(id: int) -> int:
    return counter.get(id, 0)
