此文档可作为competition_ONG.py合约的接口文档及使用介绍。

## 流程：

1. 布署合约上链后，需要执行```init```函数，初始化合约。

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
    -2 或254 表示 盘口已经初始化，但比赛结果被录入json,此时，已经调用了```saveGameResultByOracleRes```函数。
    -1 或255 表示 流盘
    0 表示 平局
    1 表示 左赢
    2 表示 右赢
    3 表示 gameId还未被初始化
    4 表示 gameId已被初始化，但diskId不合法
    5 表示 Dev应该先调用```saveGameResultByOracleRes```去获取比赛结果。
```

22. ```getDiskStatus(diskId)```根据diskId查询某盘口是否已经被结算，0表示未结算，1表示已结算。结算也正当于盘口竞猜是否结束。


## 关于核心函数接口参数说明：

23. ```sendReqToOracle(jsonIndex)```， jsonIndex为构造目的url所必须的参数。

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
