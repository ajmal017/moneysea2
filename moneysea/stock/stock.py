
from moneysea.globals import Globals
from moneysea.stock.financial import Financial


class Stock:
    def __init__(self, sid):
        self._sid = sid
        self._name = Globals.get_instance().getstockidnamemapping().getname(sid)
        if self._name == "--":
            raise Exception("Incorrect stock id")

        self._fin = Financial(sid)

    def name(self):
        return self._name

    def ffvalid(self):
        return self._fin.valid()
