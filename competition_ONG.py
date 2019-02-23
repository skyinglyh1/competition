OntCversion = '2.0.0'
"""
Competition Game
"""
from ontology.interop.Ontology.Contract import Migrate
from ontology.interop.System.App import RegisterAppCall, DynamicAppCall
from ontology.interop.System.Storage import GetContext, Get, Put, Delete
from ontology.interop.System.Runtime import CheckWitness, GetTime, Notify, Serialize, Deserialize
from ontology.interop.System.ExecutionEngine import GetExecutingScriptHash, GetScriptContainer
from ontology.interop.Ontology.Native import Invoke
from ontology.interop.Ontology.Runtime import Base58ToAddress
from ontology.builtins import concat, state
from ontology.interop.System.Transaction import GetTransactionHash
from ontology.libont import str, AddressFromVmCode

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
Dev1 = Base58ToAddress("AYqCVffRcbPkf1BVCYPJqqoiFTFmvwYKhG")
# the cooperator
Dev2 = Base58ToAddress("AbP7a7pbbqXU1SLzRKJXvw5YYxGdctoY6B")


Operater = Base58ToAddress("AQf4Mzu1YJrhz9f3aRkkwSm9n3qhXGSh4p")

INIT_KEY = "Inited"
ContractAddress = GetExecutingScriptHash()
ONGMagnitude = 1000000000
Magnitude = 1000000000000000000000000000000


OracleContract = RegisterAppCall('b108e1d2a7e8db11cb2150ccf1788d56a243996d', 'operation', 'args')
SelfContractAddress = GetExecutingScriptHash()

DEV_PROFIT_PREFIX = "DEV"
FEE_PERCENTAGE_KEY = "FEE"

MIN_BET_AMOUNT_KEY = "MBA"
DEV1_PERCENTAGE_KEY = "D1P"

SENTREQHASH_FORMGAME_PREFIX = "G1"
GAME_STATUS_PREFIX = 'G2'
GAME_RES_PREFIX = "G3"
GAME_DISKID_LIST_PREFIX = "G4"
GAME_BET_ENDTIME_PREFIX = "G5"

DISK_ONG_AMOUNT_PREFIX = "G6"
DISK_PLAYERS_LIST_PREFIX = "G7"
DISK_STATUS_PERFIX = "G8"
PLAYER_BET_PREFIX = "G9"

SENTREQHASH_SAVERES_PREFIX = "G10"
DISK_BET_PLAYER_LIST_PREFIX = "G11"
DISK_PLAYER_BET_BALANCE_PREFIX = "G12"
DISK_PLAYERS_BET_AMOUNT_PREFIX = "G13"

DefaultSide = 9
AbortSide = 8
TieSide = 0
LeftSide = 1
RightSide = 2

# SidesList = [DefaultSide, TieSide, LeftSide, RightSide, AbortSide]
SidesList = [9, 0, 1, 2, 8]


def Main(operation, args):
    if operation == "init":
        return init()
    if operation == "setDev1Percentage":
        if len(args) != 1:
            return False
        dev1Percentage = args[0]
        return setDev1Percentage(dev1Percentage)
    if operation == "setFeePercentage":
        if len(args) != 1:
            return False
        feePercentage = args[0]
        return setFeePercentage(feePercentage)
    if operation == "setMinBetAmount":
        if len(args) != 1:
            return False
        minBetAmount = args[0]
        return setMinBetAmount(minBetAmount)
    if operation == "sendReqToOracle":
        if len(args) != 2:
            return False
        jsonIndex = args[0]
        formOrSave = args[1]
        return sendReqToOracle(jsonIndex, formOrSave)

    if operation == "createGameByOracleRes":
        if len(args) != 1:
            return False
        jsonIndex = args[0]
        return createGameByOracleRes(jsonIndex)
    if operation == "createGameByHand":
        if len(args) != 4:
            return False
        jsonIndex = args[0]
        gameIdList = args[1]
        gameEndTimeList = args[2]
        diskIdList = args[3]
        return createGameByHand(jsonIndex, gameIdList, gameEndTimeList, diskIdList)
    if operation == "resetGameBetEndTime":
        if len(args) != 2:
            return False
        gameId = args[0]
        newBetEndTime = args[1]
        return resetGameBetEndTime(gameId, newBetEndTime)
    if operation == "placeBet":
        if len(args) != 5:
            return False
        address = args[0]
        gameId = args[1]
        diskId = args[2]
        betStatus = args[3]
        ongAmount = args[4]
        return placeBet(address, gameId, diskId, betStatus, ongAmount)
    if operation == "saveGameResultByOracleRes":
        if len(args) != 1:
            return False
        jsonIndex = args[0]
        return saveGameResultByOracleRes(jsonIndex)
    if operation == "endGame":
        if len(args) != 1:
            return False
        gameIdList = args[0]
        return endGame(gameIdList)
    if operation == "saveGameResultByHand":
        if len(args) != 3:
            return False
        gameId = args[0]
        diskIdList = args[1]
        diskResList = args[2]
        return saveGameResultByHand(gameId, diskIdList, diskResList)
    if operation == "endDisksByHand":
        if len(args) != 2:
            return False
        gameId = args[0]
        diskIdList = args[1]
        return endDisksByHand(gameId, diskIdList)
    if operation == "devWithdraw":
        if len(args) != 1:
            return False
        devAddr = args[0]
        return devWithdraw(devAddr)
    if operation == "migrateContract":
        Require(len(args) == 7)
        code = args[0]
        needStorage = args[1]
        name = args[2]
        version = args[3]
        author = args[4]
        email = args[5]
        description = args[6]
        return migrateContract(code, needStorage, name, version, author, email, description)

    if operation == "getDevProfit":
        if len(args) != 1:
            return False
        devAddr = args[0]
        return getDevProfit(devAddr)
    if operation == "getFeePercentage":
        return getFeePercentage()
    if operation == "getDev1Percentage":
        return getDev1Percentage()
    if operation == "getMinBetAmount":
        return getMinBetAmount()
    if operation == "getDiskIdList":
        if len(args) != 1:
            return False
        gameId = args[0]
        return getDiskIdList(gameId)
    if operation == "getGameBetEndTime":
        if len(args) != 1:
            return False
        gameId = args[0]
        return getGameBetEndTime(gameId)
    if operation == "getDiskBetAmount":
        if len(args) != 2:
            return False
        diskId = args[0]
        betStatus = args[1]
        return getDiskBetAmount(diskId, betStatus)
    if operation == "getDiskBetBalance":
        if len(args) != 3:
            return False
        diskId = args[0]
        betStatus = args[1]
        address = args[2]
        return getDiskBetBalance(diskId, betStatus, address)
    if operation == "getDiskPlayersList":
        if len(args) != 2:
            return False
        diskId = args[0]
        betStatus = args[1]
        return getDiskPlayersList(diskId, betStatus)
    if operation == "canPlaceBet":
        if len(args) != 1:
            return False
        gameId = args[0]
        return canPlaceBet(gameId)
    if operation == "getDiskResult":
        if len(args) != 2:
            return False
        gameId = args[0]
        diskId = args[1]
        return getDiskResult(gameId, diskId)
    if operation == "getDiskStatus":
        if len(args) != 1:
            return False
        diskId = args[0]
        return getDiskStatus(diskId)
    return False

def init():
    RequireWitness(Operater)
    inited = Get(GetContext(), INIT_KEY)
    if not inited:
        setFeePercentage(2)
    return True


def setDev1Percentage(dev1Percentage):
    RequireWitness(Dev1)
    Require(dev1Percentage <= 100)
    Require(dev1Percentage >= 0)
    Put(GetContext(), DEV1_PERCENTAGE_KEY, dev1Percentage)
    Notify(["setDev1Percentage", dev1Percentage])
    return True

def setFeePercentage(feePercentage):
    RequireWitness(Operater)
    Require(feePercentage <= 100)
    Require(feePercentage >= 0)
    Put(GetContext(), FEE_PERCENTAGE_KEY, feePercentage)
    Notify(["setFeePercentage", feePercentage])
    return True

def setMinBetAmount(minBetAmount):
    RequireWitness(Operater)
    Require(minBetAmount > 0)
    Put(GetContext(), MIN_BET_AMOUNT_KEY, minBetAmount)
    Notify(["setMinBetAmount", minBetAmount])
    return True


def sendReqToOracle(jsonIndex, formOrSave):
    """
    call oracle to get format or info of Games, including the, diskId
    :param jsonIndex: Int
    :param formOrSave: 0 means to form game, 1 means to save res
    :return:
    """
    RequireWitness(Operater)

    req = getOracleReq(jsonIndex)

    txhash = GetTransactionHash(GetScriptContainer())

    if formOrSave == 0:
        Put(GetContext(), concatKey(SENTREQHASH_FORMGAME_PREFIX, jsonIndex), txhash)
    elif formOrSave == 1:
        Put(GetContext(), concatKey(SENTREQHASH_SAVERES_PREFIX, jsonIndex), txhash)
    else:
        raise Exception("illegal formOrSame!")

    # if Get(GetContext(), concatKey(SENTREQHASH_FORMGAME_PREFIX, jsonIndex)):
    #     Put(GetContext(), concatKey(SENTREQHASH_SAVERES_PREFIX, jsonIndex), txhash)
    # else:
    #     Put(GetContext(), concatKey(SENTREQHASH_FORMGAME_PREFIX, jsonIndex), txhash)

    res = OracleContract('CreateOracleRequest', [req, Operater])

    Notify(["sendReqToOracle", txhash])
    return True


def createGameByOracleRes(jsonIndex):
    """
    :param jsonIndex: Int
    :return:
    """
    RequireWitness(Operater)

    # # make sure the result hasn't be saved before
    # Require(not getGameResult(gameId))

    # make sure the request to initiate games has been sent out to the oracle contract
    sentReqTxhash = Get(GetContext(), concatKey(SENTREQHASH_FORMGAME_PREFIX, jsonIndex))
    # Require(sentReqTxhash)
    if not sentReqTxhash:
        # Error 101: "Request To Initiate Game Failed!"
        Notify(["Error", 101])
        return False
    response = OracleContract('GetOracleOutcome', [sentReqTxhash])
    # Require(response)
    if not response:
        # Error 102: "Get Response From Oracle Failed!"
        Notify(["Error", 102])
        return False

    a = Deserialize(response)
    if a[2] != 0:
        # Error 103: "Get Response From Oracle With Error!"
        Notify(["Error", 103])
        return False
    b = Deserialize(a[0])

    c = b[0]
    gameIdList = []
    endTimeList = []
    gameDiskIdList = []
    # resultList = []
    for game in c:
        gameId = game[0]
        gameIdList.append(gameId)
        endTime = game[1]
        endTimeList.append(endTime)
        tmpDiskIdList = []
        tmp = game[2]
        for gameDisk in tmp:
            tmpDiskId = gameDisk[0]
            # tmpDiskRes = gameDisk[1]
            tmpDiskIdList.append(tmpDiskId)
        gameDiskIdList.append(tmpDiskIdList)

    gameIdLen = len(gameIdList)
    gameIdIndex = 0
    while gameIdIndex < gameIdLen:
        gameId = gameIdList[gameIdIndex]
        diskIdList = gameDiskIdList[gameIdIndex]
        betEndTime = endTimeList[gameIdIndex]
        Put(GetContext(), concatKey(GAME_DISKID_LIST_PREFIX, gameId), Serialize(diskIdList))
        Put(GetContext(), concatKey(GAME_BET_ENDTIME_PREFIX, gameId), betEndTime)

        gameIdIndex = Add(gameIdIndex, 1)
        # gameIdIndex = gameIdIndex + 1

    Notify(["createGameByOracleRes", gameIdList, gameDiskIdList, endTimeList])
    return True


def createGameByHand(jsonIndex, gameIdList, gameEndTimeList, diskIdList):
    RequireWitness(Operater)
    gameIdLen = len(gameIdList)
    Require(gameIdLen == len(gameEndTimeList))
    Require(gameIdLen == len(diskIdList))

    index = 0
    while index < gameIdLen:
        gameId = gameIdList[index]
        gameDiskIdList = diskIdList[index]
        betEndTime = gameEndTimeList[index]
        Put(GetContext(), concat(GAME_DISKID_LIST_PREFIX, gameId), Serialize(gameDiskIdList))
        Put(GetContext(), concat(GAME_BET_ENDTIME_PREFIX, gameId), betEndTime)
        index = Add(index, 1)

    Notify(["createGameByHand", jsonIndex, gameIdList, gameEndTimeList, diskIdList])
    return True

def resetGameBetEndTime(gameId, newBetEndTime):
    RequireWitness(Operater)
    Require(getGameBetEndTime(gameId) > 0)
    Put(GetContext(), concatKey(GAME_BET_ENDTIME_PREFIX, gameId), newBetEndTime)
    Notify(["resetBetEndTime", gameId, newBetEndTime])
    return True


def placeBet(address, gameId, diskId, betStatus, ongAmount):
    RequireWitness(address)
    # make sure address can place bet, otherwise, raise exception
    Require(canPlaceBet(gameId))

    if ongAmount < getMinBetAmount():
        # Error 201: "Please bet more ONG!"
        Notify(["Error", 201])
        return False

    Require(not getDiskStatus(diskId))
    diskIdListInfo = Get(GetContext(), concatKey(GAME_DISKID_LIST_PREFIX, gameId))

    if not diskIdListInfo:
        # Error 202: "diskId Not Exist!"
        Notify(["Error", 202])
        return False
    diskIdList = Deserialize(diskIdListInfo)
    # make sure the passing by diskId is legal
    # Require(_checkInList(diskId, diskIdList))
    if _checkInList(diskId, diskIdList) == False:
        # Error 203: "diskId illegal!"
        Notify(["Error", 203])
        return False

    # betStatus can only be 0, 1 or 2
    if betStatus == TieSide or betStatus == LeftSide or betStatus == RightSide:
        Require(_transferONG(address, ContractAddress, ongAmount))
    else:
        # Error 204: "betStatus illegal!"
        Notify(["Error", 204])
        return False
    playersList = getDiskPlayersList(diskId, betStatus)
    if not _checkInList(address, playersList):
        # update playersList
        playersList.append(address)
        Put(GetContext(), concatKey(concatKey(DISK_BET_PLAYER_LIST_PREFIX, diskId), betStatus), Serialize(playersList))

    # update address's bet balance
    Put(GetContext(), concatKey(concatKey(DISK_PLAYER_BET_BALANCE_PREFIX, diskId), concatKey(address, betStatus)), Add(getDiskBetBalance(diskId, betStatus, address), ongAmount))

    # update the disk bet amount
    Put(GetContext(), concatKey(concatKey(DISK_PLAYERS_BET_AMOUNT_PREFIX, diskId), betStatus), Add(getDiskBetAmount(diskId, betStatus), ongAmount))

    Notify(["placeBet", address, gameId, diskId, betStatus, ongAmount])

    return True


def saveGameResultByOracleRes(jsonIndex):
    """
    Before invoke this method, the sendReqToOracle(jsonIndex) should be invoked again to store the game and disk results.
    :param jsonIndex: Int
    :return:
    """
    RequireWitness(Operater)
    # make sure the request has been sent out to the oracle contract
    sentReqTxhash = Get(GetContext(), concatKey(SENTREQHASH_SAVERES_PREFIX, jsonIndex))

    # Require(sentReqTxhash)
    if not sentReqTxhash:
        # Error 301: "Request To Save Game Results Failed!"
        Notify(["Error", 301])
        return False

    response = OracleContract('GetOracleOutcome', [sentReqTxhash])

    # Require(response)
    if not response:
        # Error 302: "Get Response From Oracle Failed!"
        Notify(["Error", 302])
        return False

    a = Deserialize(response)
    if a[2] != 0:
        # Error 303: "Get Response From Oracle With Error!"
        Notify(["Error", 303])
        return False
    b = Deserialize(a[0])
    c = b[0]
    gameIdList = []
    gameDiskIdList = []
    gameDiskResultList = []
    for game in c:
        gameId = game[0]
        gameIdList.append(gameId)

        tmpDiskIdList = []
        tmpDiskResList = []
        tmp = game[2]
        for gameDisk in tmp:
            tmpDiskId = gameDisk[0]
            tmpDiskRes = gameDisk[1]
            tmpDiskIdList.append(tmpDiskId)
            tmpDiskResList.append(tmpDiskRes)
        gameDiskIdList.append(tmpDiskIdList)
        gameDiskResultList.append(tmpDiskResList)

    diskResMap = {}
    gameIdLen = len(gameIdList)
    gameIdIndex = 0
    while gameIdIndex < gameIdLen:
        gameId = gameIdList[gameIdIndex]
        Require(canPlaceBet(gameId) == False)
        savedDiskIdList = getDiskIdList(gameId)
        diskIdList = gameDiskIdList[gameIdIndex]
        diskIdLen = len(diskIdList)
        diskIdIndex = 0
        while diskIdIndex < diskIdLen:
            diskId = diskIdList[diskIdIndex]
            # make sure gameId is consistent with that provided within response
            Require(diskId == savedDiskIdList[diskIdIndex])
            diskRes = gameDiskResultList[gameIdIndex][diskIdIndex]

            Require(_checkInList(diskRes, SidesList))
            # save the match/game result requesting from oracle contract to this contract
            diskResMap[diskId] = diskRes
            diskIdIndex = diskIdIndex + 1
        Put(GetContext(), concatKey(GAME_RES_PREFIX, gameId), Serialize(diskResMap))
        gameIdIndex = gameIdIndex + 1


    Notify(["saveGameResultByOracleRes", jsonIndex, gameDiskIdList, gameDiskResultList])
    return True


def endGame(gameIdList):
    RequireWitness(Operater)
    totalDiskProfitForDev = 0
    for gameId in gameIdList:
        # make sure placing bets stage is over
        Require(canPlaceBet(gameId) == False)
        # maker sure the game results have been saved
        diskResMapInfo = Get(GetContext(), concatKey(GAME_RES_PREFIX, gameId))
        Require(diskResMapInfo)
        diskResMap = Deserialize(diskResMapInfo)

        diskIdList = getDiskIdList(gameId)
        for diskId in diskIdList:
            # if the gameId-diskId game hasn't been settled yet.
            if getDiskStatus(diskId) == 0:
                diskRes = diskResMap[diskId]
                diskProfitForDev = _endDisk(diskId, diskRes)
                totalDiskProfitForDev = Add(totalDiskProfitForDev, diskProfitForDev)
    # update the profit for dev
    _updateProfitForDev(totalDiskProfitForDev)
    return True


def saveGameResultByHand(gameId, diskIdList, diskResList):
    RequireWitness(Operater)
    Require(canPlaceBet(gameId) == False)
    diskResMapInfo = Get(GetContext(), concatKey(GAME_RES_PREFIX, gameId))
    if not diskResMapInfo:
        # 401: "Operator Should Request Game Result First!"
        Notify(["Error", 401])
        return False
    diskResMap = Deserialize(diskResMapInfo)
    gameDiskIdList = getDiskIdList(gameId)
    diskIdLen = len(diskIdList)
    diskIdIndex = 0
    while diskIdIndex < diskIdLen:

        diskId = diskIdList[diskIdIndex]
        Require(_checkInList(diskId, gameDiskIdList))
        Require(getDiskStatus(diskId) == 0)
        # Require(diskResMap[diskId] == DefaultSide)
        diskResMap[diskId] = diskResList[diskIdIndex]
        diskIdIndex = diskIdIndex + 1
    Put(GetContext(), concatKey(GAME_RES_PREFIX, gameId), Serialize(diskResMap))
    Notify(["saveGameResultByHand", gameId, diskIdList, diskResList])
    return True


def endDisksByHand(gameId, diskIdList):
    RequireWitness(Operater)
    Require(canPlaceBet(gameId) == False)
    totalDiskProfitForDev = 0
    diskIdLen = len(diskIdList)
    diskResMapInfo = Get(GetContext(), concatKey(GAME_RES_PREFIX, gameId))
    Require(diskResMapInfo)
    diskResMap = Deserialize(diskResMapInfo)
    diskIdIndex = 0
    while diskIdIndex < diskIdLen:
        diskId = diskIdList[diskIdIndex]
        diskRes = diskResMap[diskId]
        diskProfitForDev = _endDisk(diskId, diskRes)
        totalDiskProfitForDev = Add(totalDiskProfitForDev, diskProfitForDev)
        diskIdIndex = diskIdIndex + 1
    # update the profit for dev
    _updateProfitForDev(totalDiskProfitForDev)
    return True


def _endDisk(diskId, diskRes):
    """
    settle all the accounts within diskId disk bet.
    :param diskId: disk id
    :param diskRes: could be DefaultSide:9, AbortSide:8, TieSide:0, LeftSide:1, RightSide:2
    :return: profit for dev
    """
    RequireWitness(Operater)
    Require(_checkInList(diskRes, SidesList))

    if getDiskStatus(diskId) == 1 or diskRes == DefaultSide:
        return 0
    if diskRes == AbortSide:
        # mark the diskId game as end
        Put(GetContext(), concatKey(DISK_STATUS_PERFIX, diskId), 1)
        # pay back the money to the players, respectively
        _payBackToPlayers(diskId)
        Notify(["endDisk", diskId, diskRes])
        return 0
    leftBetAmount = getDiskBetAmount(diskId, LeftSide)
    rightBetAmount = getDiskBetAmount(diskId, RightSide)
    tieBetAmount = getDiskBetAmount(diskId, TieSide)
    # get winners list
    winnersList = getDiskPlayersList(diskId, diskRes)
    # if nobody wins:
    if len(winnersList) == 0:
        # mark the diskId game as end
        Put(GetContext(), concatKey(DISK_STATUS_PERFIX, diskId), 1)
        Notify(["endDisk", diskId, diskRes])
        return Add(Add(leftBetAmount, rightBetAmount), tieBetAmount)

    odds = 0
    FeePercentage = getFeePercentage()
    if diskRes == TieSide:
        odds = Div(Div(Mul(Mul(Add(leftBetAmount, rightBetAmount), Magnitude), Sub(100, FeePercentage)), tieBetAmount), 100)
    if diskRes == LeftSide:
        odds = Div(Div(Mul(Mul(Add(rightBetAmount, tieBetAmount), Magnitude), Sub(100, FeePercentage)), leftBetAmount), 100)
    if diskRes == RightSide:
        odds = Div(Div(Mul(Mul(Add(leftBetAmount, tieBetAmount), Magnitude), Sub(100, FeePercentage)), rightBetAmount), 100)
    # odds should be 20000 * 1000000000000000000000000000000  * 98 / 10000 / 100 = 1960000000000000000000000000000 or 0000004050d2559427001abd18
    totalPayOut = 0
    winnerPayAmountList = []
    for winner in winnersList:
        winnerBetBalance = getDiskBetBalance(diskId, diskRes, winner)
        payToWinner = Add(Div(Mul(winnerBetBalance, odds), Magnitude), winnerBetBalance)
        totalPayOut = Add(totalPayOut, payToWinner)
        Require(_transferONGFromContact(winner, payToWinner))
        winnerPayAmountList.append([winner, payToWinner])

    # mark the diskId game as end
    Put(GetContext(), concatKey(DISK_STATUS_PERFIX, diskId), 1)

    Notify(["endDisk", diskId, diskRes, winnerPayAmountList])
    return Sub(Add(Add(rightBetAmount, leftBetAmount), tieBetAmount), totalPayOut)

def devWithdraw(devAddr):
    RequireWitness(devAddr)
    devShare = getDevProfit(devAddr)
    if devShare <= 0:
        return False

    Require(_transferONGFromContact(devAddr, devShare))
    Delete(GetContext(), concatKey(DEV_PROFIT_PREFIX, devAddr))

    Notify(["devWithdraw", devAddr, devShare])
    return True

def migrateContract(code, needStorage, name, version, author, email, description):
    RequireWitness(Dev1)
    param = state(ContractAddress)
    totalOngAmount = Invoke(0, ONGAddress, 'balanceOf', param)
    newContractHash = AddressFromVmCode(code)
    res = _transferONGFromContact(newContractHash, totalOngAmount)
    Require(res)
    if res == True:
        res = Migrate(code, needStorage, name, version, author, email, description)
        Require(res)
        Notify(["Migrate Contract successfully", Dev1])
        return True
    else:
        # Error: 501, MigrateContractError, transfer ONG to new contract error
        Notify(["Error", 501])
        return False


def getDevProfit(devAddr):
    return Get(GetContext(), concatKey(DEV_PROFIT_PREFIX, devAddr))

def getFeePercentage():
    return Get(GetContext(), FEE_PERCENTAGE_KEY)

def getDev1Percentage():
    return Get(GetContext(), DEV1_PERCENTAGE_KEY)

def getMinBetAmount():
    return Get(GetContext(), MIN_BET_AMOUNT_KEY)

def getDiskIdList(gameId):
    diskIdListInfo = Get(GetContext(), concatKey(GAME_DISKID_LIST_PREFIX, gameId))
    if not diskIdListInfo:
        return []
    else:
        return Deserialize(diskIdListInfo)

def getGameBetEndTime(gameId):
    return Get(GetContext(), concatKey(GAME_BET_ENDTIME_PREFIX, gameId))


def getDiskBetAmount(diskId, betStatus):
    return Get(GetContext(), concatKey(concatKey(DISK_PLAYERS_BET_AMOUNT_PREFIX, diskId), betStatus))

def getDiskBetBalance(diskId, betStatus, address):
    return Get(GetContext(), concatKey(concatKey(DISK_PLAYER_BET_BALANCE_PREFIX, diskId), concatKey(address, betStatus)))


def getDiskPlayersList(diskId, betStatus):
    playersListInfo = Get(GetContext(), concatKey(concatKey(DISK_BET_PLAYER_LIST_PREFIX, diskId), betStatus))
    if not playersListInfo:
        return []
    else:
        return Deserialize(playersListInfo)

def canPlaceBet(gameId):
    """
    :param gameId:
    :return: False means can NOT place bets, True means CAN place bets.
    """
    return GetTime() < Get(GetContext(), concatKey(GAME_BET_ENDTIME_PREFIX, gameId))


def getDiskResult(gameId, diskId):
    """

    :param gameId:
    :param diskId:
    :return:
    0 means: tie
    1 means: left side wins
    2 means: right side wins

    8 means: abortion
    9 means: the diskId has already been initialized, yet
             the diskId result hasn't been recorded into json.
             Meanwhile, saveGameResultByOracleRes has already been invoked.

    10 means: gameId has not been initialized.
    11 means: gameId has been initialized, yet diskId illegal.
    12 means: dev should get game results through Oracle first by invoking saveGameResultByOracleRes method.
    """
    # make sure address can place bet, otherwise, raise exception
    Require(canPlaceBet(gameId) == False)

    diskIdListInfo = Get(GetContext(), concatKey(GAME_DISKID_LIST_PREFIX, gameId))

    if not diskIdListInfo:
        return 10
    diskIdList = Deserialize(diskIdListInfo)
    # make sure the passing by diskId is legal
    # Require(_checkInList(diskId, diskIdList))
    if _checkInList(diskId, diskIdList) == False:
        return 11

    diskResMapInfo = Get(GetContext(), concatKey(GAME_RES_PREFIX, gameId))
    if not diskResMapInfo:
        return 12
    diskResMap = Deserialize(diskResMapInfo)
    return diskResMap[diskId]


def getDiskStatus(diskId):
    """
    :param diskId:
    :return:
    0 means the diskId has NOT been ended yet.
    1 means the diskId has already been ended.
    ENDED means all the players' accounts have been settled.
    """
    return Get(GetContext(), concatKey(DISK_STATUS_PERFIX, diskId))


def _checkInList(el, eList):
    for element in eList:
        if element == el:
            return True
    return False

def _payBackToPlayers(diskId):
    betStatusList = [TieSide, LeftSide, RightSide]
    for betStatus in betStatusList:
        sidePlayersList = getDiskPlayersList(diskId, betStatus)
        if len(sidePlayersList) != 0:
            # pay back to the betStatus side players
            for sidePlayer in sidePlayersList:
                sidePlayerBetBalance = getDiskBetBalance(diskId, betStatus, sidePlayer)
                Require(_transferONGFromContact(sidePlayer, sidePlayerBetBalance))
    return True

def _updateProfitForDev(profitPorDev):
    RequireWitness(Operater)
    dev1Percentage = getDev1Percentage()
    dev1Share = Div(Mul(profitPorDev, dev1Percentage), 100)
    Put(GetContext(), concatKey(DEV_PROFIT_PREFIX, Dev1), Add(getDevProfit(Dev1), dev1Share))
    Put(GetContext(), concatKey(DEV_PROFIT_PREFIX, Dev2), Add(getDevProfit(Dev2), Sub(profitPorDev, dev1Share)))
    return True



def getOracleReq(jsonIndex):
    """
    joint different pieces to form the complete request
    :param gameId:
    :return:
    """
    url = concat(concat('"http://47.88.230.168:8886/api/publish-match?gameMatchRecordId=', str(jsonIndex)), '"')
    reqtmp = """{
    		"scheduler":{
    			"type": "runAfter",
    			"params": "2018-06-15 08:37:18"
    		},
    		"tasks":[
    			{
    			  "type": "httpGet",
    			  "params": {
    				"url":"""
    reqhead = concat(concat(reqtmp, url), """}},""")

    body = """{
                "type": "jsonParse",
                "params":
                {
                    "data":
                    [
                        {
                            "type": "Array",
                            "path": ["data", "game_game_array"],
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
    }	
    """
    req = concat(reqhead, body)
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
