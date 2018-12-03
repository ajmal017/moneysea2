# coding=utf-8
import sys
import os
import json
import urllib2
import datetime
from os import listdir
from moneysea.config import Config
from moneysea.stock.common import Common
import json


class Prices:
    def __init__(self, gbls):
        self._gbls = gbls
        self._latestprices = self.latestprices()
        pass

    def update(self):
        allstocks = self._gbls.getstockidnamemapping().getmap().keys()

        count = 0
        mylist = ""
        self.plist = {}
        for item in allstocks:
            mylist += Common().stockidlocation(item) + ","
            count += 1
            if count == 3:
                self.request(mylist)
                count = 0
                mylist = ""
        if count > 0:
            self.request(mylist)
        n = datetime.datetime.now()
        name = Config.PRICES_PATH + "/%04d%02d%02d-%02d%02d"%(n.year, n.month, n.day, n.hour, n.minute)
        json.dump(self.plist, open(name,'w'))

    def request(self, mylist):
        myurl='http://hq.sinajs.cn/list=' + mylist
        req = urllib2.Request(url = myurl)
        res = urllib2.urlopen(req)
        res = res.read()
        lines = res.split("\n")
        for line in lines:
            vals = line.split(",")
            if len(vals) < 2:
                continue
            if len(vals) < 20:
                print line
                print "Unknown response on " + mylist
                continue
            idx = vals[0][13:19]
            price = float(vals[2])
            self.plist[idx] = price

    def pathlist(self):            #list of path of all prices list
        mylist = []
        for f in listdir(Config.PRICES_PATH):
            if len(f.split("-")) != 2:
                continue
            mylist.append(f)
        mylist.sort()
        return mylist

    def prices(self, filepath):      #return the dictionary generate from the filepath
        p = json.load(open(filepath))
        try:
            p = json.load(open(filepath))
        except:
            p = None
        return p

    def latestprices(self):        #return the dictionary of latest prices
        return self.prices(Config.PRICES_PATH + "/" + self.pathlist()[-1])

    def price(self, sid):
        return self._latestprices[sid]


if __name__ == "__main__":
    if sys.getdefaultencoding() != 'utf-8':
        reload(sys)
        sys.setdefaultencoding('utf-8')

    from moneysea.globals import Globals

    p = Prices(Globals.get_instance())
#    p.update()
#    print p.pathlist()
    print len(p.latestprices().keys())


