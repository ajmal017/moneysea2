# coding=utf-8
from moneysea.globals import Globals
from moneysea.config import Config
from moneysea.fileparsers.financialfile import FinancialFile
from moneysea.fileparsers.ffnetease import FFNetEase
import datetime

class AddingFilter:
    def __init__(self, stockid, (year, season) = (None, None), n = None, p = None):
        # for public access
        self._valid = (False, "Unknown")
        self._addings = {}

        # for inner access
        self._sid = stockid

        types = Globals.get_instance().gettypes()
        industry = types.industry(stockid)
        if n == None:
            try:
                n = int(industry["n"])
            except:
                n = Config.N

        if p == None:
            try:
                p = float(industry["p"])
            except:
                p = Config.P

        self._n = n
        self._p = p

        # access the financial file
        try:
            ins = Globals.get_instance().getinputstocks()
            self._path = ins.getpath(stockid)
#            self._ff = FinancialFile(self._path + "/finance")    #revertback
            self._ff = FFNetEase(self._path)    #revertback
            self._ff.doparse()

            latest = self._ff.latestreport()
            # check if latest is up to date
            now = datetime.datetime.now()
            delta = (now.year - latest["year"])*12 + now.month - ((latest["season"] + 1)*3)
            if delta > 3:
                raise Exception("FF is not up to date")

            if (year == None) or (season == None):
                self._baseline = latest
            else:
                self._baseline = self._ff.report(year, season)

            self._pershareearning = self._pershareearning()
        except:
            self._valid = (False, "FF")     
            # in case
            # financial file is not exist
            # latest financial data is out of date
            # no financial data for baseline season
            # baseline season: per_share_earnings is None or zero; or profit is None
            # previous season: profit is None
            # previous year: profit on season 4 is None
            return
        self._data = self._ff.allreports()

        self._valid = self.addingfilter()
        pass

    def _pershareearning(self):
        #最新季报净利润/每股收益 = 总股数
        totalstocks = self._baseline["profit"] / self._baseline["per_share_earnings"]
        #每股收益 = 最近365天净利润 / 总股数
        e = self.get365profit(self._baseline) / totalstocks
        return e

    def get365profit(self, fd):
        prev_season = self._ff.report(fd["year"] - 1, fd["season"])
        prev_year = self._ff.yearreport(fd["year"] - 1)

        profit365 = fd["profit"] + prev_year["profit"] - prev_season["profit"]
        return profit365


    # template, for child access
    def historyadding(self):
        year = self._baseline["year"]
        l1year = self._ff.yearreport(year - 1)
        l2year = self._ff.yearreport(year - 2)
        report = l1year["profit_adding"] / 100

        val = (l1year["profit"] - l2year["profit"])/l2year["profit"]
        if abs(report - val) > 0.10:
            return (False, 0, "History Adding Verify")

        return (True, report, "OK")

    def _365adding(self):
        latest_profit = self.get365profit(self._baseline)

        prev_season = self._ff.report(self._baseline["year"] - 1, self._baseline["season"])
        prev_profit = self.get365profit(prev_season)

        if prev_profit < Config.MINIMAL_PROFIT: #negative is discard
            return (False, 0, "365 PROFIT SMALL")

        val = (latest_profit - prev_profit)/prev_profit
        return True, val

    def reportadding(self):
        bs = self._baseline
        report = bs["profit_adding"] / 100

        #verifying it
        bs_profit = bs["profit"]
        last = self._ff.report(bs["year"] - 1, bs["season"])
        last_profit = last["profit"]

        val = (bs_profit - last_profit)/last_profit
        if abs(val - report) > 0.10:
            return (False, 0, "Report Adding Verify")
        return (True, report, "OK")

    # for public access
    def indicatefail(self, tag):
        self._valid = (False, tag)
        pass
    def ffvalid(self):
        return self._valid

    def n(self):
        return self._n

    def p(self):
        return self._p

    def e(self):
        return self._pershareearning

    def addings(self):
        return self._addings

    @classmethod
    def statinfo(cls, key):
        if key == "PRICE":
            return "Price is zero"
        elif key == "FF":
            return '''
        Financial data invalid, in case:
            Financial file is not exist
            Latest financial data is out of date
            No financial data for baseline season
            Baseline season: per_share_earnings is None or zero; or profit is None
            Previous season: profit is None
            Previous year: profit on season 4 is None
            '''
    @classmethod
    def stat(cls, stats):
        print ""
        print "Statistics Info"
        for s in stats:
            print " ", s,"(",stats[s],")"
            print "\t", cls.statinfo(s)
        print ""

    # for inherent and public access
    def a(self):
        return (1.0 - 1.0)

    # for inherient
    def addingfilter(self):
        return (True, "OK")





if __name__ == "__main__":
    af = AddingFilter("300230")
    if af.ffvalid()[0]:
        print af.e()

