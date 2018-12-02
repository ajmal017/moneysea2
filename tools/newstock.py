import sys, os
from moneysea.globals import Globals
from moneysea.config import Config
import shlex
import subprocess

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
        # vim run
        command = 'vim ' + sdir + "/finance"
        call_params = shlex.split(command)
        subprocess.call(call_params)

        # if note.xml is not exist, just create it
        note = sdir + "/note.xml"
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
        pass


    def run(self):
        n = len(sys.argv)
        if n < 2:
            print "Please provide stockid"
            return
        self.build(sys.argv[1])


if __name__ == "__main__":
    ns = NewStock()
    ns.run()
