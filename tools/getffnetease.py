import shlex
import subprocess
from moneysea.globals import Globals
import os

class GetFFNetEase:
    def __init__(self):
        pass

    def run(self):
        imap = Globals.get_instance().getstockidnamemapping().getmap()
        os.chdir("./output")
        for k in imap.keys():
            ret = self.download(k)
            if ret != 0:
                break
        os.chdir("../")
        pass

    def download(self, k):
        url = "http://quotes.money.163.com/service/zycwzb_" + k + ".html?type=report"

        command = 'wget ' + url
        print command
        call_params = shlex.split(command)
        ret = subprocess.call(call_params)
        if ret != 0:
            print "Download error(", ret, "):" + url
        return ret

if __name__ == "__main__":
    gfe = GetFFNetEase()
    gfe.run()
