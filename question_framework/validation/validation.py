import ipaddress
import re
from types import FunctionType
from typing import Callable, List, Optional, Any
from functools import partial


def is_ip_check(ip: str) -> bool:
    try:
        ipaddress.ip_address(str(ip))
        return True
    except ValueError:
        return False


def x_hex_character_validation_gen(num_char: int) -> FunctionType:
    if not isinstance(num_char, int):
        raise TypeError("Expecting input of type int")
    if num_char == -1:
        num_char = "+"
    elif num_char < 0:
        raise TypeError("Expecting positive integer input")
    else:
        num_char = "{{{0}}}.format(num_char)"

    regex_str = "^[a-fA-F0-9]{}$".format(num_char)
    return regex_match(regex_str)


def pick_from_choices(*choices) -> FunctionType:
    if len(choices) == 0:
        raise ValueError("pick_from_choices: Must pass in a non-zero number of choices.")
    try:
        choice_list = set(choices)
    except TypeError:
        choice_list = set(choices[0])
    return lambda x: x in choice_list


def regex_match(expression: str) -> FunctionType:
    def match_fn(x):
        return True if re.match(expression, x) else False

    return match_fn


def yes_or_no(x: str) -> bool:
    x = x.lower()
    return pick_from_choices("y", "n")(x)


def is_of_type(t: type) -> FunctionType:
    """
    Helper function to build is_type 
    """

    def type_validator(x: str) -> bool:
        try:
            t(x)
            return True
        except ValueError:
            return False

    return type_validator

is_int = is_of_type(int)
is_float = is_of_type(float)
is_complex = is_of_type(complex)

def ip_range(x: str) -> bool:
    split_ips = x.replace(" ", "").split("-")
    if len(split_ips) != 2:
        return False
    ip1, ip2 = split_ips
    return is_ip_check(ip1) and is_ip_check(ip2)
