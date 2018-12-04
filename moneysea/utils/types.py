from moneysea.config import Config
from moneysea.fileparsers.classfyxml import ClassfyXml
from moneysea.fileparsers.classfyindustry import ClassfyIndustry

class Types:
    def __init__(self, gbls): # gbls => Globals
        self._gbls = gbls
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
                self.setupalltype(content)
            elif filetype == "industry":
                self.setupindustrytype(content)
            elif filetype == "available":
                self.setupavailabletype(content)
            elif filetype == "holded":
                self.setupholdedtype(content)
            else:
                print "Warning: moneysea.utils.Types unknown filetype:", filetype
                del alltypes[key]


    def setupindustrytype(self, content):
        par = ClassfyIndustry(content["filepath"])
        par.doparse()
        content["stocks"] = par.allstocks()

    def setupalltype(self, content):
        mapping = self._gbls.getstockidnamemapping()
        content["stocks"] = mapping.getmap().keys()

    def setupavailabletype(self, content):
        input = self._gbls.getinputstocks()
        content["stocks"] = input.allstocks().keys()

    def setupholdedtype(self, content):
        lhr = self._gbls.getlatestholdedrecord()
        content["stocks"] = lhr.stocks().keys()


    def listtypes(self):
        return self._cfx.alltypes().keys()

    def liststocks(self, stype):
        alltypes = self._cfx.alltypes()
        return alltypes[stype]["stocks"]

    def stocktypes(self, stock):
        alltypes = self._cfx.alltypes()
        types = []
        for typ in alltypes:
            cnt = alltypes[typ]
            if cnt["filetype"] == "all":
                continue
            if stock in cnt["stocks"]:
                types.append(cnt["name"])
            
        return types

    def industry(self, stock):
        alltypes = self._cfx.alltypes()
        for typ in alltypes:
            cnt = alltypes[typ]
            if cnt["filetype"] != "industry":
                continue
            if stock in cnt["stocks"]:
                return cnt
            
        return None

    def typeproperty(self, stype):
        return self._cfx.alltypes()[stype]


if __name__ == "__main__":
    types = Types()
    print types.listtypes()
    print types.liststocks("bank")
    print types.typeproperty("bank")
