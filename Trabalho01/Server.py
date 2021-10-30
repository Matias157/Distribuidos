import Pyro4
import datetime
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class Survey(object):
    def __init__(self):
        self.surveys = {}
        self.users = {}

    def getSurveys(self):
        return list(self.surveys.keys())

    def getUsers(self):
        return list(self.users.keys())

    def registerUser(self, name, publickey, callback):
        if not name or not publickey:
            raise ValueError("Invalid user or public key")
        if name not in self.users:
            print('Registering new user %s' % name)
            self.users[name] = []
        self.users[name].append((name, publickey, callback))
        return [name for (name, publickey, callback) in self.users[name]]

    def registerSurvey(self, survey, name, place, times, deadline):
        if not survey or not name or not place or not times or not deadline:
            raise ValueError("invalid survey")
        if survey not in self.surveys:
            print('Creating new survey %s' % survey)
            self.surveys[survey] = []
        self.surveys[survey].append((survey, name, place, times, deadline))
        for user in self.users:
            self.publish(user, "------------------\nNew survey created!\n" + "Survey: " + survey + "\nCreator: " + name + "\nPlace: " + place + "\nProposed times: " + str(times) + "\nDeadline: " + deadline + "\n------------------")
        return [survey for (survey, name, place, times, deadline) in self.surveys[survey]]

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