
# coding=utf-8
# 当季净利润，扣非净利润，营业额三个指标的增长率，选择三个指标的增长率都靠前的
# 以过去3~5年的营业额的增长平均值，做为考量一家公司的经营能力, 取其为增长参数计算delta


from moneysea.globals import Globals
from moneysea.stock.stock import Stock
from moneysea.addings.addingfilter import AddingFilter


class AswAdding(AddingFilter):
    def a(self):
        return self._a

    def addingfilter(self):
        latest = self._baseline
        if latest["profit_adding"] == None or latest["profit2_adding"] == None or latest["sales_adding"] == None or latest["sales"] == None:
            return (False, "FF-LATEST")

        y = latest["year"]

        last = self._ff.yearreport(y - 1)
        if last == None or last["sales"] == None:
            return (False, "FF-" + str(y - 1))

        old = self._ff.yearreport(y - 3)
        if old == None or old["sales"] == None:
            return (False, "FF-" + str(y - 3))

        self._addings["profit_adding"] = latest["profit_adding"]
        self._addings["profit2_adding"] = latest["profit2_adding"]
        self._addings["sales_adding"] = latest["sales_adding"]

        if old["sales"] < 10000000:
            return (False, "FF-" + str(y - 4))

        avg = ((last["sales"]/old["sales"]) ** (1.0/2)) - 1
        self._a = avg
        return (True, "OK")

class AverageSalesWay:
    def __init__(self):
        pass

    AF = AswAdding

    def run(self):
        iss = Globals.get_instance().getinputstocks()
        self._all = {}
        self._total = len(iss.allstocks())

        stat = {}
        for s in iss.allstocks():
            af = self.AF(s)
            stock = Stock(s, af)
            vlds = stock.ffvalid()
            if not vlds[0]:
                try:
                    stat[vlds[1]] += 1
                except:
                    stat[vlds[1]] = 1
                continue
            self._all[s] = stock
        self.AF.stat(stat)

        L1 = []
        L2 = []
        L3 = []

        for s in self._all:
            ss = self._all[s]

            self.addin(L1, ss, "profit_adding")
            self.addin(L2, ss, "profit2_adding")
            self.addin(L3, ss, "sales_adding")


        end = len(L1)/2
        M1 = L1[0:end]
        M2 = L2[0:end]
        M3 = L3[0:end]

        NN = []
        for v in M1:
            if (v in M2) and (v in M3):
                self.addin2(NN, v)

        for v in NN:
            print v.name(), v.addings(), v.a(),  v.dratio()

        pass


    def addin(self, LL, stock, tag):
        new = stock.addings()[tag]
        index = 0
        for v in LL:
            tmp = v.addings()[tag]
            if new > tmp:
                LL.insert(index, stock)
                break
            index += 1

        if index >= len(LL):
            LL.append(stock)
        
    def addin2(self, LL, stock):
        new = stock.dratio()
        index = 0
        for v in LL:
            tmp = v.dratio()
            if new > tmp:
                LL.insert(index, stock)
                break
            index += 1

        if index >= len(LL):
            LL.append(stock)













