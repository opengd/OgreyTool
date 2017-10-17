import elementtree.ElementTree as ET
from ogreySingleton import *

class OgreyConfig:
    def __init__(self):
        self.filepath = "ogreyConfig.xml"
        self.Resources =    {
                            "Entities" : {"paths" : [], "resources" : [], "exts" : []}, 
                            "Materials" : {"paths" : [], "resources" : [], "exts" : []}
                            }

class ConfigManager:
    __metaclass__=Singleton
    def __init__(self):
        self.Config = OgreyConfig()
        
    def Load(self):
        importElements = ET.parse(self.Config.filepath)
        root = importElements.getroot()
        
        for childElement in root.getchildren():
            if childElement.tag == "resources":
                for resources in childElement.getchildren():
                    if resources.tag == "entities":
                        for (key, value) in resources.attrib.iteritems():
                            if key == "path":
                                self.Config.Resources["Entities"]["paths"].append(value)
                            if key == "ext":
                                self.Config.Resources["Entities"]["exts"].append(value)
                    if resources.tag == "materials":
                        for (key, value) in resources.attrib.iteritems():
                            if key == "path":
                                self.Config.Resources["Materials"]["paths"].append(value)
                            if key == "ext":
                                self.Config.Resources["Materials"]["exts"].append(value)
        self.GetAllResourecePaths()
        
    def Save(self):
        root = ET.Element("ogreyConfig")
        ET.SubElement(root, "resource", attrib={"path" : self.Config.filepath})
        
    def GetAllResourecePaths(self):
        def Get(arg, dirname, names):
            xml = []
            for n in names:
                (root, ext) = os.path.splitext(n)
                for inext in self.Config.Resources[key]["exts"]:
                    if ext == inext: self.Config.Resources[key]["resources"].append(str(os.path.join(dirname,n)))        
        import os.path
        for (key, value) in self.Config.Resources.iteritems():
            for path in self.Config.Resources[key]["paths"]:
                os.path.walk(path,Get,None)
        #for r in self.Config.resourcers:
        #    print r
    def GetConfig(self):
        return self.Config

#config = ConfigManager()
#config.Load()
#c = config.GetConfig()

#for (key, value) in c.Resources.iteritems():
#            for path in c.Resources[key]["resources"]:
#                print path
                #config.GetAllResourecePaths()
#self.LoadConfig()
        