counter = {}


def increment_count(id: int):
    if id in counter:
        counter[id] += 1
    else:
        counter[id] = 1


def get_count(id: int) -> int:
    return counter[id]
