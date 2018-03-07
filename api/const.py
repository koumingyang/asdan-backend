 # -*- coding: utf-8 -*-

RED = 0
GREEN = 1
BLUE = 2
COLOR_NOT_EXIST = -1

RANDOM_CHAR_LIST = "1234567890QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm"
RANDOM_CHAR_LIST_LENGTH = 62

NOTSTARTED = 0
UNDERWAY = 1
INTRADE = 2
RESULTING = 3
OVER = 4

TEAMNOTREADY = 0
TEAMREADY = 1
TEAMUNDERWAY = 2
TEAMOVER = 3

TRADE_TEAM1 = 0
TRADE_TEAM2 = 1

TRADE_INPROGRESS = 0
TRADE_COMPLETED = 1
TRADE_FAILED = 2

TRADE_TEAM1_INPROGRESS = TRADE_INPROGRESS * 2 + TRADE_TEAM1
TRADE_TEAM2_INPROGRESS = TRADE_INPROGRESS * 2 + TRADE_TEAM2
TRADE_TEAM1_COMPLETED = TRADE_COMPLETED * 2 + TRADE_TEAM1
TRADE_TEAM2_COMPLETED = TRADE_COMPLETED * 2 + TRADE_TEAM2
TRADE_TEAM1_FAILED = TRADE_FAILED * 2 + TRADE_TEAM1
TRADE_TEAM2_FAILED = TRADE_FAILED * 2 + TRADE_TEAM2

MACHINE_UNLOCKED = 0
MACHINE_LOCKED = 1

TEAM_READY_STATE = [u"未准备", u"已准备", u"进行中", u"已结束"]

MATCH_STATE = [u"未开始", u"进行中——拍卖环节", u"进行中——生产交易环节", u"进行中——结算环节", u"已结束"]

MATERIAL = ["red", "green", "blue"]

WEB_SOCKET = 0
GAME_ID = 1
TEAM_ID = 2
USER_ID = 3

TOKEN_NEXT = 0
TOKEN_AUCTION_LIST = 1
TOKEN_RANK_LIST = 2
TOKEN_TRADE_LIST = 3
TOKEN_TIME = 4
TOKEN_TEAM_INFO = 5

MAXN = 2147483647