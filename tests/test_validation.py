import string
from random import choices
from types import FunctionType

import pytest
from delayed_assert import expect, assert_expectations

from question_framework.validation import *

hex_list = list(string.hexdigits)
not_hex_list = list(set(string.printable) - set(hex_list))


class TestIsIPCheck:
    def test_returns_bool(self):
        good = is_ip("1.1.1.1")
        bad = is_ip("abcdefg")
        expect(type(good) == bool)
        expect(type(bad) == bool)
        assert_expectations()

    def test_is_ip(self):
        ip = "192.1.1.1"
        actual = is_ip(ip)
        expected = True
        assert actual is expected

    def test_is_not_ip_check(self):
        ip = "Steve"
        actual = is_ip(ip)
        expected = False
        assert actual is expected

    def test_is_almost_an_ip_check(self):
        ip = "257.1.1.1"
        actual = is_ip(ip)
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


class TestIsOfType:

    def test_is_int(self):
        expect(is_int("5") is True)
        expect(is_int("1") is True)
        expect(is_int("-10") is True)
        expect(is_int("a") is False)
        expect(is_int("*(sjehv") is False)
        assert_expectations()

    def test_is_float(self):
        expect(is_float("5") is True)
        expect(is_float("1.15") is True)
        expect(is_float("-10.20") is True)
        expect(is_float("a") is False)
        expect(is_float("*(sjehv") is False)
        assert_expectations()

    def test_is_complex(self):
        expect(is_complex("5") is True)
        expect(is_complex("1.15-15.5j") is True)
        expect(is_complex("-10.20+20j") is True)
        expect(is_complex("a") is False)
        expect(is_complex("10 + 20j") is False)
        assert_expectations()

    def test_is_bool(self):
        is_bool = is_of_type(bool)
        expect(is_bool("5") is True)
        expect(is_bool("1.15") is True)
        expect(is_bool("-10.20") is True)
        expect(is_bool("a") is True)
        expect(is_bool("*(sjehv") is True)
        assert_expectations()


class TestPickFromChoices:
    def test_returns_function(self):
        actual = pick_from_choices("a")
        assert type(actual) == FunctionType

    def test_pick_from_choices_bad_input_with_message(self):
        with pytest.raises(ValueError):
            pick_from_choices()

    def test_pick_from_choices_bad_choice_with_message(self):
        inputs = [1, 2, 3, "a", "b", "c"]
        fn = pick_from_choices(*inputs, with_message=True)

        with pytest.raises(ValidationError):
            fn("F")

    def test_pick_from_choices_bad_choice_with_out_message(self):
        inputs = [1, 2, 3, "a", "b", "c"]
        fn = pick_from_choices(*inputs)

        expected = False
        actual = fn("F")
        assert actual is expected

    def test_pick_from_choices_mixed_types(self):
        inputs = [1, 2, 3, "a", "b", "c"]
        fn = pick_from_choices(*inputs)
        expected = True

        for i in inputs:
            actual = fn(i)
            expect(actual is expected, f"In: {i}")

        assert_expectations()
