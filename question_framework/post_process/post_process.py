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


def as_list(ans: str, sep: str = ",") -> List[str]:
    """
    Spits answer into list according to separator
    """

    items = ans.strip().split(sep)
    items = map(str.strip, items)

    return list(items)


def as_list_of(f: Callable, sep: str = ",") -> Callable[[str, str], List[Any]]:
    """
    Builds post-processor for splitting answer into list and casting to a type
    """

    def type_caster(ans: str) -> List[Any]:
        items = as_list(ans, sep)
        if f is not None:
            items = map(f, items)

        return list(items)

    return type_caster


as_strs = as_list_of(str)
as_ints = as_list_of(int)
as_floats = as_list_of(float)


def mapped_to(*fs: Callable, sep: str = ",") -> Callable[[str], List[Any]]:
    """
    Builds post-processing for mapping list-like answers to a list of post-processing functions
    """

    def mapper(ans: str, **kw) -> List[Any]:
        items = as_list(ans, sep)
        if len(items) != len(fs):
            raise ValueError('Key & Input lists have mismatched lengths')
        return [f(i) for i, f in zip(items, fs)]

    return mapper


def as_int_range(ans: str) -> range:
    """
    Compute an integer range from a string representation. Several options:
        1. dash notation: 3 - 5 (only positive values)
        2. python slice notation: :3 (start implied to be 0), 3:4 (normal), 3:55:2 (with step)
        3. natural language: 'from 3 to 5' or '-55 to 55'
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
