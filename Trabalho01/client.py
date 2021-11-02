# ------------------------------
# Trabalho 1 - Sistemas Distribuídos
# Autores: 
# Alexandre Herrero matias
# # Matheus Fonseca Alexandre de Oliveira
# Professor: Ana Cristina Vendramin
# Projeto: Doodle
# ------------------------------

# Libraries

import Pyro4
import sys
import datetime
import threading

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes

def printableMenu(option):

    if option == 0:
        print("------------------------------")
        print("====== Thanks for using our services! ======")
        print(" Leaving now...")

    if option == 1:
        print("------------------------------")
        print("====== Welcome to Doodle!, please select options below: ======")
        print(" z - Create Account")
        print(" c - Leave")
        print("====== Tip: The menu is not case sensitive ======")        
        print("------------------------------")

    if option == 2:
        print("------------------------------")
        print("====== Welcome to Doodle!, please select options below: ======")
        print(" a - Create new survey")
        print(" s - Vote for existing survey")
        print(" d - Consult existing survey")
        print(" c - Leave")
        print("====== Tip: The menu is not case sensitive ======")        
        print("------------------------------")

    if option == 3:
        print("------------------------------")
        print("====== Create Survey Menu: ======")
        print(" Here is the template for new surveys")
        print(" Survey name:  string")
        print(" Place (Room/Location):  string")
        print(" Availabe Times: please input in yyyy-mm-dd hh:mm:ss format")
        print(" Deadline to answer: please input in yyyy-mm-dd hh:mm:ss format")
        print("====== Tip: The menu is case sensitive ======")        
        print("------------------------------")

    if option == 4:
        print("------------------------------")
        print("====== Vote Survey Menu: ======")
        print("Here are existing surveys for you to vote: ")

    if option == 5:
        print("------------------------------")
        print("====== Consult Survey Menu: ======")
        print("Here are existing surveys for you to consult: ")
@Pyro4.expose
class Client(object):

    def __init__(self):
        self.surveyServer = Pyro4.Proxy('PYRONAME:survey.server')
        self.abort = 0
        

    @Pyro4.expose
    @Pyro4.oneway
    # Server callback to print messages.
    def message(self, username, message):
        print(message)

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

    def createPublicKey(self):
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )

        self.public_key = self.private_key.public_key()
        self.pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
            )

    def start(self):
        
        # User Menu
        while(True):
            # Print welcoming menu
            printableMenu(1)
            choice = input(">: ").strip()

            if choice == 'z' or choice == 'Z':
                print("")
                self.createPublicKey()
                existingUsers = self.surveyServer.getUsers()
                print("Please, type your desired username.")
                while(True):
                    username = input(">: ").strip()
                    if username in existingUsers:
                        print(" Username not available, try again!")
                    else:
                        break
                self.name = username
                self.surveyServer.registerUser(self.name, self.pem, self)
                break

            elif choice == 'c' or choice == 'C':
                printableMenu(0)
                sys.exit()

        # User logged in
        while(True):
            # Print main menu
            printableMenu(2)
            choice = input(">: ").strip()

            # Create new survey menu
            if choice == 'a' or choice == 'A':
                printableMenu(3)
                # Take input from user
                surveyName = input("Survey Name: ").strip()
                surveyPlace = input("Place: ").strip()
                print("Available times: (to stop adding use c)")

                times = {}
                # Take available time for user until it hits c/C
                while(True):
                    time = input(">: ").strip()
                    try:
                        naive_datetime = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
                        times[time] = []
                        times[time].append(0)
                    except Exception as e:
                        print(e)
                    if time == 'c' or time == 'C':
                        break
                # Take deadline from user.
                surveyDeadline = input("Deadline: ")
                try:
                    naive_datetime = datetime.datetime.strptime(surveyDeadline, "%Y-%m-%d %H:%M:%S")
                except Exception as e:
                    print(e)

                # Save survey on server.
                results = self.surveyServer.registerSurvey(surveyName, self.name, surveyPlace, times, surveyDeadline)
                print(results)

            # Vote on existing survey menu
            elif choice == 's' or choice == 'S':
                printableMenu(4)
                openSurveys = self.surveyServer.getSurveys()
                print(*openSurveys, sep = '\n')
                print("Please, type the name of a survey you would like to vote.")
                surveyName = input(">: ").strip()

                print("Please, choose one of the time slots to vote")
                print("Reminder: use yyyy-mm-dd hh:mm:ss format. \nUse c to stop voting.")
                # TODO: Show time slots to user.
                votes = []
                while(True):
                    vote = input(">: ").strip()
                    try:
                        naive_datetime = datetime.datetime.strptime(vote, "%Y-%m-%d %H:%M:%S")
                        votes.append(vote)
                    except Exception as e:
                        print(e)
                    if vote == 'c' or vote == 'C':
                        break
                
                results = self.surveyServer.voteSurvey(surveyName, self.name, votes)
                print(results)

            # Consulting survey menu
            elif choice == 'd' or choice == 'D':
                printableMenu(5)
                openSurveys = self.surveyServer.getSurveys()
                print(*openSurveys, sep = '\n')
                print("Please, type the name of a survey you would like to consult.")
                surveyName = input(">: ").strip()

                signature = self.sign()
                results = self.surveyServer.consultSurvey(self.name, surveyName, signature)
                print(results)

            elif choice == 'c' or choice == 'C':
                printableMenu(0)
                sys.exit()

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


