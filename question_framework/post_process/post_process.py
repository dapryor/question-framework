from ipaddress import ip_address
from typing import Callable, List, Optional, Any
from functools import partial
import re


def ip_range_to_list(x):
    def ip_range_generator(ip1, ip2):
        ip1 = int(ip_address(ip1))
        ip2 = int(ip_address(ip2))
        ip1, ip2 = min(ip1, ip2), max(ip1, ip2)
        for i in range(ip1, ip2 + 1):
            yield ip_address(i)

    ip1, ip2 = x.replace(" ", "").split("-")

    return ip_range_generator(ip1, ip2)


def as_list(ans: str, sep: str = ',', f: Optional[Callable[[str], Any]] = None) -> List[Any]:
    """
    Parse list elements and optionally apply a transformer to each element.
    This allows you to parse things directly as the type they should be, e.g. integers:
    as_list("3, 4", f=int) == [3, 4]
    """
    items = ans.strip().split(sep)
    items = map(str.strip, items)
    if f is not None:
        items = map(f, items)
    return list(items)


def as_list_of(f: Callable) -> Callable[[str], List[Any]]:
    """
    A helper function to build as_list alternatives on the spot.
    as_ints = as_list_of(int)
    as_ints("3, 4") == [3, 4]
    """
    return partial(as_list, f=f)


as_ints = as_list_of(int)
as_floats = as_list_of(float)


def mapped_to(*fs: Callable) -> Callable[[str], List[Any]]:
    """
    Apply a given function to the item found at a given index.
    as_mapping(int, float)("3, 3.5") == [3, 3.5]
    Both lists need to have the same length.
    """
    def mapper(ans: str, **kw):
        items = as_list(ans)
        if len(items) != len(fs):
            raise ValueError('Key & Input lists have mismatched lengths')
        items = (f(i) for i, f in zip(items, fs))
        return list(items)
    return mapper


def as_int_range(ans: str) -> range:
    """
    Compute an integer range from a string representation. Several options:
    dash notation: 3 - 5 (only positive values)
    python slice notation: :3 (start implied to be 0), 3:4 (normal), 3:55:2 (with step)
    natural language: 'from 3 to 5' or '-55 to 55'
    """
    ans = ans.strip()
    if re.match(r'^\s*\d+\s*-\s*\d+$', ans):
        start, end = ans.split('-')
        start = start.strip()
        end = end.strip()
        return range(int(start), int(end))
    if re.match(r'^(-?\d+)?:-?\d+(:-?\d+)?$', ans):
        start, end, *step = ans.split(':')
        start = int(start or 0)
        step = int(step and step[0] or 1)
        return range(start, int(end), step)
    if re.match(r'^(from\s)?\s*-?\d+\s+to\s+-?\d+$', ans, flags=re.IGNORECASE):
        *_, start, _, end = ans.split()
        start = int(start)
        end = int(end)
        step = 1 if end >= start else -1
        return range(start, end, step)
    raise ValueError(f'Could not transform {ans!r} into an integer range')
