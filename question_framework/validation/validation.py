import ipaddress
import re

from __future__ import absolute_import

from datetime import date, datetime

from .core import _validate_bool
from .common import make_optional_argument_default


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


_undefined = make_optional_argument_default()


def _validate_date(value, required=True):
    if value is None:
        if required:
            raise TypeError("required value is None")
        return

    # :class:`datetime` is a subclass of :class:`date`, but we really don't
    # want to accept it as it behaves very differently (timezones, leap
    # seconds, etc) and is usually presented in a very different way.
    if not isinstance(value, date) or isinstance(value, datetime):
        raise TypeError((
            "expected 'date', but value is of type {cls!r}"
        ).format(cls=value.__class__.__name__))


class _date_validator(object):
    def __init__(self, required):
        _validate_bool(required)
        self.__required = required

    def __call__(self, value):
        _validate_date(value, required=self.__required)

    def __repr__(self):
        args = []
        if not self.__required:
            args.append('required={required!r}'.format(
                required=self.__required,
            ))

        return 'validate_date({args})'.format(args=', '.join(args))


def validate_date(value=_undefined, required=True):
    """
    Checks that the value is a valid :class:`datetime.date` value.
    :param datetime.date value:
        The value to be validated.
    :param bool required:
        Whether the value can be `None`.  Defaults to `True`.
    :raises TypeError:
        If the value is not a date, or if it was marked as `required` but
        None was passed in.
    """
    validate = _date_validator(required=required)

    if value is not _undefined:
        validate(value)
    else:
        return validate


def _validate_datetime(value, required=True):
    if value is None:
        if required:
            raise TypeError("required value is None")
        return

    if not isinstance(value, datetime):
        raise TypeError((
            "expected 'datetime', but value is of type {cls!r}"
        ).format(cls=value.__class__.__name__))

    if value.tzinfo is None:
        raise ValueError((
            "datetime object is missing timezone"
        ))


class _datetime_validator(object):
    def __init__(self, required):
        _validate_bool(required)
        self.__required = required

    def __call__(self, value):
        _validate_datetime(value, required=self.__required)

    def __repr__(self):
        args = []
        if not self.__required:
            args.append('required={required!r}'.format(
                required=self.__required,
            ))

        return 'validate_datetime({args})'.format(args=', '.join(args))


def validate_datetime(value=_undefined, required=True):
    """
    Checks that the value is a valid :class:`datetime.datetime` value.
    The value must have a valid timezone to be accepted.  Naive `datetime`
    objects are not allowed.
    :param datetime.date value:
        The value to be validated.
    :param bool required:
        Whether the value can be `None`.  Defaults to `True`.
    :raises TypeError:
        If the value is not a datetime, or if it was marked as `required` but
        None was passed in.
    :raises ValueError:
        If the value does not have a valid timezone.
    """
    validate = _datetime_validator(required=required)

    if value is not _undefined:
        validate(value)
    else:
        return validate