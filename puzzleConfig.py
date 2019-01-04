
class PuzzleConfig:

    def __init__(self):
        self.matrix = 3
        self.orderID = {
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
        self.navAttribute = {
            "left" : "right",
            "right" : "left",
            "up" : "down",
            "down" : "up"
        }
