
from collections import namedtuple

from ._number import number as mynumber

class MyNumber(namedtuple("MyNumber", ["mynumber"])):
    pass


if __name__ == "__main__":
    print(MyNumber(mynumber))