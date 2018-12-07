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
#   . 当基准净利率太小或小于零时，是非常不好计算的. 这时往后一年取，如果不行放弃
#   . 5年平均净利率增长率，可以取 {4，5，6}年中间的一个，避免某一年份下跌严重，对评估产生影响
# b. 
#
# 评估项目：
# 1. 3季度财报出来后，预测年报增长率
#    . 3季度净利率增长率 > 50%，得出的年报增长率分布
#
# 2. 根据年报预测未来5年平均增长率
#    . 前n年的平均增长率和后5年的平均增长率高度相关吗？
#
from moneysea.globals import Globals
from moneysea.stock.stock import Stock
from moneysea.addings.addingfilter import AddingFilter
from moneysea.config import Config

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


class Average5Adding(AddingFilter):
    def addingfilter(self):
        bl = self._baseline
        y = bl["year"]
        try:
            for i in range(0, 6):
                r = self._ff.yearreport(y + i)
#                print r["year"], r["profit"] 

            r0 = self._ff.yearreport(y)
            r1 = self._ff.yearreport(y + 1)
            if r0["profit"] < Config.MINIMAL_PROFIT or r1["profit"] < Config.MINIMAL_PROFIT:
                return (False, "DISCARD")

            for i in range(1, 4):
                r = self._ff.yearreport(y - i)
                r["profit_adding"]
                r["profit2_adding"]
                r["sales_adding"]

#                print y-i, r["sales_adding"]
                
            r0 = self._ff.yearreport(y - 3)
            r1 = self._ff.yearreport(y - 2)
            if r0["profit"] < Config.MINIMAL_PROFIT or r1["profit"] < Config.MINIMAL_PROFIT:
                return (False, "DISCARD")

            r1 = self._ff.yearreport(y - 1)

        except Exception as e:
            return (False, "DISCARD")

        avg = self.nyearprofit_adding(self._ff, y - 3, y + 1)
        if avg < 0.2 or bl["sales_adding"] < 10 or r1["sales_adding"] < 10:
            return (False, "NOT")
        '''
        for i in range(1, 4):
           r = self._ff.yearreport(y - i)
           if r["profit_adding"] < 20:
               return (False, "NOT")
           if r["profit2_adding"] < 20:
               return (False, "NOT")
           if r["sales_adding"] < 20:
               return (False, "NOT")
        '''
        return (True, "OK")

    # start(0) 1 2 3 4 5 end(6)
    #     base: 0 or 1 (if 0 is negative or too small)
    #     last: max(4, 5)
    # end: last + 1
    def nyearprofit_adding(self, ff, start, end):
        ival = end - start - 1

        fd = ff.yearreport(start)
        pstart = fd["profit"]
        if pstart < Config.MINIMAL_PROFIT:
            fd2 = ff.yearreport(start + 1)
            pstart = fd2["profit"]
            ival -= 1
        if pstart < Config.MINIMAL_PROFIT:
            print "it should not happen"

        fd = ff.yearreport(end - 1)
        pend_1 = fd["profit"]
        if pend_1 > 0:
            delta_1 = (pend_1 / pstart) ** (1.0/ival) - 1

        fd = ff.yearreport(end - 2)
        pend_2 = fd["profit"]
        if pend_2 > 0:
            delta_2 = (pend_2 / pstart) ** (1.0/(ival - 1)) - 1

        if pend_1 <= 0 or pend_2 <= 0:
            return -1.9999

#        print pstart, (delta_2, ival - 1, pend_2), (delta_1, ival, pend_1)
        if delta_1 > delta_2:
            return delta_1
        else:
            return delta_2



class WayIndicatorAdding:
    def __init__(self):
        pass

    S3AF = IndicatorAdding
    START = 2011
    END = 2013
    A5AF = Average5Adding

    def run(self, arg):
        iss = Globals.get_instance().getinputstocks()
        self._all = iss.allstocks()
        self._total = len(self._all)

        if arg == "season3":
            self.season3_year()
            self.season3_result()
        elif arg == "average5":
            self.average5()
        pass

    def average5(self):
        for y in range(self.START, self.END):
            self.avg5_baseline(y)

    def avg5_baseline(self, y):
        select = []
        for s in self._all:
            af = self.A5AF(s, (y, 3))
            stock = Stock(s, af)
            ffv = stock.ffvalid()
            if not ffv[0]:
                continue
            
            select.append((stock.name(), stock.id(), self.nyearprofit_adding(stock, y, y + 6)))
#            break
#            if len(select) > 15:
#                break

        self.avg5_output(y, select)
        pass

    def avg5_output(self, y, select):
        total = len(select)

        print ""
        print "year:", y, " total:", total       

        stat = {}
        for i in range(-100, 100, 10):
            stat[i] = 0
        for s in select:
            for item in stat:
                if s[2] > (item/100.0):
                    stat[item] += 1

        keys = stat.keys()
        keys.sort()
        for k in keys:
            print "%8d"%(k),

        print ""
        for k in keys:
            print "%8.2f"%((stat[k]) * 100.0 / total),
        pass

    # start(0) 1 2 3 4 5 end(6)
    #     base: 0 or 1 (if 0 is negative or too small)
    #     last: max(4, 5)
    # end: last + 1
    def nyearprofit_adding(self, stock, start, end):
        ival = end - start - 1

        fd = stock.ff().yearreport(start)
        pstart = fd["profit"]
        if pstart < Config.MINIMAL_PROFIT:
            fd2 = stock.ff().yearreport(start + 1)
            pstart = fd2["profit"]
            ival -= 1
        if pstart < Config.MINIMAL_PROFIT:
            print "it should not happen"

        fd = stock.ff().yearreport(end - 1)
        pend_1 = fd["profit"]
        if pend_1 > 0:
            delta_1 = (pend_1 / pstart) ** (1.0/ival) - 1

        fd = stock.ff().yearreport(end - 2)
        pend_2 = fd["profit"]
        if pend_2 > 0:
            delta_2 = (pend_2 / pstart) ** (1.0/(ival - 1)) - 1

        if pend_1 <= 0 or pend_2 <= 0:
            return -1.9999

#        print pstart, (delta_2, ival - 1, pend_2), (delta_1, ival, pend_1)
        if delta_1 > delta_2:
            return delta_1
        else:
            return delta_2

    def season3_result(self):
        print ""
        for s in self._all:
            af = self.S3AF(s)
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
            af = self.S3AF(s, (y, season))
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


















