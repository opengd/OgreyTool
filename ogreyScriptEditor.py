import wx

class ScriptEditor(wx.SplitterWindow):
    def __init__(self, parent):
        wx.SplitterWindow.__init__(self, parent)
        self.parent = parent
        self.text = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE)
        self.menuBar = wx.Panel(self, -1, size=(-1, 20))
        self.saveButton = wx.Button(self.menuBar, -1, "Save")
        self.saveButton.Bind(wx.EVT_BUTTON, self.Save)
        self.SplitHorizontally(self.menuBar,  self.text, 1)
        self.SetSashGravity(0.0)
        self.SetSashPosition(25, True)
        self.text.CanCopy()
        self.text.CanCut()
        self.text.CanPaste()
        self.text.CanRedo()
        self.text.CanUndo()
        self.file = None
        
    def Load(self, file):
        self.text.LoadFile(file)
        self.file = file
    
    def Save(self,event):
        self.text.SaveFile(self.file)