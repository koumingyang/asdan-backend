
def fillFakeDataForBuildCompetition():
    response_data = fillFakeDataForModelAndCompetition()
    response_data["type"] = "game"
    response_data["name"] = "NewGame"
    return response_data

def fillFakeDataForBuildTemplate():
    response_data = fillFakeDataForModelAndCompetition()
    response_data["type"] = "addmodel"
    response_data["templetname"] = "NewModel"
    return response_data

def fillFakeDataForModelAndCompetition():
    response_data = {}
    response_data["date"] = "2000-00-00"
    response_data["teamnumber"] = 4
    response_data["membernumber"] = 3
    response_data["money"] = 2000
    response_data["rpercent"] = 2
    response_data["gpercent"] = 1
    response_data["bpercent"] = 3
    response_data["redprice"] = 10
    response_data["greenprice"] = 20
    response_data["blueprice"] = 30
    response_data["rmachineprice"] = 100
    response_data["gmachineprice"] = 300
    response_data["bmachineprice"] = 200
    return response_data
