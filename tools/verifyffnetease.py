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
            break


        for f in listdir("./input/stocks-netease/"):
            if not "zycwzb_" in f:
                continue
            fe = FFNetEase("./input/stocks-netease/" + f)
            fe.doparse()
            r = fe.yearreport(2017)
            if r == None:
                print f
                continue
            if ["profit"] == None:
                print "2017 Fail: " + f
                continue
            idx = f[7:13]
            try:
                ff = alls[idx].ff()
                r2 = ff.yearreport(2017)
                print r2["profit"], r["profit"]
                print r2["profit2"], r["profit2"]
            except Exception as e:
                pass
        pass

if __name__ == "__main__":
    vfn = VerifyFFNetease()
    vfn.run()
