
from moneysea.actions.baseaction import BaseAction
from moneysea.utils.types import Types

class TypeAction(BaseAction):
    def __init__(self):
        pass

    def cmd(self):
        return "type"

    def summary(self):
        return "show all stock types"


    def description(self):
        return '''
SYNOPSIS:
    python monsea type [list | dump | show] [<args>]
DESCRIPTION:
    show all stock types

COMMAND:
    list
        list all types
    dump type
        dump all stock of specific type
    show stockid
        show type of the specific stock 
'''


    def run(self, args, opts):
        types = Types()
        if len(args) == 0:
            print types.listtypes()
            return

        if args[0] == "list":
            print "%16s%16s%16s%16s"%("name","typetype","np","count")
            print ""
            for typ in types.listtypes():
                prop = types.typeproperty(typ)
                try:
                    np = prop["np"]
                except:
                    np = "--"
                try:
                    count = len(prop["stocks"])
                except:
                    count = 0
                print "%16s%16s%16s%16s"%(typ, prop["filetype"], np, count)
        elif args[0] == "dump":
            if len(args) < 2:
                print "please specify the stock type for dumping"
                print self.description()
                return 
            try:
                prop = types.typeproperty(args[1])
            except:
                print "Unknown type:", args[1]
                return

            try:
                stocks = prop["stocks"]
            except:
                return

            for idx in stocks:
                print idx

        elif args[0] == "show":
            print "show type of stock", args[1]
            print types.stocktypes(args[1])
        elif args[0] == "help":
            print self.description()
        else:
            print "Unknown type command:", args[0]









