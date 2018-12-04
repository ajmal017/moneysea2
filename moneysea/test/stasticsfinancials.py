
from moneysea.globals import Globals
from moneysea.actions.baseaction import BaseAction
from moneysea.stock.stock import Stock

class StasticsFinancials(BaseAction):
    def cmd(self):
        return "stat"

    def summary(self):
        return '''Scan all financials data
                            valid: statistics valid financials data
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
