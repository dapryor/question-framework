from typing import Callable, List


def all_validation(*fn: Callable[[str], str]) -> Callable[[str], bool]:
    def chained_fn(x: str) -> bool:
        res = (f(x) for f in fn)
        return all(res)

    return chained_fn


def any_validation(*fn: Callable[[str], str]) -> Callable[[str], bool]:
    def chained_fn(x: str) -> bool:
        res = (f(x) for f in fn)
        return any(res)

    return chained_fn
