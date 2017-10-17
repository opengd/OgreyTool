import wx
from ogreyEntity import *
from FoldPanelBar import *
from ogreyScriptEditor import *

import ogre.renderer.OGRE as ogre

class ogreyLevelAttributesPanel(wx.Panel):
    def __init__(self, parent, window, resourceInformation, middle):
        wx.Panel.__init__(self, parent, -1, style = wx.FULL_REPAINT_ON_RESIZE)
        self.current = None
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.window = window
        self.resourceInformation = resourceInformation
        self.parent = parent
        self.middle = middle
        self.ogreView = None
        self.ogreScene = None
        
        self.selected = True


    def select(self, selected = True):
        self.selected = selected
        
    def showAttributes(self, type, object, options = None, item = None):
        self.current = [type, object, options, item]
        #self.foldPanel = FoldPanelBar(self, wx.ID_ANY, wx.DefaultPosition,
        #                self.GetSize(), style = wx.FULL_REPAINT_ON_RESIZE)
        
        if type == "EntityInstance":
            EntityInstanceAttributes(self, object, options, item)
        
        if type == "Entity":
            EntityAttributes(self, object, options, item)
        
        if not type == None:
            pass
            #Comments(self, object, options, item)
        #self.Show()

    def Show(self, type, object, options = None, item = None):
        self.current = [type, object, options, item]
        if self.selected == True:
            self.foldPanel = FoldPanelBar(self, wx.ID_ANY, wx.DefaultPosition,
                        self.GetSize(), style = wx.FULL_REPAINT_ON_RESIZE)
            if not self.current == None: self.showAttributes(self.current[0], self.current[1], self.current[2], self.current[3])
            if not self.ogreView == None: EnviromentOptions(self, (self.ogreScene, self.ogreView), self.Level )

    def bindView(self, view):
        self.ogreView = view
        self.update()
        
    def bindScene(self, scene):
        self.ogreScene = scene
        self.update()
    
    def bindLevel(self, level):
        self.Level = level
        
    def OnSize(self, event):
        self.update()
    
    def clear(self):
        self.DestroyChildren()
    
    def update(self, event = None):
        self.clear()

        if not self.current == None:
            self.clear()
            self.Show(self.current[0], self.current[1], self.current[2], self.current[3])
        
        #self.Show(n, self.current[1], self.current[2], self.current[3]) 
    
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
        self.foldPanel.AddFoldPanelWindow(pan, tulo)

class EntityAttributes:
    def __init__(self, panel, object, tree, item):
        
        self.panel = panel
        self.object = object
        self.tree = tree
        self.item = item

        self.Attributes = [
        [
        {"type" : "text", "editable" : False, "value" : "Name", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : False, "value" : self.object.name, "style" : wx.TE_RIGHT, "event" : self.OnEntityName, "attribs" : None}, 
        ],
        [
        {"type" : "text", "editable" : False, "value" : "Name", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : False, "value" : self.object.filepath, "style" : wx.TE_RIGHT, "event" : self.OnEntityName, "attribs" : None}, 
        ],
        ]
        
        self.panel.showObjectAttributes(self.Attributes, "Entity")

    def OnEntityName(self, event):
        self.object.name = event.GetClientObject().GetValue()
        self.tree.SetItemText(self.item, self.object.name + " - Entity")

class EntityInstanceAttributes:
    def __init__(self, panel, object, tree, item):
        
        self.panel = panel
        self.object = object
        self.tree = tree
        self.item = item

        self.Attributes = [
        [
        {"type" : "text", "editable" : False, "value" : "Name", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : self.object.name, "style" : wx.TE_RIGHT, "event" : self.OnEntityName, "attribs" : None}, 
        ]
        # World Position        
        [{"type" : "text", "editable" : False, "value" : "World Position", "style" : wx.TE_LEFT | wx.TE_RICH2 , "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},],
        [{"type" : "text", "editable" : False, "value" : "X", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : str(self.object.position[0]), "style" : wx.TE_RIGHT, "event" : self.OnEntityPositionX, "attribs" : None}, ],
        [{"type" : "text", "editable" : False, "value" : "Y", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : str(self.object.position[1]), "style" : wx.TE_RIGHT, "event" : self.OnEntityPositionY, "attribs" : None}, ],
        [{"type" : "text", "editable" : False, "value" : "Z", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : str(self.object.position[2]), "style" : wx.TE_RIGHT, "event" : self.OnEntityPositionZ, "attribs" : None}, ],
        ]
        
        self.panel.showObjectAttributes(self.Attributes, "Entity Instance")

    def OnEntityName(self, event):
        self.object.name = event.GetClientObject().GetValue()
        self.tree.SetItemText(self.item, self.object.name + " - Entity Instance")

    def OnEntityPositionX(self, event):
        self.object.position.x = float(event.GetClientObject().GetValue())
        #self.update()
    def OnEntityPositionY(self, event):
        self.object.position.y = float(event.GetClientObject().GetValue())
        #self.update()
    def OnEntityPositionZ(self, event):
        self.object.position.z = float(event.GetClientObject().GetValue())
        #self.update()

class EnviromentOptions:
    def __init__(self, parent, window, object):
        self.parent = parent
        self.window, self.ogreView = window
        self.object = object
        
        self.bgcolour = wx.Colour(0,0,0)
        tempcolor = self.ogreView.viewport.backgroundColour
        self.bgcolour = wx.Colour(int(tempcolor.r*255.0),int(tempcolor.g*255.0), int(tempcolor.b*255.0))

        self.ambientcolour = wx.Colour(0,0,0)
        tempcolor = self.window.sceneManager.ambientLight
        self.ambientcolour = wx.Colour(int(tempcolor.r*255.0),int(tempcolor.g*255.0), int(tempcolor.b*255.0))
        
        self.Attributes = [
        [{"type" : "text", "editable" : False, "value" : "Background Color", "style" : wx.TE_LEFT | wx.TE_RICH2 , "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "button", "value" : "Choose Colour...", "event" : self.OnChooseColor},
        {"type" : "panel", "size" : (20,20), "style" : wx.SUNKEN_BORDER, "bgcolor" : self.bgcolour},],
        [{"type" : "text", "editable" : False, "value" : "Ambient Light Color", "style" : wx.TE_LEFT | wx.TE_RICH2 , "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "button", "value" : "Choose Colour...", "event" : self.OnAmbientChooseColor},
        {"type" : "panel", "size" : (20,20), "style" : wx.SUNKEN_BORDER, "bgcolor" : self.ambientcolour},],
        [{"type" : "empty"},],
        ]
        
        self.parent.showObjectAttributes(self.Attributes, "Level Enviroment")


    def OnChooseColor(self, event):

        dlg = wx.ColourDialog(self.parent)
        dlg.GetColourData().SetChooseFull(True)
        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetColourData()
            (r, g, b) = data.GetColour().Get()
            #print "Changing Background color to: ", str(float(r)) ,str(float(g)),str(float(b))
            self.bgcolour.Set(r, g, b)
            self.ogreView.viewport.backgroundColour = ((float(r)/255), (float(g)/255), (float(b)/255))
            self.object.clearcolor = ((float(r)/255), (float(g)/255), (float(b)/255))       
        dlg.Destroy()

        self.parent.update()

    def OnAmbientChooseColor(self, event):

        dlg = wx.ColourDialog(self.parent)
        dlg.GetColourData().SetChooseFull(True)
        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetColourData()
            (r, g, b) = data.GetColour().Get()
            #print "Changing Background color to: ", str(float(r)) ,str(float(g)),str(float(b))
            self.ambientcolour.Set(r, g, b)
            self.window.sceneManager.ambientLight = ((float(r)/255), (float(g)/255), (float(b)/255))
            self.object.ambientlight = ((float(r)/255), (float(g)/255), (float(b)/255))       
            
        dlg.Destroy()

        self.parent.update()