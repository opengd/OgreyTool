import wx
#import wxogre
#from pyogre import ogre
import wx.xrc as xrc
import elementtree.ElementTree as ET


class Entity:
    def __init__(self, name = "", Transform = [], Graphic = []):
        self.name = name
        self.Transform = Transform
        self.Graphic = Graphic

class EntityObject:
    def __init__(self):
        self.name = ""

class TransformObject:
    def __init__(self, name = "", position = (0.0, 0.0, 0.0), rotation = (0.0, 0.0, 0.0), scale = (1.0, 1.0, 1.0), node = ""):
        self.name = name
        self.position = position
        self.rotation = rotation
        self.scale = scale
        self.node = node

class GraphicObject:
    def __init__(self):
        self.name = ""
        self.model = ""
        self.material = ""
        self.node = ""

class EntityAttributes:
    def __init__(self, panel, object):
        self.panel = panel
        self.object = object
        
        wx.StaticBox(self.panel, -1, "Entity Attributes", size = (325, 350) )
        wx.StaticText(self.panel, -1, "Entity Name:", pos = (10,20))
        self.entityName = wx.TextCtrl(self.panel, -1,self.object.name,  style=wx.TE_LEFT, pos=(20,40))
        self.entityName.Bind(wx.EVT_TEXT, self.OnEntityName)
    
    def OnEntityName(self, event):
        self.object.name = self.entityName.GetValue()

class TransformAttributes:
    def __init__(self, panel, object, tree):
        self.panel = panel
        self.object = object
        self.tree = tree

        wx.StaticBox(self.panel, -1, "Transform Attributes", size= (325,350))
        wx.StaticText(self.panel, -1, "Node Name:", pos = (10,20))
        self.nodeName = wx.TextCtrl(self.panel, -1, self.object.name,  style=wx.TE_LEFT, pos=(20,40))
        self.nodeName.Bind(wx.EVT_TEXT, self.OnNodeName)
        
        wx.StaticText(self.panel, -1, "Parent Node: " + self.object.node , pos = (10,330))
    
        wx.StaticText(self.panel, -1, "Position:", pos = (10,70))
        wx.StaticText(self.panel, -1, "X:", pos = (20,90))
        self.nodePosX = wx.TextCtrl(self.panel, -1, str(self.object.position[0]),  style=wx.TE_LEFT, pos=(40,90), size = (50, -1))
        self.nodePosX.Bind(wx.EVT_TEXT, self.OnNodePosition)
        
        wx.StaticText(self.panel, -1, "Y:", pos = (100,90))
        self.nodePosY = wx.TextCtrl(self.panel, -1, str(self.object.position[1]),  style=wx.TE_LEFT, pos=(120,90),  size = (50, -1))
        self.nodePosY.Bind(wx.EVT_TEXT, self.OnNodePosition)
        
        wx.StaticText(self.panel, -1, "Z:", pos = (180,90))
        self.nodePosZ = wx.TextCtrl(self.panel, -1, str(self.object.position[2]),  style=wx.TE_LEFT, pos=(200,90),  size = (50, -1))
        self.nodePosZ.Bind(wx.EVT_TEXT, self.OnNodePosition)
        
        wx.StaticText(self.panel, -1, "Rotation:", pos = (10,120))
        wx.StaticText(self.panel, -1, "X:", pos = (20,140))
        self.nodeRotX = wx.TextCtrl(self.panel, -1, str(self.object.rotation[0]),  style=wx.TE_LEFT, pos=(40,140), size = (50, -1))
        self.nodeRotX.Bind(wx.EVT_TEXT, self.OnNodeRotation)
        
        wx.StaticText(self.panel, -1, "Y:", pos = (100,140))
        self.nodeRotY = wx.TextCtrl(self.panel, -1, str(self.object.rotation[1]),  style=wx.TE_LEFT, pos=(120,140),  size = (50, -1))
        self.nodeRotY.Bind(wx.EVT_TEXT, self.OnNodeRotation)
        
        wx.StaticText(self.panel, -1, "Z:", pos = (180,140))
        self.nodeRotZ = wx.TextCtrl(self.panel, -1, str(self.object.rotation[2]),  style=wx.TE_LEFT, pos=(200,140),  size = (50, -1))
        self.nodeRotZ.Bind(wx.EVT_TEXT, self.OnNodeRotation)
        
        wx.StaticText(self.panel, -1, "Scale:", pos = (10,170))
        wx.StaticText(self.panel, -1, "X:", pos = (20,190))
        self.nodeScaleX = wx.TextCtrl(self.panel, -1, str(self.object.scale[0]),  style=wx.TE_LEFT, pos=(40,190), size = (50, -1))
        self.nodeScaleX.Bind(wx.EVT_TEXT, self.OnNodeScale)
        
        wx.StaticText(self.panel, -1, "Y:", pos = (100,190))
        self.nodeScaleY = wx.TextCtrl(self.panel, -1, str(self.object.scale[1]),  style=wx.TE_LEFT, pos=(120,190),  size = (50, -1))
        self.nodeScaleY.Bind(wx.EVT_TEXT, self.OnNodeScale)
        
        wx.StaticText(self.panel, -1, "Z:", pos = (180,190))
        self.nodeScaleZ = wx.TextCtrl(self.panel, -1, str(self.object.scale[2]),  style=wx.TE_LEFT, pos=(200,190),  size = (50, -1))
        self.nodeScaleZ.Bind(wx.EVT_TEXT, self.OnNodeScale)
    
    def OnNodeName(self, event):
        self.object.name = self.nodeName.GetValue()
        (child, cookie) = self.tree.GetFirstChild(self.tree.GetSelection())
        if child.IsOk():
            obj = self.tree.GetItemData(child).GetData()
            obj.node = self.object.name
            while child.IsOk():
                (child, cookie) = self.tree.GetNextChild(self.tree.GetSelection(), cookie)
                if child.IsOk():
                    obj = self.tree.GetItemData(child).GetData()
                    obj.node = self.object.name
    
    def OnNodePosition(self, event):
        self.object.position = (float(self.nodePosX.GetValue()), float(self.nodePosY.GetValue()), float(self.nodePosZ.GetValue()))
        
    def OnNodeRotation(self, event):
        self.object.rotation = (float(self.nodeRotX.GetValue()), float(self.nodeRotY.GetValue()), float(self.nodeRotZ.GetValue()))
    
    def OnNodeScale(self, event):
        self.object.scale = (float(self.nodeScaleX.GetValue()), float(self.nodeScaleY.GetValue()), float(self.nodeScaleZ.GetValue()))
        
class GraphicAttributes:
    def __init__(self, panel, object):
        self.panel = panel
        self.object = object

        wx.StaticBox(self.panel, -1, "Graphic Attributes", size= (325,350))
        
        wx.StaticText(self.panel, -1, "Parent Node: " + self.object.node , pos = (10,330))
        
        wx.StaticText(self.panel, -1, "Name:", pos = (10,20))
        self.objectName = wx.TextCtrl(self.panel, -1, self.object.name,  style=wx.TE_LEFT, pos=(20,40))
        self.objectName.Bind(wx.EVT_TEXT, self.OnObjectName)

        wx.StaticText(self.panel, -1, "Mesh/Model Path:", pos = (10,70))
        self.modelPath = wx.TextCtrl(self.panel, -1, self.object.model,  style=wx.TE_LEFT, pos=(20,90), size=(200, -1))
        self.modelPath.Bind(wx.EVT_TEXT, self.OnModel)
        self.modelButton = wx.BitmapButton(self.panel, -1,wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_BUTTON), pos = (230, 90))
        self.modelButton.Bind(wx.EVT_BUTTON, self.OnModelButton)
        
        wx.StaticText(self.panel, -1, "Material:", pos = (10,120))
        self.materialName = wx.TextCtrl(self.panel, -1, self.object.material,  style=wx.TE_LEFT, pos=(20,140), size=(200, -1))
        self.materialName.Bind(wx.EVT_TEXT, self.OnMaterialName)
    
    def OnObjectName(self, event):
        self.object.name = self.objectName.GetValue()
        
    def OnModel(self, event):
        self.object.model = self.modelPath.GetValue()
    
    def OnModelButton(self, event):
        fdg = wx.FileDialog(self.panel, message = "Choose Mesh File", style=wx.OPEN, wildcard = "*.mesh")
        if fdg.ShowModal() == wx.ID_OK:
            self.object.model = fdg.GetFilename()
            self.modelPath.SetValue(self.object.model)
        fdg.Destroy()
    
    def OnMaterialName(self, event):
        self.object.material = self.materialName.GetValue()


class EntityTool(wx.Frame):
    def __init__(self, parent, inputEntity = None):
        wx.Frame.__init__(self, parent, id = -1, title = "Ogrey Entity Tool v.1.1", size=(500, 500))
        
        self.parent = parent
        self.entityPanel = wx.Panel(self, -1,size = (500,500), pos = wx.DefaultPosition, style = wx.WS_EX_PROCESS_UI_UPDATES)

        self.entityTree = wx.TreeCtrl(self.entityPanel, -1, size = (150, 350), pos = (5, 10), style = wx.TR_HAS_BUTTONS)
        if inputEntity == None: 
            # Create a new Entity Block
            self.Entity = Entity()
            self.entityTreeRoot = self.entityTree.AddRoot(text="Entity", data=wx.TreeItemData(obj=self.Entity))
        else:
            self.CreateEntityFromInputed(inputEntity)
        
        self.entityAttributePanel = wx.Panel(self.entityPanel, -1, size= (340, 350), pos = (160, 10), style= wx.NO_BORDER)
        self.exportButton = wx.Button(self.entityPanel, -1, "Export Entity", pos=(10, 430))
        self.importButton = wx.Button(self.entityPanel, -1, "Import Entity", pos=(100, 430))
        self.cancelButton = wx.Button(self.entityPanel, -1, "Cancel", pos=(300, 430))
        self.createButton = wx.Button(self.entityPanel, -1, "Create", pos=(400, 430))
        
        self.exportButton.Bind(wx.EVT_BUTTON, self.OnExportEntity)
        self.importButton.Bind(wx.EVT_BUTTON, self.OnImportEntity)
        self.cancelButton.Bind(wx.EVT_BUTTON, self.OnCancel)
        self.createButton.Bind(wx.EVT_BUTTON, self.OnExportEntity)

        
        self.Show(True)
        self.entityPopupMenu = wx.Menu()
        self.popupMenuItems = {
        "Submenu 1" : {"enabled" : True, "menuItem" : "Submenu", "name" : "Add", 
        "items" : { 
            "Root Node" : {"enabled" : True, "menuItem" : wx.MenuItem(self.entityPopupMenu, -1, "Root Transform Object"), "event" : self.AddRootTransformObject} , # Transform Object
            "Node" : {"enabled" : False, "menuItem" : wx.MenuItem(self.entityPopupMenu, -1, "Transform Object"), "event" : self.AddTransformObject} , # Transform Object
            "Graphic Object" : {"enabled" : False, "menuItem" : wx.MenuItem(self.entityPopupMenu, -1, "Graphic Object"), "event" : self.AddGraphicalObject}, # Graphic Object
            "Particle Object" : {"enabled" : False, "menuItem" :wx.MenuItem(self.entityPopupMenu, -1, "Particle Object"), "event" : self.AddParticleObject}, # Particle Object
            }
        },
        #"Seperator" : {"enabled" : True, "menuItem" : "Seperator"}, 
        "Deletet Object" : {"enabled" : True, "menuItem" :wx.MenuItem(self.entityPopupMenu, -1, "Delete Object"), "event" : self.OnDeleteObject}, # Deletet Object
        }
        self.AddMenuItems(self.entityPopupMenu, self.popupMenuItems) 
        self.entityTree.Bind(wx.EVT_RIGHT_DOWN, self.EnityTreeRightMenu)
        self.entityTree.Bind(wx.EVT_TREE_SEL_CHANGED,self.ShowObjectInformation)
        self.entityTree.SelectItem(self.entityTree.GetRootItem())
    
    def OnCancel(self, event):
        self.Destroy()
    
    def CreateTreeFromInputedEntity(self, inputEntity):
        self.Entity = inputEntity
        self.entityTreeRoot = self.entityTree.AddRoot(text="Entity", data=wx.TreeItemData(obj=self.Entity))
        for transformObj in self.Entity.Transform:
            item = self.FindTreeItem(transformObj.node, self.entityTree.GetRootItem())
            if item == None: item = self.entityTree.GetRootItem()
            self.entityTree.AppendItem(item, "Transform Object", data = wx.TreeItemData(obj=transformObj))
        
        for graphicObj in self.Entity.Graphic:    
            item = self.FindTreeItem(graphObj.node, self.entityTree.GetRootItem())
            if item == None: item = self.entityTree.GetRootItem()
            self.entityTree.AppendItem(item, "Graphic Object", data = wx.TreeItemData(obj=graphicObj))
    
    def AddToTree(self, parent, name, data):
        self.entityTree.AppendItem(parent, name, data = wx.TreeItemData(obj=data))

    def EnityTreeRightMenu(self, event):
        self.PopupMenu(self.entityPopupMenu) 
    
    def AddRootTransformObject(self, event):
        object = TransformObject()
        self.Entity.Transform.append(object)
        self.entityTree.AppendItem(self.entityTree.GetSelection(), "Transform Object", data = wx.TreeItemData(obj=object))
        object.node = "RootNode"
        self.OnAddingObject()

    def AddTransformObject(self, event):
        object = TransformObject()
        self.Entity.Transform.append(object)
        self.entityTree.AppendItem(self.entityTree.GetSelection(), "Transform Object", data = wx.TreeItemData(obj=object))
        object.node = self.entityTree.GetItemData(self.entityTree.GetSelection()).GetData().name
        self.OnAddingObject()

    def AddGraphicalObject(self, event):
        object = GraphicObject()
        self.Entity.Graphic.append(object)
        self.entityTree.AppendItem(self.entityTree.GetSelection(), "Graphic Object", data = wx.TreeItemData(obj=object))
        object.node = self.entityTree.GetItemData(self.entityTree.GetSelection()).GetData().name
        self.OnAddingObject()
    def OnAddingObject(self):
        self.ExpandAllInTreeItem(self.entityTree, self.entityTree.GetSelection())

    def AddParticleObject(self, event):
        pass

    def OnMenuClick(self, event):
        pass
        
    def OnDeleteObject(self, event):
        if not self.entityTree.GetSelection() == self.entityTree.GetRootItem():
            parent = self.entityTree.GetItemParent(self.entityTree.GetSelection())
            object = self.entityTree.GetItemData(self.entityTree.GetSelection())
            find = False
            for i in range(len(self.Entity.Transform)):
                if self.Entity.Transform[i]:
                    del self.Entity.Transform[i]
                    find = True
                    break
                else: find = False
            if find == False: 
                for i in range(len(self.Entity.Graphic[i])):
                    if self.Entity.Graphic[i]:
                        del self.Entity.Graphic[i]
                        find = True
                        break
                    else: find = False
            self.entityTree.Delete(self.entityTree.GetSelection())
            self.entityTree.SelectItem(parent)
            #sprint len(self.Entity["Transform"])
    
    def AddMenuItems(self, menu, items, parentMenu = None):
        if parentMenu == None:
            parentMenu = menu
        for menuItem in items.itervalues():
            if menuItem["enabled"] == True:
                if menuItem["menuItem"] == "Submenu":
                    subMenu = self.AddMenuItems(wx.Menu(), menuItem["items"], menu)
                    menu.AppendMenu(id = -1, text=menuItem["name"], submenu = subMenu)
                elif not menuItem["menuItem"] == "Seperator":
                    menu.AppendItem(menuItem["menuItem"])
                    if not menuItem["event"] == False:
                        parentMenu.Bind(wx.EVT_MENU, menuItem["event"], id =menuItem["menuItem"].GetId())
                elif menuItem["menuItem"] == "Seperator": 
                    self.enityPopupMenu.AppendSeparator()
        return menu
    
    def FlushMenu(self, menu):
        #menu.Destroy()
        #return wx.Menu()
        items = menu.GetMenuItems()
        for i in items:
            menu.Remove(i.GetId())
    
    def ShowObjectInformation(self, event):
        self.entityAttributePanel.DestroyChildren()
        if self.entityTree.GetItemText(self.entityTree.GetSelection()) == "Entity":
            self.EntityAttributes()
            if len(self.Entity.Transform) < 1:
                self.getMenuItem(self.popupMenuItems, "Submenu 1")["enabled"] = True
                item = self.getMenuItem(self.popupMenuItems, "Submenu 1")["items"]
                self.getMenuItem(item,"Root Node")["enabled"] = True
                self.getMenuItem(item, "Node")["enabled"] = False
                self.getMenuItem(item, "Graphic Object")["enabled"] = False
                
                self.getMenuItem(self.popupMenuItems, "Deletet Object")["enabled"] = False
            else:
                self.getMenuItem(self.popupMenuItems, "Submenu 1")["enabled"] = False
                self.getMenuItem(self.popupMenuItems, "Deletet Object")["enabled"] = False

                
        elif self.entityTree.GetItemText(self.entityTree.GetSelection()) == "Transform Object":
            self.TransformAttributes()
            self.getMenuItem(self.popupMenuItems, "Submenu 1")["enabled"] = True
            item = self.getMenuItem(self.popupMenuItems, "Submenu 1")["items"]

            self.getMenuItem(item,"Root Node")["enabled"] = False
            self.getMenuItem(item, "Node")["enabled"] = True
            self.getMenuItem(item, "Graphic Object")["enabled"] = True
                
            self.getMenuItem(self.popupMenuItems, "Deletet Object")["enabled"] = True
                        
        elif self.entityTree.GetItemText(self.entityTree.GetSelection()) == "Graphic Object":
            self.GraphicAttributes()
            self.getMenuItem(self.popupMenuItems, "Submenu 1")["enabled"] = False
            self.getMenuItem(self.popupMenuItems, "Deletet Object")["enabled"] = True

        self.FlushMenu(self.entityPopupMenu)
        self.AddMenuItems(self.entityPopupMenu, self.popupMenuItems)
    
    def getMenuItem(list, findItem):
        for item in list:
            if item["name"] == findItem:
                return item

    def EntityAttributes(self):
        EntityAttributes(self.entityAttributePanel, self.entityTree.GetItemData(self.entityTree.GetSelection()).GetData())
        pass

    def TransformAttributes(self):
        TransformAttributes(self.entityAttributePanel, self.entityTree.GetItemData(self.entityTree.GetSelection()).GetData(), self.entityTree)
        pass
    
    def GraphicAttributes(self):
        GraphicAttributes(self.entityAttributePanel, self.entityTree.GetItemData(self.entityTree.GetSelection()).GetData())
        pass
    
    def OnExportEntity(self,event):
        exportDialog = wx.FileDialog(self.entityPanel, message="Save file", wildcard="*.xml", style=wx.SAVE | wx.OVERWRITE_PROMPT)
        if exportDialog.ShowModal() == wx.ID_OK:
            root = ET.Element("entity", attrib = {"name" : self.Entity.name})
            if not len(self.Entity.Transform) == 0:
                transformobject = ET.SubElement(root, "transformobject")
                for transObject in self.Entity.Transform:
                    node = ET.SubElement(transformobject, "node", attrib={"name" : transObject.name, "parent" : transObject.node})
                    ET.SubElement(node, "position", attrib={"x" : str(transObject.position[0]), "y" : str(transObject.position[1]), "z" : str(transObject.position[2])})
                    ET.SubElement(node, "rotation", attrib={"x" : str(transObject.rotation[0]), "y" : str(transObject.rotation[1]), "z" : str(transObject.rotation[2])})
                    ET.SubElement(node, "scale", attrib={"x" : str(transObject.scale[0]), "y" : str(transObject.scale[1]), "z" : str(transObject.scale[2])})
            if not len(self.Entity.Graphic) == 0:
                graphicobject = ET.SubElement(root, "graphicobject")
                for grapObject in self.Entity.Graphic:
                    mesh = ET.SubElement(graphicobject, "mesh", attrib={"name" : grapObject.name, "model" : grapObject.model, "material" : grapObject.material, "node" : grapObject.node})
        
            ET.ElementTree(root).write(exportDialog.GetPath(), 'utf-8')
        
        exportDialog.Destroy()
        pass
    def OnImportEntity(self,event):
        importDialog = wx.FileDialog(self.entityPanel, message="Import file", wildcard="*.xml", style=wx.OPEN)
        if importDialog.ShowModal() == wx.ID_OK:
            for path in importDialog.GetPaths():
                self.CreateEntityFromXML(path)
                self.ExpandAllInTreeItem(self.entityTree, self.entityTree.GetRootItem())
    
    def CreateEntityFromXML(self, file):
        self.Entity = Entity()
        self.entityTree.DeleteAllItems()
        self.entityTreeRoot = self.entityTree.AddRoot(text="Entity", data=wx.TreeItemData(obj=self.Entity))

        importElements = ET.parse(file)
        root = importElements.getroot()
        for (key, value) in root.attrib.iteritems():
            if key == "name":
                self.Entity.name = value
        for childElement in root.getchildren():
            
            #TRANSFORM OBJECT
            if childElement.tag == "transformobject":
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
                                Obj.position = (nodechild.attrib["x"], nodechild.attrib["y"] , nodechild.attrib["z"])
                            elif nodechild.tag == "rotation":
                                Obj.rotation = (nodechild.attrib["x"],nodechild.attrib["y"], nodechild.attrib["z"])
                            elif nodechild.tag == "scale":
                                Obj.scale = (nodechild.attrib["x"], nodechild.attrib["y"] , nodechild.attrib["z"])
                    item = self.FindTreeItem(Obj.node, self.entityTree.GetRootItem())
                    if item == None: item = self.entityTree.GetRootItem()
                    self.entityTree.AppendItem(item, "Transform Object", data = wx.TreeItemData(obj=Obj))

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
                    item = self.FindTreeItem(Obj.node, self.entityTree.GetRootItem())
                    if item == None: item = self.entityTree.GetRootItem()
                    self.entityTree.AppendItem(item, "Graphic Object", data = wx.TreeItemData(obj=Obj))
    
    # Looping throw a tree structure from inuted item and Expand its child structure
    def ExpandAllInTreeItem(self, tree, startitem):
        if startitem == tree.GetRootItem():
            tree.SelectItem(self.entityTree.GetRootItem())
        tree = self.entityTree
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
    
    # Finds a iteam in a tree to a node name, loopin throw tree and return item when found
    def FindTreeItem(self, node, startitem):
        tree = self.entityTree
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
        
class MyFrame(wx.Frame):
    def __init__(self, *args, **kw):
        wx.Frame.__init__(self, *args, **kw)
        EntityTool(self)

       
class MyApp(wx.App):
    def OnInit(self):
        self.frame = EntityTool(None)
        self.frame.Show(True)
        return True

if __name__ == '__main__':
    app = MyApp(False)
    app.MainLoop() 
    
    

#self.moduleTree = wx.TreeCtrl(self.parentPanel, -1, size = (175, 250), pos = (310, 10), style = wx.TR_HIDE_ROOT|wx.TR_HAS_BUTTONS)
        #self.moduleTreeRoot = self.moduleTree.AddRoot("Modules")
        #self.moduleTree.AppendItem(self.moduleTreeRoot, "Transform Object")
        #self.moduleTree.AppendItem(self.moduleTreeRoot, "Graphic Object")
        #self.moduleTree.AppendItem(self.moduleTreeRoot, "Child")

        #self.addChildName = wx.TextCtrl(self.parentPanel, 654,"Enter",  style=wx.TE_LEFT, pos=(10,280))
        #self.addChildName.SetValue("")
        #self.addChildName.Bind(wx.EVT_TEXT_ENTER, self.addChild)
        
        #self.dt = ParentTarget(self)
        #self.parentTree.SetDropTarget(self.dt)
        
        #self.moduleTree.Bind(wx.EVT_MOTION, self.TreeBoxDrag,id = self.moduleTree.GetId())
        #self.moduleTree.Bind(wx.EVT_TREE_SEL_CHANGED,self.GetTreeItem,id = self.moduleTree.GetId())
        
##        def TreeBoxDrag(self, event):
##        if event.Dragging():
##            print "Drag item"
##            item = self.moduleTree.GetItemText(self.moduleTree.GetSelection())
##            tdo = wx.PyTextDataObject(item)
##            tds = wx.DropSource(self.moduleTree)
##            tds.SetData(tdo)
##            tds.DoDragDrop(True)

##
##class ParentTarget(wx.TextDropTarget):
##    def __init__(self, parent):
##        wx.TextDropTarget.__init__(self)
##        self.parent = parent
##        
##    def OnDropText(self, x, y, id):
##        print "fan"
##        self.parent.parentTree.AppendItem(self.parent.parentTreeRoot, self.parent.moduleTree.GetItemText(self.parent.moduleTree.GetSelection()))