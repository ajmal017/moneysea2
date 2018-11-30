
from moneysea.actions.baseaction import BaseAction
from moneysea.globals import Globals

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
        types = Globals.get_instance().gettypes()

        if len(args) == 0 or args[0] == "list":
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
            mapping = Globals.get_instance().getstockidnamemapping()
            print "id, \tname, \t\tdata, holded, industry"
            for idx in stocks:
                ll = len(mapping.getname(idx))

                print idx, mapping.getname(idx),
                if ll < 12:
                    print "\t",

                tps = types.stocktypes(idx)
                if "available" in tps:
                    print "\tY",
                else:
                    print "\t-",

                if "holded" in tps:
                    print "\tH",
                else:
                    print "\t-",

                for t in tps:
                    if "available" == t:
                        continue
                    if "holded" == t:
                        continue
                    print "\t", t,

                print ""

        elif args[0] == "show":
            if len(args) < 2:
                print "please specify the stock id to show its types"
                print self.description()
                return
            mapping = Globals.get_instance().getstockidnamemapping()
            print mapping.getname(args[1])
            print "types:       ",
            for typ in types.stocktypes(args[1]):
                print typ + ",",
        elif args[0] == "help":
            print self.description()
        else:
            print "Unknown type command:", args[0]









