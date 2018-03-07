 # -*- coding: utf-8 -*-

from api import const
from api.models import *
from api.team import *
import json

def buildCompetition(settings):
    compModel = CompetitionModel()

    compModel.peopleCreated = 0
    compModel.machineCount = 0
    compModel.teamCount = 0
    compModel.money = 0
    compModel.competitionState = const.NOTSTARTED
    compModel.turn = 0
    compModel.UPtime = 0

    try:
        compModel.machinePriceRed = (int)(settings["rmachineprice"])
    except:
        compModel.machinePriceRed = 0
    try:
        compModel.machinePriceGreen = (int)(settings["gmachineprice"])
    except:
        compModel.machinePriceGreen = 0
    try:
        compModel.machinePriceBlue = (int)(settings["bmachineprice"])
    except:
        compModel.machinePriceBlue = 0
    try:
        compModel.materialNeedRed = (int)(settings["rpercent"])
    except:
        compModel.materialNeedRed = 0
    try:
        compModel.materialNeedGreen = (int)(settings["gpercent"])
    except:
        compModel.materialNeedGreen = 0
    try:
        compModel.materialNeedBlue = (int)(settings["bpercent"])
    except:
        compModel.materialNeedBlue = 0
    try:
        compModel.moneyNeedRed = (int)(settings["redprice"])
    except:
        compModel.moneyNeedRed = 0
    try:
        compModel.moneyNeedGreen = (int)(settings["greenprice"])
    except:
        compModel.moneyNeedGreen = 0
    try:
        compModel.moneyNeedBlue = (int)(settings["blueprice"])
    except:
        compModel.moneyNeedBlue = 0
    try:
        compModel.money = (int)(settings["money"])
    except:
        compModel.money = 0
    try:
        compModel.peopleCount = (int)(settings["teamnumber"]) * (int)(settings["membernumber"])
    except:
        compModel.peopleCount = 0

    compModel.initialPasswordLength = 20
    try:
        compModel.name = settings["name"]
    except:
        compModel.name = "Unnamed Competition"
    try:
        compModel.date = settings["date"]
    except:
        compModel.date = "2000-00-00"
    compModel.time = "00:00:00.000"
    try:
        compModel.desc = settings["desc"]
    except:
        compModel.desc = ""

    cCountList = CompetitionCount.objects.filter(name="CompetitionCount")
    if len(cCountList) == 0:
        cCount = CompetitionCount(name="CompetitionCount", count=1)
        cCount.save()
        compModel.number = cCount.count
    else:
        cCount = CompetitionCount.objects.get(name="CompetitionCount")
        cCount.count += 1
        cCount.save()
        compModel.number = cCount.count

    try:
        teamNumber = (int)(settings["teamnumber"])
    except:
        teamNumber = 0
    try:
        memberNumber = (int)(settings["membernumber"])
    except:
        memberNumber = 0

    for i in range(teamNumber):
        teamName = "Team" + (str)(i+1)
        compModel.teamCount += 1

        buildTeam(teamName, compModel.teamCount, compModel.money, compModel.number, memberNumber, compModel.initialPasswordLength)

    compModel.save()
    #compModelOutput(compModel)

    return compModel

def compModelOutput(compModel):
    print("--------------a competition--------------------")
    print("Name: "+ compModel.name)
    print("Date: "+ compModel.date)
    print("Number: "+ (str)(compModel.number))
    print("initialMoney: "+ (str)(compModel.money))
    print("Time: "+ compModel.time)
    print("TeamCount: "+ (str)(compModel.teamCount))
    print("desc: "+ compModel.desc)
    print("competitionState: "+ (str)(compModel.competitionState))
    print("-----------------------------------------------")
