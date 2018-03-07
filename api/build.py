from django.http import JsonResponse
import json
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from api.competition import *
from api import team

def getTeamInformation(succeed, accModel, teamModel, compModel):
    team.teamCalculate(teamModel, compModel.materialNeedRed, compModel.materialNeedGreen, compModel.materialNeedBlue)

    jsonObject = {}
    if succeed == False:
        jsonObject["message"] = "failed"
        return jsonObject

    jsonObject["round"] = compModel.turn
    jsonObject["state"] = compModel.competitionState
    jsonObject["name"] = teamModel.name
    jsonObject["money"] = teamModel.money
    jsonObject["message"] = "succeed"
    jsonObject["house"] = teamModel.houses

    accModels = AccountModel.objects.filter(teamNumber=teamModel.number)
    teammate = []
    for account in accModels:
        jsonObjectAcc = {}
        jsonObjectAcc["name"] = account.nickname
        teammate.append(jsonObjectAcc)
    jsonObject["teamMates"] = teammate

    macModels = MachineModel.objects.filter(teamNumber=teamModel.number)
    machineList = []
    for machine in macModels:
        jsonObjectMac = {}
        jsonObjectMac["id"] = machine.number
        jsonObjectMac["material"] = machine.material
        jsonObjectMac["residue"] = machine.rest
        jsonObjectMac["lock"] = machine.lock
        machineList.append(jsonObjectMac)
    jsonObject["machine"] = machineList

    materialList = [teamModel.materialRed, teamModel.materialGreen, teamModel.materialBlue]
    jsonObject["material"] = materialList

    jsonObject["otherteam"], jsonObject["otherTeamInfo"] = getOtherTeamList(teamModel, compModel)
    #print(jsonObject)
    return jsonObject

def getOtherTeamList(teamModel, compModel):
    teamModels = TeamModel.objects.filter(competitionNumber=compModel.number)
    otherTeam = []
    otherTeamInfo = []
    for oneTeam in teamModels:
        if not oneTeam.number == teamModel.number:
            otherTeam.append(oneTeam.number)
            jsonObject = {}
            jsonObject["name"] = oneTeam.name
            jsonObject["id"] = oneTeam.number
            otherTeamInfo.append(jsonObject)
    return otherTeam, otherTeamInfo


def accountBuild(userid, teamid, gameid):
    accModels = AccountModel.objects.filter(number = userid)
    teamModels = TeamModel.objects.filter(number = teamid)
    compModels = CompetitionModel.objects.filter(number = gameid)

    if len(accModels) == 0 or len(teamModels) == 0 or len(compModels) == 0:
        return False, AccountModel(), TeamModel(), CompetitionModel()

    accModel = accModels[0]
    teamModel = teamModels[0]
    compModel = compModels[0]

    if not (accModel.teamNumber == teamid and teamModel.competitionNumber == gameid):
        return False, AccountModel(), TeamModel(), CompetitionModel()

    return True, accModel, teamModel, compModel

def otherTeamBuild(userid, teamid, gameid):
    accModels = AccountModel.objects.filter(number = userid)
    teamModels = TeamModel.objects.filter(number = teamid)
    compModels = CompetitionModel.objects.filter(number = gameid)

    if len(accModels) == 0 or len(teamModels) == 0 or len(compModels) == 0:
        return False, AccountModel(), TeamModel(), CompetitionModel()

    accModel = accModels[0]
    teamModel = teamModels[0]
    compModel = compModels[0]

    accTeamModels = TeamModel.objects.filter(number = accModel.teamNumber)
    if len(accTeamModels) == 0 or accModel.teamNumber == teamid:
        return False, AccountModel(), TeamModel(), CompetitionModel()

    accTeamModel = accTeamModels[0]

    if not (accTeamModel.competitionNumber == gameid and teamModel.competitionNumber == gameid):
        return False, AccountModel(), TeamModel(), CompetitionModel()

    return True, accModel, teamModel, compModel
