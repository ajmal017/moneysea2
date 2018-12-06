
from moneysea.actions.baseaction import BaseAction
from moneysea.test.averagesalesway import AverageSalesWay
from moneysea.test.wayindustryadding import WayIndustryAdding

class Ways(BaseAction):
    def cmd(self):
        return "way"

    def summary(self):
        return '''Ways on selecting stocks:
                            avgsales    Consider average sales as adding
                            industry    industry adding predict
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
        elif args[0] == "industry":
            if len(args) < 2:
                print "please specific type of stocks"
                return
            wid = WayIndustryAdding()
            wid.run(args[1])
        else:
            print "Unknow ways"




