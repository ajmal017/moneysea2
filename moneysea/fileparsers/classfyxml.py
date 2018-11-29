from moneysea.fileparsers.baseparser import BaseParser
import xml.etree.ElementTree as ET


class ClassfyXml(BaseParser):
    def doparse(self):
        tree = ET.parse(self._filepath)
        root = tree.getroot()
        self._alltypes = {}
        for child in root:
            if not (child.tag == "type"):
                continue
#            print child.tag, child.attrib["name"]
            self._alltypes[child.attrib["name"]] = child.attrib
#        print self._alltypes
        pass

    def alltypes(self):
        return self._alltypes

