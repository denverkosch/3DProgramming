from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import DirectionalLight

class Exercise2(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        base.disableMouse() # type: ignore

        # set the background color
        self.setBackgroundColor(1, 1, 1, 1)

        self.globe = self.loader.loadModel("Models/sphere")
        self.globe.setColor(0, 0, 1, 0.5)
        self.globe.reparentTo(self.render)
        self.globe.setPos(0, 0, 0)
        self.globe.setScale(2, 2, 2)
        self.globe.setShaderAuto()
        self.globe.setTransparency(1)
        self.globe.setTwoSided(True)

        self.center = self.render.attachNewNode("center")

        # Load the model
        self.ship = self.loader.loadModel("Models/ship")
        self.ship.reparentTo(self.center)
        self.ship.setPos(6.5, 0, 0)
        self.ship.setHpr(90, 90, 0)
        self.ship.setScale(0.25, 0.25, 0.25)

        self.captain = self.loader.loadModel("Models/sonic/sonic")
        self.captain.reparentTo(self.ship)
        self.captain.setPos(0, -1.5, 0.5)
        self.captain.setScale(0.2, 0.2, 0.2)
        self.captain.setHpr(180, 0, 0)

        #make a second ship
        self.center2 = self.render.attachNewNode("center2")

        self.ship2 = self.ship.copyTo(self.center2)
        self.ship2.setPos(0, 6.5, 0)
        self.ship2.setHpr(0, -90, 0)
        self.ship2.setScale(0.25, 0.25, 0.25)

        self.captain2 = self.captain.copyTo(self.ship2)
        self.captain2.setPos(0, -1.5, 0.5)
        self.captain2.setScale(0.2, 0.2, 0.2)
        self.captain2.setHpr(180, 0, 0)

        lightHprTuples = [
            (0, 0, 0),
            (90, 0, 0),
            (270, 0, 0),
            (180, 0, 0),
            (0, 90, 0),
            (0, 270, 0)
        ]

        for hpr in lightHprTuples:
            brown = (128 / 255, 66 / 255, 0 / 255, 1)
            dlight = DirectionalLight('dlight')
            dlight.setColor(brown)
            dlnp = self.ship.attachNewNode(dlight)
            dlnp.setHpr(*hpr)
            self.ship.setLight(dlnp)

            dlight = DirectionalLight('dlight')
            dlight.setColor((1, 1, 1, 1))
            dlnp = self.captain.attachNewNode(dlight)
            dlnp.setHpr(*hpr)
            self.captain.setLight(dlnp)

            dlight = DirectionalLight('dlight')
            dlight.setColor(brown)
            dlnp = self.ship2.attachNewNode(dlight)
            dlnp.setHpr(*hpr)
            self.ship2.setLight(dlnp)

            dlight = DirectionalLight('dlight')
            dlight.setColor((1, 1, 1, 1))
            dlnp = self.captain2.attachNewNode(dlight)
            dlnp.setHpr(*hpr)
            self.captain2.setLight(dlnp)

        # Initial camera setup
        self.camera.set_pos(20, -25, 0) # x (left/right), y (in/out), z (up/down)
        self.camera.look_at(0, 0, 0)

        
        self.taskMgr.add(self.move_ship, 'move_ship')


    # add a task for moving the ship around in a circular path (like sailing in a circle, not rotating)
    def move_ship(self, task):
        self.center.setHpr(self.center, 0, 0, -0.75)
        self.center2.setHpr(self.center2, 0, -0.5, 0)
        return Task.cont


app = Exercise2()
app.run()
