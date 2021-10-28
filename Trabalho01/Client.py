
import Pyro4
import sys
import time

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

# GLOBAL CONTROLLERS
menuFlag = False
userLogged = False
@Pyro4.expose
@Pyro4.callback
class Client(object):
    def __init__(self, name):
        self.name = name

    def notify(self):
        print("Callback received")

    #def loopThread(daemon):

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

def login():
    print('oooooi, josuke!')

def printMenu(option = 0, username = 'Default'):

    if option == 0:
        print("------------------------------")
        print("====== Welcome to Doodle!, please select options below: ======")
        print(" z - Create Account")
        print(" x - Login")
        print(" c - Leave")
        print("====== Tip: The menu is not case sensitive ======")        
        print("------------------------------")

    if option == 1:
        print("------------------------------")
        print("====== Create Account Menu ======")
        print("====== Tip: The credentials will be case sensitive ======")

    if option == 2:
        print("------------------------------")
        print("====== Login Menu ======")
        print("====== Tip: The credentials will be case sensitive ======")

    if option == 3:
        print("------------------------------")
        print("====== Welcome! " + str(username) + "======")

    if option == 4:
        print("------------------------------")
        print("====== Please select options below: ======")
        print(" z - Create new Survey")
        print(" x - Vote for open surveys")
        print(" c - Check for ongoing surveys ")        
        print(" v - Check for updates")
        print(" b - Leave | Shut down")
        print("====== Tip: The menu is not case sensitive ======")   

    
    if option == 6:
        print("------------------------------")
        print("====== Thanks for using our services! ======")

def main():

    # Step 1 - Init client.py and locate server named survey.server
    ns = Pyro4.locateNS()
    uri = ns.lookup("survey.server")
    surveyServer = Pyro4.Proxy(uri)

    # Step 2 - After connected to server, presents the main menu to the client.
    if not surveyServer:
        print("Sorry, something went wrong when connecting to the server. Please try again.")
        sys.exit()
    else:
        menuFlag = True

    while(menuFlag):
        printMenu(0)        
        choice = input("Input: ")

        # Create Account Menu
        if(choice == 'z' or choice == 'Z'):
            printMenu(1)
            username = input("Write your desired username: ")
            
            # TODO: Server method to create account.
            # If successful, we create client with that username.
            client = Client(username)

            print(" Account created successfully! ")
            time.sleep(5)

        # Login Menu
        elif(choice == 'x' or choice == 'X'):
            printMenu(2)
            username = input("Username: ")

            # TODO: Server method to check if credentials are correct.
            printMenu(3,username)
            menuFlag = False
            userLogged = True

        elif(choice == '3'):
            print("Thank you! Leaving now...")
            sys.exit()
        
    while(userLogged):
        printMenu(4)
        choice = input("Input: ")

        # Choice 1 - Create New Survey
        if (choice == 'z' or choice == 'Z'):
            # TODO: Menu for necessary information.
            print(" Welcome to our survey creator! Below, you will find every information necessary to create your survey.")
            # TODO: Server method to add new survey.


        # Choice 2 - Vote for open surveys
        elif (choice == 'x' or choice == 'X'):
            # TODO: Server method to vote for existing survey.
            print(" Below you will find all surveys that required your attention. Please, choose one open survey to start.")

        # Choice 3 - Check for ongoing surveys
        elif (choice == 'c' or choice == 'C'):
            # TODO: Server method to check ongoing status for surveys.
            print(" Please, inform what survey you want to know more about.")
            print(" REMINDER! YOU CAN ONLY CHECK SURVEY STATUS FOR SURVEYS YOU ALREADY PARTICIPATED!")
            # TODO: This message needs to be signed.
            # serverFunc(client.sign(message))

        # Choice 4 - Check for updates
        elif (choice == 'v' or choice == 'V'):
            # TODO: "client...?" method to receive notifications.
            client.notify()

        # Choice 5 - Leave the program
        elif (choice == 'b' or choice == 'B'):
            print("Thank you! Leaving now...")
            sys.exit()

