from direct.showbase.ShowBase import ShowBase
import math, sys, random
from panda3d.core import Vec3
from panda3d.core import CollisionTraverser, CollisionHandlerPusher
from panda3d.core import CollisionNode, CollisionSphere,BitMask32
from direct.task import Task
import DefensePaths as defensePaths
import SpaceJamClasses as SpaceClass
class SpaceJam(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.accept('escape',self.quit)
        self.Universe=SpaceClass.Universe(
            self.loader, "./assets/Universe/Universe.x", self.render, 'Universe',"./assets/Universe/Universe.jpg",(0,0,0),15000)# type: ignore
        self.Hero=SpaceClass.SpaceShip(
            self.loader,"./assets/Space_Ship/Dumbledore/Dumbledore.x", self.render,'Hero',"./assets/Space_Ship/Dumbledore/spacejet_C.png",(0,2000,300),100)# type: ignore
        self.SpaceStation=SpaceClass.SpaceStation(
            self.loader,"./assets/Space_Station/SpaceStation1B/spaceStation.x",self.render,'Space Station',"./assets/Space_Station/SpaceStation1B/SpaceStation1_Dif2.png",(150,4000,-600),10)# type: ignore
        self.Planet1=SpaceClass.Planet(
            self.loader,"./assets/Planets/protoPlanet.x",self.render,'Planet1',"./assets/Planets/Planet1/maps/Green_Planet.tif",(150,5000,67),350)# texture of Planet1 by Rebecca Deutsch # type: ignore
        self.Planet2=SpaceClass.Planet(
            self.loader,"./assets/Planets/protoPlanet.x",self.render,'Planet2',"./assets/Planets/Planet2/maps/Desert_Planet.tif",(850,4000,67),250)#Texture Found Alice Gallery no moduler# type: ignore
        self.Planet3=SpaceClass.Planet(
            self.loader,"./assets/Planets/protoPlanet.x",self.render,'Planet3',"./assets/Planets/Planet3/maps/Fire_Planet.tif",(500,4000,700),450)#Texture by Bob Rost# type: ignore
        self.Planet4=SpaceClass.Planet(
            self.loader,"./assets/Planets/protoPlanet.x",self.render,'Planet4',"./assets/Planets/Planet4/maps/Sky_planet.tif",(-500,6000,700),550)#Texture by Jon Amkawa# type: ignore
        self.Planet5=SpaceClass.Planet(
            self.loader,"./assets/Planets/protoPlanet.x",self.render, 'Planet5',"./assets/Planets/Planet5/maps/Peach_Planet.tif",(-500,4000,300),200)#Texture by Justin Hsu/Jicjen Zhu# type: ignore
        self.Planet6=SpaceClass.Planet(
            self.loader,"./assets/Planets/protoPlanet.x",self.render,'Planet6',"./assets/Planets/Planet6/maps/Hole_planet.tif",(450,5000,-500),100)#Texture by Amy Ip# type: ignore

        fullCycle=60
        for j in range(fullCycle):
            SpaceClass.Drone.droneCount+=1
            nickName="Drone"+str(SpaceClass.Drone.droneCount)

            self.DrawCloudDefense(self.Planet1,nickName)
            self.DrawBaseballSeams(self.SpaceStation,nickName,j,fullCycle,2)
            self.DrawXPlainDefense(self.Planet6, nickName, j, fullCycle, 2)
            self.DrawYPlainDefense(self.Planet5, nickName, j, fullCycle, 2)
            self.DrawZPlainDefense(self.Planet4, nickName, j, fullCycle, 2)

        self.SetCamera()
        self.SetKeyBindings()
    # type: ignore
    
    def SetKeyBindings(self):
        self.accept('w',self.Thrust,[1])
        self.accept('w-up',self.Thrust,[0])
        self.accept('a',self.leftTurn,[1])
        self.accept('a-up',self.leftTurn,[0])
        self.accept('d',self.rightTurn,[1])
        self.accept('d-up',self.rightTurn,[0])
        self.accept('s',self.reverse,[1])
        self.accept('s-up',self.reverse,[0])
        self.accept('q',self.leftRotate,[1])
        self.accept('q-up',self.leftRotate,[0])
        self.accept('e',self.rightRotate,[1])
        self.accept('e-up',self.rightRotate,[0])
        self.accept('space',self.up,[1])
        self.accept('space-up',self.up,[0])
        self.accept('control',self.down,[1])
        self.accept('control-up',self.down,[0])
    
    def SetCamera(self):
        self.disable_mouse()
        self.camera.reparentTo(self.Hero.modelNode)# type: ignore
        self.camera.setFluidPos(0,1,0)# type: ignore
        
    def Thrust(self,keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyThrust,'forward-thrust')
        else:
            self.taskMgr.remove('forward-thrust')
    def ApplyThrust(self,task):

        rate=5
        trajectory=self.render.getRelativeVector(self.Hero.modelNode,Vec3.forward())
        trajectory.normalize()
        newPos = self.Hero.modelNode.getPos() + trajectory * rate
        self.Hero.modelNode.setFluidPos(newPos)
        return task.cont
    def reverse(self,keyDown):
        if keyDown:
            self.taskMgr.add(self.Applyreverse,'back-thrust')
        else:
            self.taskMgr.remove('back-thrust')
    def Applyreverse(self,task):
        rate=-5
        trajectory=self.render.getRelativeVector(self.Hero.modelNode,Vec3.forward())
        trajectory.normalize()
        newPos = self.Hero.modelNode.getPos() + trajectory * rate
        self.Hero.modelNode.setFluidPos(newPos)
        return task.cont
    def leftTurn(self,keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyLeftTurn,'left-turn')

        else:
            self.taskMgr.remove('left-turn')

    def ApplyLeftTurn(self,task):
        rate=.5
        self.Hero.modelNode.setH(self.Hero.modelNode.getH()+rate)
        return task.cont

    def rightTurn(self,keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyRightTurn,'right-turn')

        else:
            self.taskMgr.remove('right-turn')
    def ApplyRightTurn(self,task):
        rate=-.5
        self.Hero.modelNode.setH(self.Hero.modelNode.getH()+rate)
        return task.cont

    def leftRotate(self,keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyleftRotate,'left-rotate')

        else:
            self.taskMgr.remove('left-rotate')
    def ApplyleftRotate(self,task):
        rate=-.5
        self.Hero.modelNode.setR(self.Hero.modelNode.getR()+rate)
        return task.cont

    def rightRotate(self,keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyrightRotate,'right-rotate')

        else:
            self.taskMgr.remove('right-rotate')

    def ApplyrightRotate(self,task):
        rate=.5
        self.Hero.modelNode.setR(self.Hero.modelNode.getR()+rate)
        return task.cont

    def up(self,keyDown):
        if keyDown:
            self.taskMgr.add(self.Applyup,'up')

        else:
            self.taskMgr.remove('up')
    def Applyup(self,task):
        rate=.5
        self.Hero.modelNode.setP(self.Hero.modelNode.getP()+rate)
        return task.cont
    
    def down(self,keyDown):
        if keyDown:
            self.taskMgr.add(self.Applydown,'down')

        else:
            self.taskMgr.remove('down')

    def Applydown(self,task):
        rate=-.5
        self.Hero.modelNode.setP(self.Hero.modelNode.getP()+rate)
        return task.cont
    

    def DrawBaseballSeams(self, centralObject,droneName,step,numSeams,radius=1):
        unitVec=defensePaths.BaseballSeams(step,numSeams,B=0.4)
        unitVec.normalize()
        position=unitVec*radius*250+centralObject.modelNode.getPos()
        SpaceClass.Drone(
            self.loader, "./assets/DroneDefender/DroneDefender.obj",self.render,droneName,"./assets/DroneDefender/octotoad1_auv.png", position,5)# type: ignore

    def DrawCloudDefense(self, centralObject, droneName):
        unitVec=defensePaths.Cloud()
        unitVec.normalize()
        position=unitVec*500+centralObject.modelNode.getPos()
        SpaceClass.Drone(
            self.loader, "./assets/DroneDefender/DroneDefender.obj",self.render,droneName,"./assets/DroneDefender/octotoad1_auv.png", position,10)# type: ignore
        
    def DrawXPlainDefense(self, centralObject, droneName, step, totalSteps, radius=1):
        unitVec=defensePaths.x_plain(step, totalSteps)
        unitVec.normalize()
        position=unitVec*radius*300+centralObject.modelNode.getPos()
        SpaceClass.Drone(
            self.loader, "./assets/DroneDefender/DroneDefender.obj",self.render,droneName,"./assets/DroneDefender/octotoad1_auv.png", position,10)# type: ignore
    def DrawYPlainDefense(self, centralObject, droneName, step, totalSteps, radius=1):
        unitVec=defensePaths.y_plain(step, totalSteps)
        unitVec.normalize()
        position=unitVec*radius*300+centralObject.modelNode.getPos()
        SpaceClass.Drone(
            self.loader, "./assets/DroneDefender/DroneDefender.obj",self.render,droneName,"./assets/DroneDefender/octotoad1_auv.png", position,10)# type: ignore
    def DrawZPlainDefense(self, centralObject, droneName, step, totalSteps, radius=1):
        unitVec=defensePaths.z_plain(step, totalSteps)
        unitVec.normalize()
        position=unitVec*radius*300+centralObject.modelNode.getPos()
        SpaceClass.Drone(
            self.loader, "./assets/DroneDefender/DroneDefender.obj",self.render,droneName,"./assets/DroneDefender/octotoad1_auv.png", position,10)# type: ignore

    def quit(self):
        sys.exit()

app=SpaceJam()
app.run()