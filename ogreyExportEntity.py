import wx
import elementtree.ElementTree as ET
#import cElementTree as ET
from elementtree.SimpleXMLWriter import XMLWriter
#import sys
#from indent import *


class ogreyExportEntity(wx.FileDialog):
    def __init__(self, parent, Entity):
        wx.FileDialog.__init__(self, parent, message="Save file", wildcard="*.xml", style=wx.SAVE | wx.OVERWRITE_PROMPT)
        if self.ShowModal() == wx.ID_OK:
            root = ET.Element("entity", attrib = {"name" : Entity.name})
            # Transform Object
            if not len(Entity.Transform) == 0:
                transformobject = ET.SubElement(root, "transformobject")
                for transObject in Entity.Transform:
                    if not transObject.name == "RootNode":
                        self.comment(transformobject, transObject)
                        node = ET.SubElement(transformobject, "node", attrib={"name" : transObject.name, "parent" : transObject.node})
                        ET.SubElement(node, "position", attrib={"x" : str(transObject.position.x), "y" : str(transObject.position.y), "z" : str(transObject.position.z)})
                        ET.SubElement(node, "rotation", attrib={"x" : str(transObject.rotation.x), "y" : str(transObject.rotation.y), "z" : str(transObject.rotation.z)})
                        ET.SubElement(node, "scale", attrib={"x" : str(transObject.scale.x), "y" : str(transObject.scale.y), "z" : str(transObject.scale.z)})
            # Graphic Object
            if not len(Entity.Graphic) == 0:
                graphicobject = ET.SubElement(root, "graphicobject")
                for grapObject in Entity.Graphic:
                    self.comment(graphicobject, grapObject)
                    mesh = ET.SubElement(graphicobject, "mesh", attrib={"name" : grapObject.name, "model" : grapObject.model, "material" : grapObject.material, "node" : grapObject.node})
            # Animated Graphic Object
            if not len(Entity.AnimatedGraphic) == 0:
                graphicobject = ET.SubElement(root, "animatedgraphicobject")
                grapObject = Entity.AnimatedGraphic[0]
                self.comment(graphicobject, grapObject)
                mesh = ET.SubElement(graphicobject, "mesh", attrib={"name" : grapObject.name, "model" : grapObject.model, "material" : grapObject.material, "node" : grapObject.node})            
            # Free Camera Object
            if not len(Entity.FreeCamera) == 0:
                for freeCam in Entity.FreeCamera:
                    self.comment(root, freeCam)
                    ET.SubElement(root, "freecameraobject", attrib={"sensitivity" : str(freeCam.sensitivity), "speed" : str(freeCam.speed)})
            # Follow Camera Object
            if not len(Entity.FollowCamera) == 0:
                for followCam in Entity.FollowCamera:
                    self.comment(root, followCam)
                    ET.SubElement(root, "followcameraobject", attrib={"node" : str(followCam.node)})
            # Control Object
            if not len(Entity.Control) == 0:
                for control in Entity.Control:
                    self.comment(root, control)
                    ET.SubElement(root, "controlobject", attrib={"type" : str(control.etype), "movementspeed" : str(control.movementspeed), "turnspeed" : str(control.turnspeed)})
            # Ai Object
            if not len(Entity.Ai) == 0:
                for ai in Entity.Ai:
                    self.comment(root, ai)
                    ET.SubElement(root, "aiobject", attrib={"startstate" : str(ai.startstate)})
            # Light Object
            if not len(Entity.Light) == 0:
                lightobject = ET.SubElement(root, "lightobject")
                for light in Entity.Light:
                    self.comment(lightobject, light)
                    node = ET.SubElement(lightobject, "light", attrib={"name" : light.name, "type" : light.lighttype, "node" : light.node})
                    ET.SubElement(node, "diffuse", attrib={"x" : str(light.diffuse.x), "y" : str(light.diffuse.y), "z" : str(light.diffuse.z)})
                    ET.SubElement(node, "specular", attrib={"x" : str(light.specular.x), "y" : str(light.specular.y), "z" : str(light.specular.z)})
                    ET.SubElement(node, "direction", attrib={"x" : str(light.direction.x), "y" : str(light.direction.y), "z" : str(light.direction.z)})
            # PhysicController
            if not len(Entity.PhysicController) == 0:
                for con in Entity.PhysicController:
                    phyCon = ET.SubElement(root, "physiccontrollerobject", attrib={"slopelimit" : str(con.slopelimit), "steplimit" : str(con.steplimit)})
                    self.comment(phyCon, con)
                    ET.SubElement(phyCon, "capsuleshape", attrib={"height" : str(con.shape.height), "radius" : str(con.shape.radius)})
            
            # Audio Object -Source
            if not len(Entity.Audio.source) == 0:
                audioO = ET.SubElement(root, "audioobject", attrib={})
                for source in Entity.Audio.source:
                    #self.comment(phyCon, con)
                    ET.SubElement(audioO, "source", attrib={"name" : str(source.name), "node" : str(source.node)})

            # Physic Object
            if not len(Entity.Physic) == 0:
                for physObject in Entity.Physic:
                    physicobject = ET.SubElement(root, "physicobject", attrib={"static" : str(physObject.static).lower()})
                    self.comment(physicobject, physObject)
                    actor = ET.SubElement(physicobject, "actor", attrib={"name" : physObject.name, "node" : physObject.node, "collisionenabled" : str(physObject.collisionenabled).lower(),
                                                                        "follow" : str(physObject.follow).lower()})
                    self.comment(actor, physObject.body)
                    body = ET.SubElement(actor, "body", attrib={"gravityenabled" : str(physObject.body.gravityenabled).lower(), "kinematic" : str(physObject.body.kinematic).lower(),
                            "lineardamping" : str(physObject.body.lineardamping), "angulardamping" : str(physObject.body.angulardamping),
                             "maxangularvelocity" :  str(physObject.body.maxangularvelocity)})
                    ET.SubElement(body, "linearvelocity", attrib={"x" : str(physObject.body.linearvelocity.x), "y" : str(physObject.body.linearvelocity.y), 
                            "z" : str(physObject.body.linearvelocity.z)})
                    ET.SubElement(body, "angularvelocity", attrib={"x" : str(physObject.body.angularvelocity.x), "y" : str(physObject.body.angularvelocity.y), 
                            "z" : str(physObject.body.angularvelocity.z)})
                    
                    for exShape in physObject.shapes:
                        xmlShape = ET.SubElement(actor, "shape", attrib={"name" : exShape.name, "collisiongroup" : exShape.collisiongroup, "material" : exShape.material, "density" : str(exShape.density)})
                        self.comment(xmlShape, exShape)

                        pose = ET.SubElement(xmlShape, "localpose", attrib={"node" : exShape.shape.localpose.node})
                        ET.SubElement(pose, "position", attrib={"x" : str(exShape.shape.localpose.position.x), "y" : str(exShape.shape.localpose.position.y), "z" : str(exShape.shape.localpose.position.z)})
                        ET.SubElement(pose, "rotation", attrib={"x" : str(exShape.shape.localpose.rotation.x), "y" : str(exShape.shape.localpose.rotation.y), "z" : str(exShape.shape.localpose.rotation.z)})
                        
                        if exShape.shape.shape == "boxshape":
                            ET.SubElement(xmlShape, "boxshape", attrib={"height" : str(exShape.shape.height), "width" : str(exShape.shape.width), "depth" : str(exShape.shape.depth)})
                        
                        elif exShape.shape.shape == "capsuleshape":
                            ET.SubElement(xmlShape, "capsuleshape", attrib={"height" : str(exShape.shape.height), "radius" : str(exShape.shape.radius)})  

                        elif exShape.shape.shape == "sphereshape":
                            ET.SubElement(xmlShape, "sphereshape", attrib={"radius" : str(exShape.shape.radius)})  
                        
                        elif exShape.shape.shape == "convexshape":
                            ET.SubElement(xmlShape, "convexshape", attrib={"mesh" : exShape.shape.mesh, "smoothmesh" : str(exShape.shape.smoothmesh) })  
                        
                        elif exShape.shape.shape == "triangleshape":
                            ET.SubElement(xmlShape, "triangleshape", attrib={"mesh" : exShape.shape.mesh, "smoothmesh" : str(exShape.shape.smoothmesh) })  
                
            root = indent(root)

            ET.ElementTree(root).write(self.GetPath(), 'us-ascii')

            self.Destroy()
    
    def comment(self, tree, obj):
        if not obj.comments == "":
            com = ET.Comment(obj.comments)
            tree.append(com)
            
def indent(elem, level=0):
    i = "\n" + level*"    "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "    "
        for e in elem:
            indent(e, level+1)
        if not e.tail or not e.tail.strip():
            e.tail = i
    if level and (not elem.tail or not elem.tail.strip()):
        elem.tail = i
    return elem
        
