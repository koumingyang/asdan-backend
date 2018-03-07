from api.models import *
from api import const
from api import views
from api import consumers

try:
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    import imp
    imp.reload(sys)

def getTradeMessageJson(info, state):
    jsonObject = {}
    if state == const.TRADE_TEAM1:
        jsonObject["obj"] = info.team2num
    else:
        jsonObject["obj"] = info.team1num
    jsonObject["money"] = info.dmoney
    jsonObject["material"] = [info.materialred, info.materialgreen, info.materialblue]
    jsonObject["number"] = info.number

    macModels = info.trademachine.all()
    machineList = []
    for machine in macModels:
        jsonObjectMac = {}
        jsonObjectMac["id"] = machine.number
        jsonObjectMac["material"] = machine.material
        jsonObjectMac["residue"] = machine.rest
        jsonObjectMac["lock"] = machine.lock
        machineList.append(jsonObjectMac)
    jsonObject["machine"] = machineList
    jsonObject["Type"] = info.tradetype * 2 + state

    return jsonObject

def message(response):
    teamid = response["teamid"]
    gameid = response["gameid"]
    teamModel = TeamModel.objects.get(number = teamid)

    dealMessage = []

    infoModels = Information.objects.filter(category="trade",compnum=gameid,team1num=teamid)
    for info in infoModels[::-1]:
        jsonObject = getTradeMessageJson(info, const.TRADE_TEAM1)
        dealMessage.append(jsonObject)
    infoModels = Information.objects.filter(category="trade",compnum=gameid,team2num=teamid)
    for info in infoModels[::-1]:
        jsonObject = getTradeMessageJson(info, const.TRADE_TEAM2)
        dealMessage.append(jsonObject)
    jsonList = {}
    jsonList["UPmessage"] = teamModel.UPmessage
    jsonList["dealMessage"] = dealMessage
    return jsonList


def sell(response):
    print("Trade try to sell")
    jsonObject = {}

    materialRed = 0
    materialGreen = 0
    materialBlue = 0
    money = 0

    try:
        teamid = (int)(response["teamid"])
        gameid = (int)(response["gameid"])
        userid = (int)(response["userid"])
        objteamid = (int)(response["obj"])
        money = (int)(response["money"])
        print((str)(teamid) +" "+ (str)(gameid) +" "+ (str)(userid) +" "+ (str)(objteamid) +" "+ (str)(money))
        machineIdList = response["machine"]
        materialRed = (int)(response["material"][const.RED])
        materialGreen = (int)(response["material"][const.GREEN])
        materialBlue = (int)(response["material"][const.BLUE])

        print(machineIdList)

        teamModel = TeamModel.objects.get(number = teamid)
        objTeamModel = TeamModel.objects.get(number = objteamid)
        compModel = CompetitionModel.objects.get(number = gameid)
    except:
        jsonObject["message"] = "failed"
        print("number illegal")
        return jsonObject

    jsonObject = {}
    if teamModel.materialRed < materialRed or teamModel.materialGreen < materialGreen or teamModel.materialBlue < materialBlue:
        jsonObject["message"] = "failed"
        print("material not enough")
        return jsonObject
    if money <= 0 or materialRed < 0 or materialGreen < 0 or materialBlue < 0:
        jsonObject["message"] = "failed"
        print("number illegal : not positive")
        return jsonObject
    for macId in machineIdList:
        try:
            macId = (int)(macId)
            macModel = MachineModel.objects.get(number = macId)
            if (not macModel.teamNumber == teamid):
                print("machine wrong")
                jsonObject["message"] = "failed"
                return jsonObject
        except:
            print("machine illegal")
            jsonObject["message"] = "failed"
            return jsonObject

    info = Information()
    info.category = "trade"
    info.compnum = gameid
    info.team1num = teamid
    info.team2num = objteamid
    info.materialred = materialRed
    info.materialgreen = materialGreen
    info.materialblue = materialBlue
    info.tradetype = const.TRADE_INPROGRESS
    info.dmoney = money
    iCountList = InformationCount.objects.filter(name="InformationCount")
    if len(iCountList) == 0:
        iCount = InformationCount(name="InformationCount", count=1)
        iCount.save()
        info.number = iCount.count
    else:
        iCount = InformationCount.objects.get(name="InformationCount")
        iCount.count += 1
        iCount.save()
        info.number = iCount.count
    info.save()

    for macId in machineIdList:
        print(macId)
        macId = (int)(macId)
        macModel = MachineModel.objects.get(number = macId)
        if not macModel.lock == const.MACHINE_LOCKED:
            macModel.lock = const.MACHINE_LOCKED
            macModel.save()
            info.trademachine.add(macModel)

            print("trade machine "+(str)(macModel.teamNumber)+" "+(str)(teamModel.number))

    machineList = info.trademachine.all()
    for macModel in machineList:
        print(macModel.number)

    info.save()

    jsonObject["message"] = "succeed"
    jsonObject["number"] = info.number

    teamModel.UPmessage = teamModel.UPmessage + 1
    objTeamModel.UPmessage = objTeamModel.UPmessage + 1
    teamModel.save()
    objTeamModel.save()

    consumers.sendWebSocketTeamMessage(info.compnum, info.team1num, userid)
    consumers.sendWebSocketTeamMessage(info.compnum, info.team2num, userid)
    consumers.sendWebSocketTradeMessage(info.compnum, info.team1num, info.team2num)
    return jsonObject

def cancel(response):
    number = (int)(response["Number"])
    userid = (int)(response["userid"])

    jsonObject = {}
    info = Information.objects.get(number=number)
    if not info.tradetype == const.TRADE_INPROGRESS:
        jsonObject["go"] = "no"
        return jsonObject

    machineList = info.trademachine.all()
    for macModel in machineList:
        macModel.lock = const.MACHINE_UNLOCKED
        macModel.save()

    info.tradetype = const.TRADE_FAILED
    #info.tradestate = const.TRADE_FINISHED
    info.save()
    jsonObject["go"] = "yes"

    teamModel = TeamModel.objects.get(number = info.team1num)
    objTeamModel = TeamModel.objects.get(number = info.team2num)
    teamModel.UPmessage = teamModel.UPmessage + 1
    objTeamModel.UPmessage = objTeamModel.UPmessage + 1
    teamModel.save()
    objTeamModel.save()

    consumers.sendWebSocketTeamMessage(info.compnum, info.team1num, userid)
    consumers.sendWebSocketTeamMessage(info.compnum, info.team2num, userid)
    consumers.sendWebSocketTradeMessage(info.compnum, info.team1num, info.team2num)
    return jsonObject

def accept(response):
    number = (int)(response["Number"])
    userid = (int)(response["userid"])
    info = Information.objects.get(number=number)
    gameid = info.compnum
    teamid = info.team2num
    objteamid = info.team1num
    teamModel = TeamModel.objects.get(number = teamid)
    objTeamModel = TeamModel.objects.get(number = objteamid)
    compModel = CompetitionModel.objects.get(number = gameid)

    #team1(objTeamModel): sell   team2(teamModel): buy

    jsonObject = {}
    if not info.tradetype == const.TRADE_INPROGRESS:
        jsonObject["go"] = "no"
        return jsonObject

    if info.dmoney > teamModel.money or info.materialred > objTeamModel.materialRed or info.materialgreen > objTeamModel.materialGreen or info.materialblue > objTeamModel.materialBlue:
        jsonObject["go"] = "no"
        return jsonObject

    machineList = info.trademachine.all()
    for macModel in machineList:
        if (not macModel.teamNumber == objteamid):
            jsonObject["go"] = "no"
            return jsonObject

    info.tradetype = const.TRADE_COMPLETED
    info.save()

    for macModel in machineList:
        macModel.teamNumber = teamid
        macModel.lock = const.MACHINE_UNLOCKED
        macModel.save()

    teamModel.money -= info.dmoney
    teamModel.materialRed += info.materialred
    teamModel.materialGreen += info.materialgreen
    teamModel.materialBlue += info.materialblue
    teamModel.UPmessage = teamModel.UPmessage + 1
    teamModel.save()

    objTeamModel.money += info.dmoney
    objTeamModel.materialRed -= info.materialred
    objTeamModel.materialGreen -= info.materialgreen
    objTeamModel.materialBlue -= info.materialblue
    objTeamModel.UPmessage = objTeamModel.UPmessage + 1
    objTeamModel.save()

    consumers.sendWebSocketModifyRank(gameid, teamid)
    consumers.sendWebSocketTeamMessage(info.compnum, info.team1num, userid)
    consumers.sendWebSocketTeamMessage(info.compnum, info.team2num, userid)
    consumers.sendWebSocketTradeMessage(gameid, teamid, objteamid)

    jsonObject["go"] = "yes"
    return jsonObject



def adminInfo(infoList):
    jsonList = {}
    data1 = []
    for info in infoList[::-1]:
        if info.category == "trade":
            jsonObject = {}
            jsonObject["number"] = info.number
            jsonObject["partA"] = info.team1num
            jsonObject["partB"] = info.team2num
            jsonObject["money"] = info.dmoney
            if info.tradetype == const.TRADE_INPROGRESS:
                jsonObject["operate"] = "waiting"
            elif info.tradetype == const.TRADE_COMPLETED:
                jsonObject["operate"] = "completed"
            elif info.tradetype == const.TRADE_FAILED:
                jsonObject["operate"] = "failed"
            data1.append(jsonObject)
    jsonList["data1"] = data1
    return jsonList
