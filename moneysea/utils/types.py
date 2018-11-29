from moneysea.config import Config
from moneysea.fileparsers.classfyxml import ClassfyXml
from moneysea.fileparsers.classfyindustry import ClassfyIndustry

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
                self.setupindustrytype(content)
            else:
                print "Warning: moneysea.utils.Types unknown filetype:", filetype
                del alltypes[key]


    def setupindustrytype(self, content):
        par = ClassfyIndustry(content["filepath"])
        par.doparse()
        content["stocks"] = par.allstocks()



    def listtypes(self):
        return self._cfx.alltypes().keys()

    def liststocks(self, stype):
        alltypes = self._cfx.alltypes()
        return alltypes[stype]["stocks"]

    def stocktypes(self, stock):
        pass

    def typeproperty(self, stype):
        return self._cfx.alltypes()[stype]


if __name__ == "__main__":
    types = Types()
    print types.listtypes()
    print types.liststocks("bank")
    print types.typeproperty("bank")
