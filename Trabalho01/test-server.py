import sys
import threading
import Pyro4
import datetime

if sys.version_info < (3, 0):
    input = raw_input

# The daemon is running in its own thread, to be able to deal with server
# callback messages while the main thread is processing user input.

class Client(object):
    def __init__(self):
        self.surveyServer = Pyro4.core.Proxy('PYRONAME:survey.server')
        self.abort = 0

    @Pyro4.expose
    @Pyro4.oneway
    def message(self, name, msg):
        print(msg)

    def start(self):
        users = self.surveyServer.getUsers()
        if users:
            print("The following people are on the server: ")
            for user in users:
                print(user)
        surveys = self.surveyServer.getSurveys()
        if surveys:
            print("The following surveys already exist: ")
            for survey in surveys:
                print(survey)
        self.name = input('Inform your name: ').strip()
        self.publickey = input('Inform your public key: ').strip()
        print(self.surveyServer.registerUser(self.name, self.publickey, self))
        create = input("Do you want to create a survey? ").strip()
        if create == "y":
            survey = input('Inform the name of the survey: ').strip()
            place = input('Inform the place of the survey: ').strip()
            print("Inform the times of the survey using the format yyyy-mm-dd hh:mm:ss")
            print("To stop enter s")
            times = []
            while(True):
                time = input().strip()
                try:
                    naive_datetime = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
                    times.append(naive_datetime)
                except Exception as e:
                    print(e)
                if time == 's':
                    break
            deadline = input("Inform the deadline of the survey using the format yyyy-mm-dd hh:mm:ss ")
            try:
                naive_datetime = datetime.datetime.strptime(deadline, "%Y-%m-%d %H:%M:%S")
            except Exception as e:
                print(e)
            print(self.surveyServer.registerSurvey(survey, self.name, place, times, naive_datetime))
        while(True):
            pass
class DaemonThread(threading.Thread):
    def __init__(self, client):
        threading.Thread.__init__(self)
        self.client = client
        self.setDaemon(True)

    def run(self):
        with Pyro4.core.Daemon() as daemon:
            daemon.register(self.client)
            daemon.requestLoop(lambda: not self.client.abort)

client = Client()
daemonthread = DaemonThread(client)
daemonthread.start()
client.start()
print('Exit.')