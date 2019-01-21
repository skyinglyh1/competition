"""
Competition Game
"""
from boa.interop.Ontology.Contract import Migrate
from boa.interop.System.App import RegisterAppCall, DynamicAppCall
from boa.interop.System.Storage import GetContext, Get, Put, Delete
from boa.interop.System.Runtime import CheckWitness, GetTime, Notify, Serialize, Deserialize
from boa.interop.System.ExecutionEngine import GetExecutingScriptHash, GetScriptContainer
from boa.interop.Ontology.Native import Invoke
from boa.interop.Ontology.Runtime import GetCurrentBlockHash
from boa.builtins import ToScriptHash, concat, state, sha256
from boa.interop.System.Transaction import GetTransactionHash

"""
https://github.com/ONT-Avocados/python-template/blob/master/libs/Utils.py
"""
def Revert():
    """
    Revert the transaction. The opcodes of this function is `09f7f6f5f4f3f2f1f000f0`,
    but it will be changed to `ffffffffffffffffffffff` since opcode THROW doesn't
    work, so, revert by calling unused opcode.
    """
    raise Exception(0xF1F1F2F2F3F3F4F4)


"""
https://github.com/ONT-Avocados/python-template/blob/master/libs/SafeCheck.py
"""
def Require(condition):
    """
	If condition is not satisfied, return false
	:param condition: required condition
	:return: True or false
	"""
    if not condition:
        Revert()
    return True

def RequireScriptHash(key):
    """
    Checks the bytearray parameter is script hash or not. Script Hash
    length should be equal to 20.
    :param key: bytearray parameter to check script hash format.
    :return: True if script hash or revert the transaction.
    """
    Require(len(key) == 20)
    return True

def RequireWitness(witness):
    """
	Checks the transaction sender is equal to the witness. If not
	satisfying, revert the transaction.
	:param witness: required transaction sender
	:return: True if transaction sender or revert the transaction.
	"""
    Require(CheckWitness(witness))
    return True
"""
https://github.com/ONT-Avocados/python-template/blob/master/libs/SafeMath.py
"""

def Add(a, b):
    """
    Adds two numbers, throws on overflow.
    """
    c = a + b
    Require(c >= a)
    return c

def Sub(a, b):
    """
    Substracts two numbers, throws on overflow (i.e. if subtrahend is greater than minuend).
    :param a: operand a
    :param b: operand b
    :return: a - b if a - b > 0 or revert the transaction.
    """
    Require(a>=b)
    return a-b

def ASub(a, b):
    if a > b:
        return a - b
    if a < b:
        return b - a
    else:
        return 0

def Mul(a, b):
    """
    Multiplies two numbers, throws on overflow.
    :param a: operand a
    :param b: operand b
    :return: a - b if a - b > 0 or revert the transaction.
    """
    if a == 0:
        return 0
    c = a * b
    Require(c / a == b)
    return c

def Div(a, b):
    """
    Integer division of two numbers, truncating the quotient.
    """
    Require(b > 0)
    c = a / b
    return c

def Pwr(a, b):
    """
    a to the power of b
    :param a the base
    :param b the power value
    :return a^b
    """
    c = 0
    if a == 0:
        c = 0
    elif b == 0:
        c = 1
    else:
        i = 0
        c = 1
        while i < b:
            c = Mul(c, a)
            i = i + 1
    return c

def Sqrt(a):
    """
    Return sqrt of a
    :param a:
    :return: sqrt(a)
    """
    c = Div(Add(a, 1), 2)
    b = a
    while(c < b):
        b = c
        c = Div(Add(Div(a, c), c), 2)
    return c

ONGAddress = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02')
# the original company
Dev1 = ToScriptHash("AYqCVffRcbPkf1BVCYPJqqoiFTFmvwYKhG")
# the cooperator
Dev2 = ToScriptHash("ANTPeXCffDZCaCXxY9u2UdssB2EYpP4BMh")

Operater = ToScriptHash("AQf4Mzu1YJrhz9f3aRkkwSm9n3qhXGSh4p")

INIT_KEY = "Inited"
ContractAddress = GetExecutingScriptHash()
ONGMagnitude = 1000000000
Magnitude = 1000000000000000000000000000000


OracleContract = RegisterAppCall('ff4d2c2765346c9229201687604af4f59a0a334f', 'operation', 'args')
SelfContractAddress = GetExecutingScriptHash()

DEV_PROFIT_PREFIX = "DEV"
FEE_PERCENTAGE_KEY = "FEE"


SENTREQHASH_FORMGAME_PREFIX = "G1"
GAME_STATUS_PREFIX = 'G2'
GAME_RES_PREFIX = "G3"
GAME_DISKID_PREFIX = "G4"
GAME_BET_ENDTIME_PREFIX = "G5"

DISK_ONG_AMOUNT_PREFIX = "G6"
DISK_PLAYERS_LIST_PREFIX = "G7"
DISK_STATUS_KEY = "G8"
PLAYER_BET_PREFIX = "G9"

SENTREQHASH_SAVERES_PREFIX = "G10"

AbortSide = -1
TieSide = 0
LeftSide = 1
RightSide = 2

Dev1Percentage = 80

def Main(operation, args):
    if operation == "init":
        return init()

    return False

def init():
    RequireWitness(Operater)
    inited = Get(GetContext(), INIT_KEY)
    if not inited:
        setFeePercentage(5)

    return True

def setFeePercentage(feePercentage):
    RequireWitness(Operater)
    Require(feePercentage < 100)
    Require(feePercentage >= 0)
    Put(GetContext(), FEE_PERCENTAGE_KEY, feePercentage)
    Notify(["setFeePercentage", feePercentage])
    return True

def startGame(gameId):
    RequireWitness(Operater)

    # mark the gameId betting starts
    Put(GetContext(), concatKey(GAME_STATUS_PREFIX, gameId), 1)
    Notify(["startGame", gameId])
    return True


def sendReqToOracle(gameId, gameNum, diskNumList):
    """
    call oracle to get format or info of Games, including the gameId, diskId
    """
    RequireWitness(Operater)

    req = getOracleReq(gameId, gameNum, diskNumList)

    txhash = GetTransactionHash(GetScriptContainer())
    if Get(GetContext(), concatKey(SENTREQHASH_FORMGAME_PREFIX, gameId)):
        Put(GetContext(), concatKey(SENTREQHASH_SAVERES_PREFIX, gameId), txhash)
    else:
        Put(GetContext(), concatKey(SENTREQHASH_FORMGAME_PREFIX, gameId), txhash)
    res = OracleContract('CreateOracleRequest', [req, Operater])
    # if res == False:
    #      Notify(['callOracle failed'])
    #      return False
    Notify(["sendReqToOracle", txhash, res])
    return True


def createGameByOracleRes(gameId):
    RequireWitness(Operater)

    # # make sure the result hasn't be saved before
    # Require(not getGameResult(gameId))

    # make sure the request has been sent out to the oracle contract
    sentReqTxhash = Get(GetContext(), concatKey(SENTREQHASH_FORMGAME_PREFIX, gameId))
    Require(sentReqTxhash)
    response = OracleContract('GetOracleOutcome', [sentReqTxhash])
    Require(response)

    res = Deserialize(response)


    # extract game and disk info from res
    # make sure gameId is consistent with that provided within response
    # gameId, diskIdList, betEndTime
    diskIdList = [1, 2, 3]
    betEndTime = 100

    Put(GetContext(), concatKey(GAME_DISKID_PREFIX, gameId), Serialize(diskIdList))
    Put(GetContext(), concatKey(GAME_BET_ENDTIME_PREFIX, gameId), betEndTime)

    return True


def placeBet(address, gameId, diskId, betStatus, ongAmount):
    RequireWitness(address)
    # make sure address can place bet, otherwise, raise exception
    Require(canPlaceBet(gameId) == True)
    diskIdListInfo = Get(GetContext(), concatKey(GAME_DISKID_PREFIX, gameId))

    if not diskIdListInfo:
        Notify(["placeBet", "diskId illegal!"])
        return False
    diskIdList = Deserialize(diskIdListInfo)
    # make sure the passing by diskId is legal
    Require(_checkInList(diskId, diskIdList))

    # betStatus can only be 0, 1 or 2
    if betStatus > 2 or betStatus < 0:
        Notify(["placeBet", "betStatus illegal!"])
        return False

    Require(_transferONG(address, ContractAddress, ongAmount))

    playersList = getDiskPlayersList(gameId, diskId, betStatus)
    if not _checkInList(address, playersList):
        # update playersList
        playersList.append(address)
        Put(GetContext(), concatKey(concatKey(gameId, diskId), betStatus), Serialize(playersList))

    # update address's bet balance
    Put(GetContext(), concatKey(concatKey(gameId, diskId), concatKey(address, betStatus)), Add(getDiskBetBalance(gameId, diskId, betStatus, address), ongAmount))

    # update the disk bet amount
    Put(GetContext(), concatKey(concatKey(gameId, diskId), betStatus), Add(getDiskBetAmount(gameId, diskId, betStatus), ongAmount))

    Notify(["placeBet", address, gameId, diskId, betStatus, ongAmount])

    return True


def saveGameResultByOracleRes(gameId):
    RequireWitness(Operater)

    # # make sure the result hasn't be saved before
    # Require(not getGameResult(gameId))

    # make sure the request has been sent out to the oracle contract
    sentReqTxhash = Get(GetContext(), concatKey(SENTREQHASH_SAVERES_PREFIX, gameId))
    Require(sentReqTxhash)
    response = OracleContract('GetOracleOutcome', [sentReqTxhash])
    Require(response)

    res = Deserialize(response)


    # save the match/game result requesting from oracle contract to this contract
    diskIdList = [1, 2, 3, 4]
    diskResList = [-1, 0, 1, 2]
    diskResMap = {
        diskIdList[0]:-1,
        diskIdList[1]: 0,
        diskIdList[2]: 1,
        diskIdList[3]: 2,
                 }

    Put(GetContext(), concatKey(GAME_RES_PREFIX, gameId), Serialize(diskResMap))
    Notify(["saveGameResultByOracleRes", gameId, diskIdList, diskResList])
    return True



def endGame(gameId):
    RequireWitness(Operater)
    # make sure placing bets stage is over
    Require(canPlaceBet(gameId) == False)
    totalPayOut = 0
    # maker sure the game results have been saved
    diskResMapInfo = Get(GetContext(), concatKey(GAME_RES_PREFIX, gameId))
    Require(diskResMapInfo)
    diskResMap = Deserialize(diskResMapInfo)
    diskIdListInfo = Get(GetContext(), concatKey(GAME_DISKID_PREFIX, gameId))
    Require(diskIdListInfo)
    diskIdList = Deserialize(diskIdListInfo)
    totalDiskProfitForDev = 0
    for diskId in diskIdList:
        # if the gameId-diskId game hasn't been ended yet.
        if not Get(GetContext(), concatKey(concatKey(gameId, diskId), DISK_STATUS_KEY)):
            diskRes = diskResMap[diskId]
            diskProfitForDev = endDisk(gameId, diskId, diskRes)
            totalDiskProfitForDev = Add(totalDiskProfitForDev, diskProfitForDev)
            # mark the gameId-diskId game as end
            Put(GetContext(), concatKey(concatKey(gameId, diskId), DISK_STATUS_KEY), 1)
    # update the profit for dev
    _updateProfitForDev(totalDiskProfitForDev)
    return True


def endDisk(gameId, diskId, diskRes):
    """
    settle all the accounts within gameId-diskId disk bet.
    :param gameId:
    :param diskId:
    :param diskRes: could be -1, 0, 1, 2
    :return: profit for dev
    """
    RequireWitness(Operater)

    if diskRes == AbortSide:
        # pay back the money to the players, respectively
        _payBackToPlayers(gameId, diskId)
        Notify(["endDisk", gameId, diskId, diskRes])
        return 0
    leftBetAmount = getDiskBetAmount(gameId, diskId, 1)
    rightBetAmount = getDiskBetAmount(gameId, diskId, 2)

    odds = 0
    FeePercentage = getFeePercentage()
    if diskRes == TieSide:
        # TODO
        pass
    if diskRes == LeftSide:
        odds = rightBetAmount * Magnitude  * (100 - FeePercentage) / leftBetAmount
    if diskRes == RightSide:
        odds = leftBetAmount * Magnitude * (100 - FeePercentage) / rightBetAmount

    # get winners list
    winnersList = getDiskPlayersList(gameId, diskId, diskRes)
    if len(winnersList) == 0:
        Notify(["endDisk", gameId, diskId, diskRes])
        return Add(leftBetAmount, rightBetAmount)

    totalPayOut = 0
    winnerPayAmountList = []
    for winner in winnersList:
        winnerBetBalance = getDiskBetBalance(gameId, diskId, diskRes, winner)
        payToWinner = winnerBetBalance * odds / Magnitude + winnerBetBalance
        totalPayOut = Add(totalPayOut, payToWinner)
        Require(_transferONGFromContact(winner, payToWinner))
        winnerPayAmountList.append([winner, payToWinner])
    Notify(["endDisk", gameId, diskId, diskRes, winnerPayAmountList])
    return Sub(Add(rightBetAmount, leftBetAmount), totalPayOut)


def devWithdraw(devAddr):
    RequireWitness(devAddr)
    devShare = getDevProfit(devAddr)
    if devShare <= 0:
        return False

    Require(_transferONGFromContact(devAddr, devShare))
    Delete(GetContext(), concatKey(DEV_PROFIT_PREFIX, devAddr))

    Notify(["devWithdraw", devAddr, devAddr])
    return True




def getDevProfit(devAddr):
    return Get(GetContext(), concatKey(DEV_PROFIT_PREFIX, devAddr))

def getFeePercentage():
    return Get(GetContext(), FEE_PERCENTAGE_KEY)

def getDiskBetAmount(gameId, diskId, betStatus):
    return Get(GetContext(), concatKey(concatKey(gameId, diskId), betStatus))

def getDiskBetBalance(gameId, diskId, betStatus, address):
    return Get(GetContext(), concatKey(concatKey(gameId, diskId), concatKey(address, betStatus)))


def getDiskPlayersList(gameId, diskId, betStatus):
    playersListInfo = Get(GetContext(), concatKey(concatKey(gameId, diskId), betStatus))
    if not playersListInfo:
        return []
    else:
        return Deserialize(playersListInfo)

def canPlaceBet(gameId):
    """
    :param gameId:
    :return: 0 means can NOT place bets, 1 means CAN place bets.
    """
    return GetTime() < Get(GetContext(), concatKey(gameId, GAME_BET_ENDTIME_PREFIX))



def getDiskGameStatus(gameId, diskId):
    """
    :param gameId:
    :param diskId:
    :return:
    0 means the gameId-diskId has NOT been ended yet.
    1 means the gameId-diskId has already been ended.
    ENDED means all the players' accounts have been settled.
    """
    return Get(GetContext(), concatKey(concatKey(gameId, diskId), DISK_STATUS_KEY))


def _checkInList(el, eList):
    for element in eList:
        if element == el:
            return True
    return False

def _payBackToPlayers(gameId, diskId):
    leftSidePlayersList = getDiskPlayersList(gameId, diskId, 1)
    if len(leftSidePlayersList) != 0:
        # pay back to the left side players
        for leftSidePlayer in leftSidePlayersList:
            leftSidePlayerBetBalance = getDiskPlayersList(gameId, diskId, 1)
            Require(_transferONGFromContact(leftSidePlayer, leftSidePlayerBetBalance))
    rightSidePlayersList = getDiskPlayersList(gameId, diskId, 2)
    if len(rightSidePlayersList) != 0:
        # pay back to the right side players
        for rightSidePlayer in rightSidePlayersList:
            rightSidePlayerBetBalance = getDiskPlayersList(gameId, diskId, 2)
            Require(_transferONGFromContact(rightSidePlayer, rightSidePlayerBetBalance))
    return True

def _updateProfitForDev(profitPorDev):
    RequireWitness(Operater)
    dev1Share = Div(Mul(profitPorDev, Sub(100, Dev1Percentage)), 100)
    Put(GetContext(), concatKey(DEV_PROFIT_PREFIX, Dev1), Add(getDevProfit(Dev1), dev1Share))
    Put(GetContext(), concatKey(DEV_PROFIT_PREFIX, dev2), add(getDevProfit(Dev2), Sub(profitPorDev, dev1Share)))
    return True



def getOracleReq(gameId, gameNum, diskNumList):
    """
    joint different pieces to form the complete request
    :param gameId:
    :return:
    """
    # url = concat(concat('"http://data.nba.net/prod/v2/', gameId), '/scoreboard.json"')
    # url = concat('"https://github.com/skyinglyh1/competition/blob/master/test.json')
    # reqtmp = """{
    # 		"scheduler":{
    # 			"type": "runAfter",
    # 			"params": "2018-06-15 08:37:18"
    # 		},
    # 		"tasks":[
    # 			{
    # 			  "type": "httpGet",
    # 			  "params": {
    # 				"url":"""
    # reqhead = concat(concat(reqtmp, url), """}},""")
    # body = """{
    # 				"type": "jsonParse",
    # 				"params":
    # 				{
    # 					"data":
    # 					[
    # 						{
    # 							"type": "Array",
    # 							"path": ["data", "game_game_array","1"],
    # 							"sub_type":
    # 							[
    # 								{
    # 									"type": "Struct",
    # 									"sub_type":
    # 									[
    # 										{
    # 											"type": "Int",
    # 											"path": ["game_game_id"]
    # 										},
    # 										{
    # 											"type": "Int",
    # 											"path": ["count_down_time"]
    # 										},
    # 										{
    # 											"type": "Array",
    # 											"path": ["game_disk_array"],
    # 											"sub_type":
    # 											[
    # 											    {
    # 											        "type": "Struct",
    # 											        "sub_type":
    # 											        [
    # 											            {
    # 											                "type": "Int",
    # 											                "path": ["game_disk_id"]
    # 											            },
    # 											            {
    # 											                "type": "Int",
    # 											                "path": ["game_disk_result"]
    # 											            }
    # 											        ]
    # 											    }
    # 											]
    # 										}
    #
    # 									]
    # 								}
    # 							]
    # 						}
    # 					]
    # 				}
    # 			}
    # 		]
    # 	}
    #     """
    # req = concat(reqhead, body)

    req = """{
    		"scheduler":{
    			"type": "runAfter",
    			"params": "2018-06-15 08:37:18"
    		},
    		"tasks":[
    			{
    			  "type": "httpGet",
    			  "params": {
    				"url": https://github.com/skyinglyh1/competition/blob/master/test.json
    			  }
    			},
    			{
    				"type": "jsonParse",
    				"params":
    				{
    					"data":
    					[
    						{
    							"type": "Array",
    							"path": ["data", "game_game_array","1"],
    							"sub_type":
    							[
    								{
    									"type": "Struct",
    									"sub_type":
    									[
    										{
    											"type": "Int",
    											"path": ["game_game_id"]
    										},
    										{
    											"type": "Int",
    											"path": ["count_down_time"]
    										},
    										{
    											"type": "Array",
    											"path": ["game_disk_array"],
    											"sub_type":
    											[
    											    {
    											        "type": "Struct",
    											        "sub_type":
    											        [
    											            {
    											                "type": "Int",
    											                "path": ["game_disk_id"]
    											            },
    											            {
    											                "type": "Int",
    											                "path": ["game_disk_result"]
    											            }
    											        ]
    											    }
    											]
    										}
    										
    									]
    								}
    							]
    						}
    					]
    				}
    			}
    		]
    	}"""

    return req

def _transferONG(fromAcct, toAcct, amount):
    """
    transfer ONG
    :param fromacct:
    :param toacct:
    :param amount:
    :return:
    """
    RequireWitness(fromAcct)
    param = state(fromAcct, toAcct, amount)
    res = Invoke(0, ONGAddress, 'transfer', [param])
    if res and res == b'\x01':
        return True
    else:
        return False

def _transferONGFromContact(toAcct, amount):
    param = state(ContractAddress, toAcct, amount)
    res = Invoke(0, ONGAddress, 'transfer', [param])
    if res and res == b'\x01':
        return True
    else:
        return False

def concatKey(str1,str2):
    """
    connect str1 and str2 together as a key
    :param str1: string1
    :param str2:  string2
    :return: string1_string2
    """
    return concat(concat(str1, '_'), str2)