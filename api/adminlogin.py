from api.models import *
from api import const
import json

def adminLogin(response):
    jsonObject = {}

    username = response["username"]
    password = response["password"]

    accList = AdminAccountModel.objects.all()
    if len(accList) == 0:
        acc1 = AdminAccountModel()
        acc1.username = "admin1"
        acc1.password = "asdfghjkl"
        acc1.save()
        acc2 = AdminAccountModel()
        acc2.username = "admin2"
        acc2.password = "asdfghjkl"
        acc2.save()
        acc3 = AdminAccountModel()
        acc3.username = "admin3"
        acc3.password = "asdfghjkl"
        acc3.save()

    accFilter = AdminAccountModel.objects.filter(username=username,password=password)
    if len(accFilter) == 0:
        jsonObject["ok"] = "no"
    else:
        jsonObject["ok"] = "yes"

    return jsonObject
