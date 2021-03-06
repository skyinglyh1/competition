此文档可作为competition_ONG_1.py合约的接口文档及使用介绍。 、
## 注意事项：

a. smartX上应使用2.0编译器。

b. 在测试网上测试时，需要将
```
OracleContract = RegisterAppCall('b108e1d2a7e8db11cb2150ccf1788d56a243996d', 'operation', 'args')
```
更改为
```
OracleContract = RegisterAppCall('e0d635c7eb2c5eaa7d2207756a4c03a89790934a', 'operation', 'args')
```
如果是主网，需要改为
```
OracleContract = RegisterAppCall('a6ee997b142b002d49670ab73803403b09a23fa0', 'operation', 'args')
```

c. Dev1 和 Dev2为利润分成地址。

d. Operator为合约管理员，请确保管理员帐户内有充足的ONG以供管理员执行合约函数时使用。



## 流程：

1. 布署合约上链后，需要执行```init```函数，初始化合约, 然后调用```setDev1Percentage``` 传入dev1应享有的分成比例(需要Dev1来设置)，比例范围为0到100。

2. 开启一轮游戏时，项目方后台调用```sendReqToOracle```，目的是让赛事合约组成目的url，并根据此url向oracle发出请求，Orale获取到该url下对应的json文件内容。
json文件内容应包含不同的对局及不同对局下对应的盘口。

3. 经过30秒后，项目方调用```createGameByOracleRes```，目的是让赛事合约得到Oracle获取到的赛事信息，并根据此赛事信息，初始化赛事游戏。

4. 赛事竞猜游戏已经开始，用户可通过调用```placeBet```对不同对局下的不同盘口下注。

5. 正式游戏比赛进行中。

6. 当用户不能下注时或时间到达对局截止时间时，项目方在更新json文件后，后台调用```sendReqToOracle```，目的是让赛事合约组成目的url，并根据此url向oracle发出请求，Orale获取到该url下对应的json文件内容。
json文件内容应包含不同的对局及不同对局下对应的盘口及不同盘口对应的比赛结果。

7. 等待30秒后，后台调用```saveGameResultByOracleRes```，让赛事合约获取到Oracle内的赛事结果，并存储到赛事合约。

8. 后台调用```endGame```，将会结束某对局下的所有盘口游戏。

## 补充接口：
9. 若由于意外，项目方未能在5与6之间，在json文件中添加该json中所有的对局对应的比赛结果，则可通过```saveGameResultByHand```来手动录入比赛结果。

10. 若由于意外，项目方在执行8后，发现有部分盘口已经有比赛结果但未成功结算
(比如，项目方以为json文件中的所有盘口比赛结果都已填入，然后执行8，但实际上，存在部分盘口比赛结果未填入)，则项目方可通过调用```endDisksByHand```来结算某些盘口。


## 关于Dev利润：
11. 通过调用```devWithdraw(devAddr)```，dev可对利润进行提现，ONG直接到账, dev有两个地址，待提供。

12. 通过预执行```getDevProfit(devAddr)```，dev可查询某devAddr地址下的利润多少。

## 其他可改动参数：
13. ```setFeePercentage(feePercentage)``` 可更改抽成比例feePercentage，只有Operator可更改。feePercentage应为[0, 100)

31. ```setMinBetAmount(minBetAmount)```可更改用户最小下注的ONG的量(>=minBetAmount是合法的),只有Operator可对这个值进行更改。


## 其他可查询信息 (通过预执行的方式)

14. ```getFeePercentage()``` 查询抽成比例。

15. ```getDiskIdList(gameId)```根据gameId查询该对局下的所有盘口diskId.

16. ```getGameBetEndTime(gameId)```根据gameId查询该对局下所有盘口的投注截止时间。

17. ```getDiskBetAmount(diskId, betStatus)```根据diskId及投注的状态(平、左、右)来查询投注某盘口某状态的总竞猜资金。

18. ```getDiskBetBalance(diskId, betStatus, address)```根据diskId、投注的状态及投注的地址来查询某地址投注某盘口某状态的所有竞猜资金。

19. ```getDiskPlayersList(diskId, betStatus)``` 根据diskId及投注状态，查询所有投注此盘口及此状态的用户地址列表。

20. ```canPlaceBet(gameId)``` 根据对局gameId 来判断用户是否可下注，0表示不可下注，1表示可下注。

21. ```getDiskResult(gameId, diskId)``` 根据对局gameId及盘口diskId来查询该diskId盘口的比赛结果，返回：

```
    
    0 表示 平局
    1 表示 左赢
    2 表示 右赢
    
    8 表示 流盘
    9 表示 盘口已经初始化，但比赛结果被录入json,此时，已经调用了```saveGameResultByOracleRes```函数。
    10 表示 gameId还未被初始化
    11 表示 gameId已被初始化，但diskId不合法
    12 表示 Dev应该先调用```saveGameResultByOracleRes```去获取比赛结果。
```

22. ```getDiskStatus(diskId)```根据diskId查询某盘口是否已经被结算，0表示未结算，1表示已结算。结算也正当于盘口竞猜是否结束。

32. ```getMinBetAmount()``` 可查询用户最小下注的ONG的量(>=minBetAmount是合法的)。


## 关于核心函数接口参数说明：

23. ```sendReqToOracle(jsonIndex, formOrSave)```， jsonIndex为构造目的url所必须的参数,
```
jsonIndex:
formOrSave: 0 means to form game（也就是流程中的第2步）, 1 means to save res（也就是流程中的第6步）。
```

24. ```createGameByOracleRes(jsonIndex)```,  jsonIndex为构造目的url所必须的参数。

25. ```saveGameResultByOracleRes(jsonIndex):```, jsonIndex为构造目的url所必须的参数。
 注： 对于同一个json， 23 24 25的参数是一致的。

26. ```placeBet(address, gameId, diskId, betStatus, ongAmount)```， 用户下注函数.

```
address为用户地址，合约内会对该地址验签
gameId为用户投注盘口所属的对局id
diskId为用户投注的盘口id
betStatus为用户投注的状态，其值可为0, 1, 2.
ongAmount为用户投注和竞猜金额
```

27. ```endGame(gameIdList)```,gameIdList为项目方想要结束的对局gameId的List.

28. ```saveGameResultByHand(gameId, diskIdList, diskResList)```, 项目方想要手动录入比赛结果到赛事合约内部需要调用此函数。
```
gameId为指定对局id.
diskIdList为该对局下想要手动录入的盘口id组成的List.
diskResList为想要录入多个盘口id对应的比赛结果，应于diskIdList一一对应。
```
29. ```endDisksByHand(gameId, diskIdList)```,项目方想要手动结算几个特殊未结算的盘口。
```
gameId为这些盘口对应的对局id.
diskIdList为这些盘口组成的list.
```

30. ```resetGameBetEndTime(gameId, newBetEndTime)```, 项目方想要手动更改某对局的下注截止时间。
```
gameId 为某对局id
newBetEndTime为该对局新的下注截止时间
```

31. 在第```13```条下面

32. 在第```22```条下面

33. ```migragteContract```, 项目方可对合约进行迁移，```Dev1```拥有执行此函数的权力，迁移的效果是旧合约里的所有数据都会被转移至新合约内，且旧合约的资产(ONG)也会被转移到新合约内。
```
code: 新合约的avm Code
needStorage: True
name: String类
version: String 类
author: String 类
email: String 类
description: String 类
```

34. ```createGameByHand```, 项目方手动初始化多场对局(防止Oracle未能正常工作的情况出现)，```Operator```拥有执行此函数的权力。
```
jsonIndex： 初始化的这多场对局对应于哪个json文件，合约不对此数据作存储，只是在链上一个Notify内的存证使用。
gameIdList：[gameId1, gameId2, gameId3]
gameEndTimeList: [gameId1_endTime, gameId2_endTime, gameId3_endTime]
diskIdList: [
	[gameId1_diskId11, gameId1_diskId12, gameId1_diskId13],
	[gameId2_diskId21, gameId2_diskId22, gameId1_diskId23],
	[gameId3_diskId31, gameId3_diskId32, gameId1_diskId33]
]
```