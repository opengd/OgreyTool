import wx

class PopupMenu(wx.Menu):
    def __init__(self):
        wx.Menu.__init__(self)
        self.home = self
        
    def AddMenuItems(self, items, parentMenu = None, home = None):
        if not parentMenu == None:
            self = wx.Menu()
        if not home == None:
            self.home = home
        for menuItem in items:
            if menuItem["enabled"] == True:
                if menuItem["menuItem"] == "Submenu":
                    subMenu = self.home.AddMenuItems(menuItem["items"], self, self.home)
                    self.AppendMenu(id = -1, text=menuItem["name"], submenu = subMenu)                
                elif menuItem["menuItem"] == "Seperator": 
                    self.AppendSeparator()
                else: #  menuItem["menuItem"] == "Seperator":
                    self.AppendItem(item = menuItem["menuItem"])
                    if not menuItem["event"] == False:
                        self.home.Bind(wx.EVT_MENU, menuItem["event"], id =menuItem["menuItem"].GetId())
        return self
    
    def FlushMenu(self):
        items = self.GetMenuItems()
        for i in items:
            self.Remove(i.GetId())