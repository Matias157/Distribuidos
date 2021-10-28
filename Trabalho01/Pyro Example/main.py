
import Pyro4
import Pyro4.util
import sys

from Person import Person

sys.excepthook = Pyro4.util.excepthook

matheus = Person("Math")
matias = Person("Matias")
doodle = Pyro4.Proxy("PYRONAME:doodle.server")

matheus.visit(doodle)
matias.visit(doodle)