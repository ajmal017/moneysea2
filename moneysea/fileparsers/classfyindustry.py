from moneysea.fileparsers.baseparser import BaseParser
from moneysea.stock.common import Common

class ClassfyIndustry(BaseParser):
    def doparse(self):
        self._stocks = []
        with open(self._filepath) as f:
            for line in f:
                items = line.split()
                if len(items) < 12:
                    continue
                idx = Common().stockidsimple(items[0])
                if idx != None:
                    self._stocks.append(idx)
        pass

    def allstocks(self):
        return self._stocks
 
