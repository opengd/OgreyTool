import wx
from ogreyEntity import *
from FoldPanelBar import *
import ogre.renderer.OGRE as ogre

class ogreyOptionsPanel(wx.Panel):
    def __init__(self, parent, resourceInformation):
        wx.Panel.__init__(self, parent, -1, style = wx.FULL_REPAINT_ON_RESIZE, size = (242,parent.GetSizeTuple()[1]))
        
        self.parent = parent
        #self.window = window
        self.current = None
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.ogreView = None
        self.ogreScene = None
        self.resourceInformation = resourceInformation
        
        self.selected = True
        #self.GetSize()
        #self.Show()
    
    def Show(self):
        if self.selected == True:
            self.foldPanel = FoldPanelBar(self, wx.ID_ANY, wx.DefaultPosition, size=self.GetSize(), style = wx.FULL_REPAINT_ON_RESIZE)#( 242,1000)
            if not self.ogreView == None: Render(self, self.ogreView)
            ShadowOptions(self, self.ogreScene)
            if not self.ogreView == None: EnviromentOptions(self, (self.ogreScene, self.ogreView))
            DefaultLight(self, self.ogreScene)
            Sky(self, self.ogreScene)
        
    def select(self, selected = True):
        self.selected = selected
    
    def update(self, event = None):
        self.DestroyChildren()
        self.Show() 

    def OnSize(self, event):
        self.update()
    
    def bindView(self, view):
        self.ogreView = view
        self.update()
        
    def bindScene(self, scene):
        self.ogreScene = scene
        self.update()
        
    def showObjectAttributes(self, Attributes, name):

        column = (5, 105, 205)
        row = 22        
        
        pan = self.foldPanel.AddFoldPanel(name, True)

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
                    comboBox = wx.ComboBox(tulo, -1, pos=(column[c], row*r), choices=rowItem["value"], style=rowItem["style"], size = (self.GetSizeTuple()[0] -8,-1))
                    comboBox.Bind(wx.EVT_COMBOBOX, rowItem["event"])
                    if not rowItem["selection"] == None: comboBox.SetStringSelection(rowItem["selection"])
                
                elif rowItem["type"] == "comboboxstandard":
                    comboBox = wx.ComboBox(tulo, -1, pos=(column[c], row*r), choices=rowItem["value"], style=rowItem["style"], size = (self.GetSizeTuple()[0]-110, -1))
                    comboBox.Bind(wx.EVT_COMBOBOX, rowItem["event"])
                    if not rowItem["selection"] == None: comboBox.SetStringSelection(rowItem["selection"])


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
                
                elif rowItem["type"] == "comment":
                    text = wx.StaticText(tulo, -1,label = rowItem["label"],pos = (column[c], row*r))
                
                elif rowItem["type"] == "radio":
                    radio = wx.RadioButton(tulo, -1, rowItem["value"],pos = (column[c], row*r), style=rowItem["style"])
                    radio.Bind(wx.EVT_RADIOBUTTON, rowItem["event"])
                    radio.SetValue(rowItem["attribs"])
                    
                elif rowItem["type"] == "empty":
                    pass
                
                c += 1
            r += 1
        tulo.Fit()
        self.foldPanel.AddFoldPanelWindow(pan, tulo)

class ShadowOptions:
    def __init__(self, parent, window):
        self.parent = parent
        self.window = window
        
        self.items = {"SHADOWTYPE_NONE" : ogre.SHADOWTYPE_NONE, 
        "SHADOWDETAILTYPE_ADDITIVE" : ogre.SHADOWDETAILTYPE_ADDITIVE, 
        "SHADOWDETAILTYPE_MODULATIVE" : ogre.SHADOWDETAILTYPE_MODULATIVE,
        "SHADOWDETAILTYPE_STENCIL" : ogre.SHADOWDETAILTYPE_STENCIL, 
        "SHADOWDETAILTYPE_TEXTURE" : ogre.SHADOWDETAILTYPE_TEXTURE, 
        "SHADOWTYPE_STENCIL_MODULATIVE" : ogre.SHADOWTYPE_STENCIL_MODULATIVE,
        "SHADOWTYPE_STENCIL_ADDITIVE" : ogre.SHADOWTYPE_STENCIL_ADDITIVE, 
        "SHADOWTYPE_TEXTURE_MODULATIVE" : ogre.SHADOWTYPE_TEXTURE_MODULATIVE, 
        "SHADOWTYPE_TEXTURE_ADDITIVE" : ogre.SHADOWTYPE_TEXTURE_ADDITIVE}

        self.colour = wx.Colour(0,0,0)
        for (key, value) in self.items.iteritems():
            if self.window.sceneManager.shadowTechnique == value:
                selection = key
        
        shadowcolor = self.window.sceneManager.shadowColour

        self.colour = wx.Colour(int(shadowcolor.r*255.0),int(shadowcolor.g*255.0), int(shadowcolor.b*255.0))
    
        self.Attributes = [
        [{"type" : "text", "editable" : False, "value" : "Type", "style" : wx.TE_LEFT | wx.TE_RICH2 , "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},],
        [{"type" : "combobox", "editable" : True, "value" : self.items.keys(), "style" : wx.CB_READONLY | wx.CB_SORT, "event" : self.OnSetShadowType, "attribs" : None, "selection" : selection}, ],
        [{"type" : "empty"}],
        [{"type" : "text", "editable" : False, "value" : "Color", "style" : wx.TE_LEFT | wx.TE_RICH2 , "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "button", "value" : "Choose Colour...", "event" : self.OnChooseColor},
        {"type" : "panel", "size" : (20,20), "style" : wx.SUNKEN_BORDER, "bgcolor" : self.colour},],
        ]
        
        self.parent.showObjectAttributes(self.Attributes, "Shadows")

    def OnChooseColor(self, event):

        dlg = wx.ColourDialog(self.parent)
        dlg.GetColourData().SetChooseFull(True)
        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetColourData()
            (r, g, b) = data.GetColour().Get()
            #print "Changing shadow color to: ", str(float(r)) ,str(float(g)),str(float(b))
            self.colour.Set(r, g, b)
            self.window.sceneManager.shadowColour = ((float(r)/255), (float(g)/255), (float(b)/255))            
        dlg.Destroy()

        self.parent.update()

    
    def OnSetShadowType(self, event):
        
        self.window.sceneManager.shadowTechnique = self.items[event.GetString()]
        
    def update(self, level):
        pass


class EnviromentOptions:
    def __init__(self, parent, window):
        self.parent = parent
        self.window, self.ogreView = window
        
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
        [
        {"type" : "text", "editable" : False, "value" : "Show Floor (On/Off)", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "checkbox", "editable" : True, "value" : "", "style" : wx.CHK_2STATE , "event" : self.OnOnOff, "attribs" : None, "state" : self.window.sceneFloor.getVisible()}, 
        ],
        [{"type" : "text", "editable" : False, "value" : "Floor Size", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},],
        [{"type" : "text", "editable" : False, "value" : "X", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : str(self.window.sceneFloor.getScale().x), "style" : wx.TE_RIGHT, "event" : self.OnScaleX, "attribs" : None}, ],
        [{"type" : "text", "editable" : False, "value" : "Z", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : str(self.window.sceneFloor.getScale().y), "style" : wx.TE_RIGHT, "event" : self.OnScaleY, "attribs" : None}, ],
        
        [{"type" : "text", "editable" : False, "value" : "Floor Position", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},],
        [{"type" : "text", "editable" : False, "value" : "X", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : str(self.window.sceneFloor.getPosition().x), "style" : wx.TE_RIGHT, "event" : self.OnPositionX, "attribs" : None}, ],
        [{"type" : "text", "editable" : False, "value" : "Y", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : str(self.window.sceneFloor.getPosition().y), "style" : wx.TE_RIGHT, "event" : self.OnPositionY, "attribs" : None}, ],
        [{"type" : "text", "editable" : False, "value" : "Z", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : str(self.window.sceneFloor.getPosition().z), "style" : wx.TE_RIGHT, "event" : self.OnPositionZ, "attribs" : None}, ],
        
        [{"type" : "text", "editable" : False, "value" : "Material", "style" : wx.TE_LEFT | wx.TE_RICH2 , "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},],
        [{"type" : "combobox", "editable" : True, "value" : self.parent.resourceInformation.loadedMaterials, "style" : wx.CB_READONLY | wx.CB_SORT, "event" : self.OnMaterialNameCombobox, "attribs" : None, "selection" : None}, ],
        [{"type" : "empty"}],
        [{"type" : "text", "editable" : False, "value" : "World Scale Multiple", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},],
        [{"type" : "text", "editable" : False, "value" : "X", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : str(self.window.worldScaleMultiple.x), "style" : wx.TE_RIGHT, "event" : self.OnWorldScaleX, "attribs" : None}, ],
        [{"type" : "text", "editable" : False, "value" : "Y", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : str(self.window.worldScaleMultiple.y), "style" : wx.TE_RIGHT, "event" : self.OnWorldScaleY, "attribs" : None}, ],
        [{"type" : "text", "editable" : False, "value" : "Z", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : str(self.window.worldScaleMultiple.z), "style" : wx.TE_RIGHT, "event" : self.OnWorldScaleZ, "attribs" : None}, ],
        ]
        
        self.parent.showObjectAttributes(self.Attributes, "Enviroment")
    
    def OnMaterialNameCombobox(self, event):
        self.window.sceneFloor.setMaterial(event.GetString())

    def OnChooseColor(self, event):

        dlg = wx.ColourDialog(self.parent)
        dlg.GetColourData().SetChooseFull(True)
        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetColourData()
            (r, g, b) = data.GetColour().Get()
            #print "Changing Background color to: ", str(float(r)) ,str(float(g)),str(float(b))
            self.bgcolour.Set(r, g, b)
            self.ogreView.viewport.backgroundColour = ((float(r)/255), (float(g)/255), (float(b)/255))            
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
        dlg.Destroy()

        self.parent.update()

    def OnOnOff(self, event):
        self.window.sceneFloor.setVisible(event.IsChecked())

    def OnScaleX(self, event):
        self.window.sceneFloor.setScale((float(event.GetClientObject().GetValue()), 0.0, self.window.sceneFloor.getScale().z))
        
    def OnScaleY(self, event):
        self.window.sceneFloor.setScale((self.window.sceneFloor.getScale().x, 0.0, float(event.GetClientObject().GetValue())))

    def OnPositionX(self, event):
        self.window.sceneFloor.setPosition((float(event.GetClientObject().GetValue()), self.window.sceneFloor.getPosition().y, self.window.sceneFloor.getPosition().z))        
    def OnPositionY(self, event):
        self.window.sceneFloor.setPosition((self.window.sceneFloor.getPosition().x, float(event.GetClientObject().GetValue()), self.window.sceneFloor.getPosition().z))
    def OnPositionZ(self, event):
        self.window.sceneFloor.setPosition((self.window.sceneFloor.getPosition().x, self.window.sceneFloor.getPosition().y, float(event.GetClientObject().GetValue())))
    
    def OnWorldScaleX(self, event):
        self.window.worldScaleMultiple = ogre.Vector3((float(event.GetClientObject().GetValue()), self.window.worldScaleMultiple.y, self.window.worldScaleMultiple.z))
        self.window.updateEntities()        
    def OnWorldScaleY(self, event):
        self.window.worldScaleMultiple = ogre.Vector3((self.window.worldScaleMultiple.x, float(event.GetClientObject().GetValue()), self.window.worldScaleMultiple.z))
        self.window.updateEntities()        
    def OnWorldScaleZ(self, event):
        self.window.worldScaleMultiple = ogre.Vector3((self.window.worldScaleMultiple.x, self.window.worldScaleMultiple.y, float(event.GetClientObject().GetValue())))
        self.window.updateEntities()        
        
class DefaultLight:
    def __init__(self, parent, window):
        self.parent = parent
        self.window = window
        
        self.Attributes = [
        [
        {"type" : "text", "editable" : False, "value" : "Light On/Off", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "checkbox", "editable" : True, "value" : "", "style" : wx.CHK_2STATE , "event" : self.OnOnOff, "attribs" : None, "state" : self.window.defaultLight.visible}, 
        ],
        [{"type" : "text", "editable" : False, "value" : "Position", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},],
        [{"type" : "text", "editable" : False, "value" : "X", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : str(self.window.defaultLight.position.x), "style" : wx.TE_RIGHT, "event" : self.OnPositionX, "attribs" : None}, ],
        [{"type" : "text", "editable" : False, "value" : "Y", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : str(self.window.defaultLight.position.y), "style" : wx.TE_RIGHT, "event" : self.OnPositionY, "attribs" : None}, ],
        [{"type" : "text", "editable" : False, "value" : "Z", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : str(self.window.defaultLight.position.z), "style" : wx.TE_RIGHT, "event" : self.OnPositionZ, "attribs" : None}, ],
        
        [{"type" : "comment", "label" : "* Only active when no lights are in scene"},],
        ]
        
        self.parent.showObjectAttributes(self.Attributes, "Default Light")
    
    def OnOnOff(self, event):
        self.window.defaultLight.visible = event.IsChecked()
        
    def OnPositionX(self, event):
        self.window.defaultLight.position.x = float(event.GetClientObject().GetValue())
        
    def OnPositionY(self, event):
        self.window.defaultLight.position.y = float(event.GetClientObject().GetValue())

    def OnPositionZ(self, event):
        self.window.defaultLight.position.z = float(event.GetClientObject().GetValue())

class Sky:
    def __init__(self, parent, window):
        self.parent = parent
        self.window = window
        self.sky = False
        self.activeType = "None"
        #self.skyMaterial = self.window.loadedMaterials[0]
        self.cubeMaterials = []
        
        materialIterator = ogre.MaterialManager.getSingleton().getResourceIterator()

        #self.loadedMaterials = []
        while (materialIterator.hasMoreElements()):
            mat = ogre.MaterialManager.getSingleton().getByName(materialIterator.peekNextValue().name)
            
            if mat.numTechniques > 0:
                if mat.getTechnique(0).numPasses > 0:
                    if mat.getTechnique(0).getPass(0).numTextureUnitStates > 0:
                        if mat.getTechnique(0).getPass(0).getTextureUnitState(0).cubic == True:
                            self.cubeMaterials.append(mat.name)
            materialIterator.moveNext()
        
        self.Attributes = [
        #[
        #{"type" : "text", "editable" : False, "value" : "Sky On/Off", "style" : wx.TE_LEFT | wx.TE_RICH2 | wx.NO_BORDER, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        #{"type" : "checkbox", "editable" : True, "value" : "", "style" : wx.CHK_2STATE , "event" : self.OnOnOff, "attribs" : None, "state" : self.sky}, 
        #],
        [{"type" : "text", "editable" : False, "value" : "Type", "style" : wx.TE_LEFT | wx.TE_RICH2 , "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},],
        [{"type" : "combobox", "editable" : True, "value" : ["None", "Sky Box", "Sky Dome"], "style" : wx.CB_READONLY | wx.CB_SORT, "event" : self.OnSkyType, "attribs" : None, "selection" : "None"}, ],

        [{"type" : "text", "editable" : False, "value" : "Material", "style" : wx.TE_LEFT | wx.TE_RICH2 , "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},],
        [{"type" : "combobox", "editable" : True, "value" : self.cubeMaterials, "style" : wx.CB_READONLY | wx.CB_SORT, "event" : self.OnSkyMaterial, "attribs" : None, "selection" : None}, ],

        ]
        
        self.parent.showObjectAttributes(self.Attributes, "Sky")
        
    def OnOnOff(self, event):
        self.sky = event.IsChecked()
        if self.activeType == "Sky Plane":
            self.window.sceneManager.skyPlaneEnabled = self.sky
        elif self.activeType == "Sky Box":
            self.window.sceneManager.skyBoxEnabled = self.sky
        elif self.activeType == "Sky Dome":
            self.window.sceneManager.skyDomeEnabled = self.sky
    
    def OnSkyType(self, event):
        self.activeType = event.GetString()
        self.SetSky()

    def OnSkyMaterial(self, event):
        self.skyMaterial = event.GetString()
        if not self.activeType == "None": self.SetSky()
    
    def SetSky(self):
        if self.activeType == "Sky Plane":
            #self.Off()
            #self.window.sceneManager.setSkyPlane(True
            pass
        elif self.activeType == "Sky Box":
            self.Off()
            self.window.sceneManager.setSkyBox(True, self.skyMaterial)
            pass
        elif self.activeType == "Sky Dome":
            self.Off()
            self.window.sceneManager.setSkyDome(True, self.skyMaterial)
        elif self.activeType == "None":
            self.Off()
            pass
        
    def Off(self):
        #self.window.sceneManager.skyPlaneEnabled = False
        self.window.sceneManager.setSkyBox(False, self.skyMaterial)
        self.window.sceneManager.setSkyDome(False, self.skyMaterial)


class Render:
    def __init__(self, parent, window):
        self.parent = parent
        self.window = window
        mode = self.window.camera.polygonMode  
        
        if mode == ogre.PM_SOLID: mode = "Solid"
        elif mode == ogre.PM_WIREFRAME: mode = "Wireframe"
        elif mode == ogre.PM_POINTS: mode = "Points"
        
        self.Attributes = [
        [{"type" : "text", "editable" : False, "value" : "Rendermode", "style" : wx.TE_LEFT | wx.TE_RICH2 , "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "comboboxstandard", "editable" : True, "value" : ["Solid","Wireframe", "Points"] , "style" : wx.CB_READONLY , "event" : self.OnRenderMode, "attribs" : None, "selection" : mode}, ],

        ]

        self.parent.showObjectAttributes(self.Attributes, "Render")
        
    def OnRenderMode(self, event):
        if event.GetString() == "Solid":
            self.window.renderModeSolid()
        elif event.GetString() == "Wireframe": 
            self.window.renderModeWireframe()
        elif event.GetString() == "Points":
            self.window.renderModePoints()

        
        
