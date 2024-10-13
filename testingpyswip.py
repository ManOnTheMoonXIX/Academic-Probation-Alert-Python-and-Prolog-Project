from pyswip import Prolog

prolog = Prolog()

prolog.assertz("father(michael,john)")

result = list(prolog.query("father(michael,X)"))  # [{'X': 'john'}]

print(result)