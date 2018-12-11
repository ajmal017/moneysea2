# coding=utf-8
from moneysea.addings.addingfilter import AddingFilter
from moneysea.stock.stock import Stock
import shlex
import subprocess
import os

class ReportProcess:
    def __init__(self):
        pass
    def run(self):
        ss = self.stocks()

        for s in ss:
            af = AddingFilter(s)
            stock = Stock(s, af)
            bs = stock.baseline()
#            print stock.name(), stock.id(), bs["profit"], bs["profit_adding"], bs["profit2_adding"], bs["sales_adding"]
            rlt = self.processreport(s)
            if not rlt[0]:
                continue

            if rlt[1] != None and (rlt[1] + 10) < bs["profit_adding"]:  #四季度增长基本加快
                continue

            if rlt[1] == None:
                val = bs["profit_adding"]
            else:
                val = (rlt[1] + bs["profit_adding"])/2
            print stock.id(), stock.name(), val
        pass

    def processreport(self, sid):
        filename = "./output/" + "yjyg_" + sid + ".html"
        with open(filename) as f:
            for l in f:
                line = l.strip()
                i = line.find("预计")
                if i == -1:
                    continue

                i = line.find("2018")
                if i == -1:
                    return (False, 0)
                
                if ("年度" in line and not "半年度" in line) or "全年" in line or "1-12月" in line:
                    pass
                else:
                    return (False, 0)

                if "变动幅度" in line:
                    return self.report1(line)
                elif self.description(line):
                    return (True, None)
                else:
                    return (False, 0)

        return (False, 0)

    def report1(self, line):
        orgline = line
        tmp = line.find("变动幅度：")
        if tmp == -1:
            return (False, 0)

        line = line[tmp + len("变动幅度："):]
        tmp = line.find("。")
        if tmp == -1:
            return (False, 0)
        line = line[0:tmp]
        items = line.split("至")
        if len(items) == 1 and "%" in items[0]:
            val = float(items[0][0:-1])
            return (True, val)
        elif len(items) == 2 and "%" in items[0] and "%" in items[1]:
            val1 = float(items[0][0:-1])
            val2 = float(items[1][0:-1])
            if val1 < 0.001 or val2 < 0.001:
                return (False, 0)
            return (True, (val1 + val2)/2)
        return (True, 0)


    def description(self, line):
        i = line.find("大幅")
        if i == -1:
            i = line.find("明显")
            if i == -1:
                i = line.find("较大")

        if i == -1:
            return False
        tmp = line[i:]


        if ("增长" in line or "上升" in line or "增加" in line or "增幅" in line):
            return True
        else:
            return False



 
        

    def downloadreports(self):
        ss = self.stocks()
        os.chdir("./output")
        for s in ss:
            self.accessreport(s)
        os.chdir("../")


    def accessreport(self, sid):
        url = "http://quotes.money.163.com/f10/yjyg_" + sid + ".html#01c03"
        command = 'wget ' + url
        print command
        call_params = shlex.split(command)
        ret = subprocess.call(call_params)
        if ret != 0:
            print "Download error(", ret, "):" + url
        return ret

    def stocks(self):
        ss = []
        with open("operation/season3_result") as f:
            for line in f:
                items = line.split()
                if len(items) != 2:
                    continue
                ss.append(items[1])
        return ss


if __name__ == "__main__":
    rp = ReportProcess()
#    rp.downloadreports()
    rp.run()
