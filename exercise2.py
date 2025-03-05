from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import DirectionalLight, AmbientLight

brown = (128 / 255, 66 / 255, 0 / 255, 1)
white = (1, 1, 1, 1)
black = (0, 0, 0, 1)


class Exercise2(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        base.disableMouse() # type: ignore

        # set the background color
        self.setBackgroundColor(black)

        self.globe = self.loader.loadModel("Models/sphere")
        globeTexture = self.loader.loadTexture("Models/earthTex.jpg")
        self.globe.setTexture(globeTexture, 1)
        self.globe.reparentTo(self.render)
        self.globe.setPos(0, 0, 0)
        self.globe.setScale(7, 7, 7)
        self.globe.setShaderAuto()
        self.globe.setTwoSided(True)

        self.sunlight = DirectionalLight('sunlight')
        self.sunlight.setColor(white)  # White light, like the sun
        self.sunlight_node = self.render.attachNewNode(self.sunlight)
        self.sunlight_node.node().setShadowCaster(True)

        self.orbit = self.render.attachNewNode("orbit")
        self.orbit.setPos(0, 0, 0)
        self.sunlight_node.reparentTo(self.orbit)

        self.sunlight_node.setPos(0, -100, 0)
        self.sunlight_node.lookAt(self.orbit)

        self.render.setLight(self.sunlight_node)


        self.center = self.render.attachNewNode("center")

        # Load the model

        self.ship = self.loader.loadModel("Models/ship")
        self.ship.reparentTo(self.center)
        self.ship.setPos(23, 0, 0)
        self.ship.setHpr(90, 90, 0)
        self.ship.setScale(0.25, 0.25, 0.25)
        self.ship.setColor(brown)


        self.captain = self.loader.loadModel("Models/sonic/sonic")
        self.captain.reparentTo(self.ship)
        self.captain.setPos(0, -1.5, 0.5)
        self.captain.setScale(0.18, 0.18, 0.18)
        self.captain.setHpr(180, 0, 0)

        # Ambient light
        self.alight = self.render.attachNewNode(AmbientLight("Ambient"))
        self.alight.node().setColor((0.3, 0.3, 0.3, 1))
        self.render.setLight(self.alight)

        # Initial camera setup
        self.camera.reparentTo(self.ship)
        self.camera.setPos(0, -60, 35)
        self.camera.lookAt(self.ship)

        # Set basic Hpr, key bindings will manipulate these and update will move the ship according to the hpr
        self.shipH = self.shipP = self.shipR = 0

        self.accept('w', self.moveForward)
        self.accept('w-up', self.stopForward)
        self.accept('a', self.turnLeft)
        self.accept('a-up', self.stopLeft)
        self.accept('s', self.moveBackward)
        self.accept('s-up', self.stopForward)
        self.accept('d', self.turnRight)
        self.accept('d-up', self.stopRight)
        self.accept('r', self.reset)

        self.taskMgr.add(self.update, "update")
        self.taskMgr.add(self.rotateSun, "rotateSun")


    def update(self, task):
        self.center.setHpr(self.center, self.shipH, self.shipP, self.shipR)
        return Task.cont

    def moveForward(self):
        self.shipR = -1

    def stopForward(self):
        self.shipR = 0

    def moveBackward(self):
        self.shipR = 0.25

    def turnLeft(self):
        if self.shipP < 1:
            self.shipP += 1

    def stopLeft(self):
        if (self.shipP > 0):
            self.shipP -= 1
    
    def turnRight(self):
        if self.shipP > -1:
            self.shipP -= 1
    
    def stopRight(self):
        if (self.shipP < 0):
            self.shipP += 1
    
    def reset(self):
        self.center.setPos(0, 0, 0)
        self.center.setHpr(0, 0, 0)

    def rotateSun(self, task):
        self.orbit.setHpr(self.orbit, 0, 0.5, 0)
        return Task.cont
app = Exercise2()
app.run()
