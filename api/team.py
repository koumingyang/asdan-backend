 # -*- coding: utf-8 -*-

from api.models import *
from api import const
import random
import json
try:
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    import imp
    imp.reload(sys)

def buildTeam(teamName, teamCount, initialMoney, compNumber, memberNumber, initialPasswordLength):
    teamModel = TeamModel()

    teamModel.name = teamName
    teamModel.teamNumber = teamCount
    teamModel.money = initialMoney
    teamModel.competitionNumber = compNumber

    tCountList = TeamCount.objects.filter(name="TeamCount")
    if len(tCountList) == 0:
        tCount = TeamCount(name="TeamCount", count=1)
        tCount.save()
        teamModel.number = tCount.count
    else:
        tCount = TeamCount.objects.get(name="TeamCount")
        tCount.count += 1
        tCount.save()
        teamModel.number = tCount.count

    teamModel.peopleCount = 0
    teamModel.materialRed = 0
    teamModel.materialBlue = 0
    teamModel.materialGreen = 0
    teamModel.rank = 1
    teamModel.houses = 0
    teamModel.ready = const.TEAMNOTREADY
    teamModel.UPmessage = 0

    random.seed()
    for nowUser in range(memberNumber):
        username = "C"+(str)(compNumber)+"T"+(str)(teamModel.number)+"U"+(str)(nowUser)
        password = "123456"

        #for i in range(initialPasswordLength):
        #    password += const.RANDOM_CHAR_LIST[random.randint(0, const.RANDOM_CHAR_LIST_LENGTH-1)]
        buildAccount(username, password, teamModel.number)

    teamModel.save()

def buildAccount(username, password, teamNumber):
    accModel = AccountModel()

    accModel.username = username
    accModel.nickname = username
    accModel.password = password
    accModel.teamNumber = teamNumber
    accModel.ready = const.TEAMNOTREADY

    aCountList = AccountCount.objects.filter(name="AccountCount")
    if len(aCountList) == 0:
        aCount = AccountCount(name="AccountCount", count=1)
        aCount.save()
        accModel.number = aCount.count
    else:
        aCount = AccountCount.objects.get(name="AccountCount")
        aCount.count += 1
        aCount.save()
        accModel.number = aCount.count

    accModel.save()

def getTotalResult(teamModels):
    jsonList = {}
    data1 = []
    for teamModel in teamModels:
        jsonObject = {}
        jsonObject["rank"] = teamModel.rank
        jsonObject["teamid"] = teamModel.number
        jsonObject["name"] = teamModel.name
        jsonObject["home"] = teamModel.houses
        jsonObject["money"] = teamModel.money

        allmachine = 0
        redmachine = 0
        bluemachine = 0
        greenmachine = 0
        machineModels = MachineModel.objects.filter(teamNumber=teamModel.number)
        for macModel in machineModels:
            if macModel.material == const.RED:
                redmachine += 1
            elif macModel.material == const.GREEN:
                greenmachine += 1
            elif macModel.material == const.BLUE:
                bluemachine += 1
            allmachine += 1
        jsonObject["allmachine"] = allmachine
        jsonObject["redmachine"] = redmachine
        jsonObject["greenmachine"] = greenmachine
        jsonObject["bluemachine"] = bluemachine

        data1.append(jsonObject)

    jsonList["data1"] = data1
    return jsonList

def teamRankTotal(teamModels):
    jsonList = {}
    data1 = []

    for teamModel in teamModels:
        jsonObject = {}
        jsonObject["ranking"] = teamModel.rank
        jsonObject["teamid"] = teamModel.number
        jsonObject["name"] = teamModel.name
        jsonObject["total"] = teamModel.houses
        jsonObject["money"] = teamModel.money
        data1.append(jsonObject)

    jsonList["ranking"] = data1
    return jsonList

def cmp_to_key(mycmp):
    'Convert a cmp= function into a key= function'
    class K(object):
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return K

def sortedCmp(a, b):
    if a.houses == b.houses:
        return b.money - a.money
    else:
        return b.houses - a.houses

def teamRankCalculate(teamModels, mRed, mGreen, mBlue):
    print("TeamRankCalculate")
    for teamModel in teamModels:
        teamCalculate(teamModel, mRed, mGreen, mBlue)
    teamModels = sorted(teamModels, key=cmp_to_key(sortedCmp))
    lastRank = 1
    lastHouses = 0
    lastMoney = 0
    for teamModel in teamModels:
        if teamModel.houses == lastHouses and teamModel.money == lastMoney:
            teamModel.rank = lastRank
        else:
            teamModel.rank = teamModels.index(teamModel) + 1
            lastRank = teamModel.rank
            lastMoney = teamModel.money
            lastHouses = teamModel.houses
        teamModel.save()
    return teamModels

def teamCalculate(teamModel, mRed, mGreen, mBlue):
    nowmin = -1
    #print("TeamCalculate " + (str)(teamModel.number))
    #print("Red "+(str)(mRed)+" "+(str)(teamModel.materialRed))
    #print("Green "+(str)(mGreen)+" "+(str)(teamModel.materialGreen))
    #print("Blue "+(str)(mBlue)+" "+(str)(teamModel.materialBlue))
    if not mRed == 0:
        nowmin = min(nowmin, teamModel.materialRed / mRed)
        if nowmin == -1:
            nowmin = teamModel.materialRed / mRed
    if not mGreen == 0:
        nowmin = min(nowmin, teamModel.materialGreen / mGreen)
        if nowmin == -1:
            nowmin = teamModel.materialRed / mGreen
    if not mBlue == 0:
        nowmin = min(nowmin, teamModel.materialBlue / mBlue)
        if nowmin == -1:
            nowmin = teamModel.materialRed / mBlue
    if nowmin == -1:
        teamModel.houses = 0
    else:
        teamModel.houses = (int)(nowmin)
    print("TeamCalculate " + (str)(teamModel.number) + " " + (str)(teamModel.houses))
    teamModel.save()

def outputTeamModel(teamModel):
    print("--------------a team--------------------")
    print("Name: "+ teamModel.name)
    print("Number: "+ (str)(teamModel.number))
    print("Money: "+ (str)(teamModel.money))
    print("Materials: ")
    print("RED:  "+ (str)(teamModel.materialRed))
    print("GREEN:  "+ (str)(teamModel.materialGreen))
    print("BLUE:  "+ (str)(teamModel.materialBlue))
    print("rank: "+ (str)(teamModel.rank))
    print("competitionNumber: "+ (str)(teamModel.competitionNumber))
    print("houses: "+ (str)(teamModel.houses))
    print("ready: "+ (str)(teamModel.ready))
    print("-----------------------------------------------")
