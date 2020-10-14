import string
from random import choices
import pytest
from delayed_assert import expect, assert_expectations
from question_framework.validation import *

hex_list = list(string.hexdigits)
not_hex_list = list(set(string.printable) - set(hex_list))


class TestIsIPCheck:
    def test_returns_bool(self):
        good = is_ip_check("1.1.1.1")
        bad = is_ip_check("abcdefg")
        expect(type(good) == bool)
        expect(type(bad) == bool)
        assert_expectations()

    def test_is_ip_check(self):
        ip = "192.1.1.1"
        actual = is_ip_check(ip)
        expected = True
        assert actual is expected

    def test_is_not_ip_check(self):
        ip = "Steve"
        actual = is_ip_check(ip)
        expected = False
        assert actual is expected

    def test_is_almost_an_ip_check(self):
        ip = "257.1.1.1"
        actual = is_ip_check(ip)
        expected = False
        assert actual is expected


class TestXHexCharacterValidationGen:
    def test_returns_function(self):
        actual = x_hex_character_validation_gen(1)
        assert type(actual) == FunctionType

    def test_good_match(self):
        validation_fn = x_hex_character_validation_gen(1)
        for c in hex_list:
            actual = validation_fn(c)
            expect(actual is True)
        assert_expectations()

    def test_good_length(self):
        for i in range(1, 10):
            validation_fn = x_hex_character_validation_gen(i)
            payload = choices(hex_list, k=i)
            payload = "".join(payload)
            actual = validation_fn(payload)
            expect(actual is True)
        assert_expectations()

    def test_any_length(self):
        validation_fn = x_hex_character_validation_gen(-1)
        for i in range(1, 10):
            payload = choices(hex_list, k=i)
            payload = "".join(payload)
            actual = validation_fn(payload)
            expect(actual is True)
        assert_expectations()

    def test_bad_characters(self):
        validation_fn = x_hex_character_validation_gen(1)
        for c in not_hex_list:
            actual = validation_fn(c)
            expect(actual is False)
        assert_expectations()

    def test_bad_length(self):
        for i in range(1, 10):
            validation_fn = x_hex_character_validation_gen(i)
            payload = choices(hex_list, k=i + 1)
            payload = "".join(payload)
            actual = validation_fn(payload)
            expect(actual is False)
        for i in range(1, 10):
            validation_fn = x_hex_character_validation_gen(i)
            payload = choices(hex_list, k=i - 1)
            payload = "".join(payload)
            actual = validation_fn(payload)
            expect(actual is False)
        assert_expectations()

    def test_bad_input(self):
        with pytest.raises(TypeError, match="Expecting input of type int"):
            x_hex_character_validation_gen("abcdef")
        with pytest.raises(TypeError, match="Expecting positive integer input"):
            x_hex_character_validation_gen(-2)
