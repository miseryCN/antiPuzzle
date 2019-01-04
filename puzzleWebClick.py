"""
使用selenium自动化测试工具操作网页拼图
"""
from selenium import webdriver
from puzzleRecover import PuzzleRecover
from time import sleep

image = "image2"
wd = webdriver.Chrome()
url = "http://puzzle.xiaoweigod.com"
orderID = {
            0 : "00",
            1: "10",
            2: "20",
            3: "01",
            4: "11",
            5: "21",
            6: "02",
            7: "12",
            8: "22"
        }

def recover_puzzle():
    wd.get(url)
    initStatus = {}
    wd.find_element_by_id(image).click()
    for order,id in orderID.items():
        rect = wd.find_element_by_id(id).rect
        posX = int((rect["x"] - 300) / 200)
        posY = int(rect["y"] / 200)
        initStatus[order] = (posX, posY)
    print(initStatus)

    moveIDs = find_step(initStatus)
    for ID in moveIDs:
        wd.find_element_by_id(ID).click()
        sleep(0.01)

def find_step(initStatus):
    while True:
        recover = PuzzleRecover()
        recover.main(initStatus)
        moveIDs = recover.moveIDs
        print("计算最佳步数-->",len(moveIDs))
        if len(moveIDs) < 150:
            break
    print("计算完成，共",len(moveIDs),"步！")
    if not moveIDs == None:
        return moveIDs

if __name__ == '__main__':
    recover_puzzle()