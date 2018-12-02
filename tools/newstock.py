import sys, os
from moneysea.globals import Globals
from moneysea.config import Config
import shlex
import subprocess
import pyperclip
from moneysea.fileparsers.financialfile import FinancialFile

class NewStock:
    def __init__(self):
        pass

    def build(self, idx):
        gbls = Globals.get_instance()
        name = gbls.getstockidnamemapping().getname(idx)
        if name == "--":
            print "Unknown stock id, please specific a correct one"
            return       
        #check if is it available
        tps = gbls.gettypes()
        stocks = tps.typeproperty("available")["stocks"]
        if idx in stocks:
            s = name + "(" + idx + ")" + "is exist, would you like update it? (N/Y) Default N:"
            var = raw_input(s)
            if var != 'y' and var != "Y":
                #create note it is not exist
                pinyin = gbls.getinputstocks().getpinyin(idx)
                note = Config.STOCKS_PATH + "/" + pinyin + "-" + idx + "/note.xml"
                self.createnote(note)
                return

        #build directory string
        ins = gbls.getinputstocks()
        try:
            pinyin = ins.getpinyin(idx)
        except:
            while True:
                pinyin = raw_input("Please input pinyin of %s:"%name)
                if len(pinyin) < 3:
                    print "please input a correct pinyin, at least 3 letters"
                else:
                    break

        sdir = Config.STOCKS_PATH + "/" + pinyin + "-" + idx
        command = 'mkdir -p ' + sdir
        call_params = shlex.split(command)
        subprocess.call(call_params)
        # print the finance url and copy it to system paste board
        url = "http://stockpage.10jqka.com.cn/" + idx + "/finance/#finance"
        print url
        pyperclip.copy(url)
        # vim run
        command = 'vim ' + sdir + "/finance"
        call_params = shlex.split(command)
        subprocess.call(call_params)

        # if note.xml is not exist, just create it
        note = sdir + "/note.xml"
        self.createnote(note)

        # make a simple file parsing to verify
        ff = FinancialFile(sdir + "/finance")
        ff.doparse()
        r = ff.yearreport(2017)
        print r

        pass

    def createnote(self, note):
        if not os.path.isfile(note):
            with open(note, 'w') as the_file:
                the_file.write(
'''
<xml>
    <adding></adding>
    <note>
    </note>
    <summary>
    </summary>
</xml>
''')


    def run(self):
        n = len(sys.argv)
        if n < 2:
            print "Please provide stockid"
            return
        self.build(sys.argv[1])


if __name__ == "__main__":
    ns = NewStock()
    ns.run()
