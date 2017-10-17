import wx

class ErrorDialog(wx.MiniFrame):
    def __init__(self, parent, name, errors):
        wx.MiniFrame.__init__(self, parent, -1, name)
        self.errorbox = wx.TextCtrl(self, -1)
        for e in errors:
            self.errorbox.AppendText(e)
            
        self.Show()