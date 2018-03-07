 # -*- coding: utf-8 -*-

from django.test import TestCase, Client
from api import views
from api import const
from api import competition
from api import team
from api.models import *
from api.fillfakedata import *
import json
try:
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    import imp
    imp.reload(sys)

# Create your tests here.
class testAdminLogin(TestCase):
    def testLoginSucceed(self):
        c = Client()
        response_data = {}
        response_data["username"] = "admin1"
        response_data["password"] = "asdfghjkl"
        req = c.post("/api/adminin",json.dumps(response_data), content_type="application/json")
        response = json.loads(req.content.decode("utf-8"))
        self.assertEqual(response["ok"], "yes")
    def testLoginFailed(self):
        c = Client()
        response_data = {}
        response_data["username"] = "admin1"
        response_data["password"] = "aeargeragl"
        req = c.post("/api/adminin",json.dumps(response_data), content_type="application/json")
        response = json.loads(req.content.decode("utf-8"))
        self.assertEqual(response["ok"], "no")

class testBuild(TestCase):
    def testBuildEmptyCompetition(self):
        c = Client()
        response_data = {}
        response_data["type"] = "game"
        req = c.post("/api/build",json.dumps(response_data), content_type="application/json")
        response = json.loads(req.content.decode("utf-8"))
        self.assertEqual(response["ok"], "yes")
        self.assertEqual(response["gameid"], 1)
        compModel = CompetitionModel.objects.get(number=1)
        competition.compModelOutput(compModel)
        response_data = fillFakeDataForBuildCompetition()
        req = c.post("/api/build",json.dumps(response_data), content_type="application/json")
        response = json.loads(req.content.decode("utf-8"))
        self.assertEqual(response["ok"], "yes")
        self.assertEqual(response["gameid"], 2)

    def testRequireModel(self):
        c = Client()
        response_data = {}
        response_data["type"] = "requiremodel"
        req = c.post("/api/build",json.dumps(response_data), content_type="application/json")
        response = json.loads(req.content.decode("utf-8"))
    def testAddModel(self):
        c = Client()
        response_data = fillFakeDataForBuildTemplate()
        req = c.post("/api/build",json.dumps(response_data), content_type="application/json")
        response = json.loads(req.content.decode("utf-8"))
        #self.assertEqual(response["ok"], "yes")
    def testFailedAddModel(self):
        c = Client()
        response_data = {}
        response_data["type"] = "addmodel"
        response_data["templetname"] = "NewModel"
        req = c.post("/api/build",json.dumps(response_data), content_type="application/json")
        response = json.loads(req.content.decode("utf-8"))
        self.assertEqual(response["ok"], "no")

class testIllegalMain(TestCase):
    def testIllegalString(self):
        c = Client()
        response_data = {}
        response_data["gameid"] = 1
        response_data["teamid"] = 4
        response_data["machine"] = const.MATERIAL[const.BLUE]
        response_data["money"] = "sanbaiyuan"
        response_data["desc"] = "brfh"
        req = c.post("/api/sale",json.dumps(response_data), content_type="application/json")
        response = json.loads(req.content.decode("utf-8"))
        self.assertEqual(response["ok"], "no")

class testIllegalAuction(TestCase):
    def testIllegalString(self):
        c = Client()
        response_data = {}
        response_data["gameid"] = 1
        response_data["turn"] = 1
        response_data["unit"] = "illegalstate"
        try:
            req = c.post("/api/main",json.dumps(response_data), content_type="application/json")
        except:
            print("illegal auction main except")

class testIllegalUserSetting(TestCase):
    def testIllegalString(self):
        c = Client()
        response_data = {}
        response_data["userid"] = "feifade"
        req = c.post("/api/userSetting",json.dumps(response_data), content_type="application/json")

class testIllegalCheck(TestCase):
    def testIllegalCheckString(self):
        c = Client()
        response_data = {}
        response_data["gameid"] = "feifade"
        response_data["teamid"] = 1
        response_data["userid"] = 1
        req = c.post("/api/check",json.dumps(response_data), content_type="application/json")
        response = json.loads(req.content.decode("utf-8"))
        print(response)

    def testIllegalCheckNoCompetition(self):
        c = Client()
        response_data = {}
        response_data["gameid"] = 3
        response_data["teamid"] = 1
        response_data["userid"] = 1
        req = c.post("/api/check",json.dumps(response_data), content_type="application/json")
        response = json.loads(req.content.decode("utf-8"))
        print(response)

    def testIllegalCheckSameTeam(self):
        c = Client()
        response_data = fillFakeDataForBuildCompetition()
        req = c.post("/api/build",json.dumps(response_data), content_type="application/json")
        response = json.loads(req.content.decode("utf-8"))
        self.assertEqual(response["ok"], "yes")
        self.assertEqual(response["gameid"], 1)
        response_data = fillFakeDataForBuildCompetition()
        req = c.post("/api/build",json.dumps(response_data), content_type="application/json")
        response_data = {}
        response_data["gameid"] = 1
        response_data["teamid"] = 1
        response_data["userid"] = 1
        req = c.post("/api/check",json.dumps(response_data), content_type="application/json")
        response = json.loads(req.content.decode("utf-8"))
        print(response)
        response_data = {}
        response_data["gameid"] = 2
        response_data["teamid"] = 2
        response_data["userid"] = 1
        req = c.post("/api/check",json.dumps(response_data), content_type="application/json")
        response = json.loads(req.content.decode("utf-8"))
        print(response)

class testCompetitionLogic(TestCase):
    def testWholeCompetition(self):
        c = Client()

        #build
        response_data = fillFakeDataForBuildCompetition()
        req = c.post("/api/build",json.dumps(response_data), content_type="application/json")
        response = json.loads(req.content.decode("utf-8"))
        self.assertEqual(response["ok"], "yes")
        self.assertEqual(response["gameid"], 1)
        req = c.get("/api/overview")
        response = json.loads(req.content.decode("utf-8"))
        self.assertEqual(len(response["data1"]), 1)

        #user login
        response_data = {}
        response_data["username"] = "C1T1U0"
        response_data["password"] = "123456"
        req = c.post("/api/login",json.dumps(response_data), content_type="application/json")
        response = json.loads(req.content.decode("utf-8"))
        self.assertEqual(response["go"], "yes")

        response_data = {}
        response_data["username"] = "C1T1U0"
        response_data["password"] = "111111"
        req = c.post("/api/login",json.dumps(response_data), content_type="application/json")
        response = json.loads(req.content.decode("utf-8"))
        self.assertEqual(response["go"], "no")


        response_data = {}
        response_data["userid"] = 1
        response_data["teamid"] = 1
        response_data["gameid"] = 1
        response_data["nickname"] = "setrb"
        response_data["newPassWord"] = "111111"
        req = c.post("/api/userSetting",json.dumps(response_data), content_type="application/json")
        response = json.loads(req.content.decode("utf-8"))
        self.assertEqual(response["go"], "yes")

        response_data = {}
        response_data["userid"] = 1
        response_data["teamid"] = 1
        response_data["gameid"] = 1
        response_data["nickname"] = "setrb"
        response_data["newPassWord"] = "!!!!!!"
        req = c.post("/api/userSetting",json.dumps(response_data), content_type="application/json")
        response = json.loads(req.content.decode("utf-8"))
        self.assertEqual(response["go"], "no")

        response_data = {}
        response_data["username"] = "C1T1U0"
        response_data["password"] = "111111"
        req = c.post("/api/login",json.dumps(response_data), content_type="application/json")
        response = json.loads(req.content.decode("utf-8"))
        self.assertEqual(response["go"], "yes")

        #init
        response_data = {}
        response_data["gameid"] = 1
        response_data["turn"] = 1
        response_data["unit"] = const.UNDERWAY
        req = c.post("/api/ready",json.dumps(response_data), content_type="application/json")
        response = json.loads(req.content.decode("utf-8"))
        #print(response)
        self.assertEqual(len(response["data1"]), 4)

        try:
            req = c.post("/api/main",json.dumps(response_data), content_type="application/json")
        except:
            print("main except")

        accModels = AccountModel.objects.filter(teamNumber=1)
        accModel = accModels[0]
        print(accModel.username + " " + (str)(accModel.number))

        #auction
        response_data = {}
        response_data["gameid"] = 1
        req = c.post("/api/account",json.dumps(response_data), content_type="application/json")
        response = json.loads(req.content.decode("utf-8"))
        self.assertEqual(response["state"], const.UNDERWAY)

        print("Here is line 244------------------------------------------------------------")
        response_data = {}
        response_data["gameid"] = 1
        response_data["teamid"] = 1
        response_data["machine"] = const.MATERIAL[const.RED]
        response_data["money"] = 100
        response_data["desc"] = "sretbh"
        req = c.post("/api/sale",json.dumps(response_data), content_type="application/json")
        response = json.loads(req.content.decode("utf-8"))
        print(response)

        response_data = {}
        response_data["gameid"] = 1
        response_data["teamid"] = 2
        response_data["machine"] = const.MATERIAL[const.GREEN]
        response_data["money"] = 200
        response_data["desc"] = "rwefh"
        req = c.post("/api/sale",json.dumps(response_data), content_type="application/json")
        response = json.loads(req.content.decode("utf-8"))
        print(response)

        response_data = {}
        response_data["gameid"] = 1
        response_data["teamid"] = 4
        response_data["machine"] = const.MATERIAL[const.BLUE]
        response_data["money"] = 300
        response_data["desc"] = "brfh"
        req = c.post("/api/sale",json.dumps(response_data), content_type="application/json")
        response = json.loads(req.content.decode("utf-8"))
        print(response)

        response_data = {}
        response_data["gameid"] = 1
        response_data["teamid"] = 3
        response_data["machine"] = "fake machine"
        response_data["money"] = 200
        response_data["desc"] = "rwefh"
        req = c.post("/api/sale",json.dumps(response_data), content_type="application/json")
        response = json.loads(req.content.decode("utf-8"))
        self.assertEqual(response["ok"], "no")

        #auction all
        response_data = {}
        response_data["gameid"] = 1
        response_data["teamid"] = 1
        response_data["userid"] = 1
        req = c.post("/api/auction",json.dumps(response_data), content_type="application/json")
        response = json.loads(req.content.decode("utf-8"))
        print(response)

        response_data = {}
        response_data["gameid"] = 1
        response_data["teamid"] = 1
        response_data["userid"] = 4
        req = c.post("/api/auction",json.dumps(response_data), content_type="application/json")
        response = json.loads(req.content.decode("utf-8"))
        print(response)

        response_data = {}
        response_data["gameid"] = 1
        response_data["teamid"] = 100
        response_data["userid"] = 4
        req = c.post("/api/auction",json.dumps(response_data), content_type="application/json")
        response = json.loads(req.content.decode("utf-8"))
        print(response)

        #auction list
        response_data = {}
        response_data["gameid"] = 1
        response_data["teamid"] = 1
        response_data["userid"] = 1
        req = c.post("/api/myAuctionList",json.dumps(response_data), content_type="application/json")
        response = json.loads(req.content.decode("utf-8"))
        self.assertEqual(len(response["infolist"]), 1)

        response_data = {}
        response_data["gameid"] = 1
        req = c.post("/api/AuctionList",json.dumps(response_data), content_type="application/json")
        response = json.loads(req.content.decode("utf-8"))
        self.assertEqual(len(response["infolist"]), 3)

        #auction machinelock
        response_data = {}
        response_data["gameid"] = 1
        response_data["teamid"] = 2
        response_data["userid"] = 1
        req = c.post("/api/check",json.dumps(response_data), content_type="application/json")
        response = json.loads(req.content.decode("utf-8"))
        print(response)

        response_data = {}
        response_data["gameid"] = 1
        req = c.post("/api/next",json.dumps(response_data), content_type="application/json")
        response = json.loads(req.content.decode("utf-8"))
        self.assertEqual(response["state"], const.UNDERWAY)

        #trade
        response_data = {}
        response_data["gameid"] = 1
        response_data["turn"] = 1
        response_data["unit"] = const.INTRADE
        req = c.post("/api/ready",json.dumps(response_data), content_type="application/json")
        response = json.loads(req.content.decode("utf-8"))

        response_data = {}
        response_data["gameid"] = 1
        response_data["time"] = "1800"
        try:
            req = c.post("/api/trade",json.dumps(response_data), content_type="application/json")
        except:
            print("tradestart except")
        response = json.loads(req.content.decode("utf-8"))
        print(response)
        self.assertEqual(len(response["data1"]), 4)

        response_data = {}
        response_data["gameid"] = 1
        response_data["teamid"] = 2
        response_data["userid"] = 4
        response_data["obj"] = 1
        response_data["money"] = 500
        response_data["machine"] = [2]
        response_data["material"] = [0, 0, 0]
        try:
            req = c.post("/api/dealOut",json.dumps(response_data), content_type="application/json")
        except:
            print("send trade except")
        response = json.loads(req.content.decode("utf-8"))
        #self.assertEqual(response["message"], "succeed")
        #self.assertEqual(response["number"], 1)

        #produce(illegal)
        response_data = {}
        response_data["userid"] = 4
        response_data["gameid"] = 1
        response_data["teamid"] = 2
        response_data["id"] = 2
        response_data["total"] = 20
        response_data["totalMoney"] = 400
        req = c.post("/api/produce",json.dumps(response_data), content_type="application/json")
        response = json.loads(req.content.decode("utf-8"))
        #self.assertEqual(response["do"], "no")

        response_data = {}
        response_data["userid"] = 1
        response_data["gameid"] = 1
        response_data["teamid"] = 1
        response_data["id"] = 1
        response_data["total"] = 30
        response_data["totalMoney"] = 400
        req = c.post("/api/produce",json.dumps(response_data), content_type="application/json")
        response = json.loads(req.content.decode("utf-8"))
        #self.assertEqual(response["do"], "no")

        response_data = {}
        response_data["userid"] = 4
        response_data["gameid"] = 1
        response_data["teamid"] = 2
        response_data["id"] = 1
        response_data["total"] = 30
        response_data["totalMoney"] = 300
        req = c.post("/api/produce",json.dumps(response_data), content_type="application/json")
        response = json.loads(req.content.decode("utf-8"))
        #self.assertEqual(response["do"], "no")

        response_data = {}
        response_data["userid"] = 4
        response_data["gameid"] = 1
        response_data["teamid"] = 2
        response_data["id"] = 100
        response_data["total"] = 20
        response_data["totalMoney"] = 400
        req = c.post("/api/produce",json.dumps(response_data), content_type="application/json")
        response = json.loads(req.content.decode("utf-8"))
        #self.assertEqual(response["do"], "no")

        #trade_accept
        response_data = {}
        response_data["Number"] = 1
        response_data["userid"] = 1
        response_data["Type"] = 1
        try:
            req = c.post("/api/retDeal",json.dumps(response_data), content_type="application/json")
        except:
            print("deal except")
        response = json.loads(req.content.decode("utf-8"))
        #self.assertEqual(response["go"], "yes")

        response_data = {}
        response_data["userid"] = 1
        response_data["gameid"] = 1
        response_data["teamid"] = 1
        response_data["id"] = 2
        response_data["total"] = 20
        response_data["totalMoney"] = 400
        req = c.post("/api/produce",json.dumps(response_data), content_type="application/json")
        response = json.loads(req.content.decode("utf-8"))
        #self.assertEqual(response["do"], "yes")

        response_data = {}
        response_data["userid"] = 1
        response_data["gameid"] = 1
        response_data["teamid"] = 1
        response_data["id"] = 1
        response_data["total"] = 10
        response_data["totalMoney"] = 100
        req = c.post("/api/produce",json.dumps(response_data), content_type="application/json")
        response = json.loads(req.content.decode("utf-8"))
        #self.assertEqual(response["do"], "yes")

        response_data = {}
        response_data["userid"] = 11
        response_data["gameid"] = 1
        response_data["teamid"] = 4
        response_data["id"] = 3
        response_data["total"] = 30
        response_data["totalMoney"] = 900
        req = c.post("/api/produce",json.dumps(response_data), content_type="application/json")
        response = json.loads(req.content.decode("utf-8"))
        #self.assertEqual(response["do"], "yes")

        response_data = {}
        response_data["gameid"] = 1
        response_data["teamid"] = 1
        response_data["userid"] = 1
        req = c.post("/api/myProduceList",json.dumps(response_data), content_type="application/json")
        response = json.loads(req.content.decode("utf-8"))
        self.assertEqual(len(response["infolist"]), 2)

        #illegal or successful trade
        response_data = {}
        response_data["gameid"] = 1
        response_data["teamid"] = 4
        response_data["userid"] = 11
        response_data["obj"] = 1
        response_data["money"] = 700
        response_data["machine"] = [3]
        response_data["material"] = [0, 0, 10]
        try:
            req = c.post("/api/dealOut",json.dumps(response_data), content_type="application/json")
        except:
            print("send trade except")
        response = json.loads(req.content.decode("utf-8"))
        ##self.assertEqual(response["message"], "succeed")
        #self.assertEqual(response["number"], 2)

        response_data = {}
        response_data["Number"] = 2
        response_data["Type"] = 1
        response_data["userid"] = 1
        try:
            req = c.post("/api/retDeal",json.dumps(response_data), content_type="application/json")
        except:
            print("deal except")
        response = json.loads(req.content.decode("utf-8"))
        #self.assertEqual(response["go"], "yes")

        response_data = {}
        response_data["Number"] = 2
        response_data["Type"] = 1
        response_data["userid"] = 1
        try:
            req = c.post("/api/retDeal",json.dumps(response_data), content_type="application/json")
        except:
            print("deal except")
        response = json.loads(req.content.decode("utf-8"))
        #self.assertEqual(response["go"], "no")

        response_data = {}
        response_data["gameid"] = 1
        response_data["teamid"] = 1
        response_data["userid"] = 1
        response_data["obj"] = 3
        response_data["money"] = 700
        response_data["machine"] = []
        response_data["material"] = [0, 0, 10]
        try:
            req = c.post("/api/dealOut",json.dumps(response_data), content_type="application/json")
        except:
            print("send trade except")
        response = json.loads(req.content.decode("utf-8"))
        #self.assertEqual(response["message"], "succeed")
        #self.assertEqual(response["number"], 3)

        response_data = {}
        response_data["Number"] = 3
        response_data["Type"] = 0
        response_data["userid"] = 7
        try:
            req = c.post("/api/retDeal",json.dumps(response_data), content_type="application/json")
        except:
            print("deal except")
        response = json.loads(req.content.decode("utf-8"))
        #self.assertEqual(response["go"], "yes")

        response_data = {}
        response_data["Number"] = 3
        response_data["Type"] = 0
        response_data["userid"] = 7
        try:
            req = c.post("/api/retDeal",json.dumps(response_data), content_type="application/json")
        except:
            print("deal except")
        response = json.loads(req.content.decode("utf-8"))
        #self.assertEqual(response["go"], "no")

        response_data = {}
        response_data["gameid"] = 1
        response_data["teamid"] = 1
        response_data["userid"] = 1
        req = c.post("/api/auction",json.dumps(response_data), content_type="application/json")
        response = json.loads(req.content.decode("utf-8"))
        print(response)

        response_data = {}
        response_data["gameid"] = 1
        response_data["time"] = "600"
        try:
            req = c.post("/api/trade",json.dumps(response_data), content_type="application/json")
        except:
            print("trade api except line 556-----------------------------")
        response = json.loads(req.content.decode("utf-8"))
        print(response)
        #self.assertEqual(len(response["data1"]), 3)

        response_data = {}
        response_data["gameid"] = 1
        response_data["teamid"] = 1
        req = c.post("/api/dealInit",json.dumps(response_data), content_type="application/json")
        response = json.loads(req.content.decode("utf-8"))
        print(response)

        response_data = {}
        response_data["gameid"] = 1
        response_data["teamid"] = 2
        response_data["userid"] = 4
        req = c.post("/api/dealMessage",json.dumps(response_data), content_type="application/json")
        response = json.loads(req.content.decode("utf-8"))
        print(response)
        self.assertEqual(len(response["dealMessage"]), 1)

        response_data = {}
        response_data["gameid"] = 1
        response_data["teamid"] = 1
        response_data["userid"] = 1
        req = c.post("/api/dealMessage",json.dumps(response_data), content_type="application/json")
        response = json.loads(req.content.decode("utf-8"))
        print(response)
        self.assertEqual(len(response["dealMessage"]), 3)

        #illegal trade
        response_data = {}
        response_data["gameid"] = "illegal"
        response_data["teamid"] = 2
        response_data["userid"] = 4

        response_data["obj"] = 3
        response_data["money"] = 500
        response_data["machine"] = []
        response_data["material"] = [0, 0, 0]
        try:
            req = c.post("/api/dealOut",json.dumps(response_data), content_type="application/json")
        except:
            print("send trade except")
        response = json.loads(req.content.decode("utf-8"))
        self.assertEqual(response["message"], "failed")

        response_data = {}
        response_data["gameid"] = 1
        response_data["teamid"] = 1
        response_data["userid"] = 1
        response_data["obj"] = 3
        response_data["money"] = 500
        response_data["machine"] = []
        response_data["material"] = [1000, 0, 0]
        try:
            req = c.post("/api/dealOut",json.dumps(response_data), content_type="application/json")
        except:
            print("send trade except")
        response = json.loads(req.content.decode("utf-8"))
        self.assertEqual(response["message"], "failed")

        response_data = {}
        response_data["gameid"] = 1
        response_data["teamid"] = 1
        response_data["userid"] = 1
        response_data["obj"] = 3
        response_data["money"] = 100000
        response_data["machine"] = [2]
        response_data["material"] = [0, 0, 0]
        try:
            req = c.post("/api/dealOut",json.dumps(response_data), content_type="application/json")
        except:
            print("send trade except")
        response = json.loads(req.content.decode("utf-8"))
        self.assertEqual(response["message"], "failed")

        response_data = {}
        response_data["gameid"] = 1
        response_data["teamid"] = 4
        response_data["userid"] = 11
        response_data["obj"] = 1
        response_data["money"] = 10
        response_data["machine"] = ["illegal"]
        response_data["material"] = [0, 0, 0]
        try:
            req = c.post("/api/dealOut",json.dumps(response_data), content_type="application/json")
        except:
            print("send trade except")
        response = json.loads(req.content.decode("utf-8"))
        self.assertEqual(response["message"], "failed")

        response_data = {}
        response_data["gameid"] = 1
        response_data["teamid"] = 1
        response_data["userid"] = 1
        response_data["obj"] = 4
        response_data["money"] = 10
        response_data["machine"] = [1]
        response_data["material"] = [0, 0, 0]
        try:
            req = c.post("/api/dealOut",json.dumps(response_data), content_type="application/json")
        except:
            print("send trade except")
        response = json.loads(req.content.decode("utf-8"))
        #self.assertEqual(response["message"], "succeed")

        response_data = {}
        response_data["Number"] = 4
        response_data["Type"] = 0
        response_data["userid"] = 11
        try:
            req = c.post("/api/retDeal",json.dumps(response_data), content_type="application/json")
        except:
            print("deal except")
        response = json.loads(req.content.decode("utf-8"))
        #self.assertEqual(response["go"], "yes")

        response_data = {}
        response_data["gameid"] = 1
        response_data["turn"] = 1
        response_data["unit"] = const.RESULTING
        req = c.post("/api/ready",json.dumps(response_data), content_type="application/json")
        response = json.loads(req.content.decode("utf-8"))

        response_data = {}
        response_data["gameid"] = 1
        req = c.post("/api/result",json.dumps(response_data), content_type="application/json")
        response = json.loads(req.content.decode("utf-8"))

        response_data = {}
        response_data["gameid"] = 1
        req = c.post("/api/ranking",json.dumps(response_data), content_type="application/json")
        response = json.loads(req.content.decode("utf-8"))

        teamModel = TeamModel.objects.get(number=1)
        team.outputTeamModel(teamModel)
