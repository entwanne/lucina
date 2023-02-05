import enum

from lucina.utils import ordered_enum


def test_ordered_enum():
    @ordered_enum
    class Enum(enum.Enum):
        A = 'a'
        B = 'b'
        C = 'c'

    assert Enum.A.rank == 0
    assert Enum.B.rank == 1
    assert Enum.C.rank == 2

    assert Enum('b').rank == 1
