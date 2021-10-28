
# Client 

import threading

import Pyro4
import sys
from Pyro4.core import callback
from Pyro4.core import Daemon
from threading import Thread

if sys.version_info < (3, 0):
    input = raw_input

class Person(object):
    def __init__(self, name):
        self.name = name

    def visit(self, warehouse):
        print("This is {0}".format(self.name))
        self.deposit(warehouse)
        self.retrieve(warehouse)
        print("Thank you, come again!")

    def deposit(self, warehouse):
        print("The warehouse contains: ", warehouse.listContents())
        item = input("Type a thing you want to store (or empty): ").strip()
        if item:
            warehouse.store(self.name, item)

    def retrieve(self, warehouse):
        print("The warehouse contains: ", warehouse.listContents())
        item = input("Type a thing you want to retrieve (or empty): ").strip()
        if item:
            warehouse.take(self.name, item)

    
