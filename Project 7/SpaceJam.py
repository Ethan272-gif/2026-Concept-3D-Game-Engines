from direct.showbase.ShowBase import ShowBase
import math, sys, random
from panda3d.core import BitMask32, CollisionNode, CollisionSphere
from panda3d.core import Vec3
from panda3d.core import CollisionTraverser, CollisionHandlerPusher
from panda3d.core import CollisionNode, CollisionSphere,BitMask32
from direct.task import Task
from panda3d.core import CollisionTraverser,TransparencyAttrib
import DefensePaths as defensePaths
import SpaceJamClasses as SpaceClass
from direct.gui.OnscreenImage import OnscreenImage
from SpaceJamClasses import Missile
from panda3d.core import CollisionHandlerEvent
from direct.interval.LerpInterval import LerpFunc
from direct.particles.ParticleEffect import ParticleEffect
import re
from SpaceJamClasses import Planet, Orbiter


class SpaceJam(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.accept('escape',self.quit)
        self.Universe=SpaceClass.Universe(
            self.loader, "./assets/Universe/Universe.x", self.render, 'Universe',"./assets/Universe/Universe.jpg",(0,0,0),15000)# type: ignore
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
        


        
        
        #for inporting variable from other page classes
        test_missile=Missile(self.loader,'./assets/Phaser/phaser.x',self.render,'temp',Vec3(0,0,0))# type: ignore
        self.reloadTime=test_missile.reloadTime
        self.reloadTime_mega=test_missile.reloadTime_mega
        self.missileDistance=test_missile.missileDistance
        self.modelNode=test_missile.modelNode
        self.missileBay=test_missile.missileBay
        self.speedMultiplier=1
        fullCycle=60

        for j in range(fullCycle):
            SpaceClass.Drone.droneCount+=1
            nickName="Drone"+str(SpaceClass.Drone.droneCount)
            self.DrawCloudDefense(self.Planet1,nickName)
            self.DrawBaseballSeams(self.SpaceStation,nickName,j,fullCycle,2)
            self.DrawXPlainDefense(self.Planet6, nickName, j, fullCycle, 2)
            self.DrawYPlainDefense(self.Planet5, nickName, j, fullCycle, 2)
            self.DrawZPlainDefense(self.Planet4, nickName, j, fullCycle, 2)


        self.rootAssetFolder = "./assets/"
        self.cTrav=CollisionTraverser()
        self.pusher=CollisionHandlerPusher()
        self.SetScene()
        self.SetKeyBindings()
        self.SetCamera()
        self.HeroColliderNP = self.render.attachNewNode('HeroCollider')
        self.pusher.addCollider(self.Hero.collisionNode,self.Hero.modelNode)
        self.cTrav.addCollider(self.Hero.collisionNode,self.pusher)
        self.taskMgr.add(self.CheckIntervals,'CheckTheMissiles')
        self.EnableHUD()
        

        #project 6
        self.cntExplode=0
        self.explodeIntervals={}
        self.SetParticles()
        self.traverser=self.cTrav
        self.handler=CollisionHandlerEvent()
        self.handler.addInPattern('into')
        self.accept('into',self.HandleInto)
            
        
        
    
    # type: ignore
    def SetScene(self):
        self.Universe=SpaceClass.UniverseCol(
            self.loader,self.rootAssetFolder+"./Universe/Universe.x",self.render,'Universe',# type: ignore
            self.rootAssetFolder+"./Universe/Universe.jpg",(0,0,0),15000)# type: ignore
        self.SpaceStation=SpaceClass.SpaceStationCol(
            self.loader,self.rootAssetFolder+"./Space_Station/SpaceStation1B/spaceStation.x",'Space Station',# type: ignore
            self.render,(150,4000,-600),10)# type: ignore
        self.Hero=SpaceClass.SpaceShipCol(
            self.loader,self.taskMgr,self.accept,self.rootAssetFolder+"./Space_Ship/Dumbledore/Dumbledore.x",self.render,'Hero',# type: ignore
            self.rootAssetFolder+"./Space_Ship/Dumbledore/spacejet_C.png",(0,2000,300),100)# type: ignore
        self.Planet1=SpaceClass.PlanetCol(
            self.loader,self.taskMgr,self.accept,self.rootAssetFolder+"./Planets/protoPlanet.x",self.render,'Planet1',# type: ignore
            self.rootAssetFolder+"./Planets/Planet1/maps/Green_Planet.tif",(150,5000,67),350)# type: ignore
        self.Planet2=SpaceClass.PlanetCol(
            self.loader,self.taskMgr,self.accept,self.rootAssetFolder+"./Planets/protoPlanet.x",self.render,'Planet2',# type: ignore
            self.rootAssetFolder+"./Planets/Planet2/maps/Desert_Planet.tif",(850,4000,67),250)# type: ignore
        self.Planet3=SpaceClass.PlanetCol(
            self.loader,self.taskMgr,self.accept,self.rootAssetFolder+"./Planets/protoPlanet.x",self.render,'Planet3',# type: ignore
            self.rootAssetFolder+"./Planets/Planet3/maps/Fire_Planet.tif",(500,4000,700),450)# type: ignore
        self.Planet4=SpaceClass.PlanetCol(
            self.loader,self.taskMgr,self.accept,self.rootAssetFolder+"./Planets/protoPlanet.x",self.render,'Planet4',# type: ignore
            self.rootAssetFolder+"./Planets/Planet4/maps/Sky_planet.tif",(-500,6000,700),550)# type: ignore
        self.Planet5=SpaceClass.PlanetCol(
            self.loader,self.taskMgr,self.accept,self.rootAssetFolder+"./Planets/protoPlanet.x",self.render,'Planet5',# type: ignore
            self.rootAssetFolder+"./Planets/Planet5/maps/Peach_Planet.tif",(-500,4000,300),200)# type: ignore
        self.Planet6=SpaceClass.PlanetCol(
            self.loader,self.taskMgr,self.accept,self.rootAssetFolder+"./Planets/protoPlanet.x",self.render,'Planet6',# type: ignore
            self.rootAssetFolder+"./Planets/Planet6/maps/Hole_planet.tif",(450,5000,-500),100)# type: ignore
        
        # project 7
        self.Sentinal1=SpaceClass.Orbiter(
            self.loader,self.taskMgr,self.rootAssetFolder+"/DroneDefender/DroneDefender.obj",self.render,# type: ignore
            "Drone",15.0,self.rootAssetFolder+"/DroneDefender/octotoad1_auv.png",self.Planet5,900,"MLB",self.Hero)# type: ignore

        self.Sentinal2=SpaceClass.Orbiter(
            self.loader,self.taskMgr,self.rootAssetFolder+"/DroneDefender/DroneDefender.obj",self.render,# type: ignore
            "Drone",15.0,self.rootAssetFolder+"/DroneDefender/octotoad1_auv.png",self.Planet2,500,"Cloud",self.Hero)# type: ignore
        
        self.Sentinal3=SpaceClass.Orbiter(
            self.loader,self.taskMgr,self.rootAssetFolder+"/DroneDefender/DroneDefender.obj",self.render,# type: ignore
            "Drone",15.0,self.rootAssetFolder+"/DroneDefender/octotoad1_auv.png",self.Planet4,900,"MLB",self.Hero)# type: ignore
        
        self.Sentinal4=SpaceClass.Orbiter(
            self.loader,self.taskMgr,self.rootAssetFolder+"/DroneDefender/DroneDefender.obj",self.render,# type: ignore
            "Drone",15.0,self.rootAssetFolder+"/DroneDefender/octotoad1_auv.png",self.Planet1,500,"Cloud",self.Hero)# type: ignore

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
        self.accept('mouse1', self.Fire) #fire the missile
        self.accept('mouse3', self.MegaBlast)#fire megablast
        self.accept('1',self.sprint,[1])
        self.accept('1-up',self.sprint,[0])
        self.accept('2',self.cameraswitch,[1])
        self.accept('2-up',self.cameraswitch,[0])
        self.accept('3',self.zoom,[1])
        self.accept('3-up',self.zoom,[0])
    
    def zoom(self,keyDown):
        if keyDown:
            self.camera.setPos(0,30,0)#type: ignore
        else:
            self.camera.setPos(0, 0, 0)#type: ignore

    def cameraswitch(self,keyDown):
        if keyDown:
            self.camera.reparentTo(self.Hero.modelNode)# type: ignore
            self.camera.setPos(0,-30, 0)#type: ignore
            self.camera.lookAt(self.Hero.modelNode)# type: ignore
        else:
            self.camera.reparentTo(self.Hero.modelNode)# type: ignore
            self.camera.setPos(0, 0, 0)#type: ignore
            self.camera.setHpr(0, 0, 0)# type: ignore

    def sprint(self,keyDown):
        if keyDown:
            self.speedMultiplier=3
        else:
            self.speedMultiplier=1

    def HandleInto(self,entry):
        fromNode=entry.getFromNodePath().getName()
        print("formNode: "+fromNode)
        intoNode=entry.getIntoNodePath().getName()
        print("intoNode: "+intoNode)

        intoPosition=Vec3(entry.getSurfacePoint(self.render))

        tempVar=fromNode.split('_')
        print("tempVar: ", str(tempVar))
        shooter=tempVar[0]
        print("Shooter: ", str(shooter))
        tempVar=intoNode.split('_')
        print("tempVar1: ", str(tempVar))
        tempVar=intoNode.split('_')
        print("tempVar2: ", str(tempVar))
        victim=tempVar[0]
        print("Victim: "+str(victim))
        pattern=r'[0-9]'
        strippedString=re.sub(pattern,'',victim)

        if (strippedString=="Drone"or strippedString=="Planet" or strippedString=="Space Station"):
            # print(victim,'hit at',intoPosition)
            intoNodePath = entry.getIntoNodePath()
            if not intoNodePath.isEmpty():
                parentNode = intoNodePath.getParent()  # the visible model
                parentNode.detachNode()
            
            # explosion
            if not hasattr(self,'explodeNode'):
                self.SetParticles()
            self.explodeNode.setPos(intoPosition)
            self.Explode()

            print(shooter+' is Done.')
            Missile.Intervals[shooter].finish()
    def DestroyObject(self,hitID,hitPosition):
        nodeID = self.render.find("**/" + hitID)  # find by name in scene graph
        if not nodeID.isEmpty():
            nodeID.detachNode()

        if not hasattr(self,'explodeNode'):
            self.SetParticles()

        # start explosion
        self.explodeNode.setPos(hitPosition)
        self.Explode()

    def Explode(self):
        self.cntExplode+=1
        tag='particles-'+str(self.cntExplode)

        self.explodeIntervals[tag]=LerpFunc(self.ExplodeLight,duration=4.0)
        self.explodeIntervals[tag].start()

    def ExplodeLight(self,t):
        if t==1.0 and self.explodeEffect:
            self.explodeEffect.disable()
        elif t==0:
            self.explodeEffect.start(self.explodeNode)

    def SetParticles(self,mega=False):
        self.enableParticles()
        self.explodeEffect=ParticleEffect()
        self.explodeEffect.loadConfig("./assets/Part-Efx/basic_xpld_efx.ptf")
        scale=500 if mega else 20
        self.explodeEffect.setScale(scale)
        self.explodeNode=self.render.attachNewNode('ExplosionEffects')
        self.explodeEffect.start(parent=self.explodeNode,renderParent=self.render)


    def Fire(self):
        if self.missileBay:
            travRate=self.missileDistance
            aim=self.Hero.modelNode.getQuat().getForward() #direction of missiles
            aim.normalize()
            fireSolution=aim*travRate
            inFront=aim*150
            travVec=fireSolution+self.Hero.modelNode.getPos()
            self.missileBay-=1
            tag='Missile'+str(SpaceClass.Missile.missileCount)
            posVec=self.Hero.modelNode.getPos()+inFront #spawn missile in front of the ship

            #create our Missile
            currentMissile=SpaceClass.Missile(self.loader,'./assets/Phaser/phaser.egg',self.render,tag,posVec,4.0)# type: ignore
            SpaceClass.Missile.Intervals[tag]=currentMissile.modelNode.posInterval(2.0, travVec, startPos=posVec, fluid=1)# type: ignore

            #Missile fire
            SpaceClass.Missile.Intervals[tag].start()

            #project 6
            self.traverser.addCollider(currentMissile.collisionNode,self.handler)
        
        else:
            #If we aren't reloading, we want to start reloading.
            if not self.taskMgr.hasTaskNamed('reload'):
                print('Initializing reload...')
                #Call the reload method on no delay
                self.taskMgr.doMethodLater(0,self.Reload,'reload')
                return Task.cont
    def SetCamera(self):
        self.disable_mouse()
        self.camera.reparentTo(self.Hero.modelNode)# type: ignore
        self.camera.setPos(0, 0, 0)#type: ignore
        # self.camera.setPos(0, -30, 20)#type: ignore
        self.camera.lookAt(self.Hero.modelNode)# type: ignore
    def MegaBlast(self):
        if self.missileBay:
            self.Mega=True
            travRate=self.missileDistance
            aim=self.Hero.modelNode.getQuat().getForward() #direction of missiles
            aim.normalize()
            fireSolution=aim*travRate
            inFront=aim*150
            travVec=fireSolution+self.Hero.modelNode.getPos()
            self.missileBay-=1
            tag='Missile'+str(SpaceClass.Missile.missileCount)
            posVec=self.Hero.modelNode.getPos()+inFront #spawn missile in front of the ship

            #create our Missile
            currentMissile=SpaceClass.Missile(self.loader,'./assets/Phaser/phaserII.x',self.render,tag,posVec,40.0)# type: ignore
            SpaceClass.Missile.Intervals[tag]=currentMissile.modelNode.posInterval(2.0, travVec, startPos=posVec, fluid=1)# type: ignore
            #Missile fire
            SpaceClass.Missile.Intervals[tag].start()
            self.SetParticles(mega=True)

            self.traverser.addCollider(currentMissile.collisionNode,self.handler)

        else:
            #If we aren't reloading, we want to start reloading.
            if not self.taskMgr.hasTaskNamed('reload'):
                print('Initializing reload...')
                #Call the reload method on no delay
                self.taskMgr.doMethodLater(0,self.MegaReload,'reload')
                return Task.cont
    def Reload(self,task):
        if task.time>self.reloadTime:
            self.missileBay+=1
            print("Reload complete.")
        if self.missileBay>1: #remove if you want more than 1 missile
            self.missileBay=1
        elif task.time<=self.reloadTime:
            print("Reload proceeding...")
            return Task.cont
    def MegaReload(self,task):
        if task.time>self.reloadTime_mega:
            self.missileBay+=1
            print("MegaBlast Ready")
        if self.missileBay>1: #remove if you want more than 1 missile
            self.missileBay=1
        elif task.time<=self.reloadTime_mega:
            print("Megablast reloading!!!!!")
            return Task.cont
    def CheckIntervals(self,i):
        allMissile=list(Missile.Intervals.keys())
        for i in allMissile:
            if not Missile.Intervals[i].isPlaying():
                Missile.cNodes[i].detachNode()
                Missile.fireModels[i].detachNode()
                del Missile.Intervals[i]
                del Missile.fireModels[i]
                del Missile.cNodes[i]
                del Missile.collisionSolids[i]
                print(i+'has reached the end of it fire solution')
        return Task.cont
    def EnableHUD(self):
        self.Hud=OnscreenImage(image="./assets/Hud/Reticle3b.png",pos=Vec3(0,0,0),scale=0.1)
        self.Hud.setTransparency(TransparencyAttrib.MAlpha)
    def Thrust(self,keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyThrust,'forward-thrust')
        else:
            self.taskMgr.remove('forward-thrust')
    def ApplyThrust(self,task):

        rate=25*self.speedMultiplier
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
        rate=-15*self.speedMultiplier
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
        rate=.5*self.speedMultiplier
        self.Hero.modelNode.setH(self.Hero.modelNode, rate)
        return task.cont
    def rightTurn(self,keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyRightTurn,'right-turn')

        else:
            self.taskMgr.remove('right-turn')
    def ApplyRightTurn(self,task):
        rate=-.5*self.speedMultiplier
        self.Hero.modelNode.setH(self.Hero.modelNode, rate)
        return task.cont
    def leftRotate(self,keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyleftRotate,'left-rotate')

        else:
            self.taskMgr.remove('left-rotate')
    def ApplyleftRotate(self,task):
        rate=-.5*self.speedMultiplier
        self.Hero.modelNode.setR(self.Hero.modelNode.getR()+rate)
        return task.cont
    def rightRotate(self,keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyrightRotate,'right-rotate')

        else:
            self.taskMgr.remove('right-rotate')
    def ApplyrightRotate(self,task):
        rate=.5*self.speedMultiplier
        self.Hero.modelNode.setR(self.Hero.modelNode.getR()+rate)
        return task.cont
    def up(self,keyDown):
        if keyDown:
            self.taskMgr.add(self.Applyup,'up')

        else:
            self.taskMgr.remove('up')
    def Applyup(self,task):
        rate=.5*self.speedMultiplier
        self.Hero.modelNode.setP(self.Hero.modelNode, rate)
        return task.cont
    def down(self,keyDown):
        if keyDown:
            self.taskMgr.add(self.Applydown,'down')

        else:
            self.taskMgr.remove('down')
    def Applydown(self,task):
        rate=-.5*self.speedMultiplier
        self.Hero.modelNode.setP(self.Hero.modelNode, rate)
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