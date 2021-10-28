
from __future__ import print_function
import Pyro4

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class doodleServer(object):
    def __init__(self):
        self.contents = ["chair","bike","flashlight"]

    def listContents(self):
        return self.contents

    def take(self, name, item):
        self.contents.remove(item)
        print("{0} took the {1}. ".format(name,item))

    def store(self, name, item):
        self.contents.append(item)
        print("{0} stored the {1}.".format(name, item))

def main():
    print("Server Init...")

    # This 'publish' the server on Naming Server (ns).
    # which allows to client class to find the server using lookup.
    Pyro4.Daemon.serveSimple(
        {
            doodleServer: "doodle.server"
        },
        ns= True)

if __name__=="__main__":
    main()