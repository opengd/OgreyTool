import wx
from ogreyPopupMenu import *
from ogreyOgreManagers import *
from ogreyTool import *
 
        
class Singleton(type):
    def __init__(self, *args):
        type.__init__(self, *args)
        self._instances = {}

    def __call__(self, *args):
        if not args in self._instances:
            self._instances[args] = type.__call__(self, *args)
        return self._instances[args]

class Test:
    __metaclass__=Singleton
    def __init__(self, *args): pass

            
ta1, ta2 = Test(), Test()
assert ta1 is ta2

tb1, tb2 = Test(5), Test(5)
assert tb1 is tb2

assert ta1 is not tb1


class LogList(wx.TextCtrl):
    def __init__(self, parent):
        wx.TextCtrl.__init__(self, parent, -1, "", style=wx.TE_MULTILINE)
        

class ogreyMaterialTool(wx.MiniFrame):
    def __init__(self, parent, config, ogreMgr):
        wx.MiniFrame.__init__(self, parent, -1, "Material Tool", size = (500, 500))
        self.parent = parent
        self.config = config
        #self.ogreManager = OgreManager()
        self.ogreMgr = OgreManager().ogreMgr
        self.Show(True)
        self.define()
        
        wx.EVT_CLOSE(self, self.OnClose)
    
    def OnClose(self, event):
        self.Show(False)
                
    def define(self):
        self.defineSplitters()
        self.defineTrees()
    
    def definePopupMenu(self):
        pass
##        self.popupMenu = PopupMenu()
##        self.popupMenuItems = [
##        {"type" : "AddMaterial", "enabled" : False, "menuItem" : "Submenu", "name" : "Add", 
##        "items" : [
##            {"type" : "Technique", "enabled" : False, "menuItem" : wx.MenuItem(self.entityPopupMenu, -1, "Technique"), "event" : self.AddTechnique} , # Technique
##            {"type" : "Pass", "enabled" : False, "menuItem" : wx.MenuItem(self.entityPopupMenu, -1, "Pass"), "event" : self.AddPass} , # Pass
##            {"type" : "Texture unit", "enabled" : False, "menuItem" : wx.MenuItem(self.entityPopupMenu, -1, "Texture unit"), "event" : self.AddTextureUnit} , # Textureunit
##            {"type" : "Vertex program ref", "enabled" : False, "menuItem" : wx.MenuItem(self.entityPopupMenu, -1, "Vertex program ref"), "event" : self.AddVertexProgramRef} , # "Vertex program ref
##            {"type" : "FragmentProgramRef", "enabled" : False, "menuItem" : wx.MenuItem(self.entityPopupMenu, -1, "Fragment program ref"), "event" : self.AddFragmentProgramRef} , # Fragment program ref
##            ],
##        },
##        {"type" : "AddVertexProgram", "enabled" : False, "menuItem" : "Submenu", "name" : "Add", 
##        "items" : [
##            {"type" : "Default params", "enabled" : False, "menuItem" : wx.MenuItem(self.entityPopupMenu, -1, "Default params"), "event" : self.AddDefaultParams} , # Defaultparams
##            ],
##        },
##        {"type" : "Material", "enabled" : True, "menuItem" : wx.MenuItem(self.entityPopupMenu, -1, "New Material"), "event" : self.AddMaterial} , # Create a new Entity
##        {"type" : "Vertex program", "enabled" : True, "menuItem" :wx.MenuItem(self.entityPopupMenu, -1, "New Vertex Program"), "event" : self.AddVertexProgram}, # Deletet Object
##        {"type" : "Fragment program", "enabled" : True, "menuItem" :wx.MenuItem(self.entityPopupMenu, -1, "New Fragment Program"), "event" : self.AddFragmentProgram}, # Deletet Object
##        {"type" : "Create New Material File", "enabled" : True, "menuItem" :wx.MenuItem(self.entityPopupMenu, -1, "Create New Material File"), "event" : self.OnCreateNewMaterial}, # Deletet Object
##        {"type" : "Delete", "enabled" : False, "menuItem" :wx.MenuItem(self.entityPopupMenu, -1, "Delete Object"), "event" : self.OnDelete}, # Deletet Object
##        #{"type" : "Seperator", "enabled" : True, "menuItem" : "Seperator"},
##        #{"type" : "Import", "enabled" : True, "menuItem" : wx.MenuItem(self.entityPopupMenu, -1, "Import Entity/Entities"), "event" : self.OnImport} , # Import Entity Menu Item
##        #{"type" : "Export", "enabled" : False, "menuItem" : wx.MenuItem(self.entityPopupMenu, -1, "Export Entity"), "event" : self.OnExport} , # Export Entity Menu Item
##        ]
##        self.popupMenu.AddMenuItems(self.popupMenuItems) 
##        self.Bind(wx.EVT_RIGHT_DOWN, self.EnityTreeRightMenu)
##        self.Bind(wx.EVT_TREE_SEL_CHANGED,self.ShowObjectInformation)
    
    def defineSplitters(self):
        
        self.halfsplitter = wx.SplitterWindow(self)
        self.halfsplitter.SetSashGravity(0.5)
        self.halfsplitter.SetSize(self.GetSize())
        self.leftsplitter = wx.SplitterWindow(self.halfsplitter)
        self.rightsplitter = wx.SplitterWindow(self.halfsplitter)
        self.halfsplitter.SplitVertically(self.leftsplitter, self.rightsplitter, 0.5)
    
    def defineTrees(self):
        self.materialAttributes = MaterialAttributes(self.rightsplitter)
        self.materialPreview = wx.Notebook(self.rightsplitter, -1)
        
        self.ogreScene = OgreScene(self.ogreMgr, self.materialPreview, NameFactory())
        self.ogreView = self.ogreScene.create()
        self.materialPreview.AddPage(self.ogreView, "Preview")
        self.rightsplitter.SplitHorizontally(self.materialAttributes, self.materialPreview, 0.5)
        
        self.resourceTree = MaterialResourceTree(self.leftsplitter, self.config)
        self.materialTree = MaterialTree(self.leftsplitter)
        self.leftsplitter.SplitVertically(self.resourceTree, self.materialTree, 0.5)
        
    def defineWindows(self):
        pass

class MaterialSplitter(wx.SplitterWindow):
    def __init__(self, parent):
        wx.SplitterWindow.__init__(self, parent)
        self.SetSashGravity(0.5)
        self.SetSize(parent.GetSize())

class MaterialResourceTree(wx.TreeCtrl):
    def __init__(self, parent, config):
        wx.TreeCtrl.__init__(self, parent, -1)
        self.config = config
        self.Show(True)
        
        self.AddRoot("Material Resource")
        for c in self.config.Resources["Materials"]["resources"]:
            self.AppendItem(self.GetRootItem(), c)
            
        for c in ResourceInformation().loadedMaterials:
            print c
            self.AppendItem(self.GetRootItem(), c)

class MaterialTree(wx.TreeCtrl):
    def __init__(self, parent):
        wx.TreeCtrl.__init__(self, parent, -1)
        self.Show(True)

class MaterialAttributes(wx.Notebook):
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent, -1)
                
        l1, l2 = LogList(self), LogList(self)

        self.AddPage(l1, "Log1")
        self.AddPage(l2, "Log2")
        
        l1.AppendText("moaster")
        l2.AppendText("satans")
        
class MaterialPreviewAttributes(wx.Window):
    def __init__(self, parent, ogreMgr):
        wx.Window.__init__(self, parent)

class MaterialPreviewView(wx.Window):
    def __init__(self, parent, ogreMgr):
        wx.Window.__init__(self, parent)
        self.parent = parent
        self.ogreMgr = OgreManager().ogreMgr
        self.nameFactory = NameFactory()

class Attributes:
    __metaclass__=Singleton
    def __init__(self):
        pass
    def showObjectAttributes(self, Attributes, name):

        column = (5, 105, 205)
        row = 22        
        
        pan = self.foldPanel.AddFoldPanel(name, False)

        r = 0
        tulo = wx.Panel(pan, -1, style = wx.FULL_REPAINT_ON_RESIZE)

        for attrib in Attributes:
            c = 0
            for rowItem in attrib:
                if rowItem["type"] == "text": 
                    obj = wx.TextCtrl(tulo, -1,"",  style=rowItem["style"], pos = (column[c], row*r))
                    if not rowItem["attribs"] == None: obj.SetDefaultStyle(rowItem["attribs"])
                    obj.WriteText(rowItem["value"])
                    obj.SetEditable(rowItem["editable"])
                    if not rowItem["event"] == None:
                        obj.Bind(wx.EVT_TEXT, rowItem["event"])
                
                elif rowItem["type"] == "bitmapbutton":
                    modelButton = wx.BitmapButton(tulo, -1,rowItem["image"], pos = (column[c], row*r))
                    modelButton.Bind(wx.EVT_BUTTON, rowItem["event"])
                
                elif rowItem["type"] == "combobox":
                    comboBox = wx.ComboBox(tulo, -1, pos=(column[c], row*r), choices=rowItem["value"], style=rowItem["style"], size = (self.GetSizeTuple()[0] -8, -1))
                    comboBox.Bind(wx.EVT_COMBOBOX, rowItem["event"])

                elif rowItem["type"] == "button":
                    modelButton = wx.Button(tulo, -1,rowItem["value"], pos = (column[c], row*r))
                    modelButton.Bind(wx.EVT_BUTTON, rowItem["event"])
                
                elif rowItem["type"] == "checkbox":
                    checkbox = wx.CheckBox(tulo, -1, rowItem["value"], pos = (column[c]+5, row*r))
                    checkbox.Bind(wx.EVT_CHECKBOX, rowItem["event"])
                    checkbox.SetValue(rowItem["state"])

                
                elif rowItem["type"] == "slider":
                    slider = wx.Slider(tulo, -1, value = rowItem["value"], 
                            minValue = rowItem["minValue"], maxValue = rowItem["maxValue"],
                            style = rowItem["style"], pos = (column[c], row*r))
                    slider.Bind(wx.EVT_SLIDER, rowItem["event"])
                
                elif rowItem["type"] == "panel":
                    panel = wx.Panel(tulo, -1, pos = (column[c], row*r), size = rowItem["size"], style= rowItem["style"])
                    panel.SetBackgroundColour(rowItem["bgcolor"])
                    panel.Refresh(True, None)
                
                elif rowItem["type"] == "textctrl":
                    self.text = wx.TextCtrl(tulo, -1, rowItem["value"], pos=(column[c], row*r), size = (self.GetSizeTuple()[0] -8,rowItem["height"]),style = rowItem["style"])
                    self.text.Bind(wx.EVT_TEXT, rowItem["event"])
                
                elif rowItem["type"] == "comment":
                    text = wx.StaticText(tulo, -1,label = rowItem["label"],pos = (column[c], row*r))
                
                elif rowItem["type"] == "empty":
                    pass
                
                c += 1
            r += 1
        tulo.Fit()
        self.FoldPanelWindow(pan, tulo)

class MaterialOptions:
    def __init__(self, mmaterial):
        self.object = mmaterial
        
        self.Options =[
        [
        {"type" : "text", "editable" : False, "value" : "Name", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : self.object.name, "style" : wx.TE_RIGHT, "event" : self.OnName, "attribs" : None}, 
        ]
        ]

    def OnName(self, event):
        self.object.name = event.GetClientObject().GetValue()
        
class TechniqueOptions:
    def __init__(self, mtechnique):
        self.mtechnique = mtechnique 
        
        self.Options = []

class PassOptions:
    def __init__(self, mpass):
        self.mpass = mpass

        self.Options = []

class TextureUnitOptions:
    def __init__(self, mtextureUnit):
        self.mtextureUnit = mtextureUnit
        
        self.Options = []

class VertexProgramRefOptions:
    def __init__(self, mvertexProgramRef):
        self.object = mvertexProgramRef
        
        self.Options =[
        [
        {"type" : "text", "editable" : False, "value" : "Name", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : self.object.name, "style" : wx.TE_RIGHT, "event" : self.OnName, "attribs" : None}, 
        ]
        ]

    def OnName(self, event):
        self.object.name = event.GetClientObject().GetValue()

class FragmentProgramRefOptions:
    def __init__(self, mfragmentProgramRef):
        self.object = mfragmentProgramRef
        
        self.Options =[
        [
        {"type" : "text", "editable" : False, "value" : "Name", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : self.object.name, "style" : wx.TE_RIGHT, "event" : self.OnName, "attribs" : None}, 
        ]
        ]

    def OnName(self, event):
        self.object.name = event.GetClientObject().GetValue()

class VertexProgramOptions:
    def __init__(self, mvertexProgram):
        self.object = mvertexProgram
        
        self.Options =[
        [
        {"type" : "text", "editable" : False, "value" : "Name", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : self.object.name, "style" : wx.TE_RIGHT, "event" : self.OnName, "attribs" : None}, 
        ]
        ]

    def OnName(self, event):
        self.object.name = event.GetClientObject().GetValue()

class FragmentProgramOptions:
    def __init__(self, mfragmentProgram):
        self.object = mfragmentProgram
        
        self.Options =[
        [
        {"type" : "text", "editable" : False, "value" : "Name", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : self.object.name, "style" : wx.TE_RIGHT, "event" : self.OnName, "attribs" : None}, 
        ]
        ]

    def OnName(self, event):
        self.object.name = event.GetClientObject().GetValue()
        