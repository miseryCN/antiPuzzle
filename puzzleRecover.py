"""
拼图还原算法模块

拼图还原算法：
    拼图每个块现有位置到初始位置的最小路径称为曼哈顿距离
    拼图状态混乱度 = 所有块的曼哈顿距离之和
    移动拼图前，计算每一步移动后的状态混乱度，往混乱度低的方向移动
    如果往几个方向移动后的拼图混乱度相同，那么随机取一个方向
    3*3阶拼图，多次计算，取还原步骤小于150次的实施
    目前只支持3*3拼图，4*4以上需要加上深度优先搜索算法（不会）
"""


from puzzleConfig import PuzzleConfig
from sys import setrecursionlimit
from copy import deepcopy
from random import choice


class PuzzleRecover:

    def __init__(self):
        __author__ = "xiaowei"
        setrecursionlimit(99999999)     #设置最大递归
        self.config = PuzzleConfig()
        self.frontNav = ""
        self.moveIDs = []
        self.step = 0



    def init_puzzle(self):              #生成标准的拼图模型
        count = 0
        puzzleMatrix = {}
        for x in range(self.config.matrix):
            for y in range(self.config.matrix):
                puzzleMatrix[count] = (y,x)
                count += 1
        return puzzleMatrix


    def puzzle_distance(self,status):     #计算拼图模型的整体曼哈顿距离
        initStatus = self.init_puzzle()
        distance = 0
        for order in initStatus.keys():
            distanceX = abs(status[order][0] - initStatus[order][0])
            distanceY = abs(status[order][1] - initStatus[order][1])
            distance += distanceX + distanceY
        return distance


    def move_enable(self,nowStatus):     #计算当前状态可以移动的方向
        blockPosX,blockPosY = nowStatus[self.config.matrix**2 -1]
        enable = []
        if 0 <= blockPosX -1 <=(self.config.matrix-1):  #left
            enable.append(True)
        else:
            enable.append(False)

        if 0 <= blockPosX + 1 <=(self.config.matrix-1): #right
            enable.append(True)
        else:
            enable.append(False)

        if 0 <= blockPosY -1 <= (self.config.matrix-1): #up
            enable.append(True)
        else:
            enable.append(False)

        if 0 <= blockPosY +1 <= (self.config.matrix-1):
            enable.append(True)
        else:
            enable.append(False)
        return enable,(blockPosX,blockPosY)             #返回可移动的列表，0123对应左右上下 和白块的坐标


    def block_move_distance(self,nowStatus):             #计算白块各个方向后移动的曼哈顿距离
        enable, (blockPosX, blockPosY) = self.move_enable(nowStatus)
        moveDistance = {}

        if enable[0]:  # left
            leftStatus = deepcopy(nowStatus)
            leftBlockPos = (blockPosX - 1, blockPosY)
            for leftKey in leftStatus:
                if leftStatus[leftKey] == leftBlockPos:  # get origin left block order
                    break
            leftStatus[self.config.matrix ** 2 - 1], leftStatus[leftKey] = leftBlockPos, (
            blockPosX, blockPosY)  # change block's position
            leftDistance = self.puzzle_distance(leftStatus)
            moveDistance["left"] = leftDistance, leftStatus, leftBlockPos

        if enable[1]:  # right
            rightStatus = deepcopy(nowStatus)
            rightBlockPos = (blockPosX + 1, blockPosY)
            for rightKey in rightStatus:
                if rightStatus[rightKey] == rightBlockPos:  # get origin left block order
                    break
            rightStatus[self.config.matrix ** 2 - 1], rightStatus[rightKey] = rightBlockPos, (blockPosX,
                                                                                       blockPosY)  # change block's position                                 #change left block's position
            rightDistance = self.puzzle_distance(rightStatus)
            moveDistance["right"] = rightDistance, rightStatus, rightBlockPos

        if enable[2]:  # up
            upStatus = deepcopy(nowStatus)
            upBlockPos = (blockPosX, blockPosY - 1)
            for upKey in upStatus:
                if upStatus[upKey] == upBlockPos:  # get origin left block order
                    break
            upStatus[self.config.matrix ** 2 - 1], upStatus[upKey] = upBlockPos, (blockPosX, blockPosY)
            upDistance = self.puzzle_distance(upStatus)
            moveDistance["up"] = upDistance, upStatus, upBlockPos

        if enable[3]:  # down
            downStatus = deepcopy(nowStatus)
            downBlockPos = (blockPosX, blockPosY + 1)
            for downKey in downStatus:
                if downStatus[downKey] == downBlockPos:  # get origin down block order
                    break
            downStatus[self.config.matrix ** 2 - 1], downStatus[downKey] = downBlockPos, (blockPosX, blockPosY)
            downDistance = self.puzzle_distance(downStatus)
            moveDistance["down"] = downDistance, downStatus, downBlockPos

        return moveDistance     #返回一个字典：包括 移动方向：曼哈顿距离，移动后图的坐标，移动后白块的坐标


    def find_best_nav(self,nowStatus):   #寻找最佳方向
        self.step += 1
        moveDistance = self.block_move_distance(nowStatus)
        if not self.frontNav == "":     #非第一次运行
            moveDistance.pop(self.frontNav)  #删除前一步的值 防止回头走

        distanceList = []
        for distant in moveDistance.values():
            distanceList.append(distant[0])      #获取可移动方向上的所有曼哈顿距离
        minDistance = min(distanceList)                        #取得最小的曼哈顿距离

        bestStep = {}
        for nav in moveDistance.keys():
            if moveDistance[nav][0] == minDistance:
                bestStep[nav] = minDistance                    #获取最小曼哈顿距离的移动方向 方向：距离

        finalChoice = choice(list(bestStep.keys()))            #如有多个方向，随机选择一个
        finalStatus = moveDistance[finalChoice]
        self.frontNav = self.config.navAttribute[finalChoice]  #保存本次移动的方向
        moveID = self.navPos(nowStatus,finalStatus[2])
        self.moveIDs.append(moveID)
        self.mDistance = finalStatus[0]
        #print(self.step,self.frontNav,finalStatus[0])
        return finalStatus[1]


    def navPos(self,nowStatus,targetPos):    #计算白块方向坐标
        for order in nowStatus.keys():
            if nowStatus[order] == targetPos:
                break
        id = self.config.orderID[order]
        return id


    def main(self,nowStatus):
        status = self.find_best_nav(nowStatus)
        if self.mDistance > 0:
            self.main(status)
        elif self.mDistance == 0:
            return self.moveIDs
        #elif self.step > 2000:
         #   return None