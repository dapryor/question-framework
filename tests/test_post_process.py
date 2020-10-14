from question_framework.post_process import *


def test_as_list():
    assert as_list("3, 4") == ["3", "4"]
    assert as_list("3,4") == ["3", "4"]
    assert as_list("3 , 4 ") == ["3", "4"]


class Value:
    def __init__(self, value):
        self.value = value
    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.value == other.value


def test_as_list_of():

    assert as_list_of(int)("3, 4") == [3, 4]
    assert as_list_of(float)("3.5; 6", sep=";") == [3.5, 6.0]
    assert as_list_of(Value)("33, allo") == [Value("33"), Value("allo")]


def test_mapped_to():

    assert mapped_to(int, float, str)("34, 34.5, jon") == [34, 34.5, "jon"]

    try:
        mapped_to(int, float)("34, 34, 34")
    except ValueError as ve:
        assert str(ve).endswith('mismatched lengths')

    class IntValue(Value):
        def __init__(self, value): super().__init__(int(value))
    class FloatValue(Value):
        def __init__(self, value): super().__init__(float(value))

    assert mapped_to(IntValue, FloatValue, str)("34, 34.5, jon") == [
        IntValue(34),
        FloatValue(34.5),
        "jon"
    ]

def test_as_int_range():

    assert as_int_range("3-66") == range(3, 66)
    assert as_int_range("0 - 0") == range(0)

    assert as_int_range(":33:3") == range(0, 33, 3)
    assert as_int_range(":33:") == range(0, 33)
    assert as_int_range(":33") == range(0, 33)
    assert as_int_range("0:33") == range(0, 33)
    assert as_int_range("-28:33:") == range(-28, 33)

    assert as_int_range("from 333 to -28") == range(333, -28, -1)
    assert as_int_range("from -333 to -28") == range(-333, -28, 1)
    assert as_int_range("from -333 to 28") == range(-333, 28, 1)
    assert as_int_range("333 to 2833") == range(333, 2833, 1)
