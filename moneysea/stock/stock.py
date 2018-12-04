
from moneysea.globals import Globals
from moneysea.stock.financial import Financial
from moneysea.config import Config


class Stock:
    def __init__(self, sid, n = None, p = None):
        self._sid = sid
        self._name = Globals.get_instance().getstockidnamemapping().getname(sid)
        if self._name == "--":
            raise Exception("Incorrect stock id")

        types = Globals.get_instance().gettypes()
        industry = types.industry(sid)
        if n == None:
            try:
                n = int(industry["n"])
            except:
                n = Config.N

        if p == None:
            try:
                p = float(industry["p"])
            except:
                p = Config.P

        self._n = n
        self._p = p
        self._industry = industry

        self._fin = Financial(sid)
        if not self._fin.valid():
            return

    def id(self):
        return self._sid

    def name(self):
        return self._name

    def types(self):
        types = Globals.get_instance().gettypes()
        return types.stocktypes(self._sid)

    def ffvalid(self):
        return self._fin.valid()

    def addings(self):
        return self._fin.addings()

    def n(self):
        return self._n

    def p(self):
        return self._p

    def industry(self):
        try:
            return self._industry["name"]
        except:
            return ""

    def set_adding(self, a):
        self._a =a

    def a(self):
        return self._a

    def e(self):
        return self._fin.pershareearning()

    def price(self):
        prices = Globals.get_instance().getprices()
        return prices.price(self._sid)

    #e/q = (((p+1)/(a+1))**n) * p
    def eq(self):
        if self._a < -1.0:
            raise Exception("Do not support when adding value is small than -1.0")
        return (((self._p + 1)/(self._a + 1))**self._n) * self._p

    def q(self):
        return self._fin.pershareearning() / self.eq()

    def dratio(self):
        price = self.price()
        return (self.q() - price)/price

