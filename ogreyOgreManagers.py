import wx
import wx.gizmos
import wx.lib
from wx.lib.scrolledpanel import *
import sys
import wxogre
from FlatNotebook import *
import ogre.renderer.OGRE as ogre
#from imagebrowser import *
#import Image

import time
#import FreeImagePy as FIPY

from ogreyEntity import *
from ogreyLevel import *
from ogreyEntityTree import *
from ogreyAttributesPanel import *
from ogreyLevelAttributesPanel import *
from ogreyExportEntity import *
from ogreyImportEntity import *
from ogreyOptionsPanel import *
from ogreyScriptEditor import *
from ogreyLevelTree import *
from ogreyConfig import *
from ogreyMaterialTool import *
from ogreySingleton import *
from ogreyTool import *


class PositionArrow:
    def __init__(self, parent, name):
        pass
                

class SceneFloor:
    def __init__(self, parent, name):
        self.parent = parent
        plane = ogre.Plane()
        plane.normal = ogre.Vector3(0, 1, 0)
        plane.d = 2
        ogre.MeshManager.getSingleton().createPlane(name, "General", plane, 200, 200, 1, 1, True, 1, 4, 4, (0, 0, 1))
        self.sceneFloor = self.parent.createEntity(name, name)
        #self.sceneFloor.setMaterialName('Grid')
        self.sceneFloorNode = self.parent.rootSceneNode.createChildSceneNode()
        self.sceneFloorNode.attachObject(self.sceneFloor)
        self.sceneFloor.castShadows = False
        self.sceneFloor.setVisible(True)
        self.material = None
    
    def reload(self):
        if not self.material == None:
            self.setMaterial(self.material)
    
    def setPosition(self, position):
        self.sceneFloorNode.position = position
        
    def getPosition(self):
        return self.sceneFloorNode.position
    
    def setScale(self, scale):
        self.sceneFloorNode.scale = scale
    def getScale(self):
        return self.sceneFloorNode.scale

    def setMaterial(self, material):
        self.sceneFloor.setMaterialName(material)
        self.material = material
        
    def getMaterial(self):
        return self.material
        
    def setVisible(self, visible = True):
        self.sceneFloor.setVisible(visible)
    
    def getVisible(self):
        return self.sceneFloor.visible

class ModelTree(wx.TreeCtrl):
    def __init__(self, parent):
        wx.TreeCtrl.__init__(self, parent, style = wx.TR_HIDE_ROOT)
        self.AddRoot("Root")
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelect)
        self.window = None
    
    def OnSelect(self, event):
        if not self.window == None:
            self.window.showEntity(self.GetItemData(self.GetSelection()).GetData())

    def add(self, Model):
        modelEntity = Entity()
        object = TransformObject()
        modelEntity.Transform.append(object)
        object.node = "RootNode"
        object.name = "RootNode"
        Model.node = object.name
        modelEntity.Graphic.append(Model)

        self.AppendItem(self.GetRootItem(), Model.name, data = wx.TreeItemData(obj=modelEntity))
    
    def bind(self, window):
        self.window = window
        pass

class WindowSplitter(wx.SplitterWindow):
    def __init__(self, parent):
        wx.SplitterWindow.__init__(self, parent)
        
class OgreScene:
    def __init__(self, ogreMgr, parent, nameFactory):
        #wx.Window.__init__(self, parent, -1)
        self.ogreMgr = ogreMgr
        self.sceneManager = None
        self.parent = parent
        self.ogreViews = []
        self.nameFactory = nameFactory
        
    def create(self):
        self.sceneManager = self.ogreMgr.getScene(None, None)
        view = self.getView()

        self.define()
        
        return view

    def getView(self):
        view = OgreView(self.parent, self)
        (a,b,c) = self.ogreMgr.getView(view, self.sceneManager)
        view.create(a,b,c)
        
        self.ogreViews.append(view)
        return view

    def destroyView(self, ogreView):
        pass

    def getSceneManager(self):
        return self.sceneManager
    
    def define(self):
        
        self.ModelDB = []
        self.EntityDB =  []
        self.LevelDB = []
        self.EntityInstanceDB = []
        self.worldScaleMultiple = ogre.Vector3(100.0, 100.0 ,100.0)
        self.sceneManager.showBoundingboxes = True
    
        self.sceneManager.shadowTechnique = ogre.SHADOWTYPE_NONE
        self.sceneManager.shadowColour = (1.0,1.0,1.0)
    
        self.createDefaultScene()
        
        self.frameTimer = ogre.Timer()

        self.animTimer = wx.Timer(self.parent, 404)
        self.animTimer.Start(5)
        self.parent.Bind(wx.EVT_TIMER, self.updateAnimation, id = 404)

    def createDefaultScene(self):

        self.sceneManager.ambientLight = 0.5, 0.5, 0.5

        self.sceneFloor = SceneFloor(self.sceneManager, self.nameFactory.getName())

        self.defaultLight = self.sceneManager.createLight(self.nameFactory.getName())
        self.defaultLight.position = (20, 80, 50)
        self.defaultLight.visible = True
        
        
        
        # Create Arrow

        self.ArrowNode = self.sceneManager.rootSceneNode.createChildSceneNode()
        
        # X
        self.xArrowEntity = self.sceneManager.createEntity(self.nameFactory.getName(), 'xArrow.mesh')
        self.xArrowEntity.setMaterialName('xArrow')
        #self.xArrowNode = self.sceneManager.rootSceneNode.createChildSceneNode()
        self.xArrowNode = self.ArrowNode.createChildSceneNode()
        self.xArrowNode.attachObject(self.xArrowEntity)
        self.xArrowNode.position = (0, 0, 0)
        self.xArrowNode.scale = (1.5, 1.5, 1.5)
        self.xArrowEntity.castShadows = False
        self.xArrowEntity.setVisible(False)
        
        # Y
        
        self.yArrowEntity = self.sceneManager.createEntity(self.nameFactory.getName(), 'yArrow.mesh')
        self.yArrowEntity.setMaterialName('yArrow')
        #self.yArrowNode = self.sceneManager.rootSceneNode.createChildSceneNode()
        self.yArrowNode = self.ArrowNode.createChildSceneNode()
        self.yArrowNode.attachObject(self.yArrowEntity)
        self.yArrowNode.position = (0, 0, 0)
        self.yArrowNode.scale = (1.5, 1.5, 1.5)
        self.yArrowEntity.castShadows = False
        self.yArrowEntity.setVisible(False)

        # Z
        
        self.zArrowEntity = self.sceneManager.createEntity(self.nameFactory.getName(), 'zArrow.mesh')
        self.zArrowEntity.setMaterialName('zArrow')
        #self.zArrowNode = self.sceneManager.rootSceneNode.createChildSceneNode()
        self.zArrowNode = self.ArrowNode.createChildSceneNode()
        self.zArrowNode.attachObject(self.zArrowEntity)
        self.zArrowNode.position = (0, 0, 0)
        self.zArrowNode.scale = (1.5, 1.5, 1.5)
        self.zArrowEntity.castShadows = False
        self.zArrowEntity.setVisible(False)
        
        #self.ArrowNode = self.sceneManager.rootSceneNode.createChildSceneNode()
        #self.ArrowNode.addChild(self.xArrowNode)
        #self.ArrowNode.addChild(self.yArrowNode)
        #self.ArrowNode.addChild(self.zArrowNode)
            
    def reload(self):
        self.sceneFloor.reload()
        self.updateEntities()

    def updateEntities(self):
        tempEnts = self.EntityDB
        self.clearSceneFromEntities()
        for ent in tempEnts:        
            self.showEntity(ent)
    
    def setAttributePanel(self, attributesPanel):
        self.attributesPanel = attributesPanel

    def updateAnimation(self, event):
        milli = self.frameTimer.getMilliseconds()
        #print milli
        for entity in self.EntityDB:
            for entGrapObj in entity.AnimatedGraphic:
                if not entGrapObj.animationObject.activeAnimation == None:
                    entGrapObj.animationObject.activeAnimation.addTime((milli * 0.001) * entGrapObj.animationObject.activeAnimation.speed)
        self.frameTimer.reset()

    def showEntity(self, Entity):
        self.EntityDB.append(Entity)

        for Node in Entity.Transform:
            parent = self.hasParent(Node, Entity.Transform)
            if parent == None: parent = self.sceneManager.rootSceneNode
            if not Node.ogreNode == None: 
                Node.ogreNode.removeAndDestroyAllChildren()
                Node.ogreNode = None
            Node.ogreParentNode = parent
            Node.ogreNode = parent.createChildSceneNode((Node.position))
            Node.ogreNode.scale = Node.scale * self.worldScaleMultiple
            #orien = Node.ogreNode.orientation
            #Node.ogreNode.yaw(1.0-(Node.rotation.y/360.0))
            #Node.ogreNode.rotate = ogre.Quaternion(0.0, Node.rotation.x, Node.rotation.y, Node.rotation.z)
            #Node.ogreNode.rotate = Node.rotation
            #Node.ogreNode.pitch(ogre.Degree(Node.rotation.x))
            #Node.ogreNode.roll(ogre.Degree(Node.rotation.z))
        
            for GrapObj in Entity.Graphic:
                if GrapObj.node == Node.name:
                    if not GrapObj.ogreEntity == None: 
                        self.sceneManager.destroyEntity(GrapObj.ogreEntity)
                        GrapObj.ogreEntity = None 
                    if not GrapObj.model == "": 
                        GrapObj.ogreEntity = self.sceneManager.createEntity("entit" + str(self.nameFactory.getName()), GrapObj.model)
                        Node.ogreNode.attachObject(GrapObj.ogreEntity)
                        GrapObj.ogreNode = Node.ogreNode
                        GrapObj.ogreEntity.castShadows = True
                        if not GrapObj.material == "":GrapObj.ogreEntity.setMaterialName(GrapObj.material)
            
            for GrapObj in Entity.AnimatedGraphic:
                if GrapObj.node == Node.name:
                    if not GrapObj.ogreEntity == None: 
                        self.sceneManager.destroyEntity(GrapObj.ogreEntity)
                        GrapObj.ogreEntity = None 
                    if not GrapObj.model == "":
                        #print GrapObj.model
                        name = "entity" + str(self.nameFactory.getName()) 
                        #print name
                        GrapObj.ogreEntity = self.sceneManager.createEntity(name, GrapObj.model)
                        Node.ogreNode.attachObject(GrapObj.ogreEntity)
                        GrapObj.ogreNode = Node.ogreNode
                        GrapObj.ogreEntity.castShadows = True
                        if not GrapObj.material == "":GrapObj.ogreEntity.setMaterialName(GrapObj.material)

            if len(Entity.Light) == 0:
                self.defaultLight.visible = True
            else:
                self.defaultLight.visible = False

                for light in Entity.Light:
                    if light.node == Node.name:
                        if not light.ogreLight == None:
                            self.sceneManager.destroyLight(light.ogreLight)
                            light.ogreLight = None
                        light.ogreLight = self.sceneManager.createLight("Light" + self.nameFactory.getName())
                        if light.lighttype == "point":
                            light.ogreLight.type = ogre.Light.LT_POINT
                        elif light.lighttype == "spotlight":
                            light.ogreLight.type = ogre.Light.LT_SPOTLIGHT
                            light.ogreLight.direction = light.direction
                            light.ogreLight.spotInner = ogre.Degree(light.innerAngle)
                            light.ogreLight.spotOuter = ogre.Degree(light.outerAngle)
                            light.ogreLight.spotFalloff = light.falloff
                        elif light.lighttype == "directional":
                            light.ogreLight.type = ogre.Light.LT_DIRECTIONAL
                            light.ogreLight.direction = light.direction
                        
                        light.ogreLight.diffuseColour = (light.diffuse.x, light.diffuse.y, light.diffuse.z)
                        light.ogreLight.specularColour = (light.specular.x, light.specular.y, light.specular.z)
                        light.ogreLight.powerScale = light.powerScale
                        light.ogreLight.range = light.range
                        light.ogreLight.position = Node.ogreNode.position
                        Node.ogreNode.attachObject(light.ogreLight)
                        light.ogreNode = Node.ogreNode
                        self.sceneManager.ambientLight = 0.0, 0.0, 0.0
                    
    def clearSceneFromEntities(self):
        for entity in self.EntityDB:
            for Node in entity.Transform:
                if not Node.ogreNode == None: self.sceneManager.destroySceneNode(Node.ogreNode.name)#Node.ogreNode.removeAndDestroyAllChildren()
                Node.ogreNode = None
                for GrapObj in entity.Graphic:
                    if GrapObj.node == Node.name:
                        if not GrapObj.ogreEntity == None: 
                            self.sceneManager.destroyEntity(GrapObj.ogreEntity)
                            GrapObj.ogreEntity = None
                for GrapObj in entity.AnimatedGraphic:
                    if GrapObj.node == Node.name:
                        if not GrapObj.ogreEntity == None: 
                            self.sceneManager.destroyEntity(GrapObj.ogreEntity)
                            GrapObj.ogreEntity = None
                for light in entity.Light:
                    if light.node == Node.name:
                        if not light.ogreLight == None:
                            self.sceneManager.destroyLight(light.ogreLight)
                            light.ogreLight = None
                
        del self.EntityDB
        self.EntityDB = []
    def hasParent(self, Node, Search):
        for searchNode in Search:
            if Node.node == searchNode.name and Node != searchNode:
                return searchNode.ogreNode
        return None
    
    def showLevel(self, Level):
        for EnityInstace in Level:
            pass
        
    def showModel(self, Model):
        entity = self.sceneManager.createEntity(self.nameFactory.getName(), Model)
        node = self.sceneManager.rootSceneNode.createChildSceneNode((0,0,0))
        #node.attachObject(entity)
        self.ModelDB.append(node)
            
class OgreView(wx.Window):
    def __init__(self, parent, ogreScene):
        wx.Window.__init__(self, parent, style = wx.CLIP_CHILDREN | wx.NO_FULL_REPAINT_ON_RESIZE)
        self.ogreScene = ogreScene
        self.statusbar = None
        self.sceneManager = self.ogreScene.getSceneManager()
        #self.define()
        
    def create(self, renderWindow, camera, viewport):
        self.renderWindow = renderWindow
        self.camera = camera
        self.resetcamera = self.camera.position
        self.resetcameradirection = self.camera.direction

        self.viewport = viewport # = self.ogreScene.getView(self)
        self.define()
    
    def define(self):
        
        self.marked = None
        self.oldpos = ogre.Vector3(0.0 ,0.0, 0.0)        
        
        # Cameras move scale/speeds
        
        self.MouseWheelZoomScale = 5.0
        self.MouselMiddlebuttonZoomScale = 7.0
        self.MouselMiddlebuttonMovmentScale = 1.0
        self.MouseLeftbuttonRotationScale = 5.0
        self.MouseRightbuttonRotationScale = 5.0
        self.KeyboardFreeCameraMovmentScale = 20.0
        self.MouseFreeCameraRotationScale = 2.0
        
        self.cameraControl = None
        
        #self.createDefaultScene()
        
        self.mousePos = ogre.Vector2(0,0)
        #self.Bind(wx.EVT_LEFT_DOWN, self.OnPickObject)
        self.Bind(wx.EVT_MOUSEWHEEL, self.OnSceneControlZoom)
        self.Bind(wx.EVT_MOTION, self.OnSceneControlRotate)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyEvent)
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnEnterWindow)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeaveWindow)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.flicker)
        
        # Timer for FPS Rate
        self.timer = wx.Timer(self, 1)
        
        # Update FPS
        self.timer.Start(1)
        self.Bind(wx.EVT_TIMER, self.updateFPS, id=1)
        
        self.cameraNode = self.sceneManager.rootSceneNode.createChildSceneNode()
        self.cameraNode.attachObject(self.camera)
            
    def flicker(self, event):
        pass
    
    def OnEnterWindow(self, event):
        self.SetFocus()
    
    def OnLeaveWindow(self, event):
        if self.cameraControl == "FreeCamera":
            self.WarpPointer(self.GetSizeTuple()[0]/2, self.GetSizeTuple()[1]/2)
            
    def OnSceneControlZoom(self, event):
        self.SetCursor(wx.StockCursor(wx.CURSOR_MAGNIFIER))
        wheelRot = event.GetWheelRotation()
        Direction = self.camera.direction
        Direction.z = -wheelRot/self.MouseWheelZoomScale
        self.camera.moveRelative(Direction)
    
    def OnSceneControlRotate(self, event):
        #self.ogreMgr._setCurrentSceneManager = self.sceneManager
        if not self.cameraControl == "FreeCamera": self.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
        
        if event.ButtonIsDown(wx.MOUSE_BTN_MIDDLE) and event.AltDown() == False:
            self.SetCursor(wx.StockCursor(wx.CURSOR_MAGNIFIER))
            currentMousePos = event.GetPositionTuple()
            Direction = self.camera.direction
            moveScale = self.MouselMiddlebuttonZoomScale

            if self.mousePos[1] < currentMousePos[1]:
                Direction.z += 1 * moveScale
            elif self.mousePos[1] > currentMousePos[1]:
                Direction.z -= 1 * moveScale
            else:
                Direction.z += 0.00
            #Direction.z = 10#-wheelRot/5
            self.camera.moveRelative(Direction)
            self.mousePos = currentMousePos
        
        if event.ButtonIsDown(wx.MOUSE_BTN_RIGHT) and self.marked != None and event.AltDown() == False and event.ShiftDown() == True:
            currentMousePos = event.GetPositionTuple()
            scale = self.marked.scale
            moveScale = 0.1

            if self.mousePos[1] < currentMousePos[1]:
                scale.x += 1 * moveScale
                scale.y += 1 * moveScale
                scale.z += 1 * moveScale

            elif self.mousePos[1] > currentMousePos[1]:
                scale.x -= 1 * moveScale
                scale.y -= 1 * moveScale
                scale.z -= 1 * moveScale

            else:
                pass
                #scale.z += 0.00
            
            self.marked.scale = scale
            #Direction.z = 10#-wheelRot/5
            #self.camera.moveRelative(Direction)
            self.mousePos = currentMousePos
        
        if event.ButtonIsDown(wx.MOUSE_BTN_LEFT) and self.marked != None and event.AltDown() == False and event.ShiftDown() == True:
            currentMousePos = ogre.Vector2(event.GetPositionTuple())
            moveScale = self.MouseLeftbuttonRotationScale
            
            (windX, windY) = self.GetSizeTuple()
            tx = event.GetX() / float(windX)
            ty = event.GetY() / float(windY)
            
            ray = self.camera.getCameraToViewportRay(tx, ty)           
            
            if not self.arrowMarked == None:
                if self.arrowMarked.name == self.xArrowNode.name:
                    newpos = ray.getPoint(1000)
                    self.ArrowNode.translate((newpos.x - self.oldpos.x) * moveScale, 0,0)
                    self.oldpos = newpos

                elif self.arrowMarked.name == self.yArrowNode.name:
                    newpos = ray.getPoint(1000)
                    self.ArrowNode.translate(0,(newpos.y - self.oldpos.y) * moveScale,0)
                    self.oldpos = newpos

                elif self.arrowMarked.name == self.zArrowNode.name:
                    newpos = ray.getPoint(1000)
                    self.ArrowNode.translate(0,0,(newpos.z - self.oldpos.z) * moveScale)
                    self.oldpos = newpos
                self.marked.position = self.ArrowNode.position
            self.objectHasBeingMoved = True
            
            self.mousePos = currentMousePos
        
        if event.AltDown() == True and event.ButtonIsDown(wx.MOUSE_BTN_MIDDLE):
            currentMousePos = event.GetPositionTuple()
            moveScale = self.MouselMiddlebuttonMovmentScale
            
            Direction = self.camera.direction
            
            if self.mousePos[0] < currentMousePos[0]:
                Direction.x = 1.0 * moveScale
            elif self.mousePos[0] > currentMousePos[0]:
                Direction.x = -1.0 * moveScale
            else:
                Direction.x = 0.00
                
            if self.mousePos[1] < currentMousePos[1]:
                Direction.y = -1.0 * moveScale
            elif self.mousePos[1] > currentMousePos[1]:
                Direction.y = 1.0 * moveScale
            else:
                Direction.y = 0.00
            
            self.camera.moveRelative(Direction)
        
            self.mousePos = currentMousePos
        
        if event.AltDown() == True and event.ButtonIsDown(wx.MOUSE_BTN_LEFT):
            self.SetCursor(wx.StockCursor(wx.CURSOR_SIZING))

            currentMousePos = event.GetPositionTuple()
            moveScale = self.MouseLeftbuttonRotationScale

            if self.mousePos[0] < currentMousePos[0]:
                angleX = -0.01 * moveScale
            elif self.mousePos[0] > currentMousePos[0]:
                angleX = 0.01 * moveScale
            else:
                angleX = 0.00
                
            if self.mousePos[1] < currentMousePos[1]:
                angleY = -0.01 * moveScale
            elif self.mousePos[1] > currentMousePos[1]:
                angleY = 0.01 * moveScale
            else:
                angleY = 0.00
            
            self.cameraNode.yaw(angleX)
            self.cameraNode.pitch(angleY)
        
            self.mousePos = currentMousePos
        
        if event.AltDown() == True and event.ButtonIsDown(wx.MOUSE_BTN_RIGHT):
            self.SetCursor(wx.StockCursor(wx.CURSOR_SIZEWE))

            currentMousePos = event.GetPositionTuple()
            moveScale = self.MouseRightbuttonRotationScale
            
            #self.cameraNode.detachAllObjects() 
            pos = False
            if pos == False:
            #if self.marked == None:
                pos = (0,0,0)
            #    self.cameraNode.position = pos
            else:
                self.cameraNode.position = self.marked.position
            #self.cameraNode.attachObject(self.camera)
            
            if self.mousePos[0] < currentMousePos[0]:
                angleX = -0.01 * moveScale
            elif self.mousePos[0] > currentMousePos[0]:
                angleX = 0.01 * moveScale
            else:
                angleX = 0.00
                
            if self.mousePos[1] < currentMousePos[1]:
                angleY = -0.01 * (moveScale - 50)
            elif self.mousePos[1] > currentMousePos[1]:
                angleY = 0.01 * (moveScale - 50)
            else:
                angleY = 0.00

            self.cameraNode.yaw(angleX)
            #self.cameraNode.pitch(angleY)
            self.mousePos = currentMousePos
        
        if self.cameraControl == "FreeCamera":
            self.SetCursor(wx.StockCursor(wx.CURSOR_BLANK))

            currentMousePos = event.GetPositionTuple()
            moveScale = self.MouseFreeCameraRotationScale

            if self.mousePos[0] < currentMousePos[0]:
                angleX = -0.01 * moveScale
            elif self.mousePos[0] > currentMousePos[0]:
                angleX = 0.01 * moveScale
            else:
                angleX = 0.00
                
            if self.mousePos[1] < currentMousePos[1]:
                angleY = -0.01 * moveScale
            elif self.mousePos[1] > currentMousePos[1]:
                angleY = 0.01 * moveScale
            else:
                angleY = 0.00
            
            self.camera.yaw(angleX)
            self.camera.pitch(angleY)
        
            self.mousePos = currentMousePos
                            
    def OnKeyEvent(self, event):
        key = event.GetKeyCode()
        
        self.translateVector = ogre.Vector3(0.0, 0.0, 0.0)
        moveScale = self.KeyboardFreeCameraMovmentScale
        if self.cameraControl == "FreeCamera":
            if key == 65:
                self.translateVector.x = -moveScale

            if key == 68:
                self.translateVector.x = moveScale

            if key == 87:
                self.translateVector.z = -moveScale

            if key == 83:
                self.translateVector.z = moveScale

            if key == wx.WXK_PAGEUP:
                self.translateVector.y = moveScale

            if key == wx.WXK_PAGEDOWN:
                self.translateVector.y = - moveScale
            
            self.camera.moveRelative(self.translateVector)
        
        if key == 70:
            if self.cameraControl == None:
                self.cameraControl = "FreeCamera"
                self.CaptureMouse()
                
            else:
                self.cameraControl = None
                self.ReleaseMouse()
        
        if key == 82:
            self.cameraNode.position = self.resetcamera #(0, 15, 50)
            self.cameraNode.direction = self.resetcameradirection
            self.camera.position = self.cameraNode.position
            self.camera.direction = self.cameraNode.direction

        
        event.Skip()
    
    def OnPickObject(self, event):
        if event.ButtonIsDown(wx.MOUSE_BTN_LEFT) and event.AltDown() == False:

            self.m_pray_scene_query = self.sceneManager.createRayQuery(ogre.Ray(), self.sceneManager.WORLD_GEOMETRY_TYPE_MASK)
            
            if (None == self.m_pray_scene_query):
                print "Failed to create Ogre::RaySceneQuery instance"
            self.m_pray_scene_query.setSortByDistance(True)
            
            (windX, windY) = self.GetSizeTuple()
            tx = event.GetX() / float(windX)
            ty = event.GetY() / float(windY)
            
            ent = self.RaycastFromPoint(ogre.Vector2(tx, ty), None, None)
            
            if ent == False:
                #print "No hit"
                if not self.marked == None:
                    self.marked.showBoundingBox(False)
                    self.marked = None
                    self.xArrowEntity.setVisible(False)
                    self.yArrowEntity.setVisible(False)
                    self.zArrowEntity.setVisible(False)
                
            else: 
                #pass
                if not self.marked == ent.parentSceneNode:
                    if not self.marked == None: self.markedshowBoundingBox(False)                 
                    if ent.parentSceneNode.name == self.xArrowNode.name or ent.parentSceneNode.name == self.yArrowNode.name or ent.parentSceneNode.name == self.zArrowNode.name:
                        self.arrowMarked = ent.parentSceneNode
                        #print "ass"
                    else:
                        self.arrowMarked = None 
                        self.marked = ent.parentSceneNode
                        self.marked.showBoundingBox(True)
                        self.xArrowEntity.setVisible(True)
                        self.yArrowEntity.setVisible(True)
                        self.zArrowEntity.setVisible(True)
                        self.sizeArrowsAfterMarked(ent)
                        

                elif self.marked == None:
                    self.marked = ent.parentSceneNode
                    self.marked.showBoundingBox(True)
                    self.xArrowEntity.setVisible(True)
                    self.yArrowEntity.setVisible(True)
                    self.zArrowEntity.setVisible(True)

            #ent.parentSceneNode.showBoundingBox = True
            #print "Ent name: ", ent.mesh.name
        
            #self.camera.lookAt(self.marked.position)
        #self.oldpos = ogre.Vector3(0.0 ,0.0, 0.0)
        event.Skip()
    
    def sizeArrowsAfterMarked(self, ent):

        scale = self.marked.scale

        ax = ent.boundingBox
        min = ax.minimum*scale
        max = ax.maximum*scale
        size = ogre.Vector3((max.x-min.x),(max.y-min.y),(max.z-min.z))
        center = ogre.Vector3((max.x+min.x)/2.0,(max.y+min.y)/2.0,(max.z+min.z)/2.0)

        if size.x > size.y:
            big = size.y
        else:
            big = size.y
        if (size.z > big):
            big = size.z
        else:
            big = big
        if big < 1:
            big = 1

        #//size of the widgets 60
        
        size_w = big/60.0

        self.ArrowNode.scale = (2*size_w, 2*size_w, 2*size_w)

        #mSceneMgr->getRootSceneNode()->addChild(widget);
        self.ArrowNode.position = (self.marked.worldPosition+center)
        #widget->setVisible(true);

    def RaycastFromPoint(self, point, normal, result):
        
        # create the ray to test
        #ray = ogre.Ray(ogre.Vector3(point.x, point.y, point.z),
        #              ogre.Vector3(normal.x, normal.y, normal.z))
        ray =  self.camera.getCameraToViewportRay(point.x, point.y)
        result = ogre.Vector3(0.0 , 0.0, 0.0)
        self.retRay = ray

        # check we are initialised
        if (self.m_pray_scene_query != None):
        
            # create a query object
            self.m_pray_scene_query.Ray = ray
            #execute the query, returns a vector of hits
            # for queryResult in self.m_pray_scene_query.execute():
            #    print "hih"
            if (self.m_pray_scene_query.execute().size() <= 0):
            #    # raycast did not hit an objects bounding box
                return False
        else:
            print "Cannot raycast without RaySceneQuery instance"
            return False

        # at this point we have raycast to a series of different objects bounding boxes.
        # we need to test these different objects to see which is the first polygon hit.
        # there are some minor optimizations (distance based) that mean we wont have to
        # check all of the objects most of the time, but the worst case scenario is that
        # we need to test every triangle of every object.
        closest_distance = -1.0
        closest_result = None
        
        query_result = self.m_pray_scene_query.getLastResults()
        qr_idx = 0
        while (qr_idx < query_result.size()):
            #stop checking if we have found a raycast hit that is closer
            #than all remaining entities
            
            if ((closest_distance >= 0.0) and (closest_distance < query_result[qr_idx].distance)):
                 break
           
            #only check this result if its a hit against an entity
            if ((query_result[qr_idx].movable != None) and (query_result[qr_idx].movable.movableType == "Entity")):
                #get the entity to check
                pentity = query_result[qr_idx].movable           

                # mesh data to retrieve         
                vertex_count = None
                index_count = None
                vertices = ogre.Vector3(0.0, 0.0, 0.0)
                indices = None

                #get the mesh information
                (vertics, indices) = self.GetMeshInformation(pentity.mesh, vertex_count, vertices, index_count, indices,             
                                  pentity.parentNode.position,
                                  pentity.parentNode.orientation,
                                  pentity.parentNode.scale)

                #test for hitting individual triangles on the mesh
                new_closest_found = False
                indi = 0
                #closest_distance = -1.0
                for indi in range(len(indices)):
                #for (int i = 0; i < static_cast<int>(index_count); i += 3)
                    
                    #check for a hit against this triangle
                    try: 
                        v1 = ogre.Vector3(indices[indi + 0])
                        v2 = ogre.Vector3(indices[indi + 1])
                        v3 = ogre.Vector3(indices[indi + 2])

                        (hit, distance) = ogre.Math.intersects(ray, v1 , v2 , v3, True, False)

                        bole = self.RayTriIntersect(ray, v1, v2, v3)
                        #print bole
                        #if it was a hit check if its the closest
                        if (bole):
                            if ((closest_distance < 0.0) or (distance < closest_distance)):
                                #this is the closest so far, save it off
                                closest_distance = distance
                                new_closest_found = True
                                new_closet_mesh = pentity
                    except:
                        pass
                indi += 3

                # free the verticies and indicies memory
                vertices = []
                indices = []

                # if we found a new closest raycast for this object, update the
                # closest_result before moving on to the next object.
                if (new_closest_found):
                    closest_result = ray.getPoint(closest_distance)               
            
            qr_idx += 1
        self.retDistance = closest_distance
        if (closest_distance >= 0.0):
            
            result = ogre.Vector3(closest_result.x, closest_result.y, closest_result.z)
            #print closest_result.x, closest_result.y, closest_result.z
            return new_closet_mesh
        else: 
            if not len(query_result) == 0:
                for re in query_result:
                    if re.movable.movableType == "Entity":
                        return re.movable
            return False

    # Get the mesh information for the given mesh.
    # Code found on this forum link: http://www.ogre3d.org/wiki/index.php/RetrieveVertexData
    def GetMeshInformation(self, mesh, vertex_count, vertices, index_count, indices,position, orient, scale):

        added_shared = False
        current_offset = 0
        shared_offset = 0
        next_offset = 0
        index_offset = 0
        
        verts = []
        indices = []
        useShared = False 
        for i in range(mesh.numSubMeshes):
            if not useShared:
                verts += mesh.getSubMesh(i).vertices
                useShared = mesh.getSubMesh(i).useSharedVertices

        indices += mesh.getSubMesh(i).indices
        #print len(indices)
        #print "----------------"
        #print "Total Vertices %i Indices %i" % (len(verts), len(indices))
        #print "----------------"
        
        return (verts, indices) 

       #// triangle intersect from http://www.graphics.cornell.edu/pubs/1997/MT97.pdf
    def RayTriIntersect(self, r, v0, v1, v2):
        edge1 = ogre.Vector3(0.0 , 0.0, 0.0) 
        edge2 = ogre.Vector3(0.0, 0.0, 0.0)
        pvec = ogre.Vector3(0.0 , 0.0, 0.0)
        tvec = ogre.Vector3(0.0, 0.0, 0.0)
        qvec = ogre.Vector3(0.0 ,0.0, 0.0)
        det = 0.0 
        i = 0.0
        nv_det = 0.0
        #r = 0.0
        u = 0.0
        v = 0.0

       #/* find vectors for two edges sharing vert0 */
        edge1 = v1 - v0
        edge2 = v2 - v0

       #/* begin calculating determinant - also used to calculate U parameter */
        pvec = r.direction.crossProduct(edge2)

       #/* if determinant is near zero, ray lies in plane of triangle */
        det = edge1.dotProduct(pvec);

        if (det > -0.000001 and det < 0.000001):return False
        inv_det = 1.0 / det

       #/* calculate distance from vert0 to ray origin */
        tvec = r.origin - v0

       #/* calculate U parameter and test bounds */
        u = tvec.dotProduct(pvec) * inv_det
        if (u < 0.0 or u > 1.0): return False

       #/* prepare to test V parameter */
        qvec = tvec.crossProduct(edge1);

       #/* calculate V parameter and test bounds */
        v = r.direction.dotProduct(qvec) * inv_det
        if (v < 0.0 or (u + v) > 1.0): return False

       #/* calculate t, ray intersects triangle */
        t = edge2.dotProduct(qvec) * inv_det

        return True
        
    def getAttributes(self):
        return (self.renderWindow, self.camera, self.viewport, self.root)
    
    def renderModeSolid(self):
        self.camera.polygonMode = ogre.PM_SOLID
    def renderModeWireframe(self):
        self.camera.polygonMode = ogre.PM_WIREFRAME
    def renderModePoints(self):
        self.camera.polygonMode = ogre.PM_POINTS
    
    
    def setStatusbar(self, statusbar):
        self.statusbar = statusbar
    
    def updateFPS(self, event):
        if not self.statusbar == None:
            # Remove the amount of traingles the scenfloor have, just to get the user buildup scene count of traingles
            if self.ogreScene.sceneFloor.getVisible():
                dec = 4
            else: dec = 2
            if self.sceneManager.shadowTechnique == ogre.SHADOWTYPE_NONE: dec = 2
            elif self.sceneManager.shadowTechnique == ogre.SHADOWDETAILTYPE_ADDITIVE: dec = 2
            elif self.sceneManager.shadowTechnique == ogre.SHADOWDETAILTYPE_MODULATIVE: dec = 2
            elif self.sceneManager.shadowTechnique == ogre.SHADOWDETAILTYPE_STENCIL: dec = 2

            self.statusbar.SetStatusText("FPS: " + str(int(self.renderWindow.lastFPS)) + ' | Triangle Count: ' + str(int(self.renderWindow.triangleCount)-dec),1)

class ResourceInformation:
    __metaclass__=Singleton
    def __init__(self):
        self.create()
    def create(self):
        materialIterator = ogre.MaterialManager.getSingleton().getResourceIterator()

        self.loadedMaterials = []
        self.materialsOrigin = []
        while (materialIterator.hasMoreElements()):
            #mat = ogre.MaterialPointer(ogre.MaterialManager.getSingleton().getByName(materialIterator.peekNextValue().name))
            mat = ogre.MaterialManager.getSingleton().getByName(materialIterator.peekNextValue().name)
            if not mat.origin == "":
                self.materialsOrigin.append({"name" : mat.getName(), "group" : mat.getGroup(), "origin" : mat.getOrigin()})
                self.loadedMaterials.append(mat.name)
            materialIterator.moveNext()

    def reload(self):
        self.create()
        
class Project(wx.Window):
    def __init__(self, parent):
        wx.Window.__init__(self, parent)
        self.parent = parent
    
    def create(self):
        pass
    
    def destroy(self):
        pass

class OgreyLevelProject(WindowSplitter):
    def __init__(self, parent, ogreMgr, statusbar, resourceInformation, configManager):
        WindowSplitter.__init__(self, parent)
        self.parent = parent
        self.ogreMgr = ogreMgr
        self.statusbar = statusbar
        self.resourceInformation = resourceInformation
        self.configManager = configManager
        #self.Fit()
        self.create()
        
        #wx.EVT_H
    
    def create(self):
        self.definePanels()
        self.defineTools()
    
    def definePanels(self):
        self.leftNotebook = LeftNotebook(self)
        self.topAndBottomSplitter = WindowSplitter(self)
        self.SetSashGravity(0.0)
        self.SetMinimumPaneSize(230)
        
        self.topAndBottomSplitter.SetSashGravity(1.0)
        self.topAndBottomSplitter.SetMinimumPaneSize(250)

        self.SplitVertically(self.leftNotebook,  self.topAndBottomSplitter, 1)
        self.SetSashPosition(230, True)

        self.rightNotebook = RightNotebook(self.topAndBottomSplitter)
        self.middleNotebook = MiddleNotebook(self.topAndBottomSplitter)
        self.topAndBottomSplitter.SplitVertically(self.middleNotebook, self.rightNotebook, 0.5)
    
    def defineTools(self):
        
        self.level = Level()
        self.nameFactory = NameFactory()

        self.ogreScene = OgreScene(self.ogreMgr, self.middleNotebook, self.nameFactory)
        self.ogreView = self.ogreScene.create()
              
        self.attributesPanel = ogreyLevelAttributesPanel(self.rightNotebook, self.ogreScene, self.resourceInformation, self.middleNotebook)
        self.attributesPanel.bindScene(self.ogreScene)
        self.attributesPanel.bindView(self.ogreView)
        self.attributesPanel.bindLevel(self.level)
        self.rightNotebook.AddPage(self.attributesPanel, "Level Entity Attributes")
        
        self.optionsPanel = ogreyOptionsPanel(self.rightNotebook, self.resourceInformation)
        self.optionsPanel.bindScene(self.ogreScene)
        self.optionsPanel.bindView(self.ogreView)
        self.rightNotebook.AddPage(self.optionsPanel, "Scene/View Options", True)
        self.middleNotebook.bindWindow(self.optionsPanel)         
        
        self.middleNotebook.AddPage(self.ogreView, "Entity Viewpoint", True)
        
        self.middleNotebook.AddPage(LogList(self.middleNotebook), "Error Log", False)
        
        self.levelTree = LevelTree(self.leftNotebook, self.attributesPanel)
        self.levelTree.bindLevel(self.level)
        self.leftNotebook.AddPage(self.levelTree, "Entity Instances")
                
        self.levelTree.bind(self.ogreScene)

        self.ogreView.setStatusbar(self.statusbar)
    
    def reload(self):
        self.ogreScene.reload()
            
    def destroy(self):
        pass
        

class OgreyEntityManager(WindowSplitter):
    def __init__(self, parent, ogreMgr, statusbar, resourceInformation, configManager):
        WindowSplitter.__init__(self, parent)
        #wx.Frame.__init__(self, parent, -1, "Entity Resource Manager", size=(1000, 700))
        #wx.Window.__init__(self, parent, -1)        
        self.parent = parent
        self.ogreMgr = ogreMgr
        self.statusbar = statusbar
        self.resourceInformation = resourceInformation
        self.configManager = configManager
        #self.Fit()
        #self.Show()
        self.create()

    def create(self):
        self.definePanels()
        self.defineTools()
    
    def definePanels(self):
        
        self.leftAndRightSplitter = self #WindowSplitter(self)
        self.leftNotebook = LeftNotebook(self.leftAndRightSplitter)
        self.topAndBottomSplitter = WindowSplitter(self.leftAndRightSplitter)
        self.leftAndRightSplitter.SetSashGravity(0.0)
        self.leftAndRightSplitter.SetMinimumPaneSize(230)
        
        self.topAndBottomSplitter.SetSashGravity(1.0)
        self.topAndBottomSplitter.SetMinimumPaneSize(250)

        self.leftAndRightSplitter.SplitVertically(self.leftNotebook,  self.topAndBottomSplitter, 1)
        self.leftAndRightSplitter.SetSashPosition(230, True)

        self.rightNotebook = RightNotebook(self.topAndBottomSplitter)
        self.middleNotebook = MiddleNotebook(self.topAndBottomSplitter)
        self.topAndBottomSplitter.SplitVertically(self.middleNotebook, self.rightNotebook, 0.5)
    
    def defineTools(self):
        
        self.nameFactory = NameFactory()

        self.ogreScene = OgreScene(self.ogreMgr, self.middleNotebook, self.nameFactory)
        self.ogreView = self.ogreScene.create()
              
        self.attributesPanel = ogreyAttributesPanel(self.rightNotebook, self.ogreScene, self.resourceInformation, self.middleNotebook)
        self.rightNotebook.AddPage(self.attributesPanel, "Entity Attributes")
        
        self.optionsPanel = ogreyOptionsPanel(self.rightNotebook, self.resourceInformation)
        self.optionsPanel.bindScene(self.ogreScene)
        self.optionsPanel.bindView(self.ogreView)
        self.rightNotebook.AddPage(self.optionsPanel, "Options", True)
        self.middleNotebook.bindWindow(self.optionsPanel)         
        
        self.middleNotebook.AddPage(self.ogreView, "Entity Viewpoint", True)
        
        self.middleNotebook.AddPage(LogList(self.middleNotebook), "Error Log", False)
        
        self.entityTree = EntityTree(self.leftNotebook, self.attributesPanel, self.configManager)
        self.leftNotebook.AddPage(self.entityTree, "Entities")
                
        self.entityTree.bind(self.ogreScene)

        self.ogreView.setStatusbar(self.statusbar)
        
        self.Show(True)

    
    #def getScene(self):
    #    return self.ogreScene
    
    def reload(self):
        self.ogreScene.reload()
            
    def destroy(self):
        pass
