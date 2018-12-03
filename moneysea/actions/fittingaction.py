
from moneysea.actions.baseaction import BaseAction
from moneysea.globals import Globals
from moneysea.test.fitting import Fitting

class FittingAction(BaseAction):
    def __init__(self):
        pass

    def cmd(self):
        return "fitting"

    def summary(self):
        return "try fitting to find suitable n, p value"


    def description(self):
        return '''
SYNOPSIS: 
    python moneysea fitting <type> [n=x p=x]

DESCRIPTION:
    draw fitting graph for the specific type

OPTIONS:
    <type>
        stock type
    [n=x p=x]
        n and p value, default n=5, p=0.08
'''


    def run(self, args, opts):
        try:
            prop = Globals.get_instance().gettypes().typeproperty(args[0])
            stocks = prop["stocks"]
        except:
            print "please specify valid type for fitting"
            return

        n = 5
        p = 0.08
        
        for a in args:
            items = a.split("=")
            if len(items) == 2:
                if items[0] == "n":
                    n = int(items[1])
                elif items[0] == "p":
                    p = float(items[1])

        print "Fitting (n:%d, p:%6.2f)"%(n,p)

        ft = Fitting(stocks, n, p)
        ft.run()



