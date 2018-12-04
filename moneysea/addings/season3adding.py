# coding=utf-8
# 三季报出来后，到来年一季度预报出来前，还会有四季度预报，年报预报，四季度报，年报
# 三季度的增长，是今年年报增长的基础，所以可以参考三季度的季报给出 adding值
# 缺陷：
#    事实上，三季度报出来后，已经导致了一轮市场的价格变化，这个时候接上，是否有意义？
# 
from moneysea.addings.base import Base

class Season3Adding(Base):
    def adding(self):
        r = self._stock.addings()["report"]
        # 假设4季度没有增长，假设上年4季度
        # 4    3 2 1   /  4    3 2 1
        #      -----         -----
        # 1/3   1+r       1/3    1
        new = 1.0/3 + 1 + r
        old = 1.0/3 + 1
        adding = (new - old)/old
        return adding

    def filterout(self):
        return False
