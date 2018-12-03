from sklearn import linear_model
import matplotlib.pyplot as plt
import numpy as np
from moneysea.globals import Globals
from moneysea.stock.financial import Financial


class Fitting:
    def __init__(self, stocks, n, p):
        self._stocks = stocks
        self._n = n
        self._p = p
        pass

    def run(self):
        prices = Globals.get_instance().getprices()
        mapping = Globals.get_instance().getstockidnamemapping()
        #construct e/q, adding for stocks
        valids = []
        for s in self._stocks:
            fin = Financial(s)
            if not fin.valid():
                continue
            e = fin.pershareearning()
            valids.append((s, mapping.getname(s), prices.price(s), e, fin.addings()))

        print "valids count: ", len(valids)
        ax = []
        ay = []
        
        for v in valids:
            ax.append(v[4]["report"])
            ay.append(v[3]/v[2])

        print ax
        print ay

        plt.scatter(ax, ay, color='blue')
        plt.show()
        pass
