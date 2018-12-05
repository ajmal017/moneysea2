from moneysea.addings.addingfilter import AddingFilter
from moneysea.config import Config

class DefaultAdding(AddingFilter):
    # for inherent and public access
    def a(self):
        return self._a

    # for inherient
    def addingfilter(self):
        # 1. set filters
        # to caculate addings for report, history and 365, request profit, pershareearning, profit_addings to be valid
        # {2018:4321} {2017:4321} {2016:4
        # {2018: 321} {2017:4321} {2016:43
        # {2018:  21} {2017:4321} {2016:432
        # {2018:   1} {2017:4321} {2016:4321
        y = self._baseline["year"]
        s = self._baseline["season"]
        for i in range(0, s + 1):
            if not self.test(y, i):
                return (False, "FF-" + str(y))
        for i in range(0, 4):
            if not self.test(y - 1, i):
                return (False, "FF-" + str(y - 1))
        for i in range(s, 4):
            if not self.test(y - 2, i):
                return (False, "FF-" + str(y - 2))

        # small profit as base is not suitable for evaluating
        # for "report" adding evaluating
        last = self._ff.report(y - 1, s)
        if last["profit"] < Config.MINIMAL_PROFIT:
            return (False, "PROFIT SMALL")
        # for "history" adding evaluating
        last = self._ff.report(y - 2, 3)
        if last["profit"] < Config.MINIMAL_PROFIT:
            return (False, "PROFIT SMALL")
        
        # 2. if filter pass, set self._addings
        report = self.reportadding()
        if not report[0]:
            return (False, report[2])
        self._addings["report"] = report[1]

        history = self.historyadding()
        if not history[0]:
            return (False, history[2])
        self._addings["history"] = history[1]

        tmp = self._365adding()
        if not tmp[0]:
            return (False, tmp[2])
        self._addings["365"] = tmp[1]

        # 3. set self._a
        self._a = (self._addings["report"] + self._addings["history"] + self._addings["365"])/3
        return (True, "TEST")

    @classmethod
    def statinfo(cls, key):
        info = AddingFilter.statinfo(key)
        if info == None:
            if "FF" in key:
                return "Financial data does not satisify adding calculate"
            else:
                return ""
        else:
            return info

    def test(self, year, season):
        fd = self._ff.report(year, season)
        if fd == None:
            return False
        if fd["profit"] == None or fd["per_share_earnings"] == None or fd["profit_adding"] == None:
            return False
        return True

