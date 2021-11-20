# ------------------------------
# Trabalho 2 - Sistemas Distribuídos
# Autores: 
# Alexandre Herrero matias
# Matheus Fonseca Alexandre de Oliveira
# Professor: Ana Cristina Vendramin
# Projeto: Doodle
# ------------------------------

# Libraries

from flask import Flask, request, jsonify
from flask_sse import sse
import datetime
import threading

app = Flask(__name__)
app.config["REDIS_URL"] = "redis://localhost"
app.register_blueprint(sse, url_prefix="/stream")

SURVEYS =   {
                "Meeting":  {
                                "name": "Meeting", 
                                "attendants":   [
                                                    "Alexandre"
                                                ], 
                                "place": "ExxonMobil", 
                                "proposed_times":   [ 
                                                        {
                                                            "2021-12-01 12:00:00": 0
                                                        }, 
                                                        {
                                                            "2021-12-02 12:00:00": 0
                                                        }, 
                                                        {
                                                            "2021-12-03 12:00:00": 0
                                                        }
                                                    ], 
                                "deadline": "2021-12-25 12:00:00",
                                "state": "Ongoing"
                            }
            }
USERS = {
            "Alexandre":    {
                                "name": "Alexandre"
                            }
        }

@app.route("/survey", methods=["GET"])
def getSurveys():
    all = request.args.get("all")
    if all == "True":
        return jsonify(list(SURVEYS.keys()))
    return_surveys = []
    for survey in SURVEYS:
        if SURVEYS[survey]["state"] == "Ongoing":
            return_surveys.append(survey)
    return jsonify(return_surveys)

@app.route("/user", methods=["GET"])
def getUsers():
    return jsonify(list(USERS.keys()))

@app.route("/survey/info", methods=["GET"])
def getSurveysInfo():
    return_string = ""
    for survey in SURVEYS:
        if SURVEYS[survey]["state"] == "Ongoing":
                return_string += "------------------\nSurvey: " + SURVEYS[survey]["name"] + "\nCreator: " + SURVEYS[survey]["attendants"][0] + "\nPlace: " + SURVEYS[survey]["place"] + "\nProposed times: " + str(SURVEYS[survey]["proposed_times"]) + "\nDeadline: " + SURVEYS[survey]["deadline"] + "\n------------------\n"
    return return_string

@app.route("/survey", methods=["POST"])
def postSurvey():
    request_data = request.get_json()
    if not request_data["name"] or not request_data["creator"] or not request_data["place"] or not request_data["proposed_times"] or not request_data["deadline"]:
        return "Bad Request!"
    if request_data["name"] not in SURVEYS:
        SURVEYS[request_data["name"]] = {"name": request_data["name"], "attendants": [request_data["creator"]], "place": request_data["place"], "proposed_times":[], "deadline": request_data["deadline"], "state": "Ongoing"}
        for time in request_data["proposed_times"]:
            SURVEYS[request_data["name"]]["proposed_times"].append({time: 0})
        sse.publish("\n------------------\nNew survey created!\n" + "Survey: " + request_data["name"] + "\nCreator: " + request_data["creator"] + "\nPlace: " + request_data["place"] + "\nProposed times: " + str(request_data["proposed_times"]) + "\nDeadline: " + request_data["deadline"] + "\n------------------", channel=request_data["name"])
    return SURVEYS[request_data["name"]]

@app.route("/user", methods=["POST"])
def postUser():
    request_data = request.get_json()
    if not request_data["name"]:
        return "Bad Request!"
    if request_data["name"] not in USERS:
        USERS[request_data["name"]] = {"name": request_data["name"]}
    return USERS[request_data["name"]]

@app.route("/survey/vote", methods=["GET"])
def getVotes():
    survey = request.args.get("survey")
    proposed_time = request.args.get("proposed_time")
    for time in SURVEYS[survey]["proposed_times"]:
        try:
            vote = time[proposed_time]
        except:
            pass
    return str(vote)

@app.route("/survey/vote", methods=["POST"])
def voteSurvey():
    request_data = request.get_json()
    if not request_data["name"] or not request_data["survey"] or not request_data["times"]:
        return "Bad Request!"
    if request_data["survey"] not in SURVEYS:
        return "Invalid Survey!"
    if request_data["name"] in SURVEYS[request_data["survey"]]["attendants"]:
        return "User Already on Survey!"
    if SURVEYS[request_data["survey"]]["state"] != "Ongoing":
        return "Survey Already Finished!"
    SURVEYS[request_data["survey"]]["attendants"].append(request_data["name"])
    for time_r in request_data["times"]:
        for time_s in SURVEYS[request_data["survey"]]["proposed_times"]:
            try:
                time_s[time_r] += 1
            except:
                pass
    return "Vote has been Successfully Computed!"

if __name__ == '__main__':
    app.run(debug=True)