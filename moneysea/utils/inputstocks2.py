from moneysea.fileparsers.inputstocksdir2 import InputStocksDir2
from moneysea.config import Config

class InputStocks2:
    def __init__(self):
        self._dir = InputStocksDir2(Config.STOCKS_PATH2)
        self._dir.doparse()
        pass

    def allstocks(self):                #a dict, key is the stockid, content is the pinyin
        return self._dir.allstocks()

    def getpath(self, stockid):               #return path of the stock
        return Config.STOCKS_PATH2 + "/" + "zycwzb_" + stockid + ".html?type=report"

    def getpinyin(self, stockid):
        return self._dir.allstocks()[stockid]

    def getids(self, pinyin):
        all = self._dir.allstocks()
        ids = []
        for a in all:
            if all[a] == pinyin:
                ids.append(a)
        return ids


if __name__ == "__main__":
    iss = InputStocks2()
    print iss.allstocks()
    print iss.getpath("300230")
