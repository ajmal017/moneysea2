class Common:
    def stockidsimple(self, stockid):
        if stockid[0] == 's':
            val = stockid[2:]
        else:
            val = stockid
        try:
            int(val)
            return val
        except:
            return None

    def stockidlocation(self, stockid):
        return
