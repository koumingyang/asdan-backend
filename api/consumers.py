import json
from channels import Group
from channels.sessions import channel_session
from api.models import *
from api.build import *
from api import team
from api import trade
from api import produce

@channel_session
def ws_connect(message):
    print("Websocket connect")
    message.reply_channel.send({"text":json.dumps({"go": "ok"})})

@channel_session
def ws_receive(message):
    print("Websocket receive")
    print (message.content['text'])

    response = message.content['text']
    idList = response.split(',')
    print(idList)

    print((int)(idList[0]))
    gameid = idList[0]     #gameid
    teamid = idList[1]     #teamid
    userid = idList[2]     #userid

    groupStr = "game-" + (str)(gameid) + "-team-" + (str)(teamid)
    print(groupStr)
    Group(groupStr).add(message.reply_channel)

@channel_session
def ws_disconnect(message):
    print("Websocket disconnect")
    message.reply_channel.send({"text":json.dumps({"go": "ok"})})


def sendWebSocketMessage(gameid, jsonObject):
    print("sendWebSocketMessage")
    string = json.dumps(jsonObject)
    print(string)

    teamModels = TeamModel.objects.filter(competitionNumber=gameid)
    for teamModel in teamModels:
        groupStr = "game-" + (str)(gameid) + "-team-" + (str)(teamModel.number)
        print(groupStr)
        Group(groupStr).send({"text": string,})

def sendWebSocketModifyRank(gameid, teamid):
    teamModels = TeamModel.objects.filter(competitionNumber=gameid)
    compModel = CompetitionModel.objects.get(number=gameid)
    teamModels = team.teamRankCalculate(teamModels, compModel.materialNeedRed, compModel.materialNeedGreen, compModel.materialNeedBlue)
    json_data = team.teamRankTotal(teamModels)
    json_data["token"] = const.TOKEN_RANK_LIST
    sendWebSocketMessage(gameid, json_data)

def sendWebSocketOneTeamMessage(gameid, teamid, jsonObject):
    print("sendOneTeamWebSocketMessage")
    string = json.dumps(jsonObject)
    print(string)

    teamModels = TeamModel.objects.filter(competitionNumber=gameid, number=teamid)
    for teamModel in teamModels:
        groupStr = "game-" + (str)(gameid) + "-team-" + (str)(teamModel.number)
        print(groupStr)
        Group(groupStr).send({"text": string,})

def sendWebSocketOneTeamTradeMessage(gameid, teamid):
    response = {}
    response["gameid"] = gameid
    response["teamid"] = teamid
    jsonObject = trade.message(response)
    jsonObject["token"] = const.TOKEN_TRADE_LIST
    sendWebSocketOneTeamMessage(gameid, teamid, jsonObject)

def sendWebSocketTradeMessage(gameid, team1id, team2id):
    sendWebSocketOneTeamTradeMessage(gameid, team1id)
    sendWebSocketOneTeamTradeMessage(gameid, team2id)

def sendWebSocketTeamMessage(gameid, teamid, userid):

    #print(userid, teamid, gameid)
    succeed, acc, team, comp = otherTeamBuild(userid, teamid, gameid)
    if succeed == False:
        succeed, acc, team, comp = accountBuild(userid, teamid, gameid)
    jsonObject = getTeamInformation(succeed, acc, team, comp)
    jsonObject["token"] = const.TOKEN_TEAM_INFO
    sendWebSocketOneTeamMessage(gameid, teamid, jsonObject)
