
from moneysea.actions.baseaction import BaseAction
from moneysea.test.averagesalesway import AverageSalesWay
from moneysea.test.wayindustryadding import WayIndustryAdding
from moneysea.test.wayindicatoradding import WayIndicatorAdding

class Ways(BaseAction):
    def cmd(self):
        return "way"

    def summary(self):
        return '''Ways on selecting stocks:
                            avgsales    Consider average sales as adding
                            industry    industry adding predict
                            indicator   indicator investigate [season3 or average5]
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
        elif args[0] == "indicator":
            if len(args) < 2:
                print "please specific param"
                return
            wia = WayIndicatorAdding()
            wia.run(args[1])
        else:
            print "Unknow ways"




