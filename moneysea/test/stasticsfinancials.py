
from moneysea.globals import Globals
from moneysea.actions.baseaction import BaseAction
from moneysea.stock.stock import Stock
from moneysea.addings.addingfilter import AddingFilter
from moneysea.addings.season3adding import Season3Adding
from moneysea.addings.defaultadding import DefaultAdding

class StasticsFinancials(BaseAction):

    AF = DefaultAdding

    def cmd(self):
        return "stat"

    def summary(self):
        return '''Scan all financials data
                            valid: statistics valid financials data
                            continuous: continuous adding 
                            adding: adding range of all stocks
                            delta: statistics of delta value
                ''' 

    def description(self):
        return "description"

    def run(self, args, opts):
        if len(args) == 0:
            print "please specific the sub command"
            return

        self.stat_init()

        if args[0] == "valid":
            self.stat_valid()
        elif args[0] == "continuous":
            self.stat_conti()
        elif args[0] == "adding":
            self.stat_adding()
        elif args[0] == "delta":
            self.stat_delta()
        else:
            print "Unknow stat command"

    def stat_init(self):
        iss = Globals.get_instance().getinputstocks()
        self._all = {}
        self._stat = {}
        self._total = len(iss.allstocks())
        for s in iss.allstocks():
            af = self.AF(s)
            stock = Stock(s, af)
            self._all[s] = stock

    def stat_add(self, fail):
        try:
            self._stat[fail] += 1
        except:
            self._stat[fail] = 1

    def stat_exit(self):
        self.AF.stat(self._stat)


    def stat_delta(self):
        for s in self._all:
            ss = self._all[s]
            if not ss.ffvalid()[0]:
                continue

            dratio = ss.dratio()
            print s, ss.name(), ss.a(), dratio

    def stat_adding(self):
        for s in self._all:
            ss = self._all[s]
            if not ss.ffvalid()[0]:
                continue
            print s, ss.name(), ss.addings()["report"]


    def stat_conti(self):

        continuous = 0
        for s in self._all:
            ss = self._all[s]
            if not ss.ffvalid()[0]:
                continue
            v = ss.addings()
            mini = -0.05
            if (v["report"] > mini) and (v["history"] > mini) and (v["365"] > mini):
                print s, ss.name(), ss.addings()
                continuous += 1

        print "continuous: ", continuous, "total: ", self._total, "percent: ", 100.0*continuous / self._total, "%"



    def stat_valid(self):
        valid = 0
        for s in self._all:
            ss = self._all[s]
            ff = ss.ffvalid()
            print s, ss.name(), ff
            if ff[0]:
                valid += 1
            else:
                if ff[1] == "OK":
                    raise
                self.stat_add(ff[1])

        print ""
        print "valid:", valid, "total:", self._total, "valid percent:", 100.0*valid/self._total, "%"
        self.stat_exit()




