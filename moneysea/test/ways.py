
from moneysea.actions.baseaction import BaseAction
from moneysea.test.averagesalesway import AverageSalesWay

class Ways(BaseAction):
    def cmd(self):
        return "way"

    def summary(self):
        return '''Ways on selecting stocks:
                            avgsales    Consider average sales as adding
                ''' 

    def description(self):
        return "description"

    def run(self, args, opts):
        if len(args) == 0:
            print "please specific the sub command"
            return

        if args[0] == "avgsales":
            asw = AverageSalesWay()
            asw.run()
        else:
            print "Unknow ways"




