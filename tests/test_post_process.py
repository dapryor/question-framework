import pytest
from delayed_assert import expect, assert_expectations

from question_framework.post_process import *


class Value:

    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.value == other.value


class TestAsList:

    def test_as_list(self):
        expect(as_list("3, 4") == ["3", "4"])
        expect(as_list("3,4") == ["3", "4"])
        expect(as_list("3 , 4 ") == ["3", "4"])
        assert_expectations()


class TestAsListOf:

    def test_as_list_of(self):
        expect(as_list_of(str)("2, a") == ["2", "a"])
        expect(as_list_of(int)("3, 4") == [3, 4])
        expect(as_list_of(float)("3.5, 6") == [3.5, 6.0])
        expect(as_list_of(Value)("33, allo") == [Value("33"), Value("allo")])
        assert_expectations()

    def test_as_list_of_sep(self):
        expect(as_list_of(str, ":")("2: a") == ["2", "a"])
        expect(as_list_of(int, ":")("3: 4") == [3, 4])
        expect(as_list_of(float, ":")("3.5: 6") == [3.5, 6.0])
        expect(as_list_of(Value, ":")("33: allo")
               == [Value("33"), Value("allo")])
        assert_expectations()


class TestMappedTo:

    def test_mapped_to(self):
        expect(mapped_to(int, float, str)(
            "34, 34.5, jon") == [34, 34.5, "jon"])

        with pytest.raises(ValueError, match=".*mismatched lengths"):
            mapped_to(int, float)("34, 34, 34")

        class IntValue(Value):
            def __init__(self, value): super().__init__(int(value))

        class FloatValue(Value):
            def __init__(self, value): super().__init__(float(value))

        expect(
            mapped_to(IntValue, FloatValue, str)("34, 34.5, jon") == [
                IntValue(34),
                FloatValue(34.5),
                "jon"
            ])
        assert_expectations()

    def test_mapped_to_sep(self):
        expect(mapped_to(int, float, str, sep=":")(
            "34: 34.5: jon") == [34, 34.5, "jon"])

        with pytest.raises(ValueError, match=".*mismatched lengths"):
            mapped_to(int, float)("34, 34, 34")

        class IntValue(Value):
            def __init__(self, value): super().__init__(int(value))

        class FloatValue(Value):
            def __init__(self, value): super().__init__(float(value))

        expect(
            mapped_to(IntValue, FloatValue, str, sep=":")("34: 34.5: jon") == [
                IntValue(34),
                FloatValue(34.5),
                "jon"
            ])
        assert_expectations()


class TestAsIntRange:

    def test_as_int_range(self):
        expect(as_int_range("3-66") == range(3, 66))
        expect(as_int_range("0 - 0") == range(0))

        expect(as_int_range(":33:3") == range(0, 33, 3))
        expect(as_int_range(":33") == range(0, 33))
        expect(as_int_range(":33") == range(0, 33))
        expect(as_int_range("0:33") == range(0, 33))
        expect(as_int_range("-28:33") == range(-28, 33))

        expect(as_int_range("from 333 to -28") == range(333, -28, -1))
        expect(as_int_range("from -333 to -28") == range(-333, -28, 1))
        expect(as_int_range("from -333 to 28") == range(-333, 28, 1))
        expect(as_int_range("333 to 2833") == range(333, 2833, 1))
        assert_expectations()
