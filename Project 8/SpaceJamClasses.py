from direct.showbase.ShowBase import ShowBase
from CollideObjectBase import *
from panda3d.core import *
from direct.task.Task import TaskManager
from typing import Callable
from direct.task import Task
from CollideObjectBase import SphereCollideObject
from panda3d.core import Loader,NodePath,Vec3,TextureStage,Mat4,TransformState
import math
from panda3d.core import CollisionNode, CollisionSphere, BitMask32
from panda3d.core import CollisionHandlerEvent
from direct.interval.LerpInterval import LerpFunc
from direct.particles.ParticleEffect import ParticleEffect
import re
import DefensePaths as defensePaths
from direct.interval.IntervalGlobal import Sequence

#project 8

class Follower(SphereCollideObject):
    velocity=0.015
    c=0
    def __init__(self, loader, taskMgr, modelPath, parentNode,nodeName,scale,texPath,centralObject,radius,staringAt):
        super(Follower,self).__init__(loader,modelPath,parentNode,nodeName,Vec3(0,0,0),3.2)
        self.angle=0.0
        self.taskMgr=taskMgr
        self.center=centralObject
        self.radius=radius
        self.staringAt=staringAt
        self.modelNode.setScale(scale)
        tex=loader.loadTexture(texPath)# type: ignore
        self.modelNode.setTexture(tex,1)
        Follower.c+=1
        self.taskName="Follower-"+str(Follower.c)
        self.taskMgr.add(self.Follow,self.taskName)

    def Follow(self,task):
        self.angle+=task.time*Follower.velocity
        orbit=Vec3(math.cos(self.angle)*self.radius,math.sin(self.angle)*self.radius,0)
        self.basePos=self.center.modelNode.getPos()
        self.modelNode.setPos(self.basePos+orbit)
        self.modelNode.lookAt(self.center.modelNode)
        return task.cont

class Wanderer(SphereCollideObject):
    numWanderers=0

    def __init__(self,loader:Loader,modelPath:str,parentNode:NodePath,modelName:str,scaleVec:float,texPath:str,staringAt:Vec3):
        super(Wanderer,self).__init__(loader,modelPath,parentNode,modelName,Vec3(0,0,0),3.2)

        self.modelNode.setScale(scaleVec)
        tex=loader.loadTexture(texPath)# type: ignore
        self.modelNode.setTexture(tex,1)
        self.staringAt=staringAt
        Wanderer.numWanderers+=1

        posInterval0=self.modelNode.posInterval(20,Vec3(300,6000,500),startPos=Vec3(0,2500,300))# type: ignore
        posInterval1=self.modelNode.posInterval(20,Vec3(700,-2000,100),startPos=Vec3(300,6000,500))# type: ignore
        posInterval2=self.modelNode.posInterval(20,Vec3(300,6000,500),startPos=Vec3(700,-2000,100))# type: ignore

        self.travelRoute=Sequence(posInterval0,posInterval1,posInterval2,name="Traveler")

        self.travelRoute.loop()
class Wanderertwo(SphereCollideObject):
    numWanderers=0

    def __init__(self,loader:Loader,modelPath:str,parentNode:NodePath,modelName:str,scaleVec:float,texPath:str,staringAt:Vec3):
        super(Wanderertwo,self).__init__(loader,modelPath,parentNode,modelName,Vec3(0,0,0),3.2)

        self.modelNode.setScale(scaleVec)
        tex=loader.loadTexture(texPath)# type: ignore
        self.modelNode.setTexture(tex,1)
        self.staringAt=staringAt
        Wanderertwo.numWanderers+=1

        posInterval0=self.modelNode.posInterval(20,Vec3(300,5800,500),startPos=Vec3(0,2200,300))# type: ignore
        posInterval1=self.modelNode.posInterval(20,Vec3(700,-2200,100),startPos=Vec3(300,5800,500))# type: ignore
        posInterval2=self.modelNode.posInterval(20,Vec3(300,5800,500),startPos=Vec3(700,-2200,100))# type: ignore

        self.travelRoute=Sequence(posInterval0,posInterval1,posInterval2,name="Traveler2")

        self.travelRoute.loop()

class Planet:
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        self.modelNode=loader.loadModel(modelPath)# type: ignore
        self.modelNode.reparentTo(parentNode)

        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        self.modelNode.setName(nodeName)
        tex=loader.loadTexture(texPath)# type: ignore
        self.modelNode.setTexture(tex,1)
class Universe:
    def __init__(self, loader: Loader, modelPath: str, parentNode:NodePath, nodeName: str, texPath:str, posVec:Vec3, scaleVec:float):
        self.modelNode=loader.loadModel(modelPath)# type: ignore
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        self.modelNode.setName(nodeName)
        tex=loader.loadTexture(texPath)# type: ignore
        self.modelNode.setTexture(tex,1)
class SpaceStation:
    def __init__(self, loader: Loader, modelPath: str, parentNode:NodePath, nodeName: str, texPath:str, posVec:Vec3, scaleVec:float):
        self.modelNode=loader.loadModel(modelPath)# type: ignore
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        self.modelNode.setName(nodeName)
        tex=loader.loadTexture(texPath)# type: ignore
        self.modelNode.setTexture(tex,1)
class SpaceShip:
    def __init__(self, loader: Loader, modelPath: str, parentNode:NodePath, nodeName: str, texPath:str, posVec:Vec3, scaleVec:float):
        self.modelNode=loader.loadModel(modelPath)# type: ignore
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        self.modelNode.setName(nodeName)
        tex=loader.loadTexture(texPath)# type: ignore
        self.modelNode.setTexture(tex,1)
class Drone:
    #How many drones will spawn
    droneCount=0
    def __init__(self, loader: Loader, modelPath: str, parentNode:NodePath, nodeName: str, texPath:str, posVec:Vec3, scaleVec:float):
        self.modelNode=loader.loadModel(modelPath)# type: ignore
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        self.modelNode.setName(nodeName)
        tex=loader.loadTexture(texPath)# type: ignore
        self.modelNode.setTexture(tex,1)

        self.collider=self.modelNode.attachNewNode(
            CollisionNode(nodeName+"_cNode")
        )
        self.collider.node().addSolid(CollisionSphere(0,0,0,5))
class UniverseCol(InverseSphereCollideObject):
    def __init__(self,loader:Loader,modelPath:str,parentNode:NodePath,nodeName:str,texPath:str,posVec:Vec3,scaleVec:float):
        super(UniverseCol,self).__init__(loader,modelPath,parentNode,nodeName,Vec3(0,0,0),0.9)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        self.modelNode.setName(nodeName)
        tex=loader.loadTexture(texPath)# type: ignore
        self.modelNode.setTexture(tex,1)
class SpaceStationCol(CapsuleCollidableObject):
    def __init__(self,loader:Loader,modelPath:str,nodeName:str,parentNode:NodePath,posVec:Vec3,scaleVec:float):
        super(SpaceStationCol, self).__init__(loader,modelPath,parentNode,nodeName,1,-1,5,1,-1,-5,10)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        self.modelNode.setName(nodeName)
class SpaceShipCol(SphereCollideObject):
    def __init__(self,loader:Loader,taskMgr:TaskManager,accept:Callable[[str,Callable],None],modelPath:str,parentNode:NodePath,nodeName:str,texPath:str,posVec:Vec3,scaleVec:float):
        super(SpaceShipCol,self).__init__(loader,modelPath,parentNode,nodeName,Vec3(0,0,0),1)
        self.taskMgr=taskMgr
        self.accept=accept
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        self.modelNode.setName(nodeName)
        tex=loader.loadTexture(texPath)# type: ignore
        self.modelNode.setTexture(tex,1)
        # self.taskMgr.add(self.CheckIntervals,'checkMissiles',34)

#project 7
class Orbiter(SphereCollideObject):
    numOrbits=0
    velocity=0.015
    cloudTimer=240
    def __init__(self,loader:Loader,taskMgr:TaskManager,modelPath:str,parentNode:NodePath,nodeName:str,scale:float,texPath:str,
                 centralObject:PlaceObject,orbitRadius:float,orbitType:str,staringAt:Vec3):
        super(Orbiter,self).__init__(loader,modelPath,parentNode,nodeName,Vec3(0,0,0),3.2)
        self.taskMgr=taskMgr
        self.orbitType=orbitType
        self.modelNode.setScale(scale)
        tex=loader.loadTexture(texPath)# type: ignore
        self.modelNode.setTexture(tex,1)
        self.orbitObject=centralObject
        self.orbitRadius=orbitRadius
        self.staringAt=staringAt
        Orbiter.numOrbits+=1

        self.cloudClock=0
        self.taskFlag="Traveler-"+str(Orbiter.numOrbits)

        

        self.taskMgr.add(self.Orbit,self.taskFlag)

    def Orbit(self,task):
        if self.orbitType=="MLB":
            positionVec=defensePaths.BaseballSeams(task.time*Orbiter.velocity,self.numOrbits,2.0)
            self.modelNode.setPos(positionVec*self.orbitRadius+self.orbitObject.modelNode.getPos())

        elif self.orbitType=="Cloud":
            if self.cloudClock<Orbiter.cloudTimer:
                self.cloudClock+=1

            else:
                self.cloudClock=0
                positionVec=defensePaths.Cloud()
                self.modelNode.setPos(positionVec*self.orbitRadius+self.orbitObject.modelNode.getPos())

        self.modelNode.lookAt(self.staringAt.modelNode)# type: ignore
        return task.cont


class PlanetCol(SphereCollideObject):
    def __init__(self,loader:Loader,taskMgr:TaskManager,accept:Callable[[str,Callable],None],modelPath:str,parentNode:NodePath,nodeName:str,texPath:str,posVec:Vec3,scaleVec:float):
        super(PlanetCol,self).__init__(loader,modelPath,parentNode,nodeName,Vec3(0,0,0),1)
        self.taskMgr=taskMgr
        self.accept=accept
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        self.modelNode.setName(nodeName)
        tex=loader.loadTexture(texPath)# type: ignore
        self.modelNode.setTexture(tex,1)
class DroneCol(SphereCollideObject):
    def __init__(self,loader:Loader,taskMgr:TaskManager,accept:Callable[[str,Callable],None],modelPath:str,parentNode:NodePath,nodeName:str,texPath:str,posVec:Vec3,scaleVec:float):
        super(DroneCol,self).__init__(loader,modelPath,parentNode,nodeName,Vec3(0,0,0),1)
        self.taskMgr=taskMgr
        self.accept=accept
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        self.modelNode.setName(nodeName)
        tex=loader.loadTexture(texPath)# type: ignore
        self.modelNode.setTexture(tex,1)
class Missile(SphereCollideObject):
    fireModels={}
    cNodes={}
    collisionSolids={}
    Intervals={}
    missileCount=0

    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath,nodeName: str, posVec: Vec3, scaleVec: float=1.0):
        super(Missile,self).__init__(loader,modelPath,parentNode,nodeName,Vec3(0,0,0),3.0)
        self.modelNode.setScale(scaleVec)
        self.modelNode.setPos(posVec)
        self.reloadTime=.25
        self.reloadTime_mega=.75
        self.missileDistance=4000 #distance until missle explode
        self.missileBay=1 #max number of missile in the missle bay at launch or clip
        
        Missile.missileCount+=1

        Missile.fireModels[nodeName]=self.modelNode
        Missile.cNodes[nodeName]=self.collisionNode
        #We retrieve the solid for our collisionNode
        Missile.collisionSolids[nodeName]=self.collisionNode.node().getSolid(0)
        Missile.cNodes[nodeName].show()
        print("Fire torpedo #" +str(Missile.missileCount))