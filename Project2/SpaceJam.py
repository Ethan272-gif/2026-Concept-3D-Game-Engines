from direct.showbase.ShowBase import ShowBase
import math, sys, random
from panda3d.core import CollisionTraverser, CollisionHandlerPusher
from panda3d.core import CollisionNode, CollisionSphere,BitMask32
import DefensePaths as defensePaths
import SpaceJamClasses as SpaceClass
class SpaceJam(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.accept('escape',self.quit)
        self.Universe=SpaceClass.Universe(
            self.loader, "./assets/Universe/Universe.x", self.render, 'Universe',"./assets/Universe/Universe.jpg",(0,0,0),15000)
        self.Hero=SpaceClass.SpaceShip(
            self.loader,"./assets/Space_Ship/Dumbledore/Dumbledore.x", self.render,'Hero',"./assets/Space_Ship/Dumbledore/spacejet_C.png",(450,5000,-500),100)
        self.SpaceStation=SpaceClass.SpaceStation(
            self.loader,"./assets/Space_Station/SpaceStation1B/spaceStation.x",self.render,'Space Station',"./assets/Space_Station/SpaceStation1B/SpaceStation1_Dif2.png",(150,4000,-600),10)
        self.Planet1=SpaceClass.Planet(
            self.loader,"./assets/Planets/protoPlanet.x",self.render,'Planet1',"./assets/Planets/Planet1/maps/Green_Planet.tif",(150,5000,67),350)# texture of Planet1 by Rebecca Deutsch 
        self.Planet2=SpaceClass.Planet(
            self.loader,"./assets/Planets/protoPlanet.x",self.render,'Planet2',"./assets/Planets/Planet2/maps/Desert_Planet.tif",(850,4000,67),250)#Texture Found Alice Gallery no moduler
        self.Planet3=SpaceClass.Planet(
            self.loader,"./assets/Planets/protoPlanet.x",self.render,'Planet3',"./assets/Planets/Planet3/maps/Fire_Planet.tif",(500,4000,700),450)#Texture by Bob Rost
        self.Planet4=SpaceClass.Planet(
            self.loader,"./assets/Planets/protoPlanet.x",self.render,'Planet4',"./assets/Planets/Planet4/maps/Sky_planet.tif",(-500,6000,700),550)#Texture by Jon Amkawa
        self.Planet5=SpaceClass.Planet(
            self.loader,"./assets/Planets/protoPlanet.x",self.render, 'Planet5',"./assets/Planets/Planet5/maps/Peach_Planet.tif",(-500,4000,300),200)#Texture by Justin Hsu/Jicjen Zhu
        self.Planet6=SpaceClass.Planet(
            self.loader,"./assets/Planets/protoPlanet.x",self.render,'Planet6',"./assets/Planets/Planet6/maps/Hole_planet.tif",(0,2000,300),100)#Texture by Amy Ip


        fullCycle=60
        for j in range(fullCycle):
            SpaceClass.Drone.droneCount+=1
            nickName="Drone"+str(SpaceClass.Drone.droneCount)

            self.DrawCloudDefense(self.Planet1,nickName)
            self.DrawBaseballSeams(self.SpaceStation,nickName,j,fullCycle,2)
            self.DrawXPlainDefense(self.Planet6, nickName, j, fullCycle, 2)
            self.DrawYPlainDefense(self.Planet5, nickName, j, fullCycle, 2)
            self.DrawZPlainDefense(self.Planet4, nickName, j, fullCycle, 2)
    def DrawBaseballSeams(self, centralObject,droneName,step,numSeams,radius=1):
        unitVec=defensePaths.BaseballSeams(step,numSeams,B=0.4)
        unitVec.normalize()
        position=unitVec*radius*250+centralObject.modelNode.getPos()
        SpaceClass.Drone(
            self.loader, "./assets/DroneDefender/DroneDefender.obj",self.render,droneName,"./assets/DroneDefender/octotoad1_auv.png", position,5)

    def DrawCloudDefense(self, centralObject, droneName):
        unitVec=defensePaths.Cloud()
        unitVec.normalize()
        position=unitVec*500+centralObject.modelNode.getPos()
        SpaceClass.Drone(
            self.loader, "./assets/DroneDefender/DroneDefender.obj",self.render,droneName,"./assets/DroneDefender/octotoad1_auv.png", position,10)
        
    def DrawXPlainDefense(self, centralObject, droneName, step, totalSteps, radius=1):
        unitVec=defensePaths.x_plain(step, totalSteps)
        unitVec.normalize()
        position=unitVec*radius*300+centralObject.modelNode.getPos()
        SpaceClass.Drone(
            self.loader, "./assets/DroneDefender/DroneDefender.obj",self.render,droneName,"./assets/DroneDefender/octotoad1_auv.png", position,10)
    def DrawYPlainDefense(self, centralObject, droneName, step, totalSteps, radius=1):
        unitVec=defensePaths.y_plain(step, totalSteps)
        unitVec.normalize()
        position=unitVec*radius*300+centralObject.modelNode.getPos()
        SpaceClass.Drone(
            self.loader, "./assets/DroneDefender/DroneDefender.obj",self.render,droneName,"./assets/DroneDefender/octotoad1_auv.png", position,10)
    def DrawZPlainDefense(self, centralObject, droneName, step, totalSteps, radius=1):
        unitVec=defensePaths.z_plain(step, totalSteps)
        position=unitVec*radius*300+centralObject.modelNode.getPos()
        SpaceClass.Drone(
            self.loader, "./assets/DroneDefender/DroneDefender.obj",self.render,droneName,"./assets/DroneDefender/octotoad1_auv.png", position,10)
        
        unitVec.normalize()
        position=unitVec*radius*300+centralObject.modelNode.getPos()

    def quit(self):
        sys.exit()

app=SpaceJam()
app.run()