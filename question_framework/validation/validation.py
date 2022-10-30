import ipaddress
import re
from typing import Callable


class ValidationError(Exception):
    pass


def is_ip(ip: str) -> bool:
    try:
        ipaddress.ip_address(str(ip))
        return True
    except ValueError:
        return False


def is_ip_range(x: str) -> bool:
    split_ips = x.replace(" ", "").split("-")
    if len(split_ips) != 2:
        return False
    ip1, ip2 = split_ips
    return is_ip(ip1) and is_ip(ip2)


def x_hex_character_validation_gen(num_char: int) -> Callable[[str], bool]:
    if not isinstance(num_char, int):
        raise TypeError("Expecting input of type int")
    if num_char == -1:
        num_char = "+"
    elif num_char < 0:
        raise TypeError("Expecting positive integer input")
    else:
        num_char = f"{{{num_char}}}"

    regex_str = f"^[a-fA-F0-9]{num_char}$"
    return regex_match(regex_str)


def pick_from_choices(*choices, with_message=False) -> Callable[[str], bool]:
    if len(choices) == 0:
        raise ValueError("pick_from_choices: Must pass in a non-zero number of choices.")
    try:
        choice_list = set(choices)
    except TypeError:
        choice_list = set(choices[0])
    choice_list = set(map(str, choice_list))

    def in_list(x: str) -> bool:
        if str(x) in choice_list:
            return True
        else:
            if with_message:
                raise ValidationError(f"Invalid Choice: {x!r}. Pick one of the following {choice_list}")
            else:
                return False

    return in_list


def yes_or_no(x: str) -> bool:
    x = x.lower()
    return pick_from_choices("y", "n")(x)


def regex_match(expression: str) -> Callable[[str], bool]:
    def match_fn(x):
        return True if re.match(expression, x) else False

    return match_fn


def is_of_type(t: type) -> Callable[[str], bool]:
    """
    Builds is_type validators
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
