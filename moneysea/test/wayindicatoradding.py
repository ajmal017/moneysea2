# coding=utf-8
# 研究某些指标，该指标统计出的，比如下一季度/年度的净利率增长率，以及接下来5年的增长率
# 1. 短期操作
# 根据上述指标，圈出下季度的预期增长率，对于业绩看好的公司，在价格回调时买入
#     --- 所以熊市也能挣钱，尤其对于震荡型的大环境，好业绩的公司股价会回调，正好收入囊中
# 2. 长期操作
# 长期操作，参考dratio值，也是用指标圈出股票的预期增长率，然后用dratio排序
# 短期操作时，也应该在dratio排前的公司里选择
# 至于何时卖出进行短期操作 --- 待考虑
#
# 细节：
# a. 对于5年平均净利率增长的计算
#   . 当基准净利率太小或小于零时，是非常不好计算的. 这时往上一年取，如果不行再往上年取值
#   . 5年平均净利率增长率，可以取 {4，5，6}年中间的一个，避免某一年份下跌严重，对评估产生影响
# b. 
#
# 评估项目：
# 1. 3季度财报出来后，预测年报增长率
#    . 3季度净利率增长率 > 50%，得出的年报增长率分布
#
#
#
#
from moneysea.globals import Globals
from moneysea.stock.stock import Stock
from moneysea.addings.addingfilter import AddingFilter

#from sklearn import linear_model
#import matplotlib.pyplot as plt
#import numpy as np


class IndicatorAdding(AddingFilter):
    def addingfilter(self):
        bl = self._baseline

        try:
            y = self._ff.yearreport(bl["year"])
#            if y["profit_adding"] == None:
#                return (False, "FF-1")
            if bl["profit_adding"] < 60:
                return (False, "DISCARD")
            if bl["profit2_adding"] < 0:
                return (False, "DISCARD")
            if bl["sales_adding"] < 0:
                return (False, "DISCARD")
            if bl["profit"] < 500000000:
                return (False, "DISCARD")
        except:
            return (False, "FF-2")

        return (True, "OK")

class WayIndicatorAdding:
    def __init__(self):
        pass

    AF = IndicatorAdding
    START = 2007
    END = 2018

    def run(self, arg):
        iss = Globals.get_instance().getinputstocks()
        self._all = iss.allstocks()
        self._total = len(self._all)

        if arg == "season3":
            self.season3_year()
            self.season3_result()

        pass

    def season3_result(self):
        print ""
        for s in self._all:
            af = self.AF(s)
            stock = Stock(s, af)
            ffv = stock.ffvalid()
            if not ffv[0]:
                continue
            print stock.name(), stock.id()


    def season3_year(self):
        season = 2
        for y in range(self.START, self.END):
            self.s3y_baseline(y, season)

    def s3y_baseline(self, y, season):
        select = []
        for s in self._all:
            af = self.AF(s, (y, season))
            stock = Stock(s, af)
            ffv = stock.ffvalid()
            if not ffv[0]:
#                print stock.name(), ffv[1]
                continue
            select.append(stock)
#            if len(select) > 15:
#                break
        self.s3y_output(y, select)

    def s3y_output(self, y, select):
        total = len(select)

        print ""
        print "year:", y, " total:", total       

        stat = {}
        for i in range(-100, 100, 10):
            stat[i] = 0
        for s in select:
            fd = s.ff().yearreport(y)
#            print fd["profit_adding"]
            for item in stat:
                if fd["profit_adding"] > item:
                    stat[item] += 1

        keys = stat.keys()
        keys.sort()
        for k in keys:
            print "%8d"%(k),

        print ""
        for k in keys:
            print "%8.2f"%((stat[k]) * 100.0 / total),
        pass


















