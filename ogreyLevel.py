import wx
import ogre.renderer.OGRE as ogre

class Level:
    def __init__(self):
        self.name = ""
        self.entityinstances = {}
        self.filepath = ""
        self.clearcolor = ogre.Vector3(0.0, 0.0, 0.0)
        self.ambientlight = ogre.Vector3(0.0, 0.0, 0.0)
        

class EntityInstance:
    def __init__(self):
        self.name = ""
        self.parent = ""
        self.filepath = ""
        self.position = ogre.Vector3(0.0, 0.0, 0.0)