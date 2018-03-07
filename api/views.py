 # -*- coding: utf-8 -*-

from django.http import JsonResponse
import json
from dwebsocket.decorators import accept_websocket,require_websocket
from django.http import HttpResponse
import threading
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from api import team
from api import auction
from api import trade
from api import produce
from api import consumers
from api.consumers import *
from api.adminlogin import *
from api.template import *
from api.build import *
from api.models import *
from api.competition import *

import time
try:
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    import imp
    imp.reload(sys)
# Create your views here.

clients = []

'''
-------------------------------------------admin api------------------------------------------
'''

@csrf_exempt
def build(req):
    print('build')
    print(req.body)
    response = json.loads(req.body.decode("utf-8")) #get json from forward end
    #deal with json data
    jsonObject = {}

    if response["type"] == "game":
        compModel = buildCompetition(response)
        jsonObject["gameid"] = compModel.number
        jsonObject["ok"] = "yes"
    elif response["type"] == "requiremodel":
        jsonObject = getTemplate()
    elif response["type"] == "addmodel":
        jsonObject = addTemplate(response)

    #print(jsonObject)
    return JsonResponse(jsonObject)  #return json

def overview(req):
    #print("overview")

    compList = CompetitionModel.objects.all()

    jsonList = {}
    data1 = []
    for compModel in compList:
        #compModelOutput(compModel)
        jsonObject = {}
        jsonObject["number"] = compModel.number
        jsonObject["name"] = compModel.name
        jsonObject["time"] = compModel.date
        jsonObject["operate"] = ""
        jsonObject["status"] = const.MATCH_STATE[compModel.competitionState]
        data1.append(jsonObject)
    jsonList["data1"] = data1
    #print(jsonList)

    return JsonResponse(jsonList)

@csrf_exempt
def main(req):
    print('main')
    print(req.body)

    response = json.loads(req.body.decode("utf-8")) #get json from forward end

    comp_id = (int)(response["gameid"])
    turn = (int)(response["turn"])
    unit = (int)(response["unit"])
    compModel = CompetitionModel.objects.get(number=comp_id)
    compModel.turn = turn
    compModel.competitionState = unit
    compModel.save()

    jsonObject = {}
    #print(compModel.competitionState)
    jsonObject["state"] = compModel.competitionState
    jsonObject["round"] = compModel.turn
    jsonObject["token"] = const.TOKEN_NEXT

    print(jsonObject)

    consumers.sendWebSocketMessage(comp_id, jsonObject)
    #try:

    #except:
    #    print("TURN OR STATE ILLEGAL")

    json_data = {}
    return JsonResponse(json_data)

@csrf_exempt
def ready(req):
    #print('ready')
    #print(req.body)
    response = json.loads(req.body.decode("utf-8")) #get json from forward end
    comp_id = (int)(response["gameid"])

    jsonList = {}
    data1 = []
    teamList = TeamModel.objects.filter(competitionNumber=comp_id)
    for teamModel in teamList:
        accountList = AccountModel.objects.filter(teamNumber=teamModel.number)
        s = ""
        p = ""
        for account in accountList:
            s += account.username + "<br/>"
            p += account.password + "<br/>"
        jsonObject = {}
        jsonObject["number"] = teamModel.number
        jsonObject["name"] = teamModel.name
        jsonObject["member"] = s
        jsonObject["password"] = p
        jsonObject["status"] = const.TEAM_READY_STATE[teamModel.ready]
        data1.append(jsonObject)
    jsonList["data1"] = data1
    #print(jsonList)

    return JsonResponse(jsonList)

@csrf_exempt
def sale(req):
    print('sale')
    response = json.loads(req.body.decode("utf-8")) #get json from forward end
    json_data = {}
    try:
        comp_id = (int)(response["gameid"])
        team_id = (int)(response["teamid"])
        material = response["machine"]
        money = (int)(response["money"])
        description = response["desc"]

        if auction.auctionRecord(comp_id, team_id, material, -money, description):
            json_data["ok"] = "yes"
            infoList = Information.objects.filter(category="auction", compnum=comp_id)
            jsonObject = auction.getAuctionInfoJson(infoList)
            jsonObject["token"] = const.TOKEN_AUCTION_LIST
            consumers.sendWebSocketMessage(comp_id, jsonObject)
        else:
            json_data["ok"] = "no"
    except:
        json_data["ok"] = "no"
    return JsonResponse(json_data)

@csrf_exempt
def tradeApi(req):
    print('trade')
    response = json.loads(req.body.decode("utf-8")) #get json from forward end
    gameid = (int)(response["gameid"])
    counttime = (int)(response["time"])

    newtime = time.time() + (float)(counttime) + (float)(8*3600)

    if not counttime == 0:
        try:
            compModel = CompetitionModel.objects.get(number=gameid)
        except:
            jsonObject = {}
            jsonObject["ok"] = "no"
            return JsonResponse(jsonObject)
        compModel.UPtime = compModel.UPtime + 1
        compModel.time = (str)(newtime)
        compModel.save()
        jsonObject = {}
        jsonObject["time"] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime((float)(compModel.time)))
        jsonObject["token"] = const.TOKEN_TIME
        consumers.sendWebSocketMessage(gameid, jsonObject)

    infoList = Information.objects.filter(compnum=gameid,category="trade")
    jsonList = trade.adminInfo(infoList)

    #print(jsonList)

    return JsonResponse(jsonList)

@csrf_exempt
def result(req):
    print("result")

    response = json.loads(req.body.decode("utf-8")) #get json from forward end
    comp_id = (int)(response["gameid"])
    teamModels = TeamModel.objects.filter(competitionNumber=comp_id)
    compModel = CompetitionModel.objects.get(number=comp_id)
    teamModels = team.teamRankCalculate(teamModels, compModel.materialNeedRed, compModel.materialNeedGreen, compModel.materialNeedBlue)
    jsonList = team.getTotalResult(teamModels)
    print(jsonList)
    return JsonResponse(jsonList)

@csrf_exempt
def adminlogin(req):
    print("adminlogin")
    print(req.body)
    response = json.loads(req.body.decode("utf-8")) #get json from forward end
    jsonObject = adminLogin(response)
    print(jsonObject)
    return JsonResponse(jsonObject)

@csrf_exempt
def deletegame(req):
    print("deletegame")
    print(req.body)
    response = json.loads(req.body.decode("utf-8")) #get json from forward end
    comp_id = (int)(response["gameid"])

    jsonObject = {}
    compModel = CompetitionModel.objects.get(number=comp_id)
    if not compModel.competitionState == const.OVER:
        jsonObject["ok"] = "no"
        print(jsonObject)
        return JsonResponse(jsonObject)

    teamModels = TeamModel.objects.filter(competitionNumber=comp_id)
    for teamModel in teamModels:
        AccountModel.objects.filter(teamNumber=teamModel.number).delete()
        MachineModel.objects.filter(teamNumber=teamModel.number).delete()
    TeamModel.objects.filter(competitionNumber=comp_id).delete()
    Information.objects.filter(compnum=comp_id).delete()
    CompetitionModel.objects.filter(number=comp_id).delete()

    jsonObject["ok"] = "yes"
    print(jsonObject)
    return JsonResponse(jsonObject)

'''
-------------------------------------------user api------------------------------------------
'''

@csrf_exempt
def login(req):
    print('---------------------------login----------------------------')
    print(req.body)
    response = json.loads(req.body.decode("utf-8")) #get json from forward end
    acc_username = response["username"]
    acc_password = response["password"]

    accModels = AccountModel.objects.filter(username=acc_username)
    jsonObject = {}

    flag = 0
    for mod in accModels:
        if mod.password == acc_password:
            flag = 1
            accModel = mod
            break

    if flag == 0:
        jsonObject["go"] = "no"
        return JsonResponse(jsonObject)

    teamModel = TeamModel.objects.get(number=accModel.teamNumber)
    compModel = CompetitionModel.objects.get(number=teamModel.competitionNumber)
    compState = compModel.competitionState

    if not (compState == const.NOTSTARTED or compState == const.UNDERWAY or compState == const.INTRADE or compState == const.RESULTING):
        jsonObject["go"] = "no"
        return JsonResponse(jsonObject)

    accModel.ready = const.TEAMREADY
    if teamModel.ready == const.TEAMNOTREADY:
        teamModel.ready = const.TEAMREADY

    accModel.save()
    teamModel.save()

    jsonObject = getTeamInformation(True, accModel, teamModel, compModel)
    jsonObject["go"] = "yes"
    jsonObject["gameid"] = teamModel.competitionNumber
    jsonObject["teamid"] = accModel.teamNumber
    jsonObject["userid"] = accModel.number
    jsonObject["nickname"] = accModel.nickname
    jsonObject["state"] = compState
    jsonObject["round"] = compModel.turn

    print(jsonObject)

    return JsonResponse(jsonObject)

@csrf_exempt
def userSetting(req):
    response = json.loads(req.body.decode("utf-8")) #get json from forward end
    jsonObject = {}
    try:
        userid = (int)(response["userid"])
        teamid = (int)(response["teamid"])
        gameid = (int)(response["gameid"])
        newNickname = response["nickname"]
        newPassword = response["newPassWord"]
        accModel = AccountModel.objects.get(number=userid)

        if len(newNickname) < 30 and len(newPassword) < 30 and newPassword.isalnum():
            jsonObject["go"] = "yes"
            accModel.nickname = newNickname
            accModel.password = newPassword
            accModel.save()
        else:
            jsonObject["go"] = "no"
    except:
        jsonObject["go"] = "no"

    return JsonResponse(jsonObject)

@csrf_exempt
def check(req):
    print('check')
    print(req.body)
    response = json.loads(req.body.decode("utf-8")) #get json from forward end
    try:
        userid = (int)(response["userid"])
        teamid = (int)(response["teamid"])
        gameid = (int)(response["gameid"])
        #print(userid, teamid, gameid)
        succeed, acc, team, comp = otherTeamBuild(userid, teamid, gameid)
        jsonObject = getTeamInformation(succeed, acc, team, comp)
    except:
        jsonObject = {}
        jsonObject["message"] = "failed"
    return JsonResponse(jsonObject)

@csrf_exempt
def next(req):
    print('next')
    print(req.body)
    response = json.loads(req.body.decode("utf-8")) #get json from forward end
    try:
        gameid = (int)(response["gameid"])
        #print(gameid)
        compModel = CompetitionModel.objects.get(number=gameid)
        jsonObject = {}
        #print(compModel.competitionState)
        jsonObject["state"] = compModel.competitionState
        jsonObject["round"] = compModel.turn
        jsonObject["token"] = const.TOKEN_NEXT
        print(jsonObject)
    except:
        jsonObject = {}
    return JsonResponse(jsonObject)

@csrf_exempt
def dealInit(req):
    print('dealInit')
    print(req.body)
    response = json.loads(req.body.decode("utf-8")) #get json from forward end
    try:
        gameid = (int)(response["gameid"])
        teamid = (int)(response["teamid"])
        compModel = CompetitionModel.objects.get(number=gameid)
        teamModel = TeamModel.objects.get(number=teamid)
        materialList = [compModel.moneyNeedRed, compModel.moneyNeedGreen, compModel.moneyNeedBlue]
        jsonObject = {}
        jsonObject["state"] = compModel.competitionState
        jsonObject["round"] = compModel.turn
        try:
            jsonObject["endtime"] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime((float)(compModel.time)))
        except:
            jsonObject["endtime"] = ""
        jsonObject["price"] = materialList
        jsonObject["UPtime"] = compModel.UPtime
        jsonObject["teamList"] = getOtherTeamList(teamModel, compModel)
        print(jsonObject)
    except:
        jsonObject = {}
    return JsonResponse(jsonObject)

@csrf_exempt
def dealMessage(req):
    print('dealMessage')
    print(req.body)
    response = json.loads(req.body.decode("utf-8")) #get json from forward end
    jsonObject = trade.message(response)
    return JsonResponse(jsonObject)

@csrf_exempt
def dealOut(req):
    print('dealOut')
    print(req.body)
    response = json.loads(req.body.decode("utf-8")) #get json from forward end
    jsonObject = trade.sell(response)
    return JsonResponse(jsonObject)

@csrf_exempt
def retDeal(req):
    print('retDeal')
    print(req.body)
    response = json.loads(req.body.decode("utf-8")) #get json from forward end
    jsonObject = {}
    if response["Type"] == 0:
        jsonObject = trade.cancel(response)
    elif response["Type"] == 1:
        jsonObject = trade.accept(response)
    return JsonResponse(jsonObject)

@csrf_exempt
def account(req):
    print('account')
    print(req.body)
    response = json.loads(req.body.decode("utf-8")) #get json from forward end
    try:
        gameid = (int)(response["gameid"])
        compModel = CompetitionModel.objects.get(number=gameid)
        jsonObject = {}
        jsonObject["state"] = compModel.competitionState
        jsonObject["round"] = compModel.turn
    except:
        jsonObject = {}
    return JsonResponse(jsonObject)

@csrf_exempt
def auctionApi(req):
    print("auction")
    print(req.body)
    response = json.loads(req.body.decode("utf-8")) #get json from forward end
    try:
        userid = (int)(response["userid"])
        teamid = (int)(response["teamid"])
        gameid = (int)(response["gameid"])
        succeed, acc, team, comp = accountBuild(userid, teamid, gameid)
        jsonObject = getTeamInformation(succeed, acc, team, comp)
        print(jsonObject)
    except:
        jsonObject = {}
    return JsonResponse(jsonObject)

@csrf_exempt
def ranking(req):
    print("ranking")
    print(req.body)
    response = json.loads(req.body.decode("utf-8")) #get json from forward end
    try:
        comp_id = (int)(response["gameid"])
        teamModels = TeamModel.objects.filter(competitionNumber=comp_id)
        compModel = CompetitionModel.objects.get(number=comp_id)
        teamModels = team.teamRankCalculate(teamModels, compModel.materialNeedRed, compModel.materialNeedGreen, compModel.materialNeedBlue)
        json_data = team.teamRankTotal(teamModels)
        print(json_data)
    except:
        json_data = {}
    return JsonResponse(json_data)

@csrf_exempt
def myAuctionList(req):
    print("myAuctionList")
    response = json.loads(req.body.decode("utf-8")) #get json from forward end
    try:
        userid = (int)(response["userid"])
        teamid = (int)(response["teamid"])
        gameid = (int)(response["gameid"])
        infoList = Information.objects.filter(category="auction", compnum=gameid, team1num=teamid)
        jsonObject = auction.getAuctionInfoJson(infoList)
        print(jsonObject)
    except:
        jsonObject = {}
    return JsonResponse(jsonObject)

@csrf_exempt
def AuctionList(req):
    print("AuctionList")
    response = json.loads(req.body.decode("utf-8")) #get json from forward end
    try:
        gameid = (int)(response["gameid"])
        infoList = Information.objects.filter(category="auction", compnum=gameid)
        jsonObject = auction.getAuctionInfoJson(infoList)
        print(jsonObject)
    except:
        jsonObject = {}
    return JsonResponse(jsonObject)

@csrf_exempt
def myProduceList(req):
    print("myProduceList")
    response = json.loads(req.body.decode("utf-8")) #get json from forward end
    userid = (int)(response["userid"])
    teamid = (int)(response["teamid"])
    gameid = (int)(response["gameid"])
    infoList = Information.objects.filter(category="produce", compnum=gameid, team1num=teamid)
    jsonObject = produce.getProduceInfoJson(infoList)
    '''
    try:
        userid = (int)(response["userid"])
        teamid = (int)(response["teamid"])
        gameid = (int)(response["gameid"])
        infoList = Information.objects.filter(category="produce", compnum=gameid, team1num=teamid)
        jsonObject = produce.getProduceInfoJson(infoList)
    except:
        jsonObject = {}
    '''
    return JsonResponse(jsonObject)

@csrf_exempt
def produceMaterial(req):
    print("------------produce-----------")
    print(req.body)
    response = json.loads(req.body.decode("utf-8")) #get json from forward end
    try:
        userid = (int)(response["userid"])
        teamid = (int)(response["teamid"])
        gameid = (int)(response["gameid"])
        #print(userid)
        machineid = (int)(response["id"])
        #print(machineid)
        totalMaterial = (int)(response["total"])
        #print(totalMaterial)
        totalMoney = (int)(response["totalMoney"])
        #print(totalMoney)

        jsonObject = produce.produceBuild(userid, teamid, gameid, machineid, totalMaterial, totalMoney)
        consumers.sendWebSocketTeamMessage(gameid, teamid, userid)
        consumers.sendWebSocketModifyRank(gameid, teamid)
    except:
        jsonObject = {}
    return JsonResponse(jsonObject)
