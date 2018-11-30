
from moneysea.actions.baseaction import BaseAction
from moneysea.globals import Globals

class PriceAction(BaseAction):
    def __init__(self):
        pass

    def cmd(self):
        return "price"

    def summary(self):
        return "update prices"


    def description(self):
        return '''
SYNOPSIS:
    python monsea price 
DESCRIPTION:
    update prices of all stocks
'''


    def run(self, args, opts):
        prices = Globals.get_instance().getprices()
        prices.update()



