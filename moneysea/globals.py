from moneysea.utils.types import Types
from moneysea.utils.stockidnamemapping import StockIdNameMapping
from moneysea.utils.inputstocks import InputStocks
from moneysea.utils.inputstocks2 import InputStocks2
from moneysea.utils.holdedrecord import HoldedRecord
from moneysea.utils.oneholdedrecord import OneHoldedRecord
from moneysea.utils.prices import Prices

class Globals:
    INSTANCE = None

    def __init__(self):
        if self.INSTANCE is not None:
            raise ValueError("An instantiation already exists!")
        self._types = None
        self._stockidnamemapping = None
        self._inputstocks = None
        self._allholdedrecords = None
        self._latestholdedrecord = None
        self._prices = None

    @classmethod
    def get_instance(cls):
        if cls.INSTANCE is None:
            cls.INSTANCE = Globals()
        return cls.INSTANCE

    def gettypes(self):               #return Types, handle to classfy files
        if self._types == None:
            self._types = Types(self)
        return self._types

    def getstockidnamemapping(self):   #return StockIdNameMapping
        if self._stockidnamemapping  == None:
            self._stockidnamemapping = StockIdNameMapping()
        return self._stockidnamemapping

    def getinputstocks(self):         #return InputStocks
        if self._inputstocks == None:
            self._inputstocks = InputStocks2() #InputStocks()                           #revertback
        return self._inputstocks

    def getallholdedrecords(self):      #return HoldedStocks
        if self._allholdedrecords == None:
            self._allholdedrecords = HoldedRecord()
        return self._allholdedrecords

    def getlatestholdedrecord(self):   #return OneHoldedRecord
        if self._latestholdedrecord == None:
            hr = self.getallholdedrecords()
            self._latestholdedrecord = OneHoldedRecord(hr.getrecordpath(-1))
        return self._latestholdedrecord


    def getprices(self):               #return Prices, handle to prices
        if self._prices == None:
            self._prices = Prices(self) 
        return self._prices


'''
    ::getdefault()              #return Default, handle to default
'''


if __name__ == "__main__":
#    ahr = Globals.get_instance().getallholdedrecords()
#    print ahr.getlist()
#    print ahr.getrecordpath(-1)
    lhr = Globals.get_instance().getlatestholdedrecord()
    print lhr.stocks()
