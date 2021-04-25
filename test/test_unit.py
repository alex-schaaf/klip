from src import slicer, find


def test_slicer():
    iterable = [1, 2, 3, 4, 5, 6]

    slice_generator = slicer(iterable)

    assert list(slice_generator) == [
        slice(1, 2, None),
        slice(2, 3, None),
        slice(3, 4, None),
        slice(4, 5, None),
        slice(5, 6, None),
    ]


def test_find():
    iterable = [1, 2, 2, 3, 4, 5, 6, 6]

    assert find(iterable, 3) == [3]
    assert find(iterable, 2) == [1, 2]
    assert find(iterable, 6) == [6, 7]