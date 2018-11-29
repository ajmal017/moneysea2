
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
            print "list all types"
            print types.listtypes()
        elif args[0] == "dump":
            print "dump stocks of type", args[1]
            print types.liststocks(args[1])
        elif args[0] == "show":
            print "show type of stock", args[1]
            print types.stocktypes(args[1])
        else:
            print "Unknown type command:", args[0]
