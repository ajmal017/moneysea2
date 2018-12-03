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
        ay2 = []
        
        for v in valids:
            adding = v[4]["history"]
            ax.append(adding)
            ay.append(v[3]/v[2])
            eq = (((self._p+1)/(adding+1))**self._n) * self._p
            ay2.append(eq)
            q = v[2] / eq
            print v[1], v[3], v[2], ">", q, " [", adding, (q - v[2])/v[2], eq, "]"

        print ax
        print ay

        plt.scatter(ax, ay, color='blue')
        plt.scatter(ax, ay2, color='red')
        plt.show()
        pass
