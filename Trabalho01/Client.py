# ------------------------------
# Trabalho 1 - Sistemas Distribuídos
# Autores: 
# Alexandre Herrero matias
# Matheus Fonseca Alexandre de Oliveira
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
        # Conecta com o server através do servidor de nomes.
        self.surveyServer = Pyro4.Proxy('PYRONAME:survey.server')
        # Para abortar a thread da classe em casos específicos
        self.abort = 0
        
    # Expondo o método pra ser executado pelo servidor
    @Pyro4.expose
    @Pyro4.oneway
    # Server callback to print messages.
    def message(self, username, message):
        print(message)

    # Assinatura do client. Não assinamos uma mensagem em si, mas sim uma mensagem base nos dois lados (server e cliente), e utilizamos a assinatura gerada para confirmar se é a mesma pessoa.
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

    # Gera a chave pública (e privada) do cliente, usando uma configuração base do RSA. Gera também a chave em formato PEM em String para facilitar a passagem dos dados pelo Pyro
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
        self.pem = self.pem.decode()

    # Método principal do Objeto.
    def start(self):
        # First while - User Menu Interaction
        while(True):
            # Print welcoming menu
            printableMenu(1)
            choice = input(">: ").strip()

            # Option 1 - Create Account
            if choice == 'z' or choice == 'Z':
                # Generate Public Key for this client process
                self.createPublicKey()

                # Get List of existing Users from server
                existingUsers = self.surveyServer.getUsers()
                print("Please, type your desired username.")

                # Wait for user to write one available name to use
                while(True):
                    username = input(">: ").strip()
                    if username in existingUsers:
                        print(" Username not available, try again!")
                    else:
                        break
                # Proceeds with user registration
                self.name = username
                self.surveyServer.registerUser(self.name, self.pem, self)
                break

            # Option to leave the program
            elif choice == 'c' or choice == 'C':
                printableMenu(0)
                sys.exit()

        # While menu for Users already logged in
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

                # Since user can add multiple timeslots, this will be done inside one dictionary
                times = {}
                # Take available time for user until it hits c/C
                while(True):
                    time = input(">: ").strip()
                    if time == 'c' or time == 'C':
                        break
                    try:
                        # Check if the written time is correct, transforming it correctly using datetime. This will be cross checked on server side
                        naive_datetime = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
                        times[time] = []
                        times[time].append(0)
                        # Writing wrong format will terminate the program.
                    except Exception as e:
                        print(e)
                    
                # Take deadline from user.
                surveyDeadline = input("Deadline: ")
                try:
                    # Check if the written time is correct, transforming it correctly using datetime. This will be cross checked on server side
                    naive_datetime = datetime.datetime.strptime(surveyDeadline, "%Y-%m-%d %H:%M:%S")
                    
                    # Writing wrong format will terminate the program.
                except Exception as e:
                    print(e)

                # Save survey on server.
                results = self.surveyServer.registerSurvey(surveyName, self.name, surveyPlace, times, surveyDeadline)
                print(results)

            # Vote on existing survey menu
            elif choice == 's' or choice == 'S':
                printableMenu(4)
                # Get Ongoing Surveys Data to show to user
                openSurveys = self.surveyServer.getSurveysInfo()
                print(openSurveys)
                print("Please, type the name of a survey you would like to vote.")
                surveyName = input(">: ").strip()

                print("Please, choose one of the time slots to vote")
                print("Reminder: use yyyy-mm-dd hh:mm:ss format. \nUse c to stop voting.")
                votes = []
                # Since user can vote on multiple time slots, this will added on the list
                while(True):
                    vote = input(">: ").strip()
                    if vote == 'c' or vote == 'C':
                        break
                    try:
                        # Check if the written time is correct, transforming it correctly using datetime. This will be cross checked on server side
                        naive_datetime = datetime.datetime.strptime(vote, "%Y-%m-%d %H:%M:%S")
                        votes.append(vote)
                        # Writing wrong format will terminate the program.
                        # Bonus: you can vote multiple times on the same timeslot here, since we compute all votes in one go only later.
                    except Exception as e:
                        print(e)
                    
                # Send the votes to server
                results = self.surveyServer.voteSurvey(surveyName, self.name, votes)
                print(results)

            # Consulting survey menu
            elif choice == 'd' or choice == 'D':
                printableMenu(5)
                # Gets all surveys (ongoing and closed) to show to user, since here he can consult all surveys available
                all = True
                openSurveys = self.surveyServer.getSurveys(all)
                # Print each survey name per line
                print(*openSurveys, sep = '\n')
                print("Please, type the name of a survey you would like to consult.")
                surveyName = input(">: ").strip()
                # Get the results from the survey in the server.
                # Here, server handles if: user already voted (has permission to see), user didn't voted (permission denied), signature from user is correct (sign, verify)
                results = self.surveyServer.consultSurvey(self.name, surveyName, self.sign())
                print(results)

            # Option to leave the program
            elif choice == 'c' or choice == 'C':
                printableMenu(0)
                sys.exit()

# Following <chatbox> example, we create threads for the class to run
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


