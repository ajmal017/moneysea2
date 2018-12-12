from moneysea.addings.addingfilter import AddingFilter
from moneysea.stock.stock import Stock
from moneysea.globals import Globals

class DratioAdding(AddingFilter):
    def seta(self, a):
        self._a = a

    def a(self):
        return self._a

class Dratio:
    def __init__(self):
        pass

    def run(self):
        ss = self.stocks()
        lists = [{},{},{},{}]
        for idx in ss:
            af = DratioAdding(idx)
            stock = Stock(idx, af)

            bs = stock.baseline()
            r2017 = stock.ff().yearreport(2017)

            if stock.e() < 0.2:             # too small which will cause wuca
#                print stock.name(), stock.id(), stock.e()
                continue

            index = 0
            for a in (ss[idx], bs["profit2_adding"], bs["sales_adding"], r2017["sales_adding"]):
                stock._af.seta(a/100.0)
#                if stock.id() == "300230":
#                print stock.name(), stock.id(), stock.a(), stock.e(), stock.dratio()
                dic = lists[index]
                dic[idx] = (idx, stock.a(), stock.dratio())
                index += 1


        LL = []
        for i in range(0, 4):
            dic = lists[i]
            #sort
            ll = self.sort(dic)
            end = len(ll)*5/12
            LL.append(ll[0:end])

        types = Globals.get_instance().gettypes()

        for tt in types.industries():
            stocks = tt["stocks"]
            tmp = tt["cname"]
            for d in LL[0]:
                d1 = self.item(d[0], LL[1])
                d2 = self.item(d[0], LL[2])
                d3 = self.item(d[0], LL[3])
                if d1 == None or d2 == None or d3 == None:
                    continue

                if not d[0] in stocks:
                    continue

                af = DratioAdding(d[0])
                stock = Stock(d[0], af)
                idt = types.industry(d[0])
                print stock.id(), "(%3.1f %12.1f), (%3.1f, %12.1f), (%3.1f, %12.1f), (%3.1f, %12.1f)"%(d[1], d[2], d1[1], d1[2], d2[1], d2[2], d3[1], d3[2]), "\t", stock.name(), "\t", tmp

        count = 0
        for d in LL[0]:
            d1 = self.item(d[0], LL[1])
            d2 = self.item(d[0], LL[2])
            d3 = self.item(d[0], LL[3])
            if d1 == None or d2 == None or d3 == None:
                continue
            count += 1

            af = DratioAdding(d[0])
            stock = Stock(d[0], af)
            idt = types.industry(d[0])
            if idt != None:
                continue
            print stock.id(), "(%3.1f %12.1f), (%3.1f, %12.1f), (%3.1f, %12.1f), (%3.1f, %12.1f)"%(d[1], d[2], d1[1], d1[2], d2[1], d2[2], d3[1], d3[2]), "\t", stock.name()

        print "total:", count

        pass

    def item(self, idx, ll):
        for i in ll:
            if idx == i[0]:
                return i
        return None

    def sort(self, dic):
        ll = []
        for d in dic:
            tmp = dic[d][2]
            if len(ll) == 0:
                ll.append(dic[d])
                continue

            index = 0
            for kk in ll:
                if tmp > kk[2]:
                    ll.insert(index, dic[d])
                    break
                index += 1
            if index >= len(ll):
                ll.append(dic[d])

#        for kk in ll:
#            print kk
        return ll






    def stocks(self):
        ss = {}
        with open("operation/buysell-1211-reportprocess") as f:
            for line in f:
                items = line.split()
                if len(items) != 4:
                    continue
                val = 0
                if items[2] == "None":
                    val = float(items[3])
                elif items[2] == "V":
                    val = float(items[3])
                else:
                    val = float(items[2])

                ss[items[1]] = val
        return ss

if __name__ == "__main__":
    dr = Dratio()
    dr.run()
