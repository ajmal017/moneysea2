
from moneysea.actions.baseaction import BaseAction
from moneysea.globals import Globals
from moneysea.stock.stock import Stock

class ParseAction(BaseAction):
    def __init__(self):
        pass

    def cmd(self):
        return "parse"

    def summary(self):
        return "parse one stock"


    def description(self):
        return '''
SYNOPSIS: 
    [--finance] parse <pinyin | id>
DESCRIPTIONS:
    parse the specific stock, show parsing result

OPTIONS:
    <pinyin | id>
        pinyin or stock id
    --finance
        only show finance information
'''


    def run(self, args, opts):
        if len(args) < 1:
            print "Please specific the stock in id or pinyin"
            return

        try:
            int(args[0])
            idx = args[0]
        except:
            #it is pinyin
            ids = Globals.get_instance().getinputstocks().getids(args[0])
            idx = self.select(ids)

        stock = Stock(idx)

        print idx, opts


    def select(self, ids):
        no = 1
        for i in ids:
            print no, i, Globals.get_instance().getstockidnamemapping().getname(i)
            no += 1

        while True:
            choice = raw_input("Please select:")
            try:
                k = int(choice)
                if k < no and k > 0:
                    return ids[k - 1]
            except:
                pass

