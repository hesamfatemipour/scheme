"""
   Scheme types that will be implemented
"""


class Types:
    Symbol = str
    List = list
    Number = (int, float)


def atom(token):
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return Types.Symbol(token)
