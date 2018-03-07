from api.models import *
from api import const

def produceBuild(userid, teamid, gameid, machineid, totalMaterial, totalMoney):
    print("try to produce")
    jsonObject = {}
    accModels = AccountModel.objects.filter(number = userid)
    teamModels = TeamModel.objects.filter(number = teamid)
    compModels = CompetitionModel.objects.filter(number = gameid)
    macModels = MachineModel.objects.filter(number = machineid)

    if len(accModels) == 0 or len(teamModels) == 0 or len(compModels) == 0 or len(macModels) == 0:
        print("model not exist")
        jsonObject["do"] = "no"
        return jsonObject

    accModel = accModels[0]
    teamModel = teamModels[0]
    compModel = compModels[0]
    macModel = macModels[0]

    if not (accModel.teamNumber == teamid and teamModel.competitionNumber == gameid and macModel.teamNumber == teamid):
        print("model not match")
        jsonObject["do"] = "no"
        return jsonObject

    if macModel.lock == const.MACHINE_LOCKED:
        print("machine locked")
        jsonObject["do"] = "no"
        return jsonObject

    moneyNeedList = []
    moneyNeedList.append(compModel.moneyNeedRed)
    moneyNeedList.append(compModel.moneyNeedGreen)
    moneyNeedList.append(compModel.moneyNeedBlue)

    if (not (totalMaterial * moneyNeedList[macModel.material] == totalMoney)) or teamModel.money < totalMoney or macModel.rest == 0:
        print("money not match")
        jsonObject["do"] = "no"
        return jsonObject

    macModel.rest -= 1
    teamModel.money -= totalMoney
    if macModel.material == const.RED:
        teamModel.materialRed += totalMaterial
    elif macModel.material == const.GREEN:
        teamModel.materialGreen += totalMaterial
    elif macModel.material == const.BLUE:
        teamModel.materialBlue += totalMaterial
    teamModel.save()
    macModel.save()

    info = Information()
    info.category = "produce"
    info.compnum = gameid
    info.team1num = teamid
    info.dmoney = totalMoney
    info.material = macModel.material
    info.machineid = macModel.number
    info.machinerest = macModel.rest
    info.restmoney1 = teamModel.money
    info.dmaterial = totalMaterial
    info.save()

    jsonObject["do"] = "yes"
    return jsonObject

def getProduceInfoJson(infoList):
    print("getProduceInfoJson")
    jsonObject = {}
    infoJsonList = []
    for info in infoList[::-1]:
        print(info.team1num)
        infoJson = {}
        infoJson["teamid"] = info.team1num
        mat = {}
        mat["Type"] = info.material
        mat["total"] = info.dmaterial
        infoJson["material"] = mat
        infoJson["money"] = info.dmoney
        infoJson["restmoney"] = info.restmoney1
        infoJsonList.append(infoJson)
    jsonObject["infolist"] = infoJsonList
    print(jsonObject)
    return jsonObject
