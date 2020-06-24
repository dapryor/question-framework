import ipaddress
import re


def is_ip_check(ip):
    try:
        ipaddress.ip_address(str(ip))
        return True
    except ValueError:
        return False


def x_hex_character_validation_gen(num_char):
    regex_str = "^[a-fA-F0-9]{%d}$" % (num_char, )
    return regex_match(regex_str)


def pick_from_choices(*choices):
    if len(choices) == 0:
        raise ValueError("pick_from_choices: Must pass in a non-zero number of choices.")
    try:
        choice_list = set(choices)
    except TypeError:
        choice_list = set(choices[0])
    return lambda x: x in choice_list


def regex_match(expression):
    return lambda x: re.match(expression, x)


def yes_or_no(x):
    x = x.lower()
    return pick_from_choices("y","n")(x)

def isint(x):
    return x.isdigit()

def ip_range(x):
    split_ips = x.replace(" ", "").split("-")
    if len(split_ips) != 2:
        return False
    ip1, ip2 = split_ips
    return is_ip_check(ip1) and is_ip_check(ip2)
