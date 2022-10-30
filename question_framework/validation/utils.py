def all_validation(*fn):
    def chained_fn(x: str):
        res = (f(x) for f in fn)
        return all(res)

    return chained_fn


def any_validation(*fn):
    def chained_fn(x: str):
        res = (f(x) for f in fn)
        return any(res)

    return chained_fn
