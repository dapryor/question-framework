from ipaddress import ip_address
from typing import Callable, List, Optional, Any
from functools import partial
import re


# Higher order post processors

def as_list(ans: str, sep: str = ' ', f: Optional[Callable[[str], ...]] = None) -> List[Any]:
    items = ans.split(sep)
    if f is not None:
        items = list(map(f, items))
    return items


def as_list_of(type: type) -> Callable[[str], List[Any]]:
    def lister(ans: str) -> List[Any]:
        return as_list(ans, f=type)
    return lister


as_ints = partial(as_list_of, int)
as_floats = partial(as_list_of, float)


def as_int_range(ans: str) -> range:
    ans = ans.strip()
    if re.match(r'[0-9]+-[0-9]+', ans):
        start, end = ans.split('-')
        return range(int(start), int(end))
    if ':' in ans:
        start, end, *step = ans.split(':')
        start = int(start or 0)
        step = int(step or 1)
        return range(start, int(end), step)
    if re.match(r'from\s+-?[0-9]+\s+to\s+-?[0-9]+', ans):
        _, start, _, end = ans.split()
        return range(int(start), int(end))
    raise ValueError(f'Could not transform {ans!r} into an integer range')

    
def ip_range_to_list(x):
    def ip_range_generator(ip1, ip2):
        ip1 = int(ip_address(ip1))
        ip2 = int(ip_address(ip2))
        ip1, ip2 = min(ip1, ip2), max(ip1, ip2)
        for i in range(ip1, ip2 + 1):
            yield ip_address(i)

    ip1, ip2 = x.replace(" ", "").split("-")

    return ip_range_generator(ip1, ip2)
