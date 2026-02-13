from direct.showbase.ShowBase import ShowBase
import math, sys, random
from panda3d.core import CollisionTraverser, CollisionHandlerPusher
from panda3d.core import CollisionNode, CollisionSphere,BitMask32

class SpaceJam(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.accept('escape',self.quit)


        #Render Universe
        self.Universe=self.loader.loadModel("./assets/Universe/Universe.x")
        self.Universe.reparentTo(self.render)
        self.Universe.setScale(15000)
        tex=self.loader.loadTexture("./assets/Universe/Universe.jpg")
        self.Universe.setTexture(tex,1)

        #Render Ship
        self.Ship=self.loader.loadModel("./assets/Space_Ship/Dumbledore/Dumbledore.x")
        self.Ship.reparentTo(self.render)
        self.Ship.setScale(100)
        self.Ship.setPos(450,5000,-500)
        Ship_tex=self.loader.loadTexture("./assets/Space_Ship/Dumbledore/spacejet_C.png")
        self.Ship.setTexture(Ship_tex,1)

        #Render Space Station
        self.Station=self.loader.loadModel("./assets/Space_Station/SpaceStation1B/spaceStation.x")
        self.Station.reparentTo(self.render)
        self.Station.setScale(10)
        self.Station.setPos(150,4000,-600)
        Station_tex=self.loader.loadTexture("./assets/Space_Station/SpaceStation1B/SpaceStation1_Dif2.png")
        self.Station.setTexture(Station_tex,1)

        #Render Planet 1
        self.Planet1=self.loader.loadModel("./assets/Planets/protoPlanet.x")
        self.Planet1.reparentTo(self.render)
        self.Planet1.setPos(150,5000,67)
        self.Planet1.setScale(350)
        planet_tex_1=self.loader.loadTexture("./assets/Planets/Planet1/maps/Green_Planet.tif")
        self.Planet1.setTexture(planet_tex_1,1)
        # texture of Planet1 by Rebecca Deutsch 

        #Render Planet 2
        self.Planet2=self.loader.loadModel("./assets/Planets/protoPlanet.x")
        self.Planet2.reparentTo(self.render)
        self.Planet2.setPos(850,4000,67)
        self.Planet2.setScale(250)
        planet_tex_2=self.loader.loadTexture("./assets/Planets/Planet2/maps/Desert_Planet.tif")
        self.Planet2.setTexture(planet_tex_2,1)
        #Texture Found Alice Gallery no moduler

        #Render Planet 3
        self.Planet3=self.loader.loadModel("./assets/Planets/protoPlanet.x")
        self.Planet3.reparentTo(self.render)
        self.Planet3.setPos(500,4000,700)
        self.Planet3.setScale(450)
        planet_tex_3=self.loader.loadTexture("./assets/Planets/Planet3/maps/Fire_Planet.tif")
        self.Planet3.setTexture(planet_tex_3,1)
        #Texture by Bob Rost

        #Render Planet 4
        self.Planet4=self.loader.loadModel("./assets/Planets/protoPlanet.x")
        self.Planet4.reparentTo(self.render)
        self.Planet4.setPos(-500,6000,700)
        self.Planet4.setScale(550)
        planet_tex_4=self.loader.loadTexture("./assets/Planets/Planet4/maps/Sky_planet.tif")
        self.Planet4.setTexture(planet_tex_4,1)
        #Texture by Jon Amkawa

        #Render Planet 5
        self.Planet5=self.loader.loadModel("./assets/Planets/protoPlanet.x")
        self.Planet5.reparentTo(self.render)
        self.Planet5.setPos(-500,4000,300)
        self.Planet5.setScale(200)
        planet_tex_5=self.loader.loadTexture("./assets/Planets/Planet5/maps/Peach_Planet.tif")
        self.Planet5.setTexture(planet_tex_5,1)
        #Texture by Justin Hsu/Jicjen Zhu

        #Render Planet 6
        self.Planet6=self.loader.loadModel("./assets/Planets/protoPlanet.x")
        self.Planet6.reparentTo(self.render)
        self.Planet6.setPos(0,2000,300)
        self.Planet6.setScale(100)
        planet_tex_6=self.loader.loadTexture("./assets/Planets/Planet6/maps/Hole_planet.tif")
        self.Planet6.setTexture(planet_tex_6,1)
        #Texture by Amy Ip
    def quit(self):
        sys.exit()

app=SpaceJam()
app.run()