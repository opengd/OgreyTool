import wx

class ogreyControlPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
    
class OrientationControl:
    def __init__(self, Entity):
        pass

class AnimationControl:
    def __init__(self, Entity):
        wx.StaticBox(self.objectAttribs, -1, "Animation", size= (193,150), pos= (0,160))
        self.animBox = wx.ComboBox(self.objectAttribs, -1, pos=(10,180), size=(150, -1), choices=[], style=wx.CB_READONLY)
        #wx.EVT_COMBOBOX(self,300, self.PlayAnim)
        
        self.playButton = wx.Button(self.objectAttribs, 401, "Play", pos=(10,220))
        self.parent.Bind(wx.EVT_BUTTON, self.PlayAnim,id=401)
        self.stopButton = wx.Button(self.objectAttribs, 402, "Stop", pos=(100,220))
        self.parent.Bind(wx.EVT_BUTTON, self.StopAnim,id=402)
        
        wx.StaticText(self.objectAttribs,-1, "Animation speed", pos = (10,250))
        self.speedSlider = wx.Slider(self.objectAttribs,id=403,pos=(10,270), size = (150, -1), style = wx.SL_HORIZONTAL)
        self.speedSlider.SetRange(0,100)
        self.speedSlider.SetValue(50)
        self.parent.Bind(wx.EVT_SLIDER, self.ChangeSpeed, id = 403)
        