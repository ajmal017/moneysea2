from moneysea.fileparsers.inputstocksdir import InputStocksDir
from moneysea.config import Config

class InputStocks:
    def __init__(self):
        self._dir = InputStocksDir(Config.STOCKS_PATH)
        self._dir.doparse()
        pass

    def allstocks(self):                #a dict, key is the stockid, content is the pinyin
        return self._dir.allstocks()

    def getpath(stockid):               #return path of the stock
        pass

    def getpinyin(self, stockid):
        return self._dir.allstocks()[stockid]

    
