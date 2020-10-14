import string
from random import choices
from types import FunctionType
from unittest import TestCase

from question_framework.validation import *

hex_list = list(string.hexdigits)
not_hex_list = list(set(string.printable) - set(hex_list))


class TestIsIPCheck(TestCase):
    def test_returns_bool(self):
        good = is_ip_check("1.1.1.1")
        bad = is_ip_check("abcdefg")
        self.assertIsInstance(good, bool, "Function did not return a bool.")
        self.assertIsInstance(bad, bool, "Function did not return a bool.")

    def test_is_ip_check(self):
        ip = "192.1.1.1"
        actual = is_ip_check(ip)
        expected = True
        self.assertTrue(actual is expected, f"IP {ip} was validated incorrectly.")

    def test_is_not_ip_check(self):
        ip = "Steve"
        actual = is_ip_check(ip)
        expected = False
        self.assertTrue(actual is expected, f"Non-IP {ip} was validated incorrectly.")

    def test_is_almost_an_ip_check(self):
        ip = "257.1.1.1"
        actual = is_ip_check(ip)
        expected = False
        self.assertTrue(actual is expected, f"Non-IP {ip} was validated incorrectly.")


class TestXHexCharacterValidationGen(TestCase):
    def test_returns_function(self):
        actual = x_hex_character_validation_gen(1)
        self.assertIsInstance(actual, FunctionType, "Function did not return a function.")

    def test_good_match(self):
        validation_fn = x_hex_character_validation_gen(1)
        for c in hex_list:
            actual = validation_fn(c)
            self.assertTrue(actual, f"Input: {c}, Output: {actual}")

    def test_good_length(self):
        for i in range(1, 10):
            validation_fn = x_hex_character_validation_gen(i)
            payload = choices(hex_list, k=i)
            payload = "".join(payload)
            actual = validation_fn(payload)
            self.assertTrue(actual, f"Input: {payload}, #{i}, Output: {actual}")

    def test_any_length(self):
        validation_fn = x_hex_character_validation_gen(-1)
        for i in range(1, 10):
            payload = choices(hex_list, k=i)
            payload = "".join(payload)
            actual = validation_fn(payload)
            self.assertTrue(actual, f"Input: {payload}, #{i}, Output: {actual}")

    def test_bad_characters(self):
        validation_fn = x_hex_character_validation_gen(1)
        for c in not_hex_list:
            actual = validation_fn(c)
            self.assertFalse(actual, f"Input: {c}, Output: {actual}")

    def test_bad_length(self):
        for i in range(1, 10):
            validation_fn = x_hex_character_validation_gen(i)
            payload = choices(hex_list, k=i + 1)
            payload = "".join(payload)
            actual = validation_fn(payload)
            self.assertFalse(actual, f"Input: {payload}, #{i}, Output: {actual}")
        for i in range(1, 10):
            validation_fn = x_hex_character_validation_gen(i)
            payload = choices(hex_list, k=i - 1)
            payload = "".join(payload)
            actual = validation_fn(payload)
            self.assertFalse(actual, f"Input: {payload}, #{i}, Output: {actual}")

    def test_bad_input(self):
        with self.assertRaises(TypeError):
            x_hex_character_validation_gen("abcdef")
        with self.assertRaises(TypeError):
            x_hex_character_validation_gen(-2)

# class TestPickFromChoices(TestCase):
#     def test_pick_from_choices(self):
#         self.fail()
#
#
# class TestRegexMatch(TestCase):
#     def test_regex_match(self):
#         self.fail()
#
#
# class TestYesOrNo(TestCase):
#     def test_yes_or_no(self):
#         self.fail()
#
#
# class TestIsInt(TestCase):
#     def test_is_int(self):
#         self.fail()
#
#
# class TestIpRange(TestCase):
#     def test_ip_range(self):
#         self.fail()
