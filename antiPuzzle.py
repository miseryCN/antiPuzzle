from copy import deepcopy
from time import sleep
from random import choice
import sys

sys.setrecursionlimit(1000000)

class AntiPuzzle:
    def __init__(self):
        self.matrix = 3
        self.frontNav = ""
        self.attributeNav = {
            "up" : "down",
            "down":"up",
            "left":"right",
            "right":"left"
        }
        self.step = 0


    def create_init(self):
    #假装生成一个3*3拼图
       count = 0
       matrixPos = {}
       for x in range(self.matrix):
           for y in range(self.matrix):
               matrixPos[count] = (y,x)
               count += 1
       return matrixPos


    def get_now_status(self):
        #测试生成一个现在的坐标
        position = {
            0:(1,1),
            1:(0,0),
            2:(0,2),
            3:(2,0),
            4:(0,1),
            5:(1,2),
            6:(1,0),
            7:(2,1),
            8:(2,2)
        }
        return position


    def c(self,status):
         #计算当前的曼哈顿距离
        init_status = self.create_init()
        distance = 0
        for order in init_status.keys():
            distanceX = abs(status[order][0] - init_status[order][0])
            distanceY = abs(status[order][1] - init_status[order][1])
            distance += distanceX + distanceY
        return distance


    #计算白块是否可以上下左右移动 顺序为 left right up down
    def enableMove(self,now_status):
        blockPosX,blockPosY = now_status[self.matrix**2 -1]
        enable = []
        if 0 <= blockPosX -1 <=(self.matrix-1):  #left
            enable.append(True)
        else:
            enable.append(False)

        if 0 <= blockPosX + 1 <=(self.matrix-1): #right
            enable.append(True)
        else:
            enable.append(False)

        if 0 <= blockPosY -1 <= (self.matrix-1): #up
            enable.append(True)
        else:
            enable.append(False)

        if 0 <= blockPosY +1 <= (self.matrix-1):
            enable.append(True)
        else:
            enable.append(False)
        return enable


    #计算移动后的曼哈顿距离
    def cMove(self,now_status):
        enable = self.enableMove(now_status)
        blockPosX,blockPosY = now_status[self.matrix**2 -1]
        moveDistance = {}

        if enable[0]: #left
            leftStatus = deepcopy(now_status)
            leftBlockPos = (blockPosX-1,blockPosY)
            for leftKey in leftStatus:
                if leftStatus[leftKey] == leftBlockPos:                             #get origin left block order
                    break
            leftStatus[self.matrix**2-1],leftStatus[leftKey] = leftBlockPos,(blockPosX,blockPosY)                          #change block's position
            leftDistance = self.c(leftStatus)
            moveDistance["left"] = leftDistance,leftStatus

        if enable[1]: #right
            rightStatus = deepcopy(now_status)
            rightBlockPos = (blockPosX+1,blockPosY)
            for rightKey in rightStatus:
                if rightStatus[rightKey] == rightBlockPos:                             #get origin left block order
                    break
            rightStatus[self.matrix ** 2 - 1], rightStatus[rightKey] = rightBlockPos, (blockPosX, blockPosY)  #change block's position                                 #change left block's position
            rightDistance = self.c(rightStatus)
            moveDistance["right"] = rightDistance,rightStatus

        if enable[2]: #up
            upStatus = deepcopy(now_status)
            upBlockPos = (blockPosX,blockPosY-1)
            for upKey in upStatus:
                if upStatus[upKey] == upBlockPos:                             #get origin left block order
                    break
            upStatus[self.matrix ** 2 - 1], upStatus[upKey] = upBlockPos, (blockPosX, blockPosY)
            upDistance = self.c(upStatus)
            moveDistance["up"] = upDistance,upStatus

        if enable[3]: #down
            downStatus = deepcopy(now_status)
            downBlockPos = (blockPosX,blockPosY+1)
            for downKey in downStatus:
                if downStatus[downKey] == downBlockPos:                             #get origin left block order
                    break
            downStatus[self.matrix ** 2 - 1], downStatus[downKey] = downBlockPos, (blockPosX, blockPosY)
            downDistance = self.c(downStatus)
            moveDistance["down"] = downDistance,downStatus

        return moveDistance


    def anti_cycle(self,now_status):
        #防止陷入死循环
        self.step += 1
        moveDistance = self.cMove(now_status)
        if not self.frontNav == "" and self.frontNav in moveDistance.keys():
            moveDistance.pop(self.frontNav)
        ValueList = []
        #查找moveDistance的最小distance
        for values in moveDistance.values():
            ValueList.append(values[0])
        minValue = min(ValueList)
        minStep = {}
        for nav in moveDistance.keys():
            if moveDistance[nav][0] == minValue:
                minStep[nav] = minValue
        minNavList = list(minStep.keys())
        finalNav = choice(minNavList)
        #finalNav = min(minNavList)
        self.frontNav = self.attributeNav[finalNav]
        finalStatus = moveDistance[finalNav]
        print(self.step,finalNav,finalStatus[0],finalStatus[1])
        if finalStatus[0] == 0:     #zheli
            exit()
        return finalStatus[1]


    def main(self,now_status):
        status = self.anti_cycle(now_status)
        #sleep(0.1)
        self.main(status)                       #is it right?

if __name__ == '__main__':
    s = AntiPuzzle()
    s.main(s.get_now_status())