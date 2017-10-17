import wx
from ogreyEntity import *
import elementtree.ElementTree as ET
import ogre.renderer.OGRE as ogre
from ogreyErrorManager import *

class ogreyImportEntity:
    def __init__(self, parent, paths):
        #wx.FileDialog.__init__(self, parent, message="Import file", wildcard="*.xml", style=wx.OPEN | wx.MULTIPLE)
        self.Entities = []
        self.loadingErrors = []
        for path in paths:
            try:
                self.Entities.append(self.CreateEntityFromXML(path))
            except:
                self.loadingErrors.append(path)
        if not len(self.loadingErrors) == 0:
            ErrorDialog(parent, "Errors when trying import file/files", self.loadingErrors)
    def CreateEntityFromXML(self, file):
        self.Entity = Entity()
        self.Entity.filepath = file
        #self.entityTree.DeleteAllItems()
        #self.entityTreeRoot = self.entityTree.AddRoot(text="Entity", data=wx.TreeItemData(obj=self.Entity))
        #print file
        importElements = ET.parse(file)
        root = importElements.getroot()
        for (key, value) in root.attrib.iteritems():
            if key == "name":
                self.Entity.name = value
        for childElement in root.getchildren():
            #if childElement.tag is ET.Comment:
            #    pass
                    #print "ass"
                    #Obj.comments = child.text
            #TRANSFORM OBJECT
            if childElement.tag == "transformobject":
                Obj = TransformObject()
                self.Entity.Transform.append(Obj)
                Obj.name = "RootNode"
                Obj.node = "RootNode"
                Obj.type = "RootNode"
                    
                for child in childElement.getchildren():
                    Obj = TransformObject()
                    self.Entity.Transform.append(Obj)
                    for (key, value) in child.attrib.iteritems():
                        if key == "name":
                            Obj.name = value
                        if key == "parent":
                            Obj.node = value
                        for nodechild in child.getchildren():
                            if nodechild.tag == "position":
                                Obj.position = ogre.Vector3(float(nodechild.attrib["x"]), float(nodechild.attrib["y"]) , float(nodechild.attrib["z"]))
                            elif nodechild.tag == "rotation":
                                Obj.rotation = ogre.Vector3(float(nodechild.attrib["x"]),float(nodechild.attrib["y"]), float(nodechild.attrib["z"]))
                            elif nodechild.tag == "scale":
                                Obj.scale = ogre.Vector3(float(nodechild.attrib["x"]), float(nodechild.attrib["y"]) , float(nodechild.attrib["z"]))
                
##                if len(childElement.getchildren()) == 0:
##                    Obj = TransformObject()
##                    self.Entity.Transform.append(Obj)
##                    Obj.name = "RootNode"
##                    Obj.node = "RootNode"
                    #item = self.FindTreeItem(Obj.node, self.entityTree.GetRootItem())
                    #if item == None: item = self.entityTree.GetRootItem()
                    #self.entityTree.AppendItem(item, "Transform Object", data = wx.TreeItemData(obj=Obj))

            # GRAPHIC OBJECT
            if childElement.tag == "graphicobject":
                for child in childElement.getchildren():
                    Obj = GraphicObject()
                    self.Entity.Graphic.append(Obj)
                    
                    for (key, value) in child.attrib.iteritems():
                        if key == "name":
                            Obj.name = value
                        elif key == "model":
                            Obj.model = value
                        elif key == "material":
                            Obj.material = value
                        elif key == "node":
                            Obj.node = value
                    #item = self.FindTreeItem(Obj.node, self.entityTree.GetRootItem())
                    #if item == None: item = self.entityTree.GetRootItem()
                    #self.entityTree.AppendItem(item, "Graphic Object", data = wx.TreeItemData(obj=Obj))
            # ANIMATED GRAPHIC OBJECT
            if childElement.tag == "animatedgraphicobject":
                for child in childElement.getchildren():
                    Obj = AnimatedGraphicObject()
                    self.Entity.AnimatedGraphic.append(Obj)
                    
                    for (key, value) in child.attrib.iteritems():
                        if key == "name":
                            Obj.name = value
                        elif key == "model":
                            Obj.model = value
                        elif key == "material":
                            Obj.material = value
                        elif key == "node":
                            Obj.node = value
                    #item = self.FindTreeItem(Obj.node, self.entityTree.GetRootItem())
                    #if item == None: item = self.entityTree.GetRootItem()
                    #self.entityTree.AppendItem(item, "Graphic Object", data = wx.TreeItemData(obj=Obj))
            # PHYSIC OBJECT
            if childElement.tag == "physicobject":
                Obj = PhysicObject()
                for (key, value) in childElement.attrib.iteritems():
                    if key == "static":
                        Obj.static = bool(value)
                for child in childElement.getchildren():
                    Obj = PhysicObject()
                    self.Entity.Physic.append(Obj)
                    for (key, value) in child.attrib.iteritems():
                        if key == "name":
                            Obj.name = value
                        if key == "node":
                            Obj.node = value
                        if key == "collisionenabled":
                            if value == "true":
                                Obj.collisionenabled = True
                            else: Obj.collisionenabled = False
                        if key == "follow":
                            if value == "true":
                                Obj.body.follow = True
                            else: Obj.body.follow = False
                    for bodyOrShape in child.getchildren():
                        if bodyOrShape.tag == "body":
                            for (key, value) in bodyOrShape.attrib.iteritems():
                                if key == "gravityenabled":
                                   if value == "true":
                                      Obj.body.gravityenabled = True
                                   else: Obj.body.gravityenabled = False
                                elif key == "kinematic":
                                    if value == "true":
                                        Obj.body.kinematic = True
                                    else: Obj.body.kinematic = False

                                elif key == "lineardamping":
                                    Obj.body.lineardamping = float(value)
                                elif key == "angulardamping":
                                    Obj.body.angulardamping = float(value)
                                elif key == "maxangularvelocity":
                                    Obj.body.maxangularvelocity = float(value)
                                for vel in bodyOrShape.getchildren():
                                    if vel.tag == "linearvelocity":
                                        for (key, value) in vel.attrib.iteritems():
                                            if key == "x":
                                                Obj.body.linearvelocity.x = float(value)
                                            if key == "y":
                                                Obj.body.linearvelocity.y = float(value)
                                            if key == "z":
                                                Obj.body.linearvelocity.z = float(value)
                                    if vel.tag == "angularvelocity":
                                        for (key, value) in vel.attrib.iteritems():
                                            if key == "x":
                                                Obj.body.angularvelocity.x = float(value)
                                            if key == "y":
                                                Obj.body.angularvelocity.y = float(value)
                                            if key == "z":
                                                Obj.body.angularvelocity.z = float(value)
                        elif bodyOrShape.tag == "shape":
                            shape = PhysicShape()
                            Obj.shapes.append(shape)
                            for (key, value) in bodyOrShape.attrib.iteritems():
                                if key == "name":
                                    shape.name = value
                                if key == "collisiongroup":
                                    shape.collisiongroup = value
                                if key == "material":
                                    shape.material = value
                                if key == "density":
                                    shape.density = float(value)
                            for posOrType in bodyOrShape.getchildren():
                                if posOrType.tag == "localpose":
                                    tempPos = localpose()
                                    for (key, value) in posOrType.attrib.iteritems():
                                        if key == "node":
                                            tempPos.node = value
                                    for posChild in posOrType.getchildren():
                                        if posChild.tag == "position":
                                            for pois in posChild.attrib.iteritems():
                                                if pois == "x":
                                                    tempPos.position.x = float(value)
                                                if pois == "y":
                                                    tempPos.position.y = float(value)
                                                if pois == "z":
                                                    tempPos.position.z = float(value)
                                        if posChild.tag == "rotation":
                                            for rois in posChild.attrib.iteritems():
                                                if rois == "x":
                                                    tempPos.rotation.x = float(value)
                                                if rois == "y":
                                                    tempPos.rotation.y = float(value)
                                                if rois == "z":
                                                    tempPos.rotation.z = float(value)
                                                    
                                elif posOrType.tag == "boxshape":
                                    shape.shape = boxshape()
                                    shape.shape.localpose = tempPos
                                        
                                    for (key, value) in posOrType.attrib.iteritems():
                                        if key == "height":
                                            shape.shape.height = float(value)
                                        if key == "width":
                                            shape.shape.width = float(value)
                                        if key == "depth":
                                            shape.shape.depth = float(value)
                                            
                                elif posOrType.tag == "capsuleshape":
                                    shape.shape = capsuleshape()
                                    shape.shape.localpose = tempPos
                                    
                                    for (key, value) in posOrType.attrib.iteritems():
                                        if key == "height":
                                            shape.shape.height = float(value)
                                        if key == "radius":
                                            shape.shape.radius = float(value)
                                            
                                elif posOrType.tag == "sphereshape":
                                    shape.shape = sphereshape()
                                    shape.shape.localpose = tempPos
                                    
                                    for (key, value) in posOrType.attrib.iteritems():
                                        if key == "radius":
                                            shape.shape.radius = float(value) 
                                                                           
                                elif posOrType.tag == "convexshape":
                                    shape.shape = convexshape()
                                    shape.shape.localpose = tempPos
                                    
                                    for (key, value) in posOrType.attrib.iteritems():
                                        if key == "mesh":
                                            shape.shape.mesh = value
                                        if key == "smoothmesh":
                                            shape.shape.smoothmesh = bool(value)
                                            
                                elif posOrType.tag == "triangleshape":
                                    shape.shape = triangleshape()
                                    shape.shape.localpose = tempPos

                                    for (key, value) in posOrType.attrib.iteritems():
                                        if key == "mesh":
                                            shape.shape.mesh = value
                                        if key == "smoothmesh":
                                            shape.shape.smoothmesh = bool(value)                                
                                
                                #shape.shape.localpose = tempPos
                            
            #FREE CAMERA OBJECT            
            if childElement.tag == "freecameraobject":
                Obj = FreeCameraObject()
                self.Entity.FreeCamera.append(Obj)

                for (key, value) in childElement.attrib.iteritems():
                    if key == "sensitivity":
                        Obj.sensitivity = float(value)
                    if key == "speed":
                        Obj.speed = float(value)
            
            #CONTROL OBJECT
            if childElement.tag == "controlobject":
                Obj = ControlObject()
                self.Entity.Control.append(Obj)
                for (key, value) in childElement.attrib.iteritems():
                    if key == "type":
                        Obj.etype = str(value)
                    if key == "movementspeed":
                        Obj.movementspeed = int(value)
                    if key == "turnspeed":
                        Obj.turnspeed = int(value)
            
            # FOLLOWCAMERA OBJECT
            if childElement.tag == "followcameraobject":
                Obj = FollowCameraObject()
                self.Entity.FollowCamera.append(Obj)
                for (key, value) in childElement.attrib.iteritems():
                    if key == "node":
                        Obj.node = str(value)
            
            # PHYSICCONTROLLER OBJECT
            if childElement.tag == "physiccontrollerobject":
                Obj = PhysicControllerObject()
                self.Entity.PhysicController.append(Obj)
                
                for (key, value) in childElement.attrib.iteritems():
                    if key == "slopelimit":
                        Obj.slopelimit = float(value)
                    elif key == "steplimit":
                        Obj.steplimit = float(value)
                for child in childElement.getchildren():
                    if child.tag == "capsuleshape":
                        Obj.shape = PhysicControllerShapeCapsule()
                        for (key, value) in child.attrib.iteritems():
                            if key == "height":
                                Obj.shape.height = float(value)
                            if key == "radius":
                                Obj.shape.radius = float(value)
            #AI OBJECT                     
            if childElement.tag == "aiobject":
                Obj = AiObject()
                self.Entity.Ai.append(Obj)
                for (key, value) in childElement.attrib.iteritems():
                    if key == "startstate":
                        Obj.startstate = str(value)
            
            # LIGHT OBJECT
            if childElement.tag == "lightobject":
                for child in childElement.getchildren():
                    Obj = LightObject()
                    self.Entity.Light.append(Obj)
                    for (key, value) in child.attrib.iteritems():
                        if key == "name":
                            Obj.name = value
                        if key == "node":
                            Obj.node = value
                        if key == "type":
                            Obj.lighttype = value
                        for nodechild in child.getchildren():
                            if nodechild.tag == "diffuse":
                                Obj.diffuse = ogre.Vector3(float(nodechild.attrib["x"]), float(nodechild.attrib["y"]) , float(nodechild.attrib["z"]))
                            elif nodechild.tag == "specular":
                                Obj.specular = ogre.Vector3(float(nodechild.attrib["x"]),float(nodechild.attrib["y"]), float(nodechild.attrib["z"]))
                            elif nodechild.tag == "direction":
                                if not len(nodechild.attrib) == 0:
                                    Obj.direction = ogre.Vector3(float(nodechild.attrib["x"]), float(nodechild.attrib["y"]) , float(nodechild.attrib["z"]))
                                else: Obj.direction = ogre.Vector3(0.0 ,0.0, 0.0)
            # AUDIO OBJECT
            if childElement.tag == "audioobject":
                #aObj = AudioObject()
                #self.Entity.Audio.append(Obj)
                for child in childElement.getchildren():
                    if child.tag == "source":
                        sObj = AudioSource()
                        self.Entity.Audio.source.append(sObj)
                        for (key, value) in child.attrib.iteritems():
                            if key == "name":
                                sObj.name = value
                            elif key == "node":
                                sObj.node = value

        
        return self.Entity
