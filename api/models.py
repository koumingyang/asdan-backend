 # -*- coding: utf-8 -*-


from django.db import models

# Create your models here.
class CompetitionCount(models.Model):
    name = models.CharField(max_length=30)
    count = models.IntegerField()

class TeamCount(models.Model):
    name = models.CharField(max_length=30)
    count = models.IntegerField()

class AccountCount(models.Model):
    name = models.CharField(max_length=30)
    count = models.IntegerField()

class MachineCount(models.Model):
    name = models.CharField(max_length=30)
    count = models.IntegerField()

class InformationCount(models.Model):
    name = models.CharField(max_length=30)
    count = models.IntegerField()

class AdminAccountModel(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

class MachineModel(models.Model):
    number = models.IntegerField(null=True)
    material = models.IntegerField(null=True)
    rest = models.IntegerField(null=True)
    lock = models.IntegerField(null=True)
    teamNumber = models.IntegerField(null=True)

class AccountModel(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    nickname = models.CharField(max_length=30, null=True)
    number = models.IntegerField(null=True)
    teamNumber = models.IntegerField(null=True)
    ready = models.IntegerField(null=True)

class TeamModel(models.Model):
    name = models.CharField(max_length=30)
    teamNumber = models.IntegerField(null=True)
    number = models.IntegerField(null=True)
    competitionNumber = models.IntegerField(null=True)
    peopleCount = models.IntegerField(null=True)
    materialRed = models.IntegerField(null=True)
    materialGreen = models.IntegerField(null=True)
    materialBlue = models.IntegerField(null=True)
    money = models.IntegerField(null=True)
    rank = models.IntegerField(null=True)
    houses = models.IntegerField(null=True)
    ready = models.IntegerField(null=True)
    UPmessage = models.IntegerField(null=True)

class CompetitionModel(models.Model):
    name = models.CharField(max_length=30)
    date = models.CharField(max_length=30)
    number = models.IntegerField(null=True)
    peopleCount = models.IntegerField(null=True)
    peopleCreated = models.IntegerField(null=True)
    machineCount = models.IntegerField(null=True)
    teamCount = models.IntegerField(null=True)
    money = models.IntegerField(null=True)
    competitionState = models.IntegerField(null=True)
    turn = models.IntegerField(null=True)
    materialNeedRed = models.IntegerField(null=True)
    materialNeedGreen = models.IntegerField(null=True)
    materialNeedBlue = models.IntegerField(null=True)
    moneyNeedRed = models.IntegerField(null=True)
    moneyNeedGreen = models.IntegerField(null=True)
    moneyNeedBlue = models.IntegerField(null=True)
    machinePriceRed = models.IntegerField(null=True)
    machinePriceGreen = models.IntegerField(null=True)
    machinePriceBlue = models.IntegerField(null=True)
    UPtime = models.IntegerField(null=True)
    time = models.CharField(max_length=30)
    desc = models.CharField(max_length=30)
    initialPasswordLength = models.IntegerField(null=True)
    teams = models.ManyToManyField(TeamModel)

class Information(models.Model):
    category = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    time = models.CharField(max_length=30)
    compnum = models.IntegerField(null=True)
    team1num = models.IntegerField(null=True)
    team2num = models.IntegerField(null=True)
    dmoney = models.IntegerField(null=True)
    material = models.IntegerField(null=True)
    dmaterial = models.IntegerField(null=True)
    restmaterial1 = models.IntegerField(null=True)
    restmaterial2 = models.IntegerField(null=True)
    restmoney1 = models.IntegerField(null=True)
    restmoney2 = models.IntegerField(null=True)
    machineid = models.IntegerField(null=True)
    machinerest = models.IntegerField(null=True)
    trademachine = models.ManyToManyField(MachineModel)
    materialred = models.IntegerField(null=True)
    materialgreen = models.IntegerField(null=True)
    materialblue = models.IntegerField(null=True)
    tradetype = models.IntegerField(null=True)
    number = models.IntegerField(null=True)
