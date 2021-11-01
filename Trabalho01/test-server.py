import sys
import threading
import Pyro4
import datetime
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes

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

    def privateKey(self):
        self.private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=1024,
            )

    def publicKey(self):
        return self.private_key.public_key()
    
    def sign(self):
        message = b"A message I want to sign"
        signature = self.private_key.sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return signature

    def saveKey(self, filename, pk):
        pem = pk.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
        with open(filename, 'wb') as pem_out:
            pem_out.write(pem)

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
        self.privateKey()
        self.saveKey(self.name + "PrivateKey.pem", self.private_key)
        print("Your private key has been generated and saved on the current directory!")
        self.surveyServer.registerUser(self.name, self.publicKey().public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo).decode(), self)
        create = input("Do you want to create a survey? ").strip()
        if create == "y":
            survey = input('Inform the name of the survey: ').strip()
            place = input('Inform the place of the survey: ').strip()
            print("Inform the times of the survey using the format yyyy-mm-dd hh:mm:ss")
            print("To stop enter s")
            times = {}
            while(True):
                time = input().strip()
                try:
                    naive_datetime = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
                    times[time] = []
                    times[time].append(0)
                except Exception as e:
                    print(e)
                if time == 's':
                    break
            deadline = input("Inform the deadline of the survey using the format yyyy-mm-dd hh:mm:ss ")
            try:
                naive_datetime = datetime.datetime.strptime(deadline, "%Y-%m-%d %H:%M:%S")
            except Exception as e:
                print(e)
            print(self.surveyServer.registerSurvey(survey, self.name, place, times, deadline))
        vote = input("Do you want to vote in a survey? ").strip()
        if vote == "y":
            survey = input('Inform the name of the survey: ').strip()
            print("Inform the times you are voting using the format yyyy-mm-dd hh:mm:ss")
            print("To stop enter s")
            times = []
            while(True):
                time = input().strip()
                try:
                    naive_datetime = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
                    times.append(time)
                except Exception as e:
                    print(e)
                if time == 's':
                    break
            print(self.surveyServer.voteSurvey(survey, self.name, times))
        consult = input("Do you want to consult a survey? ").strip()
        if consult == "y":
            survey = input('Inform the name of the survey: ').strip()
            print(self.surveyServer.consultSurvey(self.name, survey, self.sign()))
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