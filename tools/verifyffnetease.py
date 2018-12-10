from os import listdir
from moneysea.fileparsers.ffnetease import FFNetEase
from moneysea.globals import Globals
from moneysea.stock.stock import Stock
from moneysea.addings.addingfilter import AddingFilter

class VerifyFFNetease:
    def __init__(self):
        pass

    def run(self):
        iss = Globals.get_instance().getinputstocks()
        alls = {}
        for s in iss.allstocks():
            stock = Stock(s, AddingFilter(s))
            if not stock.ffvalid()[0]:
                continue
            alls[s] = stock       


        for f in listdir("./input/stocks-netease/"):
            if not "zycwzb_" in f:
                continue
            fe = FFNetEase("./input/stocks-netease/" + f)
            fe.doparse()
            r = fe.yearreport(2016)
            if r == None:
                print f
                continue
            if ["profit"] == None:
                print "2017 Fail: " + f
                continue
            idx = f[7:13]
            try:
                ff = alls[idx].ff()
                r2 = ff.yearreport(2016)
                if not self.match(r, r2):
                    print "stock ", idx, alls[idx].name()
                else:
                    pass
                    #print "match stock ", idx, alls[idx].name()
            except Exception as e:
                pass
        pass

    def match(self, r1, r2):
        for key in ("profit", "profit2", "per_share_earnings"):
            v1 = abs(r1[key])
            v2 = abs(r2[key])
            delta = abs(v1 - v2)
            if v2 < 0.000001 and v1 < 0.000001:
                return True

            if v2 < 0.000001 or v1 < 0.000001:
                print "Not match on ", key
                return False

            ratio = delta / v2
            if ratio > 0.10:
                print "delta not match on ", key, "ratio: ", ratio
                print "v1:", v1, "v2:", v2
                return False

            return True




if __name__ == "__main__":
    vfn = VerifyFFNetease()
    vfn.run()
