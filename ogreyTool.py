import wx
import wx.gizmos
import wx.lib
from wx.lib.scrolledpanel import *
import sys
import wxogre
from FlatNotebook import *
import ogre.renderer.OGRE as ogre
#from imagebrowser import *
import Image

import time
#import FreeImagePy as FIPY

from ogreyEntity import *
from ogreyLevel import *
from ogreyEntityTree import *
from ogreyAttributesPanel import *
from ogreyLevelAttributesPanel import *
from ogreyExportEntity import *
from ogreyImportEntity import *
from ogreyOptionsPanel import *
from ogreyScriptEditor import *
from ogreyLevelTree import *
from ogreyConfig import *
from ogreyMaterialTool import *
from ogreyOgreManagers import *
from ogreySingleton import *

class OgreManager:
    __metaclass__=Singleton
    def __init__(self):
        self.ogreMgr = wxOgreConfig().ogreMgr
        self.ogreMgr.initWindow()
    
    def getOgreManager(self):
        return self.ogreMgr

    def reloadResourses(self):
        if not self.ogreMgr.shouldInitResources:
            ogre.GpuProgramManager.getSingleton().removeAll()
            #ogre.CompositorManager.getSingleton().removeAll()
            ogre.TextureManager.getSingleton().removeAll()
            
            dict = []
            scripts = {}
            for value in self.resourceInformation.materialsOrigin:
                    ogre.MaterialManager.getSingleton().unload(value["name"])
                    ogre.MaterialManager.getSingleton().remove(value["name"])
            tempDic = {}
            for value in self.resourceInformation.materialsOrigin:
                tempDic[value["origin"]] = value
            
            for (key, value) in tempDic.iteritems():
                stream = ogre.ResourceGroupManager.getSingleton().openResource(key)
                if not ogre.MaterialManager.getSingleton().resourceExists(value["name"]) == True:
                    ogre.MaterialManager.getSingleton().parseScript(stream.getAsString(), value["group"])

            for value in self.resourceInformation.materialsOrigin:
                mat = ogre.MaterialPointer(ogre.MaterialManager.getSingleton().getByName(value["name"]))
                mat.compile(True)

            ogre.MeshManager.getSingleton().reloadAll()

class ProjectManager(FlatNotebook): #
    #__metaclass__=Singleton
    def __init__(self, parent):
        FlatNotebook.__init__(self, parent, style = wx.NB_TOP)
        self.parent = parent
        
        self.LevelProjects = []
        self.EntityProjects = []
        
        #self.ogreMgr = wxOgreConfig().ogreMgr
        #self.ogreMgr.initWindow()
        self.ogreMgr = OgreManager().ogreMgr
        self.configManager = ConfigManager()
        self.configManager.Load()
        
        self.shallInitResourceInforamtion = True
    
    def getOgreManager(self):
        return self.ogreMgr
    
    def getResourceInformation(self):
        return self.resourceInformation

    def createOgreyEntityManager(self):
        if self.shallInitResourceInforamtion: self.initResourceInformation()
        ogm = OgreyEntityManager(self, self.ogreMgr, self.statusbar, self.resourceInformation, self.configManager)
        self.EntityProjects.append(ogm)
        self.AddPage(ogm, "Entity Manager " + str(len(self.EntityProjects)))
        self.resourceInformation.reload()

    def createOgreyLevelProject(self):
        if self.shallInitResourceInforamtion: self.initResourceInformation()
        ogm = OgreyLevelProject(self, self.ogreMgr, self.statusbar, self.resourceInformation, self.configManager)
        self.LevelProjects.append(ogm)
        self.AddPage(ogm, "Level Project " + str(len(self.LevelProjects)))
        self.resourceInformation.reload()
        
    def initResourceInformation(self):
        self.resourceInformation = ResourceInformation()
        
        self.shallInitResourceInforamtion = False
            
    def createLevelProject(self):
        pass 
    
    def setStatusBar(self, statusbar):
        self.statusbar = statusbar

    def reloadResourses(self):
        
        if self.shallInitResourceInforamtion: self.initResourceInformation()
        
        if not self.ogreMgr.shouldInitResources:
            ogre.GpuProgramManager.getSingleton().removeAll()
            #ogre.CompositorManager.getSingleton().removeAll()
            ogre.TextureManager.getSingleton().removeAll()
            
            dict = []
            scripts = {}
            for value in self.resourceInformation.materialsOrigin:
                    ogre.MaterialManager.getSingleton().unload(value["name"])
                    ogre.MaterialManager.getSingleton().remove(value["name"])
            tempDic = {}
            for value in self.resourceInformation.materialsOrigin:
                tempDic[value["origin"]] = value
            
            for (key, value) in tempDic.iteritems():
                stream = ogre.ResourceGroupManager.getSingleton().openResource(key)
                if not ogre.MaterialManager.getSingleton().resourceExists(value["name"]) == True:
                    ogre.MaterialManager.getSingleton().parseScript(stream.getAsString(), value["group"])

            for value in self.resourceInformation.materialsOrigin:
                mat = ogre.MaterialPointer(ogre.MaterialManager.getSingleton().getByName(value["name"]))
                mat.compile(True)

            ogre.MeshManager.getSingleton().reloadAll()
            
            self.updateProjects()
    
    def updateProjects(self):
        for project in self.EntityProjects:
            project.reload()
        
        for project in self.LevelProjects:
            project.reload()

class BottomNotebook(FlatNotebook):
    def __init__(self, parent):
        FlatNotebook.__init__(self, parent, style = wx.NB_BOTTOM)

class LeftNotebook(wx.Notebook):
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent, style = wx.NB_TOP)

class TopNotebook(FlatNotebook):
    def __init__(self, parent):
        FlatNotebook.__init__(self, parent, style = wx.NB_TOP)

class MiddleNotebook(FlatNotebook):
    def __init__(self, parent):
        FlatNotebook.__init__(self, parent, style = wx.NB_TOP)
        
        #self.option = option
        self.Bind(EVT_FLATNOTEBOOK_PAGE_CHANGED, self.OnChange)
    
    def OnChange(self, event):
        try:
            self.window.bindView(self.GetPage(self.GetSelection()))
        except:
            pass
        
    def bindWindow(self, window):
        self.window = window

class RightNotebook(wx.Notebook):#(FlatNotebook):
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent, style = wx.NB_TOP)
        self.Bind(EVT_FLATNOTEBOOK_PAGE_CHANGED, self.OnSelect)
    
    def OnSelect(self, event):
        if not self.GetSelection() == -1:
            self.GetPage(self.GetPreviousSelection()).select(False)
            self.GetPage(self.GetSelection()).select(True)
            #self.Update()
        
class wxOgreConfig:        
    def __init__(self):
        self.ogreMgr = wxogre.OgreManager()

class NameFactory:
    __metaclass__=Singleton
    def __init__(self):
        self.Name = 0
    
    def getName(self):
        self.Name += 1
        return str(self.Name)

class Menu(wx.Menu):
    def __init__(self):
        wx.Menu.__init__(self)
    
    def AddMenuItems(self, items, parentMenu = None):
        if parentMenu == None:
            parentMenu = self
        else: self = wx.Menu()
        for menuItem in items:
            if menuItem["enabled"] == True:
                
                if menuItem["menuItem"] == "Submenu":
                    subMenu = parentMenu.AddMenuItems(menuItem["items"], self)
                    self.AppendMenu(id = -1, text=menuItem["name"], submenu = subMenu)
                
                elif not menuItem["menuItem"] == "Seperator":
                    self.AppendItem(item = menuItem["menuItem"])
                    if not menuItem["event"] == False:
                        parentMenu.Bind(wx.EVT_MENU, menuItem["event"], id =menuItem["menuItem"].GetId())
                
                elif menuItem["menuItem"] == "Seperator": 
                    self.AppendSeparator()
        return self
    
    def FlushMenu(self):
        items = self.GetMenuItems()
        for i in items:
            self.Remove(i.GetId())

class TextureBrowser(wx.lib.scrolledpanel.ScrolledPanel):
    def __init__(self, parent, file):
        wx.lib.scrolledpanel.ScrolledPanel.__init__(self, parent, style = wx.HSCROLL | wx.VSCROLL)        
        #try:
            #jpg1 = wx.Image(file, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        self.SetupScrolling()
        self.EnableScrolling(True, True)
        self.SetScrollbars(20, 20, 50, 50)

        
        img = Image.open(file)
        #ld = FIPY.freeimage()
        #img = FIPY.genericLoader(file)
        #img = FIPY.Image(file)
        #img.load(file)
        #del img
        #pilimg = FIPY.convertToPil(img)
        #jpg1 = jpg1.convert('RGB').tostring()
        #jpg1 = wx.EmptyImage(img.getSize().getWidth(), img.getSize().getHeight())
        #jpg1.SetData(img.convertToWx())
        #jpg1 = img.convertToWx()
        jpg1 = wx.EmptyImage(img.size[0], img.size[1])
        jpg1.SetData(img.convert('RGB').tostring())
        #jpg1 = wx.Image(img.convert('RGB').tostring() , wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        #jpg1 = wx.BitmapFromImage(wx.ImageFromStream(stream))
        stb = wx.StaticBitmap(self, -1, pos=(5, 5), size = (jpg1.GetWidth(), jpg1.GetHeight()))
        #stb.SetBitmap(jpg1.ConvertToBitmap())
        stb.SetBitmap(jpg1.ConvertToBitmap())
        #except:
        #    pass
            
class LogList(wx.TextCtrl):
    def __init__(self, parent):
        wx.TextCtrl.__init__(self, parent, -1, "", style=wx.TE_MULTILINE)
        sys.stdout = self
        sys.stderr = self

class MenuFile(wx.Menu):
    def __init__(self, parent, projectManager, name):
        wx.Menu.__init__(self)
        self.parent = parent
        self.projectManager = projectManager
        self.name = name
        self.enabled = True
        
        
        #level = self.Append(-1, "&New Level Project", "Create a new Level")
        entity = self.Append(-1, "&New Entity Manager", "Create a new Entity Manager Window Instance")
        self.AppendSeparator()
        exit = self.Append(-1, "&Exit", "Exit Ogrey")
        
        #wx.EVT_MENU(self.parent, level.GetId(), self.OnLevel)
        wx.EVT_MENU(self.parent, entity.GetId(), self.OnEntity)
        wx.EVT_MENU(self.parent, exit.GetId(), self.OnExit)
    
    def OnLevel(self, event):
        self.projectManager.createOgreyLevelProject()
    
    def OnEntity(self, event):
        self.projectManager.createOgreyEntityManager()
    
    def OnExit(self, event):
        wx.Exit()

class MenuRender(wx.Menu):
    def __init__(self, parent, window, name, ogreScene, tabs):
        wx.Menu.__init__(self)
        self.parent = parent
        self.window = window
        self.name = name
        self.tabs = tabs
        self.ogreScene = ogreScene
        #solid = self.Append(-1 ,"Solid", "Solid models",kind=wx.ITEM_RADIO )
        #wire = self.Append(-1, "Wireframe", "Wireframe models",kind=wx.ITEM_RADIO)
        #points = self.Append(-1, "Points", "Points modelse",kind=wx.ITEM_RADIO)
        getView = self.Append(-1, "Get Ogre View", "Get a OGre View")
        reload = self.Append(-1, "Reload", "Reload materials")
        #rendertarget = self.Append(-1, "Rendertarget")
        #self.AppendSeparator()
        #menuRenderShadows = wx.Menu()
        #menuRenderShadows.Append(184, "On", "Shadows On", kind=wx.ITEM_RADIO)
        #menuRenderShadows.Append(185, "Off", "Shadows Off", kind=wx.ITEM_RADIO)
        #shadows = self.Append(-1, "Shadows...", "Shadows attributes")
    
        #wx.EVT_MENU(self.parent, solid.GetId(), self.renderModeSolid)
        #wx.EVT_MENU(self.parent, wire.GetId(), self.renderModeWireframes)
        #wx.EVT_MENU(self.parent, points.GetId(), self.renderModePoints)
        wx.EVT_MENU(self.parent, getView.GetId(), self.OnGetView)
        wx.EVT_MENU(self.parent, reload.GetId(), self.OnReload)
        #wx.EVT_MENU(self.parent, shadows.GetId(), self.renderShadows)
        #wx.EVT_MENU(self.parent, rendertarget.GetId(), self.renderTarget)

    #def renderTarget(self, event):
    #    self.window.renderWindow.active = False
    
    def OnGetView(self, event):
        self.tabs.AddPage(self.ogreScene.getView(), "Entity Viewpoint")
        
    def bind(self, window):
        self.window = window
    
    def renderModeSolid(self, event):
        self.window.renderModeSolid()
    
    def renderModeWireframes(self, event):
        self.window.renderModeWireframe()
    
    def renderModePoints(self, event):
        self.window.renderModePoints()
    
    #def renderShadows(self, event):
    #    shadowAttribDialog = ShadowsDialog(self.parent, self.window)
        #returnCode = shadowAttribDialog.ShowModal()
        #shadowAttribDialog.Destroy()

class MenuBrowse(wx.Menu):
    def __init__(self, parent, window, name):
        wx.Menu.__init__(self)
        self.parent = parent
        self.window = window
        self.name = name
        openScript = self.Append(-1 ,"Open Script File...", "Open File to Edit")
        openTexture = self.Append(-1, "Open Texture...", "Open Texture")
        wx.EVT_MENU(self.parent, openScript.GetId(), self.OnOpenScript)
        wx.EVT_MENU(self.parent, openTexture.GetId(), self.OnOpenTexture)

    
    def OnOpenScript(self, event):
        fdg = wx.FileDialog(self.parent, message = "Choose File", style=wx.OPEN, wildcard = "*.*")
        if fdg.ShowModal() == wx.ID_OK:
            scrip = ScriptEditor(self.window)
            scrip.Load(fdg.GetPath())
            self.window.AddPage(scrip, fdg.GetFilename())
        fdg.Destroy()
    
    def OnSave(self, event):
        pass
    
    def OnOpenTexture(self, event):
        fdg = wx.FileDialog(self.parent, message = "Choose File", style=wx.OPEN, wildcard = "*.*")
        if fdg.ShowModal() == wx.ID_OK:
            #scrip.Load(fdg.GetPath())
            self.window.AddPage(TextureBrowser(self.window, fdg.GetPath()), fdg.GetFilename())
        fdg.Destroy()

class MenuHelp(wx.Menu):
    def __init__(self, parent, window):
        wx.Menu.__init__(self)
        self.parent = parent
        self.name = "&Help"
        self.enabled = True
        
        about = self.Append(-1 ,"About", "About Ogrey Tool")
        
        wx.EVT_MENU(self.parent, about.GetId(), self.OnAbout)
    
    def OnAbout(self, event):
        adlg = wx.AboutDialogInfo()
        adlg.SetName("Ogrey")
        adlg.SetVersion("Beta 1")
        adlg.SetDevelopers(["Erik Johansson ejevik@hotmail.com"])
        adlg.SetCopyright("GPL")
        adlg.SetDescription("Ogrey Monster Engine Entity Tool")
        adlg.SetWebSite("http://www.opengd.org") 
        wx.AboutBox(adlg)

class MenuWindow(wx.Menu):
    def __init__(self, parent, window):
        wx.Menu.__init__(self)
        self.parent = parent
        self.name = "&Window"
        self.enabled = True

class MenuEntityManager(wx.Menu):
    def __init__(self, parent, window):
        wx.Menu.__init__(self)
        self.parent = parent
        self.name = "&Entity Manager"
        self.enabled = False

class MenuEdit(wx.Menu):
    def __init__(self, parent, window):
        wx.Menu.__init__(self)
        self.parent = parent
        self.name = "&Edit"
        self.enabled = False
        self.window = window
        reload = self.Append(-1, "Reload", "Reload materials")
        wx.EVT_MENU(self.parent, reload.GetId(), self.OnReload)

    def OnReload(self, event):
        self.window.reloadResourses()
        
class OgreyStatusBar(wx.StatusBar):
    def __init__(self, parent):
        wx.StatusBar.__init__(self,parent)
        self.SetFieldsCount(2)
        self.SetStatusWidths([-5, -2])
        self.SetStatusText("Welcome to Ogrey Entity Tool",0)
        
        
class MainOgreyEntityToolFrame(wx.Frame):
    def __init__(self, *args, **kw):
        wx.Frame.__init__(self, *args, **kw)
        
        config = ConfigManager()
        config.Load()
        

        
        self.projectManager = ProjectManager(self)
        #ogreyMaterialTool(self, config.GetConfig(), self.projectManager.getOgreManager())

        
        ##self.projectManager.SetBackgroundColour(wx.Color(128,128,128))
        
        mainMenu = [
        MenuFile(self,self.projectManager, "&File"),
        MenuEdit(self, self.projectManager),
        MenuBrowse(self, self.projectManager, "&Browse"),
        MenuWindow(self, self.projectManager),
        MenuHelp(self, self.projectManager),
##        MenuRender(self, self.middleNotebook, "&Ogre", self.ogreScene, self.middleNotebook),
##        MenuEditor(self, self.middleNotebook, "&Editor")
        ]
        
        menuBar = wx.MenuBar()
        for menu in mainMenu: 
            menuBar.Append(menu, menu.name)
            #menu.Enable(0, menu.enabled)

        self.SetMenuBar(menuBar)
        
        self.statusbar = OgreyStatusBar(self)

        self.SetStatusBar(self.statusbar)
        
        self.projectManager.setStatusBar(self.statusbar)

class OgreyEntityTool(wx.App):
    def OnInit(self):
        self.frame = MainOgreyEntityToolFrame(None, -1, 'Ogrey Monster Engine Entity Tool Beta 1', size=(800,600))
        self.frame.Center(wx.CENTER_ON_SCREEN)
        self.frame.Show(True)
        return True

if __name__ == '__main__':
    app = OgreyEntityTool(False)
    app.MainLoop()
    del app
