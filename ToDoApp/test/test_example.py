def test_equal_or_not():
    assert 1 == 1
    assert 1 != 2


def test_is_in():
    assert 1 in [1, 2, 3]
    assert 2 not in [1, 3, 5]


def test_is_not_in():
    assert 1 not in [2, 3, 4]
    assert 2 in [1, 2, 3]


def test_is_instance():
    assert isinstance(1, int)
    assert isinstance("hello", str)


def test_is_not_instance():
    assert not isinstance(1, str)
    assert not isinstance("hello", int)


def test_is_none():
    assert None is None
    assert None is not 0


def test_is_not_none():
    assert 0 is not None
    assert 1 is not None


def test_is_true():
    assert True is True
    assert True is not False


def test_is_not_true():
    assert True is not False
    assert False is not True


def test_is_false():
    assert False is False
    assert False is not True


def test_is_not_false():
    assert False is not True
    assert True is not False


def test_is_not():
    assert not False
    assert not 0
    assert not None


def test_is():
    assert True
    assert 1
    assert "hello"


def test_is_not_equal():
    assert 1 == 1
    assert 1 != 2
    assert "hello" == "hello"
    assert "hello" != "world"


def test_all_or_any():
    assert all([True, True, True])
    assert any([True, False, False])
    num_list = [1, 2, 3, 4, 5]
    assert all([num > 0 for num in num_list])
    assert any([num == 3 for num in num_list])
    num_tuple = (1, 2, 3, 4, 5)
    assert all([num > 0 for num in num_tuple])
    assert any([num == 3 for num in num_tuple])
    num_set = {1, 2, 3, 4, 5}
    assert all({num > 0 for num in num_set})
    assert any({num == 3 for num in num_set})


def test_type():
    assert type(1) == int
    assert type(1.0) == float
    assert type("hello") == str
    assert type([1, 2, 3]) == list
    assert type((1, 2, 3)) == tuple
    assert type({1, 2, 3}) == set
    assert type({1: "one", 2: "two"}) == dict
    assert type(True) == bool
    assert type(None) == type(None)
    assert type(1) != type(1.0)
    assert type([1, 2, 3]) != type((1, 2, 3))
    assert type({1, 2, 3}) != type([1, 2, 3])
    assert type({1: "one", 2: "two"}) != type([1, 2, 3])
    assert type(True) == type(False)
    assert type(None) != type(1)
