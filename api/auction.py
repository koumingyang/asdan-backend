from api.models import *
from api import const

def auctionRecord(compNumber, teamNumber, material, dMoney, description):
    teamModel = TeamModel.objects.get(number=teamNumber)
    compModel = CompetitionModel.objects.get(number=compNumber)

    if material == const.MATERIAL[const.RED]:
        material = const.RED
    elif material == const.MATERIAL[const.GREEN]:
        material = const.GREEN
    elif material == const.MATERIAL[const.BLUE]:
        material = const.BLUE
    else:
        material = const.COLOR_NOT_EXIST

    print("AuctionRecord "+" Game "+(str)(compNumber)+" Team "+(str)(teamNumber)+" material "+(str)(material)+" dMoney "+(str)(dMoney))

    if (material == const.RED or material == const.BLUE or material == const.GREEN) and teamModel.money + dMoney >= 0:
        macModel = MachineModel()
        macModel.material = material
        macModel.rest = 3
        macModel.teamNumber = teamNumber
        macModel.lock = const.MACHINE_UNLOCKED
        mCountList = MachineCount.objects.filter(name="MachineCount")
        if len(mCountList) == 0:
            mCount = MachineCount(name="MachineCount", count=1)
            mCount.save()
            macModel.number = mCount.count
        else:
            mCount = MachineCount.objects.get(name="MachineCount")
            mCount.count += 1
            mCount.save()
            macModel.number = mCount.count
        macModel.save()

        teamModel.money += dMoney
        teamModel.save()

        compModel.machineCount += 1
        compModel.save()

        info = Information()
        info.category = "auction"
        info.compnum = compNumber
        info.team1num = teamNumber
        info.material = material
        info.description = description
        info.dmoney = dMoney
        info.restmoney1 = teamModel.money
        info.save()

        print("Auction Record Succeed")

        return True
    else:
        print("Auction Record Failed")
        return False

def getAuctionInfoJson(infoList):
    jsonObject = {}
    infoJsonList = []
    for info in infoList[::-1]:
        infoJson = {}
        infoJson["teamid"] = info.team1num
        infoJson["material"] = info.material
        infoJson["description"] = info.description
        infoJson["dmoney"] = -info.dmoney
        infoJson["restmoney"] = info.restmoney1
        infoJsonList.append(infoJson)
    jsonObject["infolist"] = infoJsonList
    return jsonObject
