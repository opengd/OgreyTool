import wx
from ogreyEntity import *
from FoldPanelBar import *
from ogreyScriptEditor import *

import ogre.renderer.OGRE as ogre

class ogreyAttributesPanel(wx.Panel):
    def __init__(self, parent, window, resourceInformation, middle):
        wx.Panel.__init__(self, parent, -1, style = wx.FULL_REPAINT_ON_RESIZE)
        self.current = None
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.window = window
        self.resourceInformation = resourceInformation
        self.parent = parent
        self.middle = middle

    def select(self, select):
        pass
        
    def showAttributes(self, type, object, options = None, item = None):
        self.current = [type, object, options, item]
        self.foldPanel = FoldPanelBar(self, wx.ID_ANY, wx.DefaultPosition,
                        self.GetSize(), style = wx.FULL_REPAINT_ON_RESIZE)
        
        if type == "Entity":
            #EntityAttributes(self, object, options, item)
            #print "bresddsd"
            pass
        
        elif type == "RootNode":
            RootNodeAttributes(self, object, options, item)
            
        elif type == "Transform":
            TransformAttributes(self, object, options, item)
    
        elif type == "Graphic":
            GraphicAttributes(self, object, options, item)
            #AnimationAttributes(self, object, options, item)
            MaterialAttributes(self, object, options, item)
        
        elif type == "AnimatedGraphic":
            GraphicAttributes(self, object, options, item)
            AnimationAttributes(self, object, options, item)
            MaterialAttributes(self, object, options, item)
            
        #elif type == "Physic":
        #    PhysicAttributes(self, object, options, item)

        elif type == "PhysicActor":
            PhysicActorAttributes(self, object, options, item)

        elif type == "PhysicBody":
            PhysicBodyAttributes(self, object, options, item)
            pass
        elif type == "PhysicShape":
            PhysicShapeAttributes(self, object, options, item)

        elif type == "EntityInstance":
            pass
        
        elif type == "FreeCamera":
            FreeCameraAttributes(self, object, options, item)

        elif type == "FollowCamera":
            FollowCameraAttributes(self, object, options, item)
        
        elif type == "Control":
            ControlAttributes(self, object, options, item)
        
        elif type == "Ai":
            AiAttributes(self, object, options, item)
        
        elif type == "Light":
            LightAttributes(self, object, options, item)
        
        elif type == "PhysicController":
            PhysicControllerAttributes(self, object, options, item)
            
        elif type == "PhysicControllerShapeCapsule":
            PhysicControllerShapeSphereAttributes(self, object, options, item)
    
        elif type == "AudioSource":
            AudioSourceAttributes(self, object, options, item)
        
        if not type == None:
            pass
            #Comments(self, object, options, item)

    
    def OnSize(self, event):
        self.update()
    
    def clear(self):
        self.DestroyChildren()
    
    def update(self, event = None):
        if not self.current == None:
            self.clear()
            self.showAttributes(self.current[0], self.current[1], self.current[2], self.current[3]) 
    
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
        {"type" : "text", "editable" : True, "value" : self.object.name, "style" : wx.TE_RIGHT, "event" : self.OnEntityName, "attribs" : None}, 
        ]
        ]
        
        self.panel.showObjectAttributes(self.Attributes, "Entity")

    def OnEntityName(self, event):
        self.object.name = event.GetClientObject().GetValue()
        self.tree.SetItemText(self.item, self.object.name + " - Entity")
        

class RootNodeAttributes:
    def __init__(self, panel, object, tree, item):
        self.panel = panel
        self.object = object
        self.tree = tree
        self.item = item

        self.Attributes = [
        [
        {"type" : "comment", "editable" : True, "label" : "* This node is not editable"}, 
        ]
        ]
        
        self.panel.showObjectAttributes(self.Attributes, "RootNode")

class TransformAttributes:
    def __init__(self, panel, object, tree, item):
        self.panel = panel
        self.object = object
        self.tree = tree
        self.item = item
        
        self.Attributes = [
        [{"type" : "text", "editable" : False, "value" : "Name", "style" : wx.TE_LEFT | wx.TE_RICH2 , "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : self.object.name, "style" : wx.TE_RIGHT, "event" : self.OnNodeName, "attribs" : None},],
# Local Position        
        [{"type" : "text", "editable" : False, "value" : "Local Position", "style" : wx.TE_LEFT | wx.TE_RICH2 , "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},],
        [{"type" : "text", "editable" : False, "value" : "X", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : str(self.object.position[0]), "style" : wx.TE_RIGHT, "event" : self.OnNodePositionX, "attribs" : None}, ],
        [{"type" : "text", "editable" : False, "value" : "Y", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : str(self.object.position[1]), "style" : wx.TE_RIGHT, "event" : self.OnNodePositionY, "attribs" : None}, ],
        [{"type" : "text", "editable" : False, "value" : "Z", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : str(self.object.position[2]), "style" : wx.TE_RIGHT, "event" : self.OnNodePositionZ, "attribs" : None}, ],
# Local Rotation        
        [{"type" : "text", "editable" : False, "value" : "Local Rotation", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},],
        [{"type" : "text", "editable" : False, "value" : "X", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : str(self.object.rotation[0]), "style" : wx.TE_RIGHT, "event" : self.OnNodeRotationX, "attribs" : None}, ],
        [{"type" : "text", "editable" : False, "value" : "Y", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : str(self.object.rotation[1]), "style" : wx.TE_RIGHT, "event" : self.OnNodeRotationY, "attribs" : None}, ],
        [{"type" : "text", "editable" : False, "value" : "Z", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : str(self.object.rotation[2]), "style" : wx.TE_RIGHT, "event" : self.OnNodeRotationZ, "attribs" : None}, ],
#Local Scale        
        [{"type" : "text", "editable" : False, "value" : "Local Scale", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},],
        [{"type" : "text", "editable" : False, "value" : "X", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : str(self.object.scale[0]), "style" : wx.TE_RIGHT, "event" : self.OnNodeScaleX, "attribs" : None}, ],
        [{"type" : "text", "editable" : False, "value" : "Y", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : str(self.object.scale[1]), "style" : wx.TE_RIGHT, "event" : self.OnNodeScaleY, "attribs" : None}, ],
        [{"type" : "text", "editable" : False, "value" : "Z", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : str(self.object.scale[2]), "style" : wx.TE_RIGHT, "event" : self.OnNodeScaleZ, "attribs" : None}, ]
        ]
        
        self.panel.showObjectAttributes(self.Attributes, "Transform Object")
    
    def OnNodeName(self, event):
        self.object.name = event.GetClientObject().GetValue()
        (child, cookie) = self.tree.GetFirstChild(self.tree.GetSelections()[0])
        if child.IsOk():
            obj = self.tree.GetItemData(child).GetData()
            obj.node = self.object.name
            while child.IsOk():
                (child, cookie) = self.tree.GetNextChild(self.tree.GetSelections()[0], cookie)
                if child.IsOk():
                    obj = self.tree.GetItemData(child).GetData()
                    obj.node = self.object.name
        
        self.tree.SetItemText(self.item, self.object.name + " - Transform Object")

    
    def OnNodePositionX(self, event):
        self.object.position.x = float(event.GetClientObject().GetValue())
        self.update()
    def OnNodePositionY(self, event):
        self.object.position.y = float(event.GetClientObject().GetValue())
        self.update()
    def OnNodePositionZ(self, event):
        self.object.position.z = float(event.GetClientObject().GetValue())
        self.update()
         
    def OnNodeRotationX(self, event):
        self.object.rotation.x = float(event.GetClientObject().GetValue())
        self.update()
    def OnNodeRotationY(self, event):
        self.object.rotation.y = float(event.GetClientObject().GetValue())
        self.update()
    def OnNodeRotationZ(self, event):
        self.object.rotation.z = float(event.GetClientObject().GetValue())
        self.update()
    
    def OnNodeScaleX(self, event):
        self.object.scale.x = float(event.GetClientObject().GetValue())
        self.update()
    def OnNodeScaleY(self, event):
        self.object.scale.y = float(event.GetClientObject().GetValue())
        self.update()
    def OnNodeScaleZ(self, event):
        self.object.scale.z = float(event.GetClientObject().GetValue())
        self.update()
    
    def update(self):
        self.tree.updatePreview()
        
class GraphicAttributes:
    def __init__(self, panel, object, tree, item):
        self.panel = panel
        self.object = object
        self.tree = tree
        self.item = item
        
        #if not self.object.model == "":
        #    material = 
        
        self.Attributes = [
        [
        {"type" : "text", "editable" : False, "value" : "Name", "style" : wx.TE_LEFT | wx.TE_RICH2 , "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : self.object.name, "style" : wx.TE_RIGHT, "event" : self.OnObjectName, "attribs" : None}, 
        ],
        [
        {"type" : "text", "editable" : False, "value" : "Model/Mesh", "style" : wx.TE_LEFT | wx.TE_RICH2 , "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        ],
        [
        {"type" : "text", "editable" : False, "value" : "Path", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : self.object.model, "style" : wx.TE_RIGHT, "event" : self.OnModel, "attribs" : None},
        {"type" : "bitmapbutton", "image" : wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_BUTTON), "event" : self.OnModelButton}, 
        ],
        [
        {"type" : "text", "editable" : False, "value" : "Material", "style" : wx.TE_LEFT | wx.TE_RICH2 , "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : self.object.material, "style" : wx.TE_RIGHT, "event" : self.OnMaterialName, "attribs" : None}, 
        ],
        [{"type" : "combobox", "editable" : True, "value" : self.panel.resourceInformation.loadedMaterials, "style" : wx.CB_READONLY | wx.CB_SORT, "event" : self.OnMaterialNameCombobox, "attribs" : None}, ],
        #[{"type" : "button", "value" : "Edit Material", "event" : self.OnEditMaterial},],
        ]

        self.panel.showObjectAttributes(self.Attributes, "Graphic Object")
    
    def OnObjectName(self, event):
        self.object.name = event.GetClientObject().GetValue()
        self.tree.SetItemText(self.item, self.object.name + " - Graphic Object")
        
    def OnModel(self, event):
        self.object.model = event.GetClientObject().GetValue()
        self.update()
        
    def OnModelButton(self, event):
        fdg = wx.FileDialog(self.panel, message = "Choose Mesh File", style=wx.OPEN, wildcard = "*.mesh")
        if fdg.ShowModal() == wx.ID_OK:
            self.object.model = fdg.GetFilename()
        fdg.Destroy()
        self.update()
    
    def OnMaterialName(self, event):
        self.object.material = event.GetClientObject().GetValue()
    
    def OnMaterialNameCombobox(self, event):
        self.object.material = event.GetString()
        self.update()
    
    def OnEditMaterial(self, event):
        for matorigin in self.panel.resourceInformation.materialsOrigin:
            if matorigin["name"] == self.object.material:
                #res = ogre.ResourceGroupManager.getSingleton().getResourceGroup("General")
                #resIterator = ogre.ResourceGroupManager.getSingleton().resourceLocationIndex.find(matorigin["origin"])
                resIterator = ogre.ResourceGroupManager.getSingleton().listResourceFileInfo("General")
                #while (resIterator.hasMoreElements()):
                for nm in resIterator:
                    if nm.filename == matorigin["origin"]:
                        path = nm.path
                        filename = nm.filename
                        complete = path + filename
                        #print complete
                    #filename = fileArchive.getName() + "/" + matorigin["origin"]
                    materialIterator.moveNext()
                scrip = ScriptEditor(self.panel.middle)
                scrip.Load(complete)
                self.panel.middle.AddPage(scrip, matorigin["origin"])
                break
        
    def update(self):
        #self.panel.clear()
        #self.panel.showAttributes("Graphic",self.object, self.tree, self.item)
        #self.panel.showObjectAttributes(self.Attributes)
        self.tree.updatePreview()
        self.panel.update()


class AnimationAttributes:
    def __init__(self, panel, object, tree, item):
        self.panel = panel
        self.object = object
        self.tree = tree
        self.item = item
        self.AnimationList = []
        
        self.animationObject = self.object.animationObject
        
        if not self.object.ogreEntity == None:
            animStates = self.getAllAnimations(self.object.ogreEntity)
            if not animStates == None:
                self.AnimationList = animStates
                
##                for animS in animStates:
##                    animDict[animS] = 0
##                if animDict.has_key(anim):
##                    loop = True
##                    self.speed = ogre.Math.RangeRandom(0.5, 1.5)
##                    self.activAnime = self.entity.getAnimationState(anim)
##                    self.activAnime.loop = loop
##                    self.activAnime.enabled = True
##                    self.activAnime.speed = self.speed
##                    self.Animation = True
##        
        self.Attributes = [
        [
        {"type" : "text", "editable" : False, "value" : "Animation states", "style" : wx.TE_LEFT | wx.TE_RICH2 , "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        ],
        [
        {"type" : "combobox", "editable" : True, "value" : self.AnimationList, "style" : wx.CB_READONLY | wx.CB_SORT, "event" : self.OnSetAnimation, "attribs" : None}, 
        ],
        [
        {"type" : "empty"}
        ],
        [
        {"type" : "button", "value" : "Play", "event" : self.PlayAnimation},
        {"type" : "button", "value" : "Stop", "event" : self.StopAnimation}
        ],
        [
        {"type" : "empty"}
        ],
        [
        {"type" : "text", "editable" : False, "value" : "Animation speed", "style" : wx.TE_LEFT | wx.TE_RICH2 , "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "slider", "style" : wx.SL_HORIZONTAL, "minValue" : 0,"maxValue" : 100, "value" : self.animationObject.speed * 100, "event" : self.OnChangeAnimationSpeed} 
        ],
        [
        {"type" : "empty"}
        ],
        [
        {"type" : "text", "editable" : False, "value" : "Show Skeleton", "style" : wx.TE_LEFT | wx.TE_RICH2 , "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "checkbox", "editable" : True, "value" : "", "style" : wx.CHK_2STATE , "event" : self.OnShowSkeleton, "attribs" : None, "state" : False}, 
        ],
        ]
        
        self.panel.showObjectAttributes(self.Attributes, "Animation (Non saving options)")
    
    def getAllAnimations(self, entity):
        if(entity.skeleton):
            skel = entity.skeleton
            animations = [skel.getAnimation(j).name for j in range(skel.numAnimations)]
            return animations
        else: return None
    
    def OnSetAnimation(self, event):
        if not len(self.AnimationList) == 0:
            self.animationObject.animation = event.GetString()
    
    def PlayAnimation(self, event):
        if not self.object.ogreEntity == None:
            if(self.object.ogreEntity.skeleton):
                self.animationObject.playAnimation(self.object.ogreEntity)
        
    def StopAnimation(self, event):
        if not self.object.ogreEntity == None:
            if(self.object.ogreEntity.skeleton): 
                self.animationObject.stopAnimation()
    
    def OnChangeAnimationSpeed(self, event):
        if not self.object.ogreEntity == None:
            if(self.object.ogreEntity.skeleton):
                self.animationObject.changeSpeed(event.GetInt() * 0.01)
    
    def OnShowSkeleton(self, event):
        if not self.object.ogreEntity == None:
            if(self.object.ogreEntity.skeleton):
                self.object.ogreEntity.displaySkeleton = event.IsChecked()

class MaterialAttributes:
    def __init__(self, panel, object, tree, item):
        self.panel = panel
        self.object = object
        self.tree = tree
        self.item = item
        
        self.Attributes = [
        [        
        {"type" : "text", "editable" : False, "value" : "Ambient", "style" : wx.TE_LEFT | wx.TE_RICH2 , "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        ],
        [{"type" : "text", "editable" : False, "value" : "R", "style" : wx.TE_LEFT | wx.TE_RICH2 , "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "slider", "style" : wx.SL_HORIZONTAL, "minValue" : 0,"maxValue" : 100, "value" : 0, "event" : self.OnChangeAmbientR}],
        [{"type" : "text", "editable" : False, "value" : "G", "style" : wx.TE_LEFT | wx.TE_RICH2 , "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "slider", "style" : wx.SL_HORIZONTAL, "minValue" : 0,"maxValue" : 100, "value" : 0, "event" : self.OnChangeAmbientG}],
        [{"type" : "text", "editable" : False, "value" : "B", "style" : wx.TE_LEFT | wx.TE_RICH2 , "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "slider", "style" : wx.SL_HORIZONTAL, "minValue" : 0,"maxValue" : 100, "value" : 0, "event" : self.OnChangeAmbientB}],

        [        
        {"type" : "text", "editable" : False, "value" : "Diffuse", "style" : wx.TE_LEFT | wx.TE_RICH2 , "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        ],
        [{"type" : "text", "editable" : False, "value" : "R", "style" : wx.TE_LEFT | wx.TE_RICH2 , "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "slider", "style" : wx.SL_HORIZONTAL, "minValue" : 0,"maxValue" : 100, "value" : 0, "event" : self.OnChangeDiffuseR}],
        [{"type" : "text", "editable" : False, "value" : "G", "style" : wx.TE_LEFT | wx.TE_RICH2 , "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "slider", "style" : wx.SL_HORIZONTAL, "minValue" : 0,"maxValue" : 100, "value" : 0, "event" : self.OnChangeDiffuseG}],
        [{"type" : "text", "editable" : False, "value" : "B", "style" : wx.TE_LEFT | wx.TE_RICH2 , "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "slider", "style" : wx.SL_HORIZONTAL, "minValue" : 0,"maxValue" : 100, "value" : 0, "event" : self.OnChangeDiffuseB}],
        
        [        
        {"type" : "text", "editable" : False, "value" : "Specular", "style" : wx.TE_LEFT | wx.TE_RICH2 , "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        ],
        [{"type" : "text", "editable" : False, "value" : "R", "style" : wx.TE_LEFT | wx.TE_RICH2 , "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "slider", "style" : wx.SL_HORIZONTAL, "minValue" : 0,"maxValue" : 100, "value" : 0, "event" : self.OnChangeSpecularR}],
        [{"type" : "text", "editable" : False, "value" : "G", "style" : wx.TE_LEFT | wx.TE_RICH2 , "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "slider", "style" : wx.SL_HORIZONTAL, "minValue" : 0,"maxValue" : 100, "value" : 0, "event" : self.OnChangeSpecularG}],
        [{"type" : "text", "editable" : False, "value" : "B", "style" : wx.TE_LEFT | wx.TE_RICH2 , "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "slider", "style" : wx.SL_HORIZONTAL, "minValue" : 0,"maxValue" : 100, "value" : 0, "event" : self.OnChangeSpecularB}],

        [        
        {"type" : "text", "editable" : False, "value" : "Emissive", "style" : wx.TE_LEFT | wx.TE_RICH2 , "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        ],
        [{"type" : "text", "editable" : False, "value" : "R", "style" : wx.TE_LEFT | wx.TE_RICH2 , "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "slider", "style" : wx.SL_HORIZONTAL, "minValue" : 0,"maxValue" : 100, "value" : 0, "event" : self.OnChangeEmissiveR}],
        [{"type" : "text", "editable" : False, "value" : "G", "style" : wx.TE_LEFT | wx.TE_RICH2 , "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "slider", "style" : wx.SL_HORIZONTAL, "minValue" : 0,"maxValue" : 100, "value" : 0, "event" : self.OnChangeEmissiveG}],
        [{"type" : "text", "editable" : False, "value" : "B", "style" : wx.TE_LEFT | wx.TE_RICH2 , "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "slider", "style" : wx.SL_HORIZONTAL, "minValue" : 0,"maxValue" : 100, "value" : 0, "event" : self.OnChangeEmissiveB}],
        
        [{"type" : "text", "editable" : False, "value" : "Shininess", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "slider", "style" : wx.SL_HORIZONTAL, "minValue" : 0,"maxValue" : 100, "value" : 0, "event" : self.OnChangeShininess}],
        
        
##        [{"type" : "text", "editable" : False, "value" : "Ambient", "style" : wx.TE_LEFT | wx.TE_RICH2 , "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
##        {"type" : "button", "value" : "Choose Colour...", "event" : self.OnChooseAmbientColor},
##        {"type" : "panel", "size" : (20,20), "style" : wx.SUNKEN_BORDER, "bgcolor" : self.colourAmbient},],
##
##        [{"type" : "text", "editable" : False, "value" : "Diffuse", "style" : wx.TE_LEFT | wx.TE_RICH2 , "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
##        {"type" : "button", "value" : "Choose Colour...", "event" : self.OnChooseDiffuseColor},
##        {"type" : "panel", "size" : (20,20), "style" : wx.SUNKEN_BORDER, "bgcolor" : self.colourSpecular},],
##
##        [{"type" : "text", "editable" : False, "value" : "Specular", "style" : wx.TE_LEFT | wx.TE_RICH2 , "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
##        {"type" : "button", "value" : "Choose Colour...", "event" : self.OnChooseSpecularColor},
##        {"type" : "panel", "size" : (20,20), "style" : wx.SUNKEN_BORDER, "bgcolor" : self.colour},],
##
##        [{"type" : "text", "editable" : False, "value" : "Emissive", "style" : wx.TE_LEFT | wx.TE_RICH2 , "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
##        {"type" : "button", "value" : "Choose Colour...", "event" : self.OnChooseEmissiveColor},
##        {"type" : "panel", "size" : (20,20), "style" : wx.SUNKEN_BORDER, "bgcolor" : self.colourEmissive},],
        
        ]
        
        self.panel.showObjectAttributes(self.Attributes, "Material (Non saving options)")

    def OnChooseAmbientColor(self, event):
        if not self.object.ogreEntity == None:
            dlg = wx.ColourDialog(self.parent)
            dlg.GetColourData().SetChooseFull(True)
            if dlg.ShowModal() == wx.ID_OK:
                data = dlg.GetColourData()
                (r, g, b) = data.GetColour().Get()
                #print "Changing shadow color to: ", str(float(r)) ,str(float(g)),str(float(b))
                self.colour.Set(r, g, b)
                self.loopThrowEntity(type = "ambient", color = "r", value = ((float(r)/255), (float(g)/255), (float(b)/255)))
            dlg.Destroy()

            self.parent.Update()

    def OnChooseDiffuseColor(self, event):
        if not self.object.ogreEntity == None:
            dlg = wx.ColourDialog(self.parent)
            dlg.GetColourData().SetChooseFull(True)
            if dlg.ShowModal() == wx.ID_OK:
                data = dlg.GetColourData()
                (r, g, b) = data.GetColour().Get()
                #print "Changing shadow color to: ", str(float(r)) ,str(float(g)),str(float(b))
                self.colour.Set(r, g, b)
                self.loopThrowEntity(type = "diffuse", color = "r", value = ((float(r)/255), (float(g)/255), (float(b)/255)))
            dlg.Destroy()

            self.parent.Update()

    def OnChooseSpecularColor(self, event):
        if not self.object.ogreEntity == None:
            dlg = wx.ColourDialog(self.parent)
            dlg.GetColourData().SetChooseFull(True)
            if dlg.ShowModal() == wx.ID_OK:
                data = dlg.GetColourData()
                (r, g, b) = data.GetColour().Get()
                #print "Changing shadow color to: ", str(float(r)) ,str(float(g)),str(float(b))
                self.colour.Set(r, g, b)
                self.loopThrowEntity(type = "specular", color = "r", value = ((float(r)/255), (float(g)/255), (float(b)/255)))
            dlg.Destroy()

            self.parent.Update()
        
    def OnChooseEmissiveColor(self, event):
        if not self.object.ogreEntity == None:
            dlg = wx.ColourDialog(self.parent)
            dlg.GetColourData().SetChooseFull(True)
            if dlg.ShowModal() == wx.ID_OK:
                data = dlg.GetColourData()
                (r, g, b) = data.GetColour().Get()
                #print "Changing shadow color to: ", str(float(r)) ,str(float(g)),str(float(b))
                self.colour.Set(r, g, b)
                self.loopThrowEntity(type = "emissive", color = "r", value = ((float(r)/255), (float(g)/255), (float(b)/255)))
                #self.window.sceneManager.shadowColour =             
            dlg.Destroy()

            self.parent.Update()

    def OnChangeAmbientR(self, event):
        if not self.object.ogreEntity == None:
            self.loopThrowEntity(type = "ambient", color = "r", value = event.GetInt())
    def OnChangeAmbientG(self, event):
        if not self.object.ogreEntity == None:
            self.loopThrowEntity(type = "ambient", color = "g", value = event.GetInt())
    def OnChangeAmbientB(self, event):
        if not self.object.ogreEntity == None:
            self.loopThrowEntity(type = "ambient", color = "b", value = event.GetInt())
    
    def OnChangeDiffuseR(self, event):
        if not self.object.ogreEntity == None:
            self.loopThrowEntity(type = "diffuse", color = "r", value = event.GetInt())
    def OnChangeDiffuseG(self, event):
        if not self.object.ogreEntity == None:
            self.loopThrowEntity(type = "diffuse", color = "g", value = event.GetInt())
    def OnChangeDiffuseB(self, event):
        if not self.object.ogreEntity == None:
            self.loopThrowEntity(type = "diffuse", color = "b", value = event.GetInt())
            
    def OnChangeSpecularR(self, event):
        if not self.object.ogreEntity == None:
            self.loopThrowEntity(type = "specular", color = "r", value = event.GetInt())
    def OnChangeSpecularG(self, event):
        if not self.object.ogreEntity == None:
            self.loopThrowEntity(type = "specular", color = "g", value = event.GetInt())
    def OnChangeSpecularB(self, event):
        if not self.object.ogreEntity == None:
            self.loopThrowEntity(type = "specular", color = "b", value = event.GetInt())
    
    def OnChangeEmissiveR(self, event):
        if not self.object.ogreEntity == None:
            self.loopThrowEntity(type = "emissive", color = "r", value = event.GetInt())
    def OnChangeEmissiveG(self, event):
        if not self.object.ogreEntity == None:
            self.loopThrowEntity(type = "emissive", color = "g", value = event.GetInt())
    def OnChangeEmissiveB(self, event):
        if not self.object.ogreEntity == None:
            self.loopThrowEntity(type = "emissive", color = "b", value = event.GetInt())

    def OnChangeShininess(self, event):
        if not self.object.ogreEntity == None:
            self.loopThrowEntity(type = "shininess", color = "none", value = event.GetInt())

    def loopThrowEntity(self, type, color, value):
        if not self.object.ogreEntity == None:
           for numSub in range(self.object.ogreEntity.numSubEntities): 
                subEnt = self.object.ogreEntity.getSubEntity(numSub)
                for tech in range(subEnt.material.numTechniques):
                    for passes in range(subEnt.material.getTechnique(tech).numPasses):
                        materialPass = subEnt.material.getTechnique(tech).getPass(passes)
                        
                        if color == "r": index = 0
                        elif color == "g": index = 1
                        elif color == "b": index = 2
                        value = float(value) * 0.01

                        if type == "ambient":
                            if color == "r": materialPass.ambient.r = value
                            elif color == "g": materialPass.ambient.g = value
                            elif color == "b": materialPass.ambient.b = value
                            #materialPass.ambient = value
                        elif type == "diffuse": 
                            if color == "r": materialPass.diffuse.r = value
                            elif color == "g": materialPass.diffuse.g = value
                            elif color == "b": materialPass.diffuse.b = value
                            #materialPass.diffuse = value
                        elif type == "specular" :
                            if color == "r": materialPass.specular.r = value
                            elif color == "g": materialPass.specular.g = value
                            elif color == "b": materialPass.specular.b = value
                            #materialPass.specular = value
                        elif type == "emessive" :
                            if color == "r": materialPass.emessive.r = value
                            elif color == "g": materialPass.emessive.g = value
                            elif color == "b": materialPass.emessive.b = value
                            #materialPass.emessive = value
                            
                        elif type == "shininess" : materialPass.shininess = float(value)
                        
class PhysicActorAttributes:
    def __init__(self, panel, object, tree, item):
        self.panel = panel
        self.object = object
        self.tree = tree
        self.item = item
    
        self.Attributes = [
        [
        {"type" : "text", "editable" : False, "value" : "Name", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : self.object.name, "style" : wx.TE_RIGHT, "event" : self.OnActorName, "attribs" : None},
        ],
        [{"type" : "empty"}],
        [
        {"type" : "text", "editable" : False, "value" : "Static", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "checkbox", "editable" : True, "value" : "", "style" : wx.CHK_2STATE , "event" : self.OnStatic, "attribs" : None, "state" : self.object.static}, 
        ],
        [
        {"type" : "text", "editable" : False, "value" : "Collision", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "checkbox", "editable" : True, "value" : "", "style" : wx.CHK_2STATE , "event" : self.OnCollision, "attribs" : None, "state" : self.object.collisionenabled}, 
        ],
        [
        {"type" : "text", "editable" : False, "value" : "Follow Node", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "checkbox", "editable" : True, "value" : "", "style" : wx.CHK_2STATE , "event" : self.OnFollow, "attribs" : None, "state" : self.object.follow}, 
        ],
        ]
        
        self.panel.showObjectAttributes(self.Attributes, "Physic Actor")

    
    def OnActorName(self, event):
        self.object.name = event.GetClientObject().GetValue()
        self.tree.SetItemText(self.item, self.object.name + " - Physic Object")
    
    def OnStatic(self, event):
        self.object.static = event.IsChecked()
    
    def OnCollision(self, event):
        self.object.collisionenabled = event.IsChecked()

    def OnFollow(self, event):
        self.object.follow = event.IsChecked()

class PhysicBodyAttributes:
    def __init__(self, panel, object, tree, item):
        self.panel = panel
        self.object = object
        self.tree = tree
        self.item = item
        
        self.Attributes = [
        [
        {"type" : "text", "editable" : False, "value" : "Gravity", "style" : wx.TE_LEFT | wx.TE_RICH2 , "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "checkbox", "editable" : True, "value" : "", "style" : wx.CHK_2STATE , "event" : self.OnGravity, "attribs" : None, "state" : self.object.gravityenabled}, 
        ],
        [
        {"type" : "text", "editable" : False, "value" : "Kinematic", "style" : wx.TE_LEFT | wx.TE_RICH2 , "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "checkbox", "editable" : True, "value" : "", "style" : wx.CHK_2STATE , "event" : self.OnKinematic, "attribs" : None , "state" : self.object.kinematic}, 
        ],
        [
        {"type" : "text", "editable" : False, "value" : "Linear damping", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : str(self.object.lineardamping), "style" : wx.TE_RIGHT, "event" : self.OnLinearDamping, "attribs" : None},
        ],
        [
        {"type" : "text", "editable" : False, "value" : "Angular damping", "style" : wx.TE_LEFT | wx.TE_RICH2 , "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : str(self.object.angulardamping), "style" : wx.TE_RIGHT, "event" : self.OnAngularDamping, "attribs" : None},
        ],
        [
        {"type" : "text", "editable" : False, "value" : "Max Angular Velocity", "style" : wx.TE_LEFT | wx.TE_RICH2 , "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : str(self.object.maxangularvelocity), "style" : wx.TE_RIGHT, "event" : self.OnMaxAngularDamping, "attribs" : None},
        ],
#Linear Velocity        
        [{"type" : "empty"}],
        [{"type" : "text", "editable" : False, "value" : "Linear Velocity", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},],
        [{"type" : "text", "editable" : False, "value" : "X", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : str(self.object.linearvelocity[0]), "style" : wx.TE_RIGHT, "event" : self.OnLinearVelocityX, "attribs" : None}, ],
        [{"type" : "text", "editable" : False, "value" : "Y", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : str(self.object.linearvelocity[1]), "style" : wx.TE_RIGHT, "event" : self.OnLinearVelocityY, "attribs" : None}, ],
        [{"type" : "text", "editable" : False, "value" : "Z", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : str(self.object.linearvelocity[2]), "style" : wx.TE_RIGHT, "event" : self.OnLinearVelocityZ, "attribs" : None}, ],
# Angular Velocity
        [{"type" : "empty"}],
        [{"type" : "text", "editable" : False, "value" : "Angular Velocity", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},],
        [{"type" : "text", "editable" : False, "value" : "X", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : str(self.object.angularvelocity[0]), "style" : wx.TE_RIGHT, "event" : self.OnAngularVelocityX, "attribs" : None}, ],
        [{"type" : "text", "editable" : False, "value" : "Y", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : str(self.object.angularvelocity[1]), "style" : wx.TE_RIGHT, "event" : self.OnAngularVelocityY, "attribs" : None}, ],
        [{"type" : "text", "editable" : False, "value" : "Z", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : str(self.object.angularvelocity[2]), "style" : wx.TE_RIGHT, "event" : self.OnAngularVelocityZ, "attribs" : None}, ],
        ]
        
        self.panel.showObjectAttributes(self.Attributes, "Physic Body")

    def OnGravity(self, event):
        self.object.gravityenabled = event.IsChecked() 

    def OnKinematic(self, event):
        self.object.kinematic = event.IsChecked()
    
    def OnLinearDamping(self, event):
        self.object.lineardamping = float(event.GetClientObject().GetValue())
        
    def OnAngularDamping(self, event):
        self.object.angulardamping = float(event.GetClientObject().GetValue())
        
    def OnMaxAngularDamping(self, event):
        self.object.maxangularvelocity = float(event.GetClientObject().GetValue())

    def OnLinearVelocityX(self, event):
        self.object.linearvelocity.x = float(event.GetClientObject().GetValue())
    def OnLinearVelocityY(self, event):
        self.object.linearvelocity.y = float(event.GetClientObject().GetValue())
    def OnLinearVelocityZ(self, event):
        self.object.linearvelocity.z = float(event.GetClientObject().GetValue())

    def OnAngularVelocityX(self, event):
        self.object.angularvelocity.x = float(event.GetClientObject().GetValue())
    def OnAngularVelocityY(self, event):
        self.object.angularvelocity.y = float(event.GetClientObject().GetValue())
    def OnAngularVelocityZ(self, event):
        self.object.angularvelocity.z = float(event.GetClientObject().GetValue())

        
class PhysicShapeAttributes:
    def __init__(self, panel, object, tree, item):
        self.panel = panel
        self.object = object
        self.tree = tree
        self.item = item
        
        self.Attributes = [
        [
        {"type" : "text", "editable" : False, "value" : "Name", "style" : wx.TE_LEFT | wx.TE_RICH2 , "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : self.object.name, "style" : wx.TE_RIGHT, "event" : self.OnName, "attribs" : None},
        ],
        [
        {"type" : "text", "editable" : False, "value" : "Collision Group", "style" : wx.TE_LEFT | wx.TE_RICH2 , "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : self.object.collisiongroup, "style" : wx.TE_RIGHT, "event" : self.OnCollisionGroup, "attribs" : None},
        ],
        [
        {"type" : "text", "editable" : False, "value" : "Material", "style" : wx.TE_LEFT | wx.TE_RICH2 , "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : self.object.material, "style" : wx.TE_RIGHT, "event" : self.OnMaterial, "attribs" : None},
        ],
        [
        {"type" : "text", "editable" : False, "value" : "Density", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : str(self.object.density), "style" : wx.TE_RIGHT, "event" : self.OnDensity, "attribs" : None},
        ],
        ]
        
        self.panel.showObjectAttributes(self.Attributes, "Physic Shape")

        if self.object.shape.shape == "boxshape":
            type = "Box Shape"
            shapeAttributes = [
            [
            {"type" : "text", "editable" : False, "value" : "X", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
            {"type" : "text", "editable" : True, "value" : str(self.object.shape.height), "style" : wx.TE_RIGHT, "event" : self.OnBoxShapeHight, "attribs" : None},
            ],
            [
            {"type" : "text", "editable" : False, "value" : "Y", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
            {"type" : "text", "editable" : True, "value" : str(self.object.shape.width), "style" : wx.TE_RIGHT, "event" : self.OnBoxShapeWidth, "attribs" : None},
            ],
            [
            {"type" : "text", "editable" : False, "value" : "Z", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
            {"type" : "text", "editable" : True, "value" : str(self.object.shape.depth), "style" : wx.TE_RIGHT, "event" : self.OnBoxShapeDepth, "attribs" : None},
            ],
            ] 
        if self.object.shape.shape == "capsuleshape":
            type = "Capsule Shape"
            shapeAttributes = [
            [
            {"type" : "text", "editable" : False, "value" : "Height", "style" : wx.TE_LEFT | wx.TE_RICH2 , "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
            {"type" : "text", "editable" : True, "value" : str(self.object.shape.height), "style" : wx.TE_RIGHT, "event" : self.OnCapsuleShapeHight, "attribs" : None},
            ],
            [
            {"type" : "text", "editable" : False, "value" : "Radius", "style" : wx.TE_LEFT | wx.TE_RICH2 , "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
            {"type" : "text", "editable" : True, "value" : str(self.object.shape.radius), "style" : wx.TE_RIGHT, "event" : self.OnCapsuleShapeRadius, "attribs" : None},
            ],
            ]
        if self.object.shape.shape == "sphereshape":
            type = "Sphere Shape"
            shapeAttributes = [
            [
            {"type" : "text", "editable" : False, "value" : "Radius", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
            {"type" : "text", "editable" : True, "value" : str(self.object.shape.radius), "style" : wx.TE_RIGHT, "event" : self.OnSphereShapeRadius, "attribs" : None},
            ],
            ]
        if self.object.shape.shape == "convexshape":
            type = "Convex Shape"
            shapeAttributes = [
            [
            {"type" : "text", "editable" : False, "value" : "Mesh", "style" : wx.TE_LEFT | wx.TE_RICH2 , "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
            {"type" : "text", "editable" : True, "value" : self.object.shape.mesh, "style" : wx.TE_RIGHT, "event" : self.OnConvexShapeMesh, "attribs" : None},
            {"type" : "bitmapbutton", "image" : wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_BUTTON), "event" : self.OnConvexShapeMeshButton}, 
            ],
            [{"type" : "empty"}],
            [
            {"type" : "text", "editable" : False, "value" : "Smoothmesh", "style" : wx.TE_LEFT | wx.TE_RICH2 , "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
            {"type" : "checkbox", "editable" : True, "value" : "", "style" : wx.CHK_2STATE , "event" : self.OnConvexShapeSmoothmesh, "attribs" : None}, 
            ],            
            ]
        if self.object.shape.shape == "triangleshape":
            type = "Triangle Shape"
            shapeAttributes = [
            [
            {"type" : "text", "editable" : False, "value" : "Mesh", "style" : wx.TE_LEFT | wx.TE_RICH2 , "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
            {"type" : "text", "editable" : True, "value" : self.object.shape.mesh, "style" : wx.TE_RIGHT, "event" : self.OnTriangleShapeMesh, "attribs" : None},
            {"type" : "bitmapbutton", "image" : wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_BUTTON), "event" : self.OnTriangleShapeMeshButton}, 
            ],
            [{"type" : "empty"}],
            [
            {"type" : "text", "editable" : False, "value" : "Smoothmesh", "style" : wx.TE_LEFT | wx.TE_RICH2 , "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
            {"type" : "checkbox", "editable" : True, "value" : "", "style" : wx.CHK_2STATE , "event" : self.OnTriangleShapeSmoothmesh, "attribs" : None}, 
            ],            
            ]
        
        self.panel.showObjectAttributes(shapeAttributes, type)
        
        localposeAttributes = [
# Node        
        [
        {"type" : "text", "editable" : False, "value" : "Node - Transform Object", "style" : wx.TE_LEFT | wx.TE_RICH2 , "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : self.object.shape.localpose.node, "style" : wx.TE_RIGHT, "event" : self.OnLocalposeNode, "attribs" : None},
        ],
# Position
        [{"type" : "text", "editable" : False, "value" : "Position", "style" : wx.TE_LEFT | wx.TE_RICH2 , "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},],
        [{"type" : "text", "editable" : False, "value" : "X", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : str(self.object.shape.localpose.position.x), "style" : wx.TE_RIGHT, "event" : self.OnLocalposePositionX, "attribs" : None}, ],
        [{"type" : "text", "editable" : False, "value" : "Y", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : str(self.object.shape.localpose.position.y), "style" : wx.TE_RIGHT, "event" : self.OnLocalposePositionY, "attribs" : None}, ],
        [{"type" : "text", "editable" : False, "value" : "Z", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : str(self.object.shape.localpose.position.z), "style" : wx.TE_RIGHT, "event" : self.OnLocalposePositionZ, "attribs" : None}, ],
# Roation
        [{"type" : "empty"}],
        [{"type" : "text", "editable" : False, "value" : "Rotation", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},],
        [{"type" : "text", "editable" : False, "value" : "X", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : str(self.object.shape.localpose.rotation.x), "style" : wx.TE_RIGHT, "event" : self.OnLocalposeRotationX, "attribs" : None}, ],
        [{"type" : "text", "editable" : False, "value" : "Y", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : str(self.object.shape.localpose.rotation.y), "style" : wx.TE_RIGHT, "event" : self.OnLocalposeRotationY, "attribs" : None}, ],
        [{"type" : "text", "editable" : False, "value" : "Z", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : str(self.object.shape.localpose.rotation.z), "style" : wx.TE_RIGHT, "event" : self.OnLocalposeRotationZ, "attribs" : None}, ],
        ]

        self.panel.showObjectAttributes(localposeAttributes, "Local Position")

#Main Shape Object
    def OnName(self, event):
        self.object.name = event.GetClientObject().GetValue()
        
    def OnCollisionGroup(self, event):
        self.object.collisiongroup = event.GetClientObject().GetValue()
    
    def OnMaterial(self, event):
        self.object.material = event.GetClientObject().GetValue()
        
    def OnDensity(self, event):
        self.object.density = float(event.GetClientObject().GetValue())

# Box shape
    def OnBoxShapeHight(self, event):
        self.object.shape.height = float(event.GetClientObject().GetValue())
    def OnBoxShapeWidth(self, event):
        self.object.shape.width = float(event.GetClientObject().GetValue())
    def OnBoxShapeDepth(self, event):
        self.object.shape.depth = float(event.GetClientObject().GetValue())
        
# Capsule shape
    def OnCapsuleShapeHight(self, event):
        self.object.shape.height = float(event.GetClientObject().GetValue())
    def OnCapsuleShapeRadius(self, event):
        self.object.shape.radius = float(event.GetClientObject().GetValue())
        
# Sphere shape
    def OnSphereShapeRadius(self, event):
        self.object.shape.radius = float(event.GetClientObject().GetValue())
        
# Convex shape
    def OnConvexShapeMesh(self, event):
        self.object.shape.mesh = event.GetClientObject().GetValue()
    def OnConvexShapeMeshButton(self, event):
        fdg = wx.FileDialog(self.panel, message = "Choose Mesh File", style=wx.OPEN, wildcard = "*.mesh")
        if fdg.ShowModal() == wx.ID_OK:
            self.object.shape.mesh = fdg.GetFilename()
        fdg.Destroy()
        self.panel.update()
    def OnConvexShapeSmoothmesh(self, event):
        self.object.shape.smoothmesh = event.IsChecked()
        
# Triangle shape
    def OnTriangleShapeMesh(self, event):
        self.object.shape.mesh = event.GetClientObject().GetValue()
    def OnTriangleShapeMeshButton(self, event):
        fdg = wx.FileDialog(self.panel, message = "Choose Mesh File", style=wx.OPEN, wildcard = "*.mesh")
        if fdg.ShowModal() == wx.ID_OK:
            self.object.shape.mesh = fdg.GetFilename()
        fdg.Destroy()
        self.panel.update()
    def OnTriangleShapeSmoothmesh(self, event):
        self.object.shape.smoothmesh = event.IsChecked()


# Localpose
    def OnLocalposeNode(self, event):
        self.object.shape.localpose.node = event.GetClientObject().GetValue()
    
    def OnLocalposePositionX(self, event):
        self.object.shape.localpose.position.x = float(event.GetClientObject().GetValue())
    def OnLocalposePositionY(self, event):
        self.object.shape.localpose.position.y = float(event.GetClientObject().GetValue())
    def OnLocalposePositionZ(self, event):
        self.object.shape.localpose.position.z = float(event.GetClientObject().GetValue())

    def OnLocalposeRotationX(self, event):
        self.object.shape.localpose.rotation.x = float(event.GetClientObject().GetValue())
    def OnLocalposeRotationY(self, event):
        self.object.shape.localpose.rotation.y = float(event.GetClientObject().GetValue())
    def OnLocalposeRotationZ(self, event):
        self.object.shape.localpose.rotation.z = float(event.GetClientObject().GetValue()) 
    
    
class FreeCameraAttributes:
    def __init__(self, panel, object, tree, item):
        self.panel = panel
        self.object = object
        self.tree = tree
        self.item = item
        self.Attributes = [
        [
        {"type" : "text", "editable" : False, "value" : "Sensitivity", "style" : wx.TE_LEFT | wx.TE_RICH2 , "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : str(self.object.sensitivity), "style" : wx.TE_RIGHT, "event" : self.OnSensitivity, "attribs" : None},
        ],
        [
        {"type" : "text", "editable" : False, "value" : "Speed", "style" : wx.TE_LEFT | wx.TE_RICH2 , "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : str(self.object.speed), "style" : wx.TE_RIGHT, "event" : self.OnSpeed, "attribs" : None},
        ],
        ]
        
        self.panel.showObjectAttributes(self.Attributes, "Free Camera")

    def OnSensitivity(self, event):
        self.object.sensitivity = float(event.GetClientObject().GetValue())

    def OnSpeed(self, event):
        self.object.speed = float(event.GetClientObject().GetValue())
        
class FollowCameraAttributes:
    def __init__(self, panel, object, tree, item):
        self.panel = panel
        self.object = object
        self.tree = tree
        self.item = item
        
        self.Attributes = [
        [
        {"type" : "comment", "editable" : True, "label" : "* No other settings than parent node can be set"}, 
        ]
        ]
        
        self.panel.showObjectAttributes(self.Attributes, "Follow Camera")
        

class ControlAttributes:
    def __init__(self, panel, object, tree, item):
        self.panel = panel
        self.object = object
        self.tree = tree
        self.item = item
        self.Attributes = [
        [
        {"type" : "text", "editable" : False, "value" : "Type", "style" : wx.TE_LEFT | wx.TE_RICH2 , "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : self.object.etype, "style" : wx.TE_RIGHT, "event" : self.OnType, "attribs" : None},
        ],
        [
        {"type" : "text", "editable" : False, "value" : "Movementspeed", "style" : wx.TE_LEFT | wx.TE_RICH2 , "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : str(self.object.movementspeed), "style" : wx.TE_RIGHT, "event" : self.OnMovementspeed, "attribs" : None},
        ],
        [
        {"type" : "text", "editable" : False, "value" : "Trunspeed", "style" : wx.TE_LEFT | wx.TE_RICH2 , "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : str(self.object.turnspeed), "style" : wx.TE_RIGHT, "event" : self.OnTurnspeed, "attribs" : None},
        ],
        ]
        
        self.panel.showObjectAttributes(self.Attributes, "Control")

    def OnType(self, event):
        self.object.etype = str(event.GetClientObject().GetValue())
    
    def OnMovementspeed(self, event):
        self.object.movementspeed = int(event.GetClientObject().GetValue())
    
    def OnTurnspeed(self, event):
        self.object.turnspeed = int(event.GetClientObject().GetValue())

class AiAttributes:
    def __init__(self, panel, object, tree, item):
        self.panel = panel
        self.object = object
        self.tree = tree
        self.item = item
        self.Attributes = [
        [
        {"type" : "text", "editable" : False, "value" : "Startstate", "style" : wx.TE_LEFT | wx.TE_RICH2 , "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : self.object.startstate, "style" : wx.TE_RIGHT, "event" : self.OnStartstate, "attribs" : None},
        ],
        ]
        
        self.panel.showObjectAttributes(self.Attributes, "Ai")

    def OnStartstate(self, event):
        self.object.startstate = str(event.GetClientObject().GetValue())

class LightAttributes:
    def __init__(self, panel, object, tree, item):
        self.panel = panel
        self.object = object
        self.tree = tree
        self.item = item
        self.Attributes = [
#Light Name
        [{"type" : "text", "editable" : False, "value" : "Name", "style" : wx.TE_LEFT | wx.TE_RICH2 , "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : self.object.name, "style" : wx.TE_RIGHT, "event" : self.OnLightName, "attribs" : None},],

# Light Type 
        #[{"type" : "text", "editable" : False, "value" : "Animation states", "style" : wx.TE_LEFT | wx.TE_RICH2 | wx.NO_BORDER, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        #{"type" : "combobox", "editable" : True, "value" : self.AnimationList, "style" : wx.CB_READONLY | wx.CB_SORT, "event" : self.OnSetAnimation, "attribs" : None}, ],
# Diffuse        
        [{"type" : "text", "editable" : False, "value" : "Diffuse", "style" : wx.TE_LEFT | wx.TE_RICH2 , "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},],
        [{"type" : "text", "editable" : False, "value" : "R", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : str(self.object.diffuse.x), "style" : wx.TE_RIGHT, "event" : self.OnDiffuseX, "attribs" : None}, ],
        [{"type" : "text", "editable" : False, "value" : "G", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : str(self.object.diffuse.y), "style" : wx.TE_RIGHT, "event" : self.OnDiffuseY, "attribs" : None}, ],
        [{"type" : "text", "editable" : False, "value" : "B", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : str(self.object.diffuse.z), "style" : wx.TE_RIGHT, "event" : self.OnDiffuseZ, "attribs" : None}, ],
# Specular        
        [{"type" : "text", "editable" : False, "value" : "Specular", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},],
        [{"type" : "text", "editable" : False, "value" : "R", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : str(self.object.specular.x), "style" : wx.TE_RIGHT, "event" : self.OnSpecularX, "attribs" : None}, ],
        [{"type" : "text", "editable" : False, "value" : "G", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : str(self.object.specular.y), "style" : wx.TE_RIGHT, "event" : self.OnSpecularY, "attribs" : None}, ],
        [{"type" : "text", "editable" : False, "value" : "B", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : str(self.object.specular.z), "style" : wx.TE_RIGHT, "event" : self.OnSpecularZ, "attribs" : None}, ],
# Direction        
        [{"type" : "text", "editable" : False, "value" : "Direction", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},],
        [{"type" : "text", "editable" : False, "value" : "X", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : str(self.object.direction.x), "style" : wx.TE_RIGHT, "event" : self.OnDirectionX, "attribs" : None}, ],
        [{"type" : "text", "editable" : False, "value" : "Y", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : str(self.object.direction.y), "style" : wx.TE_RIGHT, "event" : self.OnDirectionY, "attribs" : None}, ],
        [{"type" : "text", "editable" : False, "value" : "Z", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : str(self.object.direction.z), "style" : wx.TE_RIGHT, "event" : self.OnDirectionZ, "attribs" : None}, ],
        
        [{"type" : "text", "editable" : False, "value" : "Power Scale", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : str(self.object.powerScale), "style" : wx.TE_RIGHT, "event" : self.OnPowerScale, "attribs" : None},],
        [{"type" : "text", "editable" : False, "value" : "Range", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : str(self.object.range), "style" : wx.TE_RIGHT, "event" : self.OnRange, "attribs" : None},],
        ]
        
        self.panel.showObjectAttributes(self.Attributes, "Light - " + self.object.lighttype)
        
        if self.object.lighttype == "spotlight":
            SpotPanel = [
            [{"type" : "text", "editable" : False, "value" : "Inner Angle", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
            {"type" : "text", "editable" : True, "value" : str(self.object.innerAngle), "style" : wx.TE_RIGHT, "event" : self.OnInnerAngle, "attribs" : None},],
            [{"type" : "text", "editable" : False, "value" : "Outer Angle", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
            {"type" : "text", "editable" : True, "value" : str(self.object.outerAngle), "style" : wx.TE_RIGHT, "event" : self.OnOuterAngle, "attribs" : None},],
            [{"type" : "text", "editable" : False, "value" : "Falloff", "style" : wx.TE_LEFT | wx.TE_RICH2, "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
            {"type" : "text", "editable" : True, "value" : str(self.object.falloff), "style" : wx.TE_RIGHT, "event" : self.OnFalloff, "attribs" : None},],
            ]
            self.panel.showObjectAttributes(SpotPanel, "Spotlight Extra")

    
    def OnLightName(self, event):
        self.object.name = event.GetClientObject().GetValue()
        self.tree.SetItemText(self.item, self.object.name + " - Light Object")

    def OnDiffuseX(self, event):
        self.object.diffuse.x = float(event.GetClientObject().GetValue())
        self.update()
    def OnDiffuseY(self, event):
        self.object.diffuse.y = float(event.GetClientObject().GetValue())
        self.update()
    def OnDiffuseZ(self, event):
        self.object.diffuse.z = float(event.GetClientObject().GetValue())
        self.update()
         
    def OnSpecularX(self, event):
        self.object.specular.x = float(event.GetClientObject().GetValue())
        self.update()
    def OnSpecularY(self, event):
        self.object.specular.y = float(event.GetClientObject().GetValue())
        self.update()
    def OnSpecularZ(self, event):
        self.object.specular.z = float(event.GetClientObject().GetValue())
        self.update()
    
    def OnDirectionX(self, event):
        self.object.direction.x = float(event.GetClientObject().GetValue())
        self.update()
    def OnDirectionY(self, event):
        self.object.direction.y = float(event.GetClientObject().GetValue())
        self.update()
    def OnDirectionZ(self, event):
        self.object.direction.z = float(event.GetClientObject().GetValue())
        self.update()
    
    def OnPowerScale(self, event):
        self.object.powerScale = float(event.GetClientObject().GetValue())
        self.update()
    
    def OnInnerAngle(self, event):
        self.object.innerAngle = int(event.GetClientObject().GetValue())
        self.update()
    
    def OnOuterAngle(self, event):
        self.object.outerAngle = int(event.GetClientObject().GetValue())
        self.update()

    def OnFalloff(self, event):
        self.object.falloff = float(event.GetClientObject().GetValue())
        self.update()

    def OnRange(self, event):
        self.object.range = float(event.GetClientObject().GetValue())
        self.update()
    
    def update(self):
        self.tree.updatePreview()

class PhysicControllerAttributes:
    def __init__(self, panel, object, tree, item):
        self.panel = panel
        self.object = object
        self.tree = tree
        self.item = item

        self.Attributes = [
        [
        {"type" : "text", "editable" : False, "value" : "Slopelimit", "style" : wx.TE_LEFT | wx.TE_RICH2 , "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : str(self.object.slopelimit), "style" : wx.TE_RIGHT, "event" : self.OnSlopelimit, "attribs" : None},
        ],
        [
        {"type" : "text", "editable" : False, "value" : "Steplimit", "style" : wx.TE_LEFT | wx.TE_RICH2 , "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : str(self.object.steplimit), "style" : wx.TE_RIGHT, "event" : self.OnSteplimit, "attribs" : None},
        ],
        ]
        
        self.panel.showObjectAttributes(self.Attributes, "Physic Controller")

    def OnSlopelimit(self, event):
        self.object.sloplimit = float(event.GetClientObject().GetValue())

    def OnSteplimit(self, event):
        self.object.steplimit = float(event.GetClientObject().GetValue())

class PhysicControllerShapeSphereAttributes:
    def __init__(self, panel, object, tree, item):
        self.panel = panel
        self.object = object
        self.tree = tree
        self.item = item

        self.Attributes = [
        [
        {"type" : "text", "editable" : False, "value" : "Height", "style" : wx.TE_LEFT | wx.TE_RICH2 , "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : str(self.object.height), "style" : wx.TE_RIGHT, "event" : self.OnHeight, "attribs" : None},
        ],
        [
        {"type" : "text", "editable" : False, "value" : "Radius", "style" : wx.TE_LEFT | wx.TE_RICH2 , "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : str(self.object.radius), "style" : wx.TE_RIGHT, "event" : self.OnRadius, "attribs" : None},
        ],
        ]
        
        self.panel.showObjectAttributes(self.Attributes, "Capsule Shape")

    def OnHeight(self, event):
        self.object.height = float(event.GetClientObject().GetValue())

    def OnRadius(self, event):
        self.object.radius = float(event.GetClientObject().GetValue())

class Comments:
    def __init__(self, panel, object, tree, item):
        self.panel = panel
        self.object = object
        self.tree = tree
        self.item = item
        
        self.Attributes = [
        [
        {"type" : "textctrl", "editable" : True, "value" : self.object.comments, "style" : wx.TE_MULTILINE, "event" : self.OnComment, "attribs" : None, "height" : 100},
        ]
        ]
        
        self.panel.showObjectAttributes(self.Attributes, "Coments")
    
    def OnComment(self, event):
        self.object.comments = event.GetClientObject().GetValue()

class AudioSourceAttributes:
    def __init__(self, panel, object, tree, item):
        self.panel = panel
        self.object = object
        self.tree = tree
        self.item = item

        self.Attributes = [
        [
        {"type" : "text", "editable" : False, "value" : "Name", "style" : wx.TE_LEFT | wx.TE_RICH2 , "return" : None, "event" : None, "attribs" : wx.TextAttr(alignment = wx.TEXT_ALIGNMENT_RIGHT)},
        {"type" : "text", "editable" : True, "value" : str(self.object.name), "style" : wx.TE_RIGHT, "event" : self.OnName, "attribs" : None},
        ],
        ]
        
        self.panel.showObjectAttributes(self.Attributes, "Audio Source")

    def OnName(self, event):
        self.object.name = event.GetClientObject().GetValue()