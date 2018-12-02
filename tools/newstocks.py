import sys, os
from moneysea.globals import Globals
from newstock import NewStock

class NewStocks:
    def __init__(self):
        pass

    def run(self):
        n = len(sys.argv)
        if n < 2:
            print "Please provide stocks type"
            return

        gbls = Globals.get_instance()
        tps = gbls.gettypes()

        try:
            prop = tps.typeproperty(sys.argv[1])
        except:
            print "Unknown type:", sys.argv[1]
            return

        stocks = prop["stocks"]

        for s in stocks:
            ns = NewStock()
            ns.build(s)
        pass


if __name__ == "__main__":
    nss = NewStocks()
    nss.run()
