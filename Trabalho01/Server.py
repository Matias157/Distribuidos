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
    
    # Construtor
    def __init__(self):
        # "Base de dados" dos surveys criados
        self.surveys = {}
        # "Base de dados" dos usuarios cadastrados
        self.users = {}

        # Thread para verificar se a survey foi finalizada
        self.thread_surveys = threading.Thread(target=self.notifySurvey, daemon=True)
        self.thread_surveys.start()

    # Se all for True retorna todos os surveys, caso contrario retorna apenas os surveys em andamento
    def getSurveys(self, all):
        if all == True:
            # Retorna todos os nomes dos surveys
            return list(self.surveys.keys())
        else:
            resturnSurveys = []
            for survey in self.surveys:
                for (s, n, p, t, d, state) in self.surveys[survey]:
                    # Verifica se o survey esta em andamento
                    if state == "Ongoing":
                        resturnSurveys.append(survey)
            return(resturnSurveys)

    # Retorna todos os usuarios cadastrados
    def getUsers(self):
        # Retorna todos os nomes dos usuarios
        return list(self.users.keys())

    # Retorna as informacoes de todos os surveys ativos
    def getSurveysInfo(self):
        returnString = ""
        for survey in self.surveys:
            for (s, n, p, t, d, state) in self.surveys[survey]:
                # Verifica se o survey esta em andamento
                if state == "Ongoing":
                    returnString += "------------------\nSurvey: " + s + "\nCreator: " + n[0] + "\nPlace: " + p + "\nProposed times: " + str(t) + "\nDeadline: " + d + "\n------------------\n"
        return(returnString)

    # Verifica se a chave publica 'publicKey' abre a assinatura 'signature'
    def verifySignature(self, publicKey, signature):
        # Utiliza uma mensagem dummy para testar a assinatura
        message = b"A message I want to sign"
        try:
            # Verifica se a chave abre a assinatura
            publicKey.verify(
                signature,
                message,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            # Caso positivo
            return True
        except cryptography.exceptions.InvalidSignature as e:
            # Caso negativo
            return False

    # Registra o usuario
    def registerUser(self, name, publickey, callback):
        # Verifica se os parametros foram inseridos
        if not name or not publickey:
            raise ValueError("Invalid name or public key")
        # Verifica se o usuario ja foi cadastrado anteriomente
        if name not in self.users:
            print('Registering new user %s' % name)
            self.users[name] = []
        self.users[name].append((name, publickey, callback))
        return [name for (name, publickey, callback) in self.users[name]]

    # Registra um survey
    def registerSurvey(self, survey, name, place, times, deadline):
        # Verifica se os parametros foram inseridos
        if not survey or not name or not place or not times or not deadline:
            raise ValueError("invalid info")
        # Verifica se o survey ja foi criado anteriomente
        if survey not in self.surveys:
            print('Creating new survey %s' % survey)
            self.surveys[survey] = []
        # Cria uma lista para os participantes
        names = []
        names.append(name)
        self.surveys[survey].append((survey, names, place, times, deadline, "Ongoing"))
        # Informa todos os usuarios cadastrados no sistema do novo survey que foi criado
        for user in self.users:
            self.publish(user, "\n------------------\nNew survey created!\n" + "Survey: " + survey + "\nCreator: " + name + "\nPlace: " + place + "\nProposed times: " + str(times) + "\nDeadline: " + deadline + "\n------------------")
        return [survey for (survey, name, place, times, deadline, state) in self.surveys[survey]]

    # Contabiliza votos em um survey
    def voteSurvey(self, survey, name, times):
        # Verifica se os parametros foram inseridos
        if not survey or not name or not times:
            raise ValueError("invalid vote")
        # Verifica se o survey ja foi criado anteriomente
        if survey not in self.surveys:
            raise ValueError("invalid survey")
        for (s, n, p, t, d, state) in self.surveys[survey]:
            # Verifica se o usuario ja faz parte do survey
            if name in n:
                return("user already on survey")
            # Verifica se o survey ainda esta ativo
            if state != "Ongoing":
                return("survey already finished")
        # Insere o usuario no survey
        n.append(name)
        for time in times:
            for (s, n, p, t, d, state) in self.surveys[survey]:
                # Incrementa o numero de votos para cada horario
                t[time][0] += 1
        return("Vote has been successfully computed!")

    # Retorna as informacoes a respeito dos participantes, votos e estado autual de um survey
    def consultSurvey(self, name, survey, signature):
        # Verifica se os parametros foram inseridos
        if not name or not survey or not signature:
            raise ValueError("invalid info")
        for (s, n, p, t, d, state) in self.surveys[survey]:
            # Verifica se o usuario faz parte do survey
            if name not in n:
                return("Permission denied!")
        publicKeyStr = ""
        for (n, pk, c) in self.users[name]:
            publicKeyStr = pk
        # Desserializa a string da chave publica do usuario
        pubk = serialization.load_pem_public_key(publicKeyStr.encode(), default_backend())
        returnStr = "\n------------------\nUsers that already voted:\n"
        # Verifica se a chave publica abre a assinatura informada
        if self.verifySignature(pubk, base64.b64decode(signature["data"])):
            for (s, n, p, t, d, state) in self.surveys[survey]:
                for name in n:
                    returnStr += " - " + name + "\n"
                returnStr += "Proposed times:\n"
                for time in t:
                    returnStr += " - " + time + " - votes: " + str(t[time][0]) + "\n"
                returnStr += "State of the survey:\n - " + state + "\n------------------"
            return(returnStr)
        else:
            return("Permission denied!")

    # Thead que notifica todos os participantes de um survey caso este seja finalizado
    def notifySurvey(self):
        # A thread roda sempre
        while(True):
            surveycreated = self.getSurveys(True)
            # se existe algum survey no sistema
            if surveycreated:
                for survey in self.surveys:
                    for (s, n, p, t, d, state) in self.surveys[survey]:
                        # Se o survey esta ativo
                        if state == "Ongoing":
                            names = []
                            for user in self.users:
                                for (nn, pk, c) in self.users[user]:
                                    names.append(nn)
                            surveynames = n
                            names.sort()
                            surveynames.sort()
                            # Se todas as pessoas cadastradas no sistemas fazer parte do survey ou se o horario atual e maior ou igual ao deadline do survey
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

    # Envia notificacoes para um usuario especifico
    def publish(self, name, msg):
        for (name, publickey, callback) in self.users[name][:]:
            try:
                # Utiliza a referencia de objeto remoto do usuario cadastrado (callback) para enviar a mensagem
                callback.message(name, msg)
            except Pyro4.errors.ConnectionClosedError:
                # Caso o usuario nao possa receber a mensagem este sera removido do sistema
                if (name, publickey, callback) in self.users[name]:
                    self.users[name].remove((name, publickey, callback))
                    print('Removed dead listener %s %s %s' % (name, publickey, callback))


Pyro4.Daemon.serveSimple({
    Survey: "survey.server"
})