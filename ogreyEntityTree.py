import wx
from ogreyEntity import *
from ogreyPopupMenu import *
from ogreyImportEntity import *
from ogreyExportEntity import *
from ogreyConfig import *

class EntityTree(wx.TreeCtrl):
    def __init__(self, parent, attributesPanel, configManager):
        wx.TreeCtrl.__init__(self, parent, -1, style = wx.TR_HAS_BUTTONS | wx.TR_HIDE_ROOT | wx.TR_LINES_AT_ROOT | wx.TR_MULTIPLE)
        
        self.entityTreeRoot = self.AddRoot(text="NoneEntity")

        self.entityAttributePanel = attributesPanel
        self.configManager = configManager

        self.window = None
        
        self.imagelist = wx.ImageList(16, 16)
        #self.imagelist.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER, wx.ART_TOOLBAR))
        self.imagelist.Add(wx.Bitmap("globe.png"))
        self.imagelist.Add(wx.Bitmap("applications-system.png"))
        self.imagelist.Add(wx.Bitmap("ogre.png"))
        self.imagelist.Add(wx.Bitmap("box.png"))
        self.imagelist.Add(wx.Bitmap("camera.png"))
        self.imagelist.Add(wx.Bitmap("control.png"))
        self.imagelist.Add(wx.Bitmap("ai.png"))
        self.imagelist.Add(wx.Bitmap("light.png"))
        self.imagelist.Add(wx.Bitmap("physiccontroller.png"))
        self.imagelist.Add(wx.Bitmap("audio.png"))

        #self.SetImageList(self.imagelist)
        self.AssignImageList(self.imagelist)
        
        self.Show(True)
        self.entityPopupMenu = PopupMenu()
        self.popupMenuItems = [
        {"type" : "Submenu 1", "enabled" : False, "menuItem" : "Submenu", "name" : "Add", 
        "items" : [
            {"type" : "Root Node", "enabled" : False, "menuItem" : wx.MenuItem(self.entityPopupMenu, -1, "RootNode - Transform Object"), "event" : self.AddRootTransformObject} , # Transform Object
            {"type" : "Node", "enabled" : False, "menuItem" : wx.MenuItem(self.entityPopupMenu, -1, "Node - Transform Object"), "event" : self.AddTransformObject} , # Transform Object
            {"type" : "Graphic Object", "enabled" : False, "menuItem" : wx.MenuItem(self.entityPopupMenu, -1, "Model - Graphic Object"), "event" : self.AddGraphicObject}, # Graphic Object
            {"type" : "Animated Graphic Object", "enabled" : False, "menuItem" : wx.MenuItem(self.entityPopupMenu, -1, "Animated Model - Animated Graphic Object"), "event" : self.AddAnimatedGraphicObject}, # Graphic Object

            {"type" : "Physic Object", "enabled" : False, "menuItem" : wx.MenuItem(self.entityPopupMenu, -1, "Actor&Body - Physic Object"), "event" : self.AddPhysicObject},
            {"type" : "Submenu 2", "enabled" : False, "menuItem" : "Submenu", "name" : "Shape - Physic Object", 
            "items" : [
                {"type" : "Box", "enabled" : True, "menuItem" : wx.MenuItem(self.entityPopupMenu, -1, "Box"), "event" : self.AddPhysicShapeBox},
                {"type" : "Capsule", "enabled" : True, "menuItem" : wx.MenuItem(self.entityPopupMenu, -1, "Capsule"), "event" : self.AddPhysicShapeCapsule}, 
                {"type" : "Sphere", "enabled" : True, "menuItem" : wx.MenuItem(self.entityPopupMenu, -1, "Sphere"), "event" : self.AddPhysicShapeSphere}, 
                {"type" : "Convex mesh", "enabled" : True, "menuItem" : wx.MenuItem(self.entityPopupMenu, -1, "Convex mesh"), "event" : self.AddPhysicShapeConvexMesh}, 
                {"type" : "Triangle mesh", "enabled" : True, "menuItem" : wx.MenuItem(self.entityPopupMenu, -1, "Triangle mesh"), "event" : self.AddPhysicShapeTriangleMesh}, 
            ]},
            {"type" : "Submenu 3", "enabled" : False, "menuItem" : "Submenu", "name" : "Light",
            "items" : [
                {"type" : "Point", "enabled" : True, "menuItem" : wx.MenuItem(self.entityPopupMenu, -1, "Point"), "event" : self.AddLightPoint},
                {"type" : "Spotlight", "enabled" : True, "menuItem" : wx.MenuItem(self.entityPopupMenu, -1, "Spotlight"), "event" : self.AddLightSpotlight},
                {"type" : "Directional", "enabled" : True, "menuItem" : wx.MenuItem(self.entityPopupMenu, -1, "Directional"), "event" : self.AddLightDirectional},
            ]},
            {"type" : "Free Camera", "enabled" : False, "menuItem" : wx.MenuItem(self.entityPopupMenu, -1, "Free Camera - Free Camera Object"), "event" : self.AddFreeCameraObject} , # Free Camera Object
            {"type" : "Follow Camera", "enabled" : False, "menuItem" : wx.MenuItem(self.entityPopupMenu, -1, "Follow Camera - Follow Camera Object"), "event" : self.AddFollowCameraObject} , # Follow Camera Object            
            {"type" : "Control", "enabled" : False, "menuItem" : wx.MenuItem(self.entityPopupMenu, -1, "Control - Control Object"), "event" : self.AddControlObject} , # Free Camera Object
            {"type" : "Ai", "enabled" : False, "menuItem" : wx.MenuItem(self.entityPopupMenu, -1, "Ai - Ai Object"), "event" : self.AddAiObject} , # Free Camera Object
            
            {"type" : "PhysicController", "enabled" : True, "menuItem" : wx.MenuItem(self.entityPopupMenu, -1, "PhysicController - PhysicController Object"), "event" : self.AddPhysicControllerObject} , # Free Camera Object
            {"type" : "Submenu 4", "enabled" : False, "menuItem" : "Submenu", "name" : "Shape",
            "items" : [
                {"type" : "Capsule", "enabled" : True, "menuItem" : wx.MenuItem(self.entityPopupMenu, -1, "Capsule"), "event" : self.AddPhysicControllerShapeCapsule} , # Free Camera Object
            ]},
            {"type" : "Submenu 5", "enabled" : False, "menuItem" : "Submenu", "name" : "Audio",
            "items" : [
                {"type" : "Source", "enabled" : True, "menuItem" : wx.MenuItem(self.entityPopupMenu, -1, "Source"), "event" : self.AddAudioSource},
                #{"type" : "Spotlight", "enabled" : True, "menuItem" : wx.MenuItem(self.entityPopupMenu, -1, "Spotlight"), "event" : self.AddLightSpotlight},
            ]},
            ]
        },
        {"type" : "Entity", "enabled" : True, "menuItem" : wx.MenuItem(self.entityPopupMenu, -1, "Create New Entity"), "event" : self.AddEntity} , # Create a new Entity
        {"type" : "Delete Object", "enabled" : False, "menuItem" :wx.MenuItem(self.entityPopupMenu, -1, "Delete Object"), "event" : self.OnDeleteObject}, # Deletet Object
        {"type" : "Seperator", "enabled" : True, "menuItem" : "Seperator"},
        {"type" : "Import", "enabled" : True, "menuItem" : wx.MenuItem(self.entityPopupMenu, -1, "Import Entity/Entities"), "event" : self.OnImport} , # Import Entity Menu Item
        {"type" : "Export", "enabled" : False, "menuItem" : wx.MenuItem(self.entityPopupMenu, -1, "Export Entity"), "event" : self.OnExport} , # Export Entity Menu Item
        ]
        self.entityPopupMenu.AddMenuItems(self.popupMenuItems) 
        self.Bind(wx.EVT_RIGHT_DOWN, self.EnityTreeRightMenu)
        self.Bind(wx.EVT_TREE_SEL_CHANGED,self.ShowObjectInformation)
        self.Bind(wx.EVT_TREE_SEL_CHANGING, self.updatePreview)
        #self.SelectItem(self.GetRootItem())
        
        #for path in self.configManager.GetConfig().resourcers:
        #entities = ogreyImportEntity(self, self.configManager.GetConfig().resourcers).Entities
        #    print path
        #print entity
        #for entity in entities:
        #    self.ImportEntity(entity)
        
        #self.CollapseAllTreeItems()
    
    def ImportEntity(self, inputEntity):
        Entity = inputEntity
        entityItem = self.AppendItem(self.GetRootItem(), Entity.name + " - Entity", 0, data = wx.TreeItemData(obj=Entity))
        for transformObj in Entity.Transform:
            item = self.FindTreeItem(transformObj.node, entityItem)
            if item == None: item = entityItem
            self.AppendItem(item, transformObj.name + " - Transform Object", 1,data = wx.TreeItemData(obj=transformObj))
            transformObj.entity = self.GetItemData(entityItem).GetData()

        for graphicObj in Entity.Graphic:    
            item = self.FindTreeItem(graphicObj.node, entityItem)
            if item == None: item = entityItem
            self.AppendItem(item, graphicObj.name + " - Graphic Object",2, data = wx.TreeItemData(obj=graphicObj))
            graphicObj.entity = self.GetItemData(entityItem).GetData()
            
        for graphicObj in Entity.AnimatedGraphic:    
            item = self.FindTreeItem(graphicObj.node, entityItem)
            if item == None: item = entityItem
            self.AppendItem(item, graphicObj.name + " - Animated Graphic Object",2, data = wx.TreeItemData(obj=graphicObj))
            graphicObj.entity = self.GetItemData(entityItem).GetData()
        
        for lightObj in Entity.Light:
            item = self.FindTreeItem(lightObj.node, entityItem)
            if item == None: item = entityItem
            self.AppendItem(item, lightObj.name + " - " + lightObj.lighttype + " Light Object", 7,data = wx.TreeItemData(obj=lightObj))
            lightObj.entity = self.GetItemData(entityItem).GetData()        
        
        for physicObj in Entity.Physic:
            item = self.FindTreeItem(physicObj.node, entityItem)
            if item == None: item = entityItem
            actorItem = self.AppendItem(item, physicObj.name + " - Physic Object", 3,data = wx.TreeItemData(obj=physicObj))
            self.AppendItem(actorItem, "Body - Physic Object", 3,data = wx.TreeItemData(obj=physicObj.body))            
            physicObj.entity = self.GetItemData(entityItem).GetData()
            physicObj.body.entity = self.GetItemData(entityItem).GetData()
            i = 0
            for shape in physicObj.shapes:
                if shape.shape.shape == "boxshape":
                    name = "Box" + str(i)
                elif shape.shape.shape == "capsuleshape":
                    name = "Capsule" + str(i)
                elif shape.shape.shape == "sphereshape":
                    name = "Sphere" + str(i)
                elif shape.shape.shape == "convexshape":
                    name = "Convex Mesh" + str(i)
                elif shape.shape.shape == "triangleshape":
                    name = "Triangle Mesh" + str(i)
                self.AppendItem(actorItem, name + " - Physic Shape Object", 3,data = wx.TreeItemData(obj=shape))
                shape.entity = self.GetItemData(entityItem).GetData()
                i += 1
        for freeCamera in Entity.FreeCamera:
            item = self.FindTreeItem(freeCamera.node, entityItem)
            #if item == None: 
            item = entityItem
            self.AppendItem(item, "Free Camera - Free Camera Object",4, data = wx.TreeItemData(obj=freeCamera))
            freeCamera.entity = self.GetItemData(entityItem).GetData()
        
        for followCamera in Entity.FollowCamera:
            item = self.FindTreeItem(followCamera.node, entityItem)
            if item == None: item = entityItem 
            self.AppendItem(item, "Follow Camera - Follow Camera Object",4, data = wx.TreeItemData(obj=followCamera))
            followCamera.entity = self.GetItemData(entityItem).GetData()
        
        for control in Entity.Control:
            #item = None #self.FindTreeItem(control.node, entityItem)
            #if item == None: 
            item = entityItem
            self.AppendItem(item, "Control - Control Object",5, data = wx.TreeItemData(obj=control))
            control.entity = self.GetItemData(entityItem).GetData()
    
        for ai in Entity.Ai:
            #item = None #self.FindTreeItem(ai.node, entityItem)
            #if item == None: 
            item = entityItem
            self.AppendItem(item, "Ai - Control Object",6, data = wx.TreeItemData(obj=ai))
            ai.entity = self.GetItemData(entityItem).GetData()
        
        for phyCon in Entity.PhysicController:
            #item = None #self.FindTreeItem(ai.node, entityItem)
            #if item == None: 
            item = entityItem
            phyItem = self.AppendItem(item, "PhysicController - PhysicController Object",8, data = wx.TreeItemData(obj=phyCon))
            phyCon.entity = self.GetItemData(entityItem).GetData()
            if not phyCon.shape == None:
                if phyCon.shape.type == "PhysicControllerShapeCapsule":
                    self.AppendItem(phyItem, "Capsule - Shape",8, data = wx.TreeItemData(obj=phyCon.shape))
                    phyCon.shape.entity = phyCon.entity

        for source in Entity.Audio.source:    
            item = self.FindTreeItem(source.node, entityItem)
            if item == None: item = entityItem
            self.AppendItem(item, source.name + " - Audio Object",9, data = wx.TreeItemData(obj=source))
            source.entity = self.GetItemData(entityItem).GetData()
        
        self.SortChildren(entityItem)
        self.ExpandAllInTreeItem(self, entityItem)

    def FindTreeItem(self, node, startitem):
        tree = self
        (child, cookie) = tree.GetFirstChild(startitem)
        if child.IsOk():
            obj = tree.GetItemData(child).GetData()
            if obj.name == node: return child
            if tree.ItemHasChildren(child):
                returnChild = self.FindTreeItem(node, child)
                if not returnChild == None: 
                    return returnChild
            while child.IsOk():
                (child, cookie) = tree.GetNextChild(tree.GetRootItem(), cookie)
                if child.IsOk():
                    obj = tree.GetItemData(child).GetData()
                    if obj.name == node: 
                        return child
                    if tree.ItemHasChildren(child):
                        returnChild = self.FindTreeItem(node, child)
                        if not returnChild == None: 
                            return returnChild
        return None
    
    def EnityTreeRightMenu(self, event):
        self.PopupMenu(self.entityPopupMenu)
         
    def AddEntity(self, event):
        i = 1
        (child, cookie) = self.GetFirstChild(self.GetRootItem())
        if child.IsOk():
            i += 1
            while child.IsOk():
                (child, cookie) = self.GetNextChild(self.GetRootItem(), cookie)
                if child.IsOk():
                    i += 1 
        
        self.ent = Entity()
        self.ent.name = "Entity" + str(i)
        self.AppendItem(self.GetRootItem(), self.ent.name + " - Entity", 0, data = wx.TreeItemData(obj=self.ent))

    def AddRootTransformObject(self, event):
        object = TransformObject()
        self.GetItemData(self.GetSelections()[0]).GetData().Transform.append(object)
        object.name = "RootNode" #"Transform" + str(len(self.GetItemData(self.GetSelections()[0]).GetData().entity.Transform))
        self.AppendItem(self.GetSelections()[0], object.name + " - Transform Object", 1,data = wx.TreeItemData(obj=object))
        object.node = "RootNode"
        object.entity = self.GetItemData(self.GetSelections()[0]).GetData()
        object.type = "RootNode"
        self.OnAddingObject()

    def AddTransformObject(self, event):
        object = TransformObject()
        self.GetItemData(self.GetSelections()[0]).GetData().entity.Transform.append(object)
        object.name = "Transform" + str(len(self.GetItemData(self.GetSelections()[0]).GetData().entity.Transform)-1)

        self.AppendItem(self.GetSelections()[0], object.name + " - Transform Object", 1,data = wx.TreeItemData(obj=object))
        object.node = self.GetItemData(self.GetSelections()[0]).GetData().name
        object.entity = self.GetItemData(self.GetSelections()[0]).GetData().entity

        self.OnAddingObject()

    def AddGraphicObject(self, event):
        object = GraphicObject()
        self.GetItemData(self.GetSelections()[0]).GetData().entity.Graphic.append(object)
        object.name = "Graphic" + str(len(self.GetItemData(self.GetSelections()[0]).GetData().entity.Graphic))

        self.AppendItem(self.GetSelections()[0], object.name + " - Graphic Object",2, data = wx.TreeItemData(obj=object))
        object.node = self.GetItemData(self.GetSelections()[0]).GetData().name
        object.entity = self.GetItemData(self.GetSelections()[0]).GetData().entity
        self.OnAddingObject()
    
    def AddAnimatedGraphicObject(self, event):
        object = AnimatedGraphicObject()
        self.GetItemData(self.GetSelections()[0]).GetData().entity.AnimatedGraphic.append(object)
        object.name = "Animated Graphic" + str(len(self.GetItemData(self.GetSelections()[0]).GetData().entity.AnimatedGraphic))

        self.AppendItem(self.GetSelections()[0], object.name + " - Animated Graphic Object",2, data = wx.TreeItemData(obj=object))
        object.node = self.GetItemData(self.GetSelections()[0]).GetData().name
        object.entity = self.GetItemData(self.GetSelections()[0]).GetData().entity
        self.OnAddingObject()
    
    
    def AddPhysicObject(self, event):
        object = PhysicObject()
        self.GetItemData(self.GetSelections()[0]).GetData().entity.Physic.append(object)
        #object.name = "Physic" + str(len(self.GetItemData(self.GetSelections()[0]).GetData().entity.Physic))

        actorItem = self.AppendItem(self.GetSelections()[0], object.name + " - Physic Object", 3,data = wx.TreeItemData(obj=object))
        object.node = self.GetItemData(self.GetSelections()[0]).GetData().name
        object.entity = self.GetItemData(self.GetSelections()[0]).GetData().entity
        object.body.entity = object.entity
        self.AppendItem(actorItem, "Body - Physic Object", 3,data = wx.TreeItemData(obj=object.body))

        self.OnAddingObject()
        
    def AddPhysicShapeBox(self, event):
        object = PhysicShape()
        object.shape = boxshape()
        self.GetItemData(self.GetSelections()[0]).GetData().shapes.append(object)
        name = "Box" + str(len(self.GetItemData(self.GetSelections()[0]).GetData().shapes))

        actorItem = self.AppendItem(self.GetSelections()[0], name + " - Physic Shape Object", 3,data = wx.TreeItemData(obj=object))
        object.node = "none"
        object.entity = self.GetItemData(self.GetSelections()[0]).GetData().entity

        self.OnAddingObject()
        
    def AddPhysicShapeCapsule(self, event):
        object = PhysicShape()
        object.shape = capsuleshape()
        self.GetItemData(self.GetSelections()[0]).GetData().shapes.append(object)
        name = "Capsule" + str(len(self.GetItemData(self.GetSelections()[0]).GetData().shapes))

        actorItem = self.AppendItem(self.GetSelections()[0], name + " - Physic Shape Object", 3,data = wx.TreeItemData(obj=object))
        object.node = "none"
        object.entity = self.GetItemData(self.GetSelections()[0]).GetData().entity

        self.OnAddingObject()

    def AddPhysicShapeSphere(self, event):
        object = PhysicShape()
        object.shape = sphereshape()
        self.GetItemData(self.GetSelections()[0]).GetData().shapes.append(object)
        name = "Sphere" + str(len(self.GetItemData(self.GetSelections()[0]).GetData().shapes))

        actorItem = self.AppendItem(self.GetSelections()[0], name + " - Physic Shape Object", 3,data = wx.TreeItemData(obj=object))
        object.node = "none"
        object.entity = self.GetItemData(self.GetSelections()[0]).GetData().entity
 
        self.OnAddingObject()
    def AddPhysicShapeConvexMesh(self, event):
        object = PhysicShape()
        object.shape = convexshape()
        self.GetItemData(self.GetSelections()[0]).GetData().shapes.append(object)
        name = "Convex" + str(len(self.GetItemData(self.GetSelections()[0]).GetData().shapes))

        actorItem = self.AppendItem(self.GetSelections()[0], name + " - Physic Shape Object", 3,data = wx.TreeItemData(obj=object))
        object.node = "none" 
        object.entity = self.GetItemData(self.GetSelections()[0]).GetData().entity

        self.OnAddingObject()
    def AddPhysicShapeTriangleMesh(self, event):
        object = PhysicShape()
        object.shape = triangleshape()
        self.GetItemData(self.GetSelections()[0]).GetData().shapes.append(object)
        name = "Triangle" + str(len(self.GetItemData(self.GetSelections()[0]).GetData().shapes))

        actorItem = self.AppendItem(self.GetSelections()[0], name + " - Physic Shape Object", 3,data = wx.TreeItemData(obj=object))
        object.node = "none" 
        object.entity = self.GetItemData(self.GetSelections()[0]).GetData().entity

        self.OnAddingObject()
        
    def AddFreeCameraObject(self, event):
        object = FreeCameraObject()
        self.GetItemData(self.GetSelections()[0]).GetData().FreeCamera.append(object)
        object.name = "Free Camera" + str(len(self.GetItemData(self.GetSelections()[0]).GetData().FreeCamera))
        self.AppendItem(self.GetSelections()[0], object.name + " - Free Camera Object",4, data = wx.TreeItemData(obj=object))
        object.node = self.GetItemData(self.GetSelections()[0]).GetData().name
        object.entity = self.GetItemData(self.GetSelections()[0]).GetData()
        self.OnAddingObject()

    def AddFollowCameraObject(self, event):
        object = FollowCameraObject()
        self.GetItemData(self.GetSelections()[0]).GetData().entity.FollowCamera.append(object)
        object.name = "Follow Camera" #+ str(len(self.GetItemData(self.GetSelections()[0]).GetData().FreeCamera))
        self.AppendItem(self.GetSelections()[0], object.name + " - Follow Camera Object",4, data = wx.TreeItemData(obj=object))
        object.node = self.GetItemData(self.GetSelections()[0]).GetData().name
        object.entity = self.GetItemData(self.GetSelections()[0]).GetData().entity
        self.OnAddingObject()
        
    def AddControlObject(self, event):
        object = ControlObject()
        self.GetItemData(self.GetSelections()[0]).GetData().Control.append(object)
        object.name = "Control" + str(len(self.GetItemData(self.GetSelections()[0]).GetData().Control))
        self.AppendItem(self.GetSelections()[0], object.name + " - Control Object",5, data = wx.TreeItemData(obj=object))
        object.node = self.GetItemData(self.GetSelections()[0]).GetData().name
        object.entity = self.GetItemData(self.GetSelections()[0]).GetData()
        self.OnAddingObject()
        
    def AddAiObject(self, event):
        object = AiObject()
        self.GetItemData(self.GetSelections()[0]).GetData().Ai.append(object)
        object.name = "Ai" + str(len(self.GetItemData(self.GetSelections()[0]).GetData().Ai))
        self.AppendItem(self.GetSelections()[0], object.name + " - Ai Object",6, data = wx.TreeItemData(obj=object))
        object.node = self.GetItemData(self.GetSelections()[0]).GetData().name
        object.entity = self.GetItemData(self.GetSelections()[0]).GetData()
        self.OnAddingObject()
    
    def AddLightPoint(self, event):
        object = LightObject()
        self.GetItemData(self.GetSelections()[0]).GetData().entity.Light.append(object)
        object.name = "Light" + str(len(self.GetItemData(self.GetSelections()[0]).GetData().entity.Light))
        self.AppendItem(self.GetSelections()[0], object.name + " - point Light Object", 7, data = wx.TreeItemData(obj=object))
        object.node = self.GetItemData(self.GetSelections()[0]).GetData().name
        object.entity = self.GetItemData(self.GetSelections()[0]).GetData().entity
        object.lighttype = "point"
        self.OnAddingObject()
                
    def AddLightSpotlight(self, event):
        object = LightObject()
        self.GetItemData(self.GetSelections()[0]).GetData().entity.Light.append(object)
        object.name = "Light" + str(len(self.GetItemData(self.GetSelections()[0]).GetData().entity.Light))
        self.AppendItem(self.GetSelections()[0], object.name + " - spotlight Light Object", 7, data = wx.TreeItemData(obj=object))
        object.node = self.GetItemData(self.GetSelections()[0]).GetData().name
        object.entity = self.GetItemData(self.GetSelections()[0]).GetData().entity
        object.lighttype = "spotlight"
        self.OnAddingObject()
    
    def AddLightDirectional(self, event):
        object = LightObject()
        self.GetItemData(self.GetSelections()[0]).GetData().entity.Light.append(object)
        object.name = "Light" + str(len(self.GetItemData(self.GetSelections()[0]).GetData().entity.Light))
        self.AppendItem(self.GetSelections()[0], object.name + " - directional Light Object", 7, data = wx.TreeItemData(obj=object))
        object.node = self.GetItemData(self.GetSelections()[0]).GetData().name
        object.entity = self.GetItemData(self.GetSelections()[0]).GetData().entity
        object.lighttype = "directional"
        self.OnAddingObject()
    
    def AddPhysicControllerObject(self, event):
        object = PhysicControllerObject()
        self.GetItemData(self.GetSelections()[0]).GetData().entity.PhysicController.append(object)
        object.name = "PhysicController"
        self.AppendItem(self.GetSelections()[0], object.name + " - PhysicController Object",8, data = wx.TreeItemData(obj=object))
        object.node = self.GetItemData(self.GetSelections()[0]).GetData().name
        object.entity = self.GetItemData(self.GetSelections()[0]).GetData()
        self.OnAddingObject()
    
    def AddPhysicControllerShapeCapsule(self, event):
        object = PhysicControllerShapeCapsule()
        self.GetItemData(self.GetSelections()[0]).GetData().shape = object
        object.name = "Capsule"
        self.AppendItem(self.GetSelections()[0], object.name + " - Shape",8, data = wx.TreeItemData(obj=object))
        object.node = self.GetItemData(self.GetSelections()[0]).GetData().name
        object.entity = self.GetItemData(self.GetSelections()[0]).GetData().entity
        self.OnAddingObject()


    def AddAudioSource(self, event):
        aObj = self.GetItemData(self.GetSelections()[0]).GetData().entity.Audio
        object = AudioSource()
        aObj.source.append(object)
        object.name = "AudioSource" + str(len(aObj.source))

        self.AppendItem(self.GetSelections()[0], object.name + " - Audio Object",9, data = wx.TreeItemData(obj=object))
        object.node = self.GetItemData(self.GetSelections()[0]).GetData().name
        object.entity = self.GetItemData(self.GetSelections()[0]).GetData().entity
        self.OnAddingObject()
        
    def OnAddingObject(self):
        self.ExpandAllInTreeItem(self, self.GetSelections()[0])
        self.SelectItem(self.GetSelections()[0])
        self.SortChildren(self.GetSelections()[0])
        
    def OnDeleteObject(self, event):
        self.window.clearSceneFromEntities()
        if self.GetItemData(self.GetSelections()[0]).GetData().type == "Entity":
            self.entityAttributePanel.clear()
        self.DeleteObjects(self.GetSelections()[0])
        self.ShowObjectInformation(None)
    
    def DeleteObjects(self, startitem):
        object = startitem
        child = startitem
        self.DeleteChild(child)
        (child, cookie) = self.GetFirstChild(startitem)
        if child.IsOk():
            self.DeleteChild(child)
            if self.ItemHasChildren(child):
                self.DeleteObjects(child)
            while child.IsOk():
                (child, cookie) = self.GetNextChild(startitem, cookie)
                if child.IsOk():
                    self.DeleteChild(child)
                    if self.ItemHasChildren(child):
                        self.DeleteObjects(child)
        self.Delete(object)
        return None
    
    def DeleteChild(self, child):
        for Obj in range(len(self.GetItemData(child).GetData().entity.ObjectList)):
            for i in range(len(self.GetItemData(child).GetData().entity.ObjectList[Obj])):
                if self.GetItemData(child).GetData().entity.ObjectList[Obj][i]:
                    if self.GetItemData(child).GetData().entity.ObjectList[Obj][i] == self.GetItemData(child).GetData():
                        del self.GetItemData(child).GetData().entity.ObjectList[Obj][i]
                        break
    
    # Shows the object Attributes in the attribute panel and rebuild 
    # the mouse right click menu to present avaiable chooices
    def ShowObjectInformation(self, event):
        
        self.entityAttributePanel.DestroyChildren()

        if len(self.GetSelections()) == 1:
            self.allToFalse()
            self.getMenuItem(self.popupMenuItems, "Import")["enabled"] = True
            self.getMenuItem(self.popupMenuItems, "Export")["enabled"] = True
            self.getMenuItem(self.popupMenuItems, "Delete Object")["enabled"] = True
            
            if self.GetItemData(self.GetSelections()[0]).GetData().type == "Transform" or self.GetItemData(self.GetSelections()[0]).GetData().type == "RootNode":
                self.ShowAttributes()
                self.getMenuItem(self.popupMenuItems, "Submenu 1")["enabled"] = True
                item = self.getMenuItem(self.popupMenuItems, "Submenu 1")["items"]
                self.getMenuItem(item, "Node")["enabled"] = True
                self.getMenuItem(item, "Graphic Object")["enabled"] = True
                self.getMenuItem(item, "Submenu 5")["enabled"] = True

                if len(self.GetItemData(self.GetSelections()[0]).GetData().entity.AnimatedGraphic) < 1:
                    self.getMenuItem(item, "Animated Graphic Object")["enabled"] = True
                
                if len(self.GetItemData(self.GetSelections()[0]).GetData().entity.FollowCamera) < 1:
                    self.getMenuItem(item, "Follow Camera")["enabled"] = True

                self.getMenuItem(item, "Physic Object")["enabled"] = True
                self.getMenuItem(item, "Submenu 3")["enabled"] = True

                if not len(self.GetItemData(self.GetSelections()[0]).GetData().entity.Physic) == 0:
                    self.getMenuItem(item, "Physic Object")["enabled"] = False
                    self.getMenuItem(item, "Submenu 2")["enabled"] = False
            
            elif self.GetItemData(self.GetSelections()[0]).GetData().type == "Graphic":
                self.ShowAttributes()

            elif self.GetItemData(self.GetSelections()[0]).GetData().type == "AnimatedGraphic":
                self.ShowAttributes()

            elif self.GetItemData(self.GetSelections()[0]).GetData().type == "PhysicActor":
                self.ShowAttributes()
                self.getMenuItem(self.popupMenuItems, "Submenu 1")["enabled"] = True
                item = self.getMenuItem(self.popupMenuItems, "Submenu 1")["items"]

                self.getMenuItem(item, "Submenu 2")["enabled"] = True
            
            elif self.GetItemData(self.GetSelections()[0]).GetData().type == "PhysicBody":
                self.ShowAttributes()
            
            elif self.GetItemData(self.GetSelections()[0]).GetData().type == "PhysicShape":
                self.ShowAttributes()

            elif self.GetItemData(self.GetSelections()[0]).GetData().type == "FreeCamera":
                self.ShowAttributes()
            
            elif self.GetItemData(self.GetSelections()[0]).GetData().type == "FollowCamera":
                self.ShowAttributes()
            
            elif self.GetItemData(self.GetSelections()[0]).GetData().type == "Control":
                self.ShowAttributes()
                
            elif self.GetItemData(self.GetSelections()[0]).GetData().type == "Ai":
                self.ShowAttributes()
            
            elif self.GetItemData(self.GetSelections()[0]).GetData().type == "Light":
                self.ShowAttributes()
            
            elif self.GetItemData(self.GetSelections()[0]).GetData().type == "AudioSource":
                self.ShowAttributes()
            
            elif self.GetItemData(self.GetSelections()[0]).GetData().type == "PhysicController":
                if self.GetItemData(self.GetSelections()[0]).GetData().shape == None:
                    self.getMenuItem(self.popupMenuItems, "Submenu 1")["enabled"] = True
                    item = self.getMenuItem(self.popupMenuItems, "Submenu 1")["items"]
                    self.getMenuItem(item, "Submenu 4")["enabled"] = True
                self.ShowAttributes()
            
            elif self.GetItemData(self.GetSelections()[0]).GetData().type == "PhysicControllerShapeCapsule":
                self.ShowAttributes()

            elif self.GetItemData(self.GetSelections()[0]).GetData().type == "Entity":
                self.getMenuItem(self.popupMenuItems, "Submenu 1")["enabled"] = True
                item = self.getMenuItem(self.popupMenuItems, "Submenu 1")["items"]
                
                if len(self.GetItemData(self.GetSelections()[0]).GetData().Transform) < 1:
                    self.getMenuItem(item,"Root Node")["enabled"] = True

                #self.getMenuItem(item,"Node")["enabled"] = False
                
                #self.getMenuItem(item, "Graphic Object")["enabled"] = True

                #if len(self.GetItemData(self.GetSelections()[0]).GetData().entity.AnimatedGraphic) < 1:
                #    self.getMenuItem(item, "Animated Graphic Object")["enabled"] = True

                if len(self.GetItemData(self.GetSelections()[0]).GetData().FreeCamera) < 1:
                    self.getMenuItem(item,"Free Camera")["enabled"] = True
                
                if len(self.GetItemData(self.GetSelections()[0]).GetData().Control) < 1:
                    self.getMenuItem(item,"Control")["enabled"] = True
                
                if len(self.GetItemData(self.GetSelections()[0]).GetData().Ai) < 1:
                    self.getMenuItem(item,"Ai")["enabled"] = True
                
                if len(self.GetItemData(self.GetSelections()[0]).GetData().PhysicController) < 1:
                    self.getMenuItem(item,"PhysicController")["enabled"] = True
                
                self.ShowAttributes()
                        
        else:
            self.getMenuItem(self.popupMenuItems, "Submenu 1")["enabled"] = False
            self.getMenuItem(self.popupMenuItems, "Export")["enabled"] = False
            self.getMenuItem(self.popupMenuItems, "Delete Object")["enabled"] = False
        
        #print self.GetCount()
        #if not self.ItemHasChildren(self.GetRootItem()):
        #    print "ass"
        #    self.getMenuItem(self.popupMenuItems, "Submenu 1")["enabled"] = False
        #    self.getMenuItem(self.popupMenuItems, "Export")["enabled"] = False
        #    self.getMenuItem(self.popupMenuItems, "Delete Object")["enabled"] = False
        
        if (len(self.GetSelections()) > 0):
            self.getMenuItem(self.popupMenuItems, "Export")["enabled"] = True

        self.entityPopupMenu = PopupMenu()
    
        self.entityPopupMenu.AddMenuItems(self.popupMenuItems)
            
    def getMenuItem(self, list, findItem):
        for item in list:
            if item["type"] == findItem:
                return item
    
    def updatePreview(self, event = None):
        #self.window.clearSceneFromEntities()

        if not self.window == None:
            self.window.clearSceneFromEntities()
            #print len(self.GetSelections())
            for treeEntity in self.GetSelections():
                if self.GetItemParent(treeEntity) == self.GetRootItem():
                    self.window.showEntity(self.GetItemData(treeEntity).GetData())
                else: self.window.showEntity(self.GetItemData(treeEntity).GetData().entity)
                    
    def getEntityParent(self, item):
        parent = self.GetItemParent(item)
        if parent == self.GetRootItem():
            return item
        else: self.getEntityParent(parent)
    
    # Sets all standard object tools in mouse popup menu to false
    def allToFalse(self):
        self.getMenuItem(self.popupMenuItems, "Submenu 1")["enabled"] = False
        item = self.getMenuItem(self.popupMenuItems, "Submenu 1")["items"]
        self.getMenuItem(item,"Root Node")["enabled"] = False
        self.getMenuItem(item, "Node")["enabled"] = False
        self.getMenuItem(item, "Graphic Object")["enabled"] = False
        self.getMenuItem(item, "Animated Graphic Object")["enabled"] = False
        self.getMenuItem(item, "Physic Object")["enabled"] = False
        self.getMenuItem(item,"Free Camera")["enabled"] = False
        self.getMenuItem(item,"Follow Camera")["enabled"] = False
        self.getMenuItem(item,"Control")["enabled"] = False
        self.getMenuItem(item,"Ai")["enabled"] = False
        self.getMenuItem(item,"PhysicController")["enabled"] = False
        self.getMenuItem(item,"Submenu 5")["enabled"] = False
        self.getMenuItem(item,"Submenu 4")["enabled"] = False
        self.getMenuItem(item, "Submenu 2")["enabled"] = False
        self.getMenuItem(item, "Submenu 3")["enabled"] = False
    
    def ShowAttributes(self, ObjType = None):
        if ObjType == None:
            ObjType = self.GetItemData(self.GetSelections()[0]).GetData().type
        self.entityAttributePanel.showAttributes(type = ObjType, object = self.GetItemData(self.GetSelections()[0]).GetData(), options = self, item = self.GetSelections()[0])
        
    # Looping throw a tree structure from inupted item and Expand its child structure
    def ExpandAllInTreeItem(self, tree, startitem):
        if startitem == tree.GetRootItem():
            tree.SelectItem(self.GetRootItem())
        tree = self
        tree.Expand(startitem)
        (child, cookie) = tree.GetFirstChild(startitem)
        if child.IsOk():
            tree.Expand(child)
            if tree.ItemHasChildren(child):
                self.ExpandAllInTreeItem(tree,child)
            while child.IsOk():
                (child, cookie) = tree.GetNextChild(tree.GetRootItem(), cookie)
                if child.IsOk():
                    tree.Expand(child)                    
                    if tree.ItemHasChildren(child):
                        self.ExpandAllInTreeItem(tree, child)
        return None
    
    def CollapseAllTreeItems(self):
        #tree.SelectItem(self.GetRootItem())
        #tree.Expand(startitem)
        (child, cookie) = self.GetFirstChild(self.GetRootItem())
        while child.IsOk():
            self.Collapse(child)
            (child, cookie) = self.GetNextChild(self.GetRootItem(), cookie)                   
    
    def bind(self, window):
        self.window = window
        pass
    
    def OnImport(self, event):
        #entities =
        fild = wx.FileDialog(self, message="Import file", wildcard="*.xml", style=wx.OPEN | wx.MULTIPLE)
        if fild.ShowModal() == wx.ID_OK:
            entities = ogreyImportEntity(self, fild.GetPaths()).Entities
            #print entity
            for entity in entities:
                self.ImportEntity(entity)
                
    def OnExport(self, event):
        for selected in self.GetSelections():
            Entity = self.GetItemData(selected).GetData()
            ogreyExportEntity(self, Entity)
