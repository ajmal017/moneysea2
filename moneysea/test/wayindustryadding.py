# coding=utf-8
# 1. 通过行业净利润随着年份的变化，推算接下来5年的增长趋势，做为公司增长依据
#    因为行业数据比较齐备，而且变化不会太大，有更高的拟合价值
#    该模型可以验证，比如对2015，2016，2017进行验证
# 2. 选择行业里面，净利润增长快于行业的公司 (可以通过积分方法，或者说求面积方法)
#    亦可以验证, 或者给出公司增长预测算法，或者从中挑出优质公司
# 3. 当季净利润，扣非净利润，营业额三个指标的增长率，选择三个指标的增长率都靠前的 ---- 参考 averagesalesway.py
#
#
#
#
#
#
#
#
#
#
from moneysea.globals import Globals
from moneysea.stock.stock import Stock
from moneysea.addings.addingfilter import AddingFilter

#from sklearn import linear_model
import matplotlib.pyplot as plt
#import numpy as np


class IndustryAdding(AddingFilter):
    def addingfilter(self):
        for i in range(WayIndustryAdding.START, WayIndustryAdding.END):
            r = self._ff.yearreport(i)
            if r == None or r["profit"] == None:
                return (False, "No Profit")
        return (True, "OK")

class WayIndustryAdding:
    def __init__(self):
        pass

    AF = IndustryAdding
    START = 2006
    END = 2018

    def run(self, typ):
        types = Globals.get_instance().gettypes()
        slist = types.liststocks(typ)
        self._slist = []
        for sid in slist:
            af = self.AF(sid)
            stock = Stock(sid, af)
            vlds = stock.ffvalid()
            if not vlds[0]:
                continue
            self._slist.append(stock)
        
        print "stocks: ", len(self._slist)
        self.draw()

    def draw(self):
        ax = []
        ay = []
        
        prev = 0
        for i in range(self.START, self.END):
            profit = self.getprofit(i) / 10000
            if prev != 0:
                delta = (profit - prev)/prev
                ax.append(i)
                ay.append(delta)
            prev = profit

        plt.scatter(ax, ay, color='blue')
        plt.show()


    def getprofit(self, year):
        total = 0
        for s in self._slist:
            ff = s.ff()
            r = ff.yearreport(year)
            '''
            if r == None:
                continue
            if r["profit"] == None:
                continue
            '''
            total += (r["profit"] / 10000)
        return total




