# coding=utf-8

from moneysea.fileparsers.baseparser import BaseParser
import datetime

#financial data are stored in self._data{}
# _data[0] _data[1] _data[2] _data[3] --- 2009 first, second, third, forth season report data
# _data[4] _data[5] _data[6] _data[7] --- 2010 first, second, third, forth season report data

class FFNetEase(BaseParser):
    MAX_YEARS = 18  #max years of data to save for parsing

    def __init__(self, filepath):
        BaseParser.__init__(self, filepath)

        now = datetime.datetime.now()

        #[self._start, self._end]
        self._start = now.year - self.MAX_YEARS + 1 #start year
        self._end = now.year                        #end year

        self._data = {}
        for i in range(self.MAX_YEARS * 4):
            self._data[i] = None
        pass


    def doparse(self):
        #build datalist for parsing
        datalist = list()
        with open(self._filepath) as f:
            for line in f:
                items = line.split(",")
                if len(items) < 8:
                    continue
                datalist.append(items)

        i = 0
        self._oldest = 100000
        self._latest = -10000
        if len(datalist) < 1:
            return

        for date in datalist[0]:
            year, season = self.year_season(date)
            index = self.getindex(year, season)
            if index == -1:
                i += 1
                continue

            d = self.constructdata(year, season, datalist, i)
            if d == None:    #if key data is missing
                break
            self._data[index] = d

            if index > self._latest:
                self._latest = index
            if index < self._oldest:
                self._oldest = index

            i += 1

        for index in range(self._oldest + 4, self._latest + 1):
            fd = self._data[index]
            if fd == None:
                continue
            pfd = self._data[index - 4]
            if pfd == None:
                continue

            fd["profit_adding"] = self.adding(pfd, fd, "profit")
            fd["profit2_adding"] = self.adding(pfd, fd, "profit2")
            fd["sales_adding"] = self.adding(pfd, fd, "sales")

        if not self.verify():
            raise ValueError(self._filepath + " parsing verifying failed")

    def adding(self, pfd, fd, tag):
        if pfd[tag] == None or fd[tag] == None:
            return
        if pfd[tag] < 1000000:
            return
        ratio = (fd[tag] - pfd[tag])/pfd[tag]
        return ratio * 100

    def verify(self):
        '''
        for index in self._data:
            fd = self._data[index]
            if fd == None:
                continue
            val = fd["per_share_earnings"] * 100 / fd["per_share_asset"]
            tmp = abs(val - fd["asset_yield2"])
            if tmp > 1:
                print "Warning: 净资产收益率 in ", fd["year"], "season ", fd["season"], ",", ": diff is " + str(tmp) + "%"
        '''
        return True

    TABLE = ("per_share_earnings", "per_share_asset", "per_share_cash2", "sales", 
            "msales_profit", "sales_profit", "invest_gain", "other_gain", 
            "total_profit", "profit", "profit2", "total_cash", "cach_adding", 
            "total_asset", "flow_asset", "total_debt", "flow_debt",
            "rights", "asset_yield")
    def constructdata(self, year, season, datalist, i):
        fd = {}
        fd["year"] = year
        fd["season"] = season

        index = 1
        for key in self.TABLE:
            try:
                cnt = datalist[index][i]
                if "%" in cnt:
                    fd[key] = self.parseadding(cnt)
                else:
                    fd[key] = self.parsemoney(cnt)
                if index > 2 and index < 18:
                    fd[key] *= 10000
            except:
                fd[key] = None
            index += 1

        fd["profit_adding"] = None
        return fd

    def year_season(self, date):
        try:
            items = date.split("-")
            year = int(items[0])
            month = int(items[1])
            if month > 0 and month < 4:
                season = 0
            elif month > 3 and month < 7:
                season = 1
            elif month > 6 and month < 10:
                season = 2
            elif month > 9 and month < 13:
                season = 3
            else:
                season = -1
            return (year, season)
        except:
            return (-1,-1)

    def getindex(self, year, season):
        if year > self._end:
            return -1
        if year < self._start:
            return -1
        if season < 0:
            return -1
        if season > 3:
            return -1
        index = (year - self._start)*4 + season
        return index

    def parseadding(self, text):
        ret = text.replace("%", "")
        return float(ret)

    def parsemoney(self, text):
        ret = 0
        if "亿" in text:
            ret = float(text.replace("亿", "").strip()) * 10000 * 10000
        elif "万" in text:
            ret = float(text.replace("万", "").strip()) * 10000
        else:
            ret = float(text.strip())
        return ret

    def yearreport(self, year):
        index = self.getindex(year, 3)
        return self._data[index]

    def report(self, year, season):
        index = self.getindex(year, season)
        return self._data[index]

    def latestreport(self):
        return self._data[self._latest]

    def oldestreport(self):
        return self._data[self._oldest]

    def allreports(self):
        return self._data

    def range(self):
        return (self._oldest, self._latest)


if __name__ == "__main__":
    ff = FFNetEase("input/stocks-netease/zycwzb_002495.html?type=report")
    ff.doparse()
#    print ff.allreports()
#    print ff.oldestreport()
#    print ff.latestreport()
    r = ff.yearreport(2017)
#    print ff.report(2011, 2)
    from financialfile import FinancialFile
    ff2 = FinancialFile("input/stocks/jlgf-002495/finance")
    ff2.doparse()
    r2 = ff2.yearreport(2017)

    for k in FFNetEase.TABLE:
        for m in r2:
            if r[k] == None and r2[m] == None:
                print k, "---", m, ": both none"
                continue
            if r[k] == None or r2[m] == None:
                continue

            if abs(r[k]) < 0.00001 and abs(r2[m]) < 0.00001:
                print k, "---", m, ": both zero"
                continue

            if abs(r[k]) < 0.00001 or abs(r2[m]) < 0.00001:
                continue

            delta = abs(r[k] - r2[m])/abs(r[k])
            if abs(delta) < 0.2:
                print k, "---", m, ": match", delta

    pass






