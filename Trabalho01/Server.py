import Pyro4
import datetime
import base64
import threading
import cryptography.exceptions
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class Survey(object):
    def __init__(self):
        self.surveys = {}
        self.users = {}

        self.thread_surveys = threading.Thread(target=self.notifySurvey, daemon=True)
        self.thread_surveys.start()

    def getSurveys(self):
        return list(self.surveys.keys())

    def getUsers(self):
        return list(self.users.keys())

    def verifySignature(self, publicKey, signature):
        message = b"A message I want to sign"
        try:
            publicKey.verify(
                signature,
                message,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except cryptography.exceptions.InvalidSignature as e:
            return False

    def registerUser(self, name, publickey, callback):
        if not name or not publickey:
            raise ValueError("Invalid name or public key")
        if name not in self.users:
            print('Registering new user %s' % name)
            self.users[name] = []
        self.users[name].append((name, publickey, callback))
        return [name for (name, publickey, callback) in self.users[name]]

    def registerSurvey(self, survey, name, place, times, deadline):
        if not survey or not name or not place or not times or not deadline:
            raise ValueError("invalid info")
        if survey not in self.surveys:
            print('Creating new survey %s' % survey)
            self.surveys[survey] = []
        names = []
        names.append(name)
        self.surveys[survey].append((survey, names, place, times, deadline, "Ongoing"))
        for user in self.users:
            self.publish(user, "\n------------------\nNew survey created!\n" + "Survey: " + survey + "\nCreator: " + name + "\nPlace: " + place + "\nProposed times: " + str(times) + "\nDeadline: " + deadline + "\n------------------")
        return [survey for (survey, name, place, times, deadline, state) in self.surveys[survey]]

    def voteSurvey(self, survey, name, times):
        if not survey or not name or not times:
            raise ValueError("invalid vote")
        if survey not in self.surveys:
            raise ValueError("invalid survey")
        for (s, n, p, t, d, state) in self.surveys[survey]:
            if name in n:
                raise ValueError("user already on survey")
                break
        n.append(name)
        for time in times:
            for (s, n, p, t, d, state) in self.surveys[survey]:
                t[time][0] += 1
        return("Vote has been successfully computed!")

    def consultSurvey(self, name, survey, signature):
        if not name or not survey or not signature:
            raise ValueError("invalid info")
        for (s, n, p, t, d, state) in self.surveys[survey]:
            if name not in n:
                return("Permission denied!")
        publicKeyStr = ""
        for (n, pk, c) in self.users[name]:
            publicKeyStr = pk
        pubk = serialization.load_pem_public_key(publicKeyStr.encode(), default_backend())
        retorno = "\n------------------\nUsers that already voted:\n"
        if self.verifySignature(pubk, base64.b64decode(signature["data"])):
            for (s, n, p, t, d, state) in self.surveys[survey]:
                for name in n:
                    retorno += " - " + name + "\n"
                retorno += "Proposed times:\n"
                for time in t:
                    retorno += " - " + time + " - votes: " + str(t[time][0]) + "\n"
                retorno += "State of the survey:\n - " + state + "\n------------------"
            return(retorno)
        else:
            return("Permission denied!")

    def notifySurvey(self):
        while(True):
            surveycreated = self.getSurveys()
            if surveycreated:
                for survey in self.surveys:
                    for (s, n, p, t, d, state) in self.surveys[survey]:
                        if (state == "Ongoing"):
                            names = []
                            for user in self.users:
                                for (nn, pk, c) in self.users[user]:
                                    names.append(nn)
                            surveynames = n
                            names.sort()
                            surveynames.sort()
                            if (names == surveynames or datetime.datetime.now().timestamp() >= datetime.datetime.strptime(d, "%Y-%m-%d %H:%M:%S").timestamp()):
                                returnStr = "\nSurvey " + s + " has finished!\nMost voted times:\n"
                                for time in t:
                                    returnStr += " - " + time + " - votes: " + str(t[time][0]) + "\n"
                                for name in names:
                                    self.publish(name, returnStr)
                                self.surveys[survey][0] = (self.surveys[survey][0][0], self.surveys[survey][0][1], self.surveys[survey][0][2], self.surveys[survey][0][3], self.surveys[survey][0][4], "Closed")
                            else:
                                pass
                        else:
                            pass
            else:
                pass

    def publish(self, name, msg):
        for (name, publickey, callback) in self.users[name][:]:
            try:
                callback.message(name, msg)
            except Pyro4.errors.ConnectionClosedError:
                if (name, publickey, callback) in self.users[name]:
                    self.users[name].remove((name, publickey, callback))
                    print('Removed dead listener %s %s %s' % (name, publickey, callback))


Pyro4.Daemon.serveSimple({
    Survey: "survey.server"
})