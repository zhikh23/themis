from typing import Callable, Iterable, Any


def count(iterable: Iterable, predicate: Callable[[Any], bool]) -> int:
    """Возвращает число элементов item, для которых predicate(item) == True."""
    cnt = 0
    for item in iterable:
        if predicate(item):
            cnt += 1
    return cnt
