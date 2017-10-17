import wx
import ogre.renderer.OGRE as ogre

class Entity:
    def __init__(self):
        self.name = ""
        self.Transform = []
        self.Graphic = []
        self.AnimatedGraphic = []
        self.Physic = []
        self.FreeCamera = []
        self.Control = []
        self.Ai = []
        self.Light = []
        self.PhysicController = []
        self.FollowCamera = []
        self.Audio = AudioObject()
        self.type = "Entity"
        self.entity = self
        self.node = "RootNode"
        self.filepath = ""
        self.ObjectList = [self.Transform, self.Graphic, self.AnimatedGraphic,
                        self.Physic, self.FreeCamera, self.Control, self.Ai,
                        self.Light, self.PhysicController, self.FollowCamera,
                        self.Audio.source]
        
        self.comments = ""
        

class TransformObject:
    def __init__(self):
        self.name = ""
        self.position = ogre.Vector3(0.0, 0.0, 0.0)
        self.rotation = ogre.Vector3(0.0, 0.0, 0.0)
        self.scale = ogre.Vector3(1.0, 1.0, 1.0)
        self.node = ""
        self.entity = None
        self.type = "Transform"
        
        self.ogreNode = None
        self.ogreParentNode = None

        self.comments = ""


class GraphicObject:
    def __init__(self):
        self.name = ""
        self.model = ""
        self.material = ""
        self.node = ""
        self.entity = None
        self.type = "Graphic"
        
        self.ogreNode = None
        self.ogreEntity = None

        self.comments = ""

        
        #self.ogreAnimations = []
        #self.animationObject = AnimationObject()

class PhysicObject:
    def __init__(self):
        self.name = "main"
        self.node = ""
        self.static = False
        self.collisionenabled = True
        self.type = "PhysicActor"
        self.follow = False

        
        self.body = PhysicBody()
        self.shapes = []
        
        self.entity = None

        self.comments = ""

        
class PhysicBody:
    def __init__(self):
        self.gravityenabled = True 
        self.kinematic = False
        self.lineardamping = 0.0 
        self.angulardamping = 0.0 
        self.maxangularvelocity = -1.0
        self.type = "PhysicBody"

        self.linearvelocity = ogre.Vector3(0.0, 0.0, 0.0)
        self.angularvelocity = ogre.Vector3(0.0, 0.0, 0.0)
        
        self.entity = None

        self.comments = ""


class PhysicShape:
    def __init__(self):
        self.name = ""
        self.collisiongroup = "default"
        self.material = "default"
        self.density = 1.0
        self.shape = None
        self.listnum = None
        self.entity = None
        self.type = "PhysicShape"

        self.comments = ""


class boxshape:
    def __init__(self):
        self.height = 1.0 
        self.width = 1.0 
        self.depth = 1.0
        self.localpose = localpose()
        self.shape = "boxshape"
        self.listnum = None

        self.comments = ""


class capsuleshape:
    def __init__(self):
        self.height = 1.0 
        self.radius = 0.10
        self.localpose = localpose()
        self.shape = "capsuleshape"
        self.listnum = None

        self.comments = ""


        
class sphereshape:
    def __init__(self):
        self.radius = 0.5
        self.localpose = localpose()
        self.shape = "sphereshape"
        self.listnum = None

        self.comments = ""


        
class convexshape:
    def __init__(self):
        self.mesh = "" 
        self.smoothmesh = False
        self.localpose = localpose()
        self.shape = "convexshape"
        self.listnum = None
        
        self.comments = ""


class triangleshape:
    def __init__(self):
        self.mesh = "" 
        self.smoothmesh = False
        self.localpose = localpose()
        self.shape = "triangleshape"
        self.listnum = None
        
        self.comments = ""

        
       
class localpose:
    def __init__(self):
        self.node = "none"
        self.position = ogre.Vector3(0.0, 0.0, 0.0)
        self.rotation = ogre.Vector3(0.0, 0.0, 0.0)

        self.comments = ""

        

class FreeCameraObject:
    def __init__(self):
        self.sensitivity = 0.0
        self.speed = 0.0
        self.entity = None
        self.node = None
        self.type = "FreeCamera"

        self.comments = ""

class ControlObject:
    def __init__(self):
        self.etype = "simple"
        self.entity = None
        self.node = None
        self.type = "Control"
        self.movementspeed = 1
        self.turnspeed = 1

        self.comments = ""


class AiObject:
    def __init__(self):
        self.startstate = ""
        self.entity = None
        self.node = None
        self.type = "Ai"
        
        self.comments = ""


class AnimatedGraphicObject(GraphicObject):
    def __init__(self):
        GraphicObject.__init__(self)
        
        self.type = "AnimatedGraphic"
        
        self.ogreAnimations = []
        self.animationObject = AnimationObject()

        self.comments = ""



class AnimationObject:
    def __init__(self, speed = ogre.Math.RangeRandom(0.5, 1.5), loop = True, enabled = True):
        self.speed = speed
        self.loop = loop
        self.enabled = enabled
        self.animation = None
        self.activeAnimation = None
        self.entity = None

        self.comments = ""

    
    def playAnimation(self, entity):
        self.entity = entity
        if not self.animation == None: 
            self.activeAnimation = self.entity.getAnimationState(self.animation)
            self.activeAnimation.loop =  self.loop
            self.activeAnimation.enabled = True
            self.activeAnimation.speed = self.speed
    
    def stopAnimation(self):
        if not self.activeAnimation == None:
            self.activeAnimation.enabled = False
    
    def changeSpeed(self, speed):
        self.speed = speed
        if not self.activeAnimation == None:
            self.activeAnimation.speed = self.speed

class LightObject:
    def __init__(self):
        self.name = ""
        self.lighttype = ""
        self.diffuse = ogre.Vector3(1.0, 1.0, 1.0)
        self.specular = ogre.Vector3(1.0, 1.0, 1.0)
        self.direction = ogre.Vector3(0.0, 0.0, 0.0)
        self.powerScale = 1.0
        self.innerAngle = 0
        self.outerAngle = 0
        self.falloff = 1.0
        self.range = 1.0
        self.node = None
        self.entity = None
        self.type = "Light"
        self.ogreLight = None
        self.ogreNode = None

        self.comments = ""


class PointLight(LightObject):
    def __init__(self):
        LightObject.__init__(self)

class SpotLight(LightObject):
    def __init__(self):
        LightObject.__init__(self)


class DirectionLight(LightObject):
    def __init__(self):
        LightObject.__init__(self)

class PhysicControllerObject:
    def __init__(self):
        self.name = ""
        self.slopelimit = 0.0
        self.steplimit = 0.0
        self.entity = None
        self.node = None
        self.type = "PhysicController"
        self.shape = None

        self.comments = ""

    
class PhysicControllerShapeCapsule:
    def __init__(self):
        self.height = 0.0
        self.radius = 0.0
        self.type = "PhysicControllerShapeCapsule"
        self.node = None
        self.entity = None
        
        self.comments = ""

class FollowCameraObject:
    def __init__(self):
        self.node = ""
        self.entity = None
        self.type = "FollowCamera"
        
        self.comments = ""

class AudioObject:
    def __init__(self):        
        self.node = None
        self.entity = None
        
        self.source = []
        self.type = "Audio"
        self.comments = ""

class AudioSource:
    def __init__(self):
        self.name = ""
        
        self.node = None
        self.entity = None
        
        self.type = "AudioSource"
        self.comments = ""
        
