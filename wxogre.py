import atexit
import wx
import ogre.renderer.OGRE as ogre
import sys

class OgreManager(object):
    _borgDict = None
   
    def __init__(self):
        if self.__class__._borgDict is None:
            self.root = ogre.Root("plugins.cfg")
            self.SceneManagers = []
            self.objects = []
            self.renderWindows = [] 

            #loger = self.root.LogManager
            #log = loger.createLog(sys.stdout, True, True)
            #self.root = ogre.Root('Plugin.cfg')
            self._configured = False
            self._cameraIdCounter = 0
            #self.init()
           
            self.__class__._borgDict = self.__dict__
        else:
            self.__dict__ = self.__class__._borgDict
   
    def __del__(self):
        #del self.root
        pass
        
    def _bindWindowEvents(self, window, renderWindow):
        def handleClose(event):
            del renderWindow
            event.Skip()
        def handleIdle(event):
            self.root.renderOneFrame()
            event.RequestMore()
            event.Skip()
        def handleBackground(event):
            self.root.renderOneFrame()
            event.Skip()
        def handleResize(event):
            renderWindow.windowMovedOrResized()
            #self.root.renderOneFrame()
            event.Skip()
       
        window.Bind(wx.EVT_CLOSE, handleClose)
        window.Bind(wx.EVT_IDLE, handleIdle)
        window.Bind(wx.EVT_ERASE_BACKGROUND, handleBackground)
        window.Bind(wx.EVT_SIZE, handleResize)
    
    def _activatePsyco(self):        
       #"""Import Psyco if available"""
        pass
        try:
           import psyco
           psyco.full()
        #pass
        except ImportError:
            pass
   
    def configure(self):
        #renList = self.root.getAvailableRenderers()
        #for r in renList:
            #print r.name
            #if r.name.startswith( "OpenGL" ):
        #    if r.name.startswith( "Direct3D9" ):
        #        self.root.renderSystem = r
        #        return
        #return self.root.showConfigDialog()
        """This shows the config dialog and creates the renderWindow."""
        carryOn = self.root.showConfigDialog()
        #if carryOn:
        #    print "\n Init window"
            #ogre.ResourceBackgroundQueue.getSingleton().setStartBackgroundThread(False)
            #self.renderWindow = self.root.initialise(True, "OGRE Render Window")
        #    print "\n Done"
        return carryOn
    
    def setupResources(self):
        config = ogre.ConfigFile()
        config.load('resources.cfg')
        #for section, key, path in config.values:
        #    ogre.ResourceGroupManager.getSingleton().addResourceLocation(path, key, section)
        section_iter = config.getSectionIterator()
        while section_iter.hasMoreElements():
            section_name = section_iter.peekNextKey()
            settings = section_iter.getNext()
            ### settings_tuples = config.getMultiMapSettings(settings)
            ##for resource_type, resource in settings_tuples:
            ##    self.rgm.addResourceLocation(resource, resource_type, section_name)
            for item in settings:
                ogre.ResourceGroupManager.getSingleton().addResourceLocation(item.value, item.key, section_name)        
               
    def createSceneManager(self):
        #self.sceneManager = self.root.createSceneManager(ogre.ST_GENERIC, "Scene Manager")
        #self.sceneManager = 
        return self.root.createSceneManager(ogre.ST_GENERIC)
        
    def createCamera(self, cameraName, sceneManager):
        camera = sceneManager.createCamera(cameraName)
        camera.position = (0, 150, 500)
        camera.lookAt(ogre.Vector3(0, 0, -300))
        camera.nearClipDistance = 0.5
       
        return camera
   
    def createViewport(self, renderWindow, camera):
        viewport = renderWindow.addViewport(camera, 0, 0.0, 0.0, 1.0, 1.0)
        viewport.backgroundColour = 0.5, 0.5, 0.5
       
        return viewport
    
    def initWindow(self):
        self.shouldInitResources = False
       
        if not self._configured:
            self.setupResources()
            if not self.configure():
                pass#raise RuntimeError('Ogre was not configured')
            self.root.initialise(False)
            self._configured = True
        self.shouldInitResources = True
        self._activatePsyco()
        
        #self.setupResources()
        #rg = ogre.ResourceGroupManager.getSingleton().getResourceGroups()
        #if self.shouldInitResources:
        #    for r in rg:
        #        ogre.ResourceGroupManager.getSingleton().loadResourceGroup(r, True, False)
        #    for r in rg:
        #        print r
        #        ogre.ResourceGroupManager.getSingleton().initialiseResourceGroup(r)
        #    self.shouldInitResources = False


    def getScene(self, window, cameraName = None):
        sceneManager = self.createSceneManager()
        return sceneManager
    
    def getView(self, window, sceneManager, cameraName = None):
        
        renderParameters = ogre.NameValuePairList()
        renderParameters['externalWindowHandle'] = str(window.GetHandle())
        renderWindow = self.root.createRenderWindow('RenderWindow_%i' % id(window), 640, 480, False, renderParameters)
        
        if self.shouldInitResources:
            ogre.ResourceGroupManager.getSingleton().initialiseAllResourceGroups()
            self.shouldInitResources = False
        
        pass
            
        if cameraName is None:
            cameraName = 'Camera%i' % self._cameraIdCounter
            self._cameraIdCounter += 1
            
        camera = self.createCamera(cameraName, sceneManager)
        viewport = self.createViewport(renderWindow, camera)
        self._bindWindowEvents(window, renderWindow)
        return (renderWindow, camera, viewport)
        

#atexit.register(OgreManager()._cleanup) 
