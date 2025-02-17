
from direct.showbase.ShowBase import ShowBase
from random import randint

def randColorVec4():
    return (randint(0,255)/255, randint(0,255)/255, randint(0,255)/255, 1)

class ViewObject:
    def __init__(self, game_object):
        self.game_object = game_object

        self.cube = base.loader.loadModel("../Models/cube") # type: ignore
        self.cube.reparentTo(base.render) # type: ignore
        self.cube.setPos(*game_object.position)
        self.cube.setScale(1,1,1)

    def tick(self):
        pass

    def getModel(loader, kind):
        obj = None
        if kind == 'world': 
            obj = loader.loadModel("../Models/sphere")
            obj.setTexture(loader.loadTexture('../Models/earthTex.jpg'))
        elif kind == "ship":
            obj = loader.loadModel("Models/ship")
            obj.reparentTo(self.center)
            obj.setPos(23, 0, 0)
            obj.setHpr(90, 90, 0)
            obj.setScale(0.25, 0.25, 0.25)
            obj.setColor(brown)


            captain = loader.loadModel("Models/sonic/sonic")
            captain.reparentTo(obj)
            captain.setPos(0, -1.5, 0.5)
            captain.setScale(0.18, 0.18, 0.18)
            captain.setHpr(180, 0, 0)
