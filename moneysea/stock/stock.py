
from moneysea.globals import Globals
from moneysea.stock.financial import Financial
from moneysea.config import Config


class Stock:
    def __init__(self, sid, af):
        self._sid = sid
        self._name = Globals.get_instance().getstockidnamemapping().getname(sid)
        if self._name == "--":
            af.indicatefail("Incorrect stock id")

        types = Globals.get_instance().gettypes()
        industry = types.industry(sid)
        self._industry = industry
        self._af = af

    def id(self):
        return self._sid

    def name(self):
        return self._name

    def types(self):
        types = Globals.get_instance().gettypes()
        return types.stocktypes(self._sid)

    def price(self):
        prices = Globals.get_instance().getprices()
        return prices.price(self._sid)

    def industry(self):
        try:
            return self._industry["name"]
        except:
            return ""

    # financial 
    def ffvalid(self):
        fvld = self._af.ffvalid()
        if not fvld[0]:
            return fvld

        if self.price() < 0.000001:
            return (False, "PRICE")

        return self._af.ffvalid()

    def addings(self):
        return self._af.addings()

    def n(self):
        return self._af.n()

    def p(self):
        return self._af.p()

    def a(self):
        return self._af.a()

    def e(self):
        return self._af.e()

    def ff(self):
        return self._af._ff

    def baseline(self):
        return self._af._baseline


    #e/q = (((p+1)/(a+1))**n) * p
    def eq(self):
        n = self._af.n()
        p = self._af.p()
        a = self._af.a()

        return (((p + 1)/(a + 1))**n) * p

    def q(self):
        return self._af.e() / self.eq()

    def dratio(self):
        price = self.price()
        return (self.q() - price)/price

