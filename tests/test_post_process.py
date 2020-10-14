import sys
sys.path.append('..')
from question_framework.post_process import *


def test_as_list():
    assert as_list("3, 4") == ["3", "4"]
    assert as_list("3,4") == ["3", "4"]
    assert as_list("3 , 4 ") == ["3", "4"]

    
def test_as_list_of():
    assert as_list_of(int)("3, 4") == [3, 4]
    assert as_list_of(float)("3.5; 6", sep=";") == [3.5, 6.0]
    

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


if __name__ == "__main__":
    test_as_list()
    test_as_list_of()
    test_as_int_range()