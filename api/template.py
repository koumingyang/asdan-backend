 # -*- coding: utf-8 -*-
from api import const
from api.models import *
import os
import json

def getTemplate():
    jsonList = {}
    jsonObject = {}
    jsonObject["templetname"] = u"自定义"
    jsonObject["date"] = ""
    jsonObject["teamnumber"] = 0
    jsonObject["membernumber"] = 0
    jsonObject["money"] = 0
    jsonObject["rpercent"] = 0
    jsonObject["gpercent"] = 0
    jsonObject["bpercent"] = 0
    jsonObject["redprice"] = 0
    jsonObject["greenprice"] = 0
    jsonObject["blueprice"] = 0
    jsonObject["rmachineprice"] = 0
    jsonObject["gmachineprice"] = 0
    jsonObject["bmachineprice"] = 0
    data1 = []
    data1.append(jsonObject)
    print("getTemplate")
    try:
        tempTotal = open("temp/tempTotal.temp", "r")
        while 1:
            line = tempTotal.readline()
            if not line:
                break
            tempFileName = line.split(" ")[0][:-1]
            print("FILE "+tempFileName)
            try:
                jsonObject = {}
                tempFile = open("temp/"+tempFileName, "r")
                while 1:
                    l = tempFile.readline()
                    if not l:
                        break
                    a = l.split(" ")
                    #print(a)
                    if a[0] == u"模板名称:":
                        jsonObject["templetname"] = a[1]
                    elif a[0] == u"比赛日期:":
                        jsonObject["date"] = a[1]
                    elif a[0] == u"队伍数:":
                        jsonObject["teamnumber"] = a[1]
                    elif a[0] == u"每队人数:":
                        jsonObject["membernumber"] = a[1]
                    elif a[0] == u"每队起始金钱:":
                        jsonObject["money"] = a[1]
                    elif a[0] == u"造房需要红色材料数:":
                        jsonObject["rpercent"] = a[1]
                    elif a[0] == u"造房需要绿色材料数:":
                        jsonObject["gpercent"] = a[1]
                    elif a[0] == u"造房需要蓝色材料数:":
                        jsonObject["bpercent"] = a[1]
                    elif a[0] == u"红色材料生产价格:":
                        jsonObject["redprice"] = a[1]
                    elif a[0] == u"绿色材料生产价格:":
                        jsonObject["greenprice"] = a[1]
                    elif a[0] == u"蓝色材料生产价格:":
                        jsonObject["blueprice"] = a[1]
                    elif a[0] == u"红色机器起拍价格:":
                        jsonObject["rmachineprice"] = a[1]
                    elif a[0] == u"绿色机器起拍价格:":
                        jsonObject["gmachineprice"] = a[1]
                    elif a[0] == u"蓝色机器起拍价格:":
                        jsonObject["bmachineprice"] = a[1]

                #print(jsonObject)
                data1.append(jsonObject)
                tempFile.close()
            except:
                print("load file failed")

        tempTotal.close()
        jsonList["data1"] = data1
        return jsonList
    except:
        jsonList["data1"] = data1
        return jsonList

def addTemplate(response):
    try:
        templetname = response["templetname"]
        date = response["date"]
        teamnumber = response["teamnumber"]
        membernumber = response["membernumber"]
        money = response["money"]
        rpercent = response["rpercent"]
        gpercent = response["gpercent"]
        bpercent = response["bpercent"]
        redprice = response["redprice"]
        greenprice = response["greenprice"]
        blueprice = response["blueprice"]
        rmachineprice = response["rmachineprice"]
        gmachineprice = response["gmachineprice"]
        bmachineprice = response["bmachineprice"]

        print("ADD TEMPLATE INFO OK")

        temptot = 0
        if not os.path.exists("temp"):
            os.mkdir("temp")
        createTotal = open("temp/"+"tempTotal.temp", "a+")
        createTotal.close()
        readTotal = open("temp/"+"tempTotal.temp", "r")
        while 1:
            temptot += 1
            line = readTotal.readline()
            print(line)
            if not line:
                break
        #print("model"+(str)(temptot)+".txt")
        readTotal.close()
        tempTotal = open("temp/"+"tempTotal.temp", "a+")
        tempTotal.write("model"+(str)(temptot)+".txt\n")
        tempTotal.close()

        temp = open("temp/"+"model"+(str)(temptot)+".txt", "w+")
        temp.write(u"模板名称: " + templetname + " \n")
        temp.write(u"比赛日期: " + date + " \n")
        temp.write(u"队伍数: " + (str)(teamnumber) + " \n")
        temp.write(u"每队人数: " + (str)(membernumber) + " \n")
        temp.write(u"每队起始金钱: " + (str)(money) + " \n")
        temp.write(u"造房需要红色材料数: " + (str)(rpercent) + " \n")
        temp.write(u"造房需要绿色材料数: " + (str)(gpercent) + " \n")
        temp.write(u"造房需要蓝色材料数: " + (str)(bpercent) + " \n")
        temp.write(u"红色材料生产价格: " + (str)(redprice) + " \n")
        temp.write(u"绿色材料生产价格: " + (str)(greenprice) + " \n")
        temp.write(u"蓝色材料生产价格: " + (str)(blueprice) + " \n")
        temp.write(u"红色机器起拍价格: " + (str)(rmachineprice) + " \n")
        temp.write(u"绿色机器起拍价格: " + (str)(gmachineprice) + " \n")
        temp.write(u"蓝色机器起拍价格: " + (str)(bmachineprice) + " \n")
        jsonObject = {}
        jsonObject["ok"] = "yes"
        jsonObject["gameid"] = 0
        return jsonObject

    except:
        jsonObject = {}
        jsonObject["ok"] = "no"
        jsonObject["gameid"] = 0
        return jsonObject
