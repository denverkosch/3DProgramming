from direct.showbase.ShowBase import ShowBase
from random import randint
from colors import brown, white, red
from panda3d.core import DirectionalLight, AmbientLight

def randColorVec4():
    return (randint(0,255)/255, randint(0,255)/255, randint(0,255)/255, 1)

class ViewObject:
    def __init__(self, game_object, scale=(1,1,1)):
        self.game_object = game_object

        print(game_object.position)
        self.cube = self.getModel(kind=self.game_object.kind) # type: ignore
        self.cube.reparentTo(base.render) # type: ignore
        self.cube.setPos(*game_object.position)
        self.cube.setScale(*scale)

        game_object.cube = self.cube

    def tick(self):
        pass

    def getModel(self, kind):
        obj = None
        if kind == 'world': 
            obj = base.loader.loadModel("../Models/sphere") #type: ignore
            obj.setTexture(base.loader.loadTexture('../Models/earthTex.jpg')) #type: ignore
        elif kind == "ship" or kind == "player":
            obj = base.render.attachNewNode("center") #type: ignore
            ship = base.loader.loadModel("../Models/ship") #type: ignore
            ship.reparentTo(obj)
            ship.setName("ship")
            ship.setPos(23, 0, 0)
            ship.setHpr(90, 90, 0)
            ship.setScale(0.25, 0.25, 0.25)

            captain = base.loader.loadModel("../Models/sonic/sonic") #type: ignore
            captain.reparentTo(ship)
            captain.setPos(0, -1.5, 0.5)
            captain.setHpr(180, 0, 0)
            captain.setScale(0.18, 0.18, 0.18)
            if kind == "player":
                ship.setColor(brown)
            else:
                ship.setColor(red)
                captain.setColor(red)
                
        elif kind == 'sun':
            obj = base.render.attachNewNode("sunOrbiter") #type: ignore
            obj.setPos(0, 0, 0)
            sunlight = DirectionalLight('sunlight')
            sunlight.setColor(white)
            sunlight_node = base.render.attachNewNode(sunlight) #type: ignore
            sunlight_node.node().setShadowCaster(True)
            sunlight_node.reparentTo(obj)
            sunlight_node.setPos(0, -100, 0)
            sunlight_node.lookAt(obj)
            base.render.setLight(sunlight_node) #type: ignore
        elif kind == 'ambient':
            obj = base.render.attachNewNode(AmbientLight("Ambient")) #type: ignore
            obj.node().setColor((0.3, 0.3, 0.3, 1))
            base.render.setLight(obj) #type: ignore
        else:
            pass

        return obj