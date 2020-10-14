

def test_as_list():
    assert as_list("3 4") == ["3", "4"]
    assert as_list("3 4 ") == ["3", "4"]
    assert as_list("3  4 ") == ["3", "4"]
    assert as_list("3, 4", sep=',') == ["3", "4"]

    
def test_as_list_of():
    assert as_list_of(int)("3 4") == [3, 4]
    assert as_list_of(float)("3.5; 6", sep=";") == [3.5, 6.0]
    
