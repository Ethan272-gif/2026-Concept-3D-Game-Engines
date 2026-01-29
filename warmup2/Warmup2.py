from direct.showbase.ShowBase import ShowBase
import math, sys, random
class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.fighter=self.loader.loadModel('./Assets/sphere')
        self.fighter.reparentTo(self.render)
        self.fighter.setColorScale(1.0, 0.0, 0.0, 1.0)
        self.setBackgroundColor(0,0,0)
        #Set key bindings

        #move left
        self.accept('escape', self.quit)
        self.accept('arrow_left',self.negativeX,[1])
        self.accept('arrow_left-up',self.negativeX,[0])
        #move right
        self.accept('arrow_right',self.positiveX,[1])
        self.accept('arrow_right-up',self.positiveX,[0])
        #move up
        self.accept('arrow_up',self.positiveY,[1])
        self.accept('arrow_up-up',self.positiveY,[0])
        #move down
        self.accept('arrow_down',self.negativeY,[1])
        self.accept('arrow_down-up',self.negativeY,[0])
        self.parent=self.loader.loadModel("./Assets/cube")

        #Mouse control
        self.disable_mouse()
        self.camera.setPos(0.0,0.0,250.0)
        self.camera.setHpr(0.0,-90.0,0.0)
        self.accept('escape',self.quit)

        x=0
        for i in range(100):
            theta=x
            self.placeholder2=self.render.attachNewNode('Placeholder2')
            self.placeholder2.setPos(50.0*math.cos(theta),100.0*math.sin(theta),0.0*math.tan(theta))
            red=0.6+random.random()*0.4
            green=0.6+random.random()*0.4
            blue=0.6+random.random()*0.4
            self.placeholder2.setColorScale(red,green,blue,1.0)
            self.parent.instanceTo(self.placeholder2)
            x=x+0.06

    

    def negativeX(self,keyDown):
        if (keyDown):
            self.taskMgr.add(self.moveNegativeX, 'moveNegativeX')
        else:
            self.taskMgr.remove('moveNegativeX')
    def moveNegativeX(self,task):
        self.fighter.setX(self.fighter,-1)
        return task.cont
    def positiveX(self,keyDown):
        if (keyDown):
            self.taskMgr.add(self.movePositiveX, 'movePositiveX')
        else:
            self.taskMgr.remove('movePositiveX')
    def movePositiveX(self,task):
        self.fighter.setX(self.fighter,1)
        return task.cont
    def positiveY(self,keyDown):
        if (keyDown):
            self.taskMgr.add(self.movePositiveY, 'movePositiveY')
        else:
            self.taskMgr.remove('movePositiveY')
    def movePositiveY(self,task):
        self.fighter.setY(self.fighter,1)
        return task.cont
    def negativeY(self,keyDown):
        if (keyDown):
            self.taskMgr.add(self.moveNegativeY, 'moveNegativeY')
        else:
            self.taskMgr.remove('moveNegativeY')
    def moveNegativeY(self,task):
        self.fighter.setY(self.fighter,-1)
        return task.cont
    def quit(self):
        sys.exit()

app=MyApp()
app.run()