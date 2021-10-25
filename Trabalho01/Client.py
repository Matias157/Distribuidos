
# Client 

import threading
from threading import Thread
import Pyro4
from Pyro4.core import callback
from Pyro4.core import Daemon

# We are exposing the class clientCallback to Pyro
# We are telling Pyro that this class has callback
@Pyro4.expose
@Pyro4.callback
class clientCallback(object):
    def notification(self):
        print('Callback received')

    def loopThread(daemon):
        daemon.requestLoop()
        # What is daemon?

    def main():
        ns = Pyro4.locateNS()
        uri = ns.lookup("Server.py") # Like this?

        server = Pyro4.Proxy(uri)

        daemon = Pyro4.Daemon()
        callback = clientCallback()
        daemon.register(callback)

        thread = threading.Thread(target= loopThread, args=(daemon,))
        thread.daemon = True
        thread.start()

    
