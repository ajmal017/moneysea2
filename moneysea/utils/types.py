from moneysea.config import Config
from moneysea.fileparsers.classfyxml import ClassfyXml

class Types:
    def __init__(self):
        self._cfx = ClassfyXml(Config.CLASSFY_XML)
        self._cfx.doparse()
        self.setup()
        pass

    def setup(self):
        alltypes = self._cfx.alltypes()
        for key in alltypes.keys():
            content = alltypes[key]
            filetype = content["filetype"]
            if filetype == "all":
                pass
            elif filetype == "industry":
                content["stocks"] = ["aaaaa","bbbbb"]
                print  content["filepath"]
            else:
                print "Warning: moneysea.utils.Types unknown filetype:", filetype
                del alltypes[key]

        print self._cfx.alltypes()


    def listtypes(self):
        print self._cfx.alltypes().keys()
        pass

    def liststocks(self, stype):
        print stype
        pass

    def stocktypes(self, stock):
        pass

    def typeproperty(stype):
        pass


if __name__ == "__main__":
    types = Types()
    types.listtypes()
    types.liststocks("bank")
