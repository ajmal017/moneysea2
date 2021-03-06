# coding=utf-8
from moneysea.globals import Globals
from moneysea.config import Config
from moneysea.fileparsers.financialfile import FinancialFile
import datetime


class Financial:
    # (year, season): baseline for adding caculate
    def __init__(self, stockid, (year, season) = (None, None)):
        # for public access
        self._valid = False
        self._addings = {}

        # for inner access
        self._sid = stockid

        try:
            ins = Globals.get_instance().getinputstocks()
            self._path = ins.getpath(stockid)
        except:
            self.error("no financial dir")
            return

        self._ff = FinancialFile(self._path + "/finance")
        self._ff.doparse()
        self._data = self._ff.allreports()

        try:
            latest = self._ff.latestreport()
        except:
            self.error("no latest financial report")
            return

        # check if latest is up to date
        now = datetime.datetime.now()
        delta = (now.year - latest["year"])*12 + now.month - ((latest["season"] + 1)*3)
        if delta > 3:
            self.error("report is not up to date, discard it")
            return

        if (year == None) or (season == None):
            self._baseline = latest
        else:
            try:
                self._baseline = self._ff.report(year, season)
            except:
                self.error("can not get financial data of %d:%d"%(year, season))
                return
                    
        #check if the financial data is enough
        if not self.ffenough():
            return
    
        if not self.setupaddings():
            print self.error("setup addings failed")
            return

        if self._baseline["per_share_earnings"] == 0:
            return
        self._pershareearning = self._pershareearning()

        self._valid = True

    def _pershareearning(self):
        #最新季报净利润/每股收益 = 总股数
        totalstocks = self._baseline["profit"] / self._baseline["per_share_earnings"]
        #每股收益 = 最近365天净利润 / 总股数
        e = self.get365profit(self._baseline) / totalstocks
        return e


    def error(self, err):
        print Globals.get_instance().getstockidnamemapping().getname(self._sid), self._sid, ":", err

    def ffenough(self):
        # adding caculate
        # {2018:4321} {2017:4321} {2016:4321} {2015:4321}
        # {2018: 321} {2017:4321} {2016:4321} {2015:4321}
        # {2018:  21} {2017:4321} {2016:4321} {2015:4321}
        # {2018:   1} {2017:4321} {2016:4321} {2015:4321}
        #
        # report adding: 
        # 365 adding: 
        # lastyear adding: from 2016->2017

        lyear = self._baseline["year"]
        lseason = self._baseline["season"]
        
        # be sure 3 years financial data are valid
        for s in range(0, lseason):
            r = self._ff.report(lyear, s)
            if r == None:
                self.error("invalid financial report in %d:%d"%(lyear, s))
                return False

        for s in range(0, 4):
            r = self._ff.report(lyear - 1, s)
            if r == None:
                self.error("invalid financial report in %d:%d"%(lyear - 1, s))
                return False

        for s in range(lseason, 4):
            r = self._ff.report(lyear - 2, s)
            if r == None:
                self.error("invalid financial report in %d:%d"%(lyear - 2, s))
                return False
        return True


    def setupaddings(self):
        ret, val = self.reportadding()
        if not ret:
            return False
        self._addings["report"] = val

        ret, val = self._365adding()
        if not ret:
            return False
        self._addings["365"] = val

        ret, val = self.historyadding()
        if not ret:
            return False
        self._addings["history"] = val
        return True

    def historyadding(self):
        year = self._baseline["year"]
        l1year = self._ff.yearreport(year - 1)
        l2year = self._ff.yearreport(year - 2)
        report = l1year["profit_adding"] / 100

        #verifying it
        if l2year["profit"] < Config.MINIMAL_PROFIT: #negative is discard
            return self.negativeadding(l2year["profit"], l1year["profit"])

        val = (l1year["profit"] - l2year["profit"])/l2year["profit"]
        if abs(report - val) > 0.10:
            self.error("caculate history adding, verifying failed ")
            return (False, 0)

        return True, report

    def _365adding(self):
        latest_profit = self.get365profit(self._baseline)

        prev_season = self._ff.report(self._baseline["year"] - 1, self._baseline["season"])
        prev_profit = self.get365profit(prev_season)

        if prev_profit < Config.MINIMAL_PROFIT: #negative is discard
            return self.negativeadding(prev_profit, latest_profit)

        val = (latest_profit - prev_profit)/prev_profit
        return True, val

    def negativeadding(self, a1, a2):
        if a2 < Config.MINIMAL_PROFIT:
            self.error("Discard it as recent profit is too small or negative: " + str(a2))
            return (False, 0)
        tmp = abs(a1) + abs(a2)
        v1 = tmp + a1
        v2 = tmp + a2
        vv = (v2 - v1)/v1
        return (True, vv)

    def reportadding(self):
        bs = self._baseline
        report = bs["profit_adding"] / 100

        #verifying it
        bs_profit = bs["profit"]
        last = self._ff.report(bs["year"] - 1, bs["season"])
        last_profit = last["profit"]

        if last_profit < Config.MINIMAL_PROFIT: #negative is discard
            return self.negativeadding(last_profit, bs_profit)

        val = (bs_profit - last_profit)/last_profit
        if abs(val - report) > 0.10:
            self.error("caculate latest report adding, verifying failed ")
            return (False, 0)
        return (True, report)

    def get365profit(self, fd):
        prev_season = self._ff.report(fd["year"] - 1, fd["season"])
        prev_year = self._ff.yearreport(fd["year"] - 1)

        profit365 = fd["profit"] + prev_year["profit"] - prev_season["profit"]
        return profit365




        
    ######################################## public ################################################################
    def addings(self):
        return self._addings

    def valid(self):
        return self._valid

    def pershareearning(self):
        return self._pershareearning


if __name__ == "__main__":
    fin = Financial("300230")
    if fin.valid():
        print fin.addings()
        print fin.pershareearning()
