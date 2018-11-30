from moneysea.config import Config
from os import listdir


class HoldedRecord:
    def __init__(self):
        mylist = []
        for f in listdir(Config.CURRENT_HOLDED_PATH):
            if len(f.split("-")) != 3:
                continue
            mylist.append(f)
        mylist.sort()
        self._list = mylist
        pass

    def getlist(self):             #list of record name, the last one is the latest
        return self._list

    def getrecordpath(self, index):  #-1 is the latest one

        return Config.CURRENT_HOLDED_PATH + "/" +  self._list[-1]


if __name__ == "__main__":
    hr = HoldedRecord()
    print hr.getlist()
    print hr.getrecordpath(-1)
