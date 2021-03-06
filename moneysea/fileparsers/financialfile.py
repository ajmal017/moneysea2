# coding=utf-8
# file source: On Ubuntu, using chromium to open 同花顺--永利股份，select 财务指标，按报告期
# Provide: 
# Verify: every season, 净资产收益率-摊薄 = 每股收益/每股净资产

from moneysea.fileparsers.baseparser import BaseParser
import datetime

#financial data are stored in self._data{}
# _data[0] _data[1] _data[2] _data[3] --- 2009 first, second, third, forth season report data
# _data[4] _data[5] _data[6] _data[7] --- 2010 first, second, third, forth season report data

class FinancialFile(BaseParser):
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
                items = line.split()
                if len(items) < 8:
                    continue
                datalist.append(items)

        i = 0
        self._oldest = 100000
        self._latest = -10000

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

        if not self.verify():
            raise ValueError(self._filepath + " parsing verifying failed")

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

    TABLE = ("per_share_earnings", "profit", "profit_adding", "profit2", "profit2_adding",
            "sales", "sales_adding", "per_share_asset", "asset_yield", "asset_yield2", 
            "asset_debt_ratio", "per_share_fund", "per_share_keep_profit", "per_share_cash",
            "sales_gross")
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
            except:
                fd[key] = None
            index += 1

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
    ff = FinancialFile("input/stocks/ylgf-300230/finance")
#    ff = FinancialFile("input/stocks/yxkj-300231/finance")
    ff.doparse()
#    print ff.allreports()
#    print ff.oldestreport()
#    print ff.latestreport()
#    print ff.yearreport(2017)
    print ff.report(2011, 2)
    pass

