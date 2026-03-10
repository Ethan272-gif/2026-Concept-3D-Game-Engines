from direct.showbase.ShowBase import ShowBase
from CollideObjectBase import *
from panda3d.core import *
from direct.task.Task import TaskManager
from typing import Callable
from direct.task import Task
from CollideObjectBase import SphereCollideObject
from panda3d.core import Loader,NodePath,Vec3

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