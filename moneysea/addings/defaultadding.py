from moneysea.addings.addingfilter import AddingFilter

class DefaultAdding(AddingFilter):
    # for inherent and public access
    def a(self):
        return (1.0 - 1.0)

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
                return (False, "FF%d:%d"%(y,i))
        for i in range(0, 4):
            if not self.test(y - 1, i):
                return (False, "FF%d:%d"%(y - 1,i))
        for i in range(s, 4):
            if not self.test(y - 2, i):
                return (False, "FF%d:%d"%(y - 2,i))
        
        # 2. if filter pass, set self._addings
        report = self.reportadding()
        if not report[0]:
            return (False, report[2])
        self._addings["report"] = report[1]

        history = self.historyadding()
        if not history[0]:
            return (False, report[2])
        self._addings["history"] = history[1]

        self._addings["365"] = 0.1

        # 3. set self._a
        return (True, "TEST")

    @classmethod
    def statinfo(cls, key):
        info = AddingFilter.statinfo(key)
        if info == None:
            return "this is test"
        else:
            return info

    def test(self, year, season):
        fd = self._ff.report(year, season)
        if fd == None:
            return False
        if fd["profit"] == None or fd["per_share_earnings"] == None or fd["profit_adding"] == None:
            return False
        return True

