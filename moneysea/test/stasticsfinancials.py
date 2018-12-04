
from moneysea.globals import Globals
from moneysea.actions.baseaction import BaseAction
from moneysea.stock.stock import Stock

class StasticsFinancials(BaseAction):
    def cmd(self):
        return "stat"

    def summary(self):
        return '''Scan all financials data
                            valid: statistics valid financials data
                            continuous: continuous adding 
                            adding: adding range of all stocks
                ''' 

    def description(self):
        return "description"

    def run(self, args, opts):
        if len(args) == 0:
            print "please specific the sub command"
            return

        self._iss = Globals.get_instance().getinputstocks()
        if args[0] == "valid":
            self.stat_valid()
        elif args[0] == "continuous":
            self.stat_conti()
        elif args[0] == "adding":
            self.stat_adding()


    def stat_adding(self):
        all = {}
        for s in self._iss.allstocks():
            stock = Stock(s)
            all[s] = stock

        for s in all:
            ss = all[s]
            if not ss.ffvalid():
                continue
            print s, ss.name(), ss.addings()["report"]


    def stat_conti(self):
        all = {}
        for s in self._iss.allstocks():
            stock = Stock(s)
            all[s] = stock

        count = 0
        continuous = 0
        for s in all:
            ss = all[s]
            if not ss.ffvalid():
                continue
            print s, ss.name(), ss.addings()
            v = ss.addings()
            mini = -0.05
            if (v["report"] > mini) and (v["history"] > mini) and (v["365"] > mini):
                continuous += 1
            count += 1
        print "continuous: ", continuous, "total: ", count, "percent: ", 100.0*continuous / count, "%"

    def stat_valid(self):
        all = {}
        for s in self._iss.allstocks():
            stock = Stock(s)
            all[s] = stock

        count = 0
        valid = 0
        for s in all:
            ss = all[s]
            print s, ss.name(), ss.ffvalid()
            if ss.ffvalid():
                valid += 1
            count += 1

        print ""
        print "valid:", valid, "total:", count, "valid percent:", 100.0*valid/count, "%"
