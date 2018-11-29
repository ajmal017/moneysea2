from moneysea.utils.types import Types
from moneysea.utils.stockidnamemapping import StockIdNameMapping

class Globals:
    INSTANCE = None

    def __init__(self):
        if self.INSTANCE is not None:
            raise ValueError("An instantiation already exists!")
        self._types = None
        self._stockidnamemapping = None

    @classmethod
    def get_instance(cls):
        if cls.INSTANCE is None:
            cls.INSTANCE = Globals()
        return cls.INSTANCE

    def gettypes(self):               #return Types, handle to classfy files
        if self._types == None:
            self._types = Types()
        return self._types

    def getstockidnamemapping(self):   #return StockIdNameMapping
        if self._stockidnamemapping  == None:
            self._stockidnamemapping = StockIdNameMapping()
        return self._stockidnamemapping

'''
    ::getholded()               #return Holded, handle to holded files
    ::getstocks()               #return Stocks, handle to all stocks
    :;getprices()               #return Prices, handle to prices
    ::getdefault()              #return Default, handle to default
'''


