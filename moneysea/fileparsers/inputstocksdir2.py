from moneysea.fileparsers.baseparser import BaseParser
from inputstocksdir import InputStocksDir
from os import listdir

class InputStocksDir2(InputStocksDir):
    def doparse(self):
        self._stocks = {}
        for f in listdir(self._filepath):
            if not "zycwzb_" in f:
                continue
            idx = f[7:13]
            self._stocks[idx] = idx
        pass

    def allstocks(self):           #a dict, key is the stockid, content is the pinyin
        return self._stocks
