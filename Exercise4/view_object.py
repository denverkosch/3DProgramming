from direct.showbase.ShowBase import ShowBase
from colors import brown, white, red
from panda3d.core import DirectionalLight, AmbientLight

class ViewObject:
    def __init__(self, game_object, ):
        self.game_object = game_object

        print(game_object.position, game_object.kind)

        self.cube = self.getModel(kind=self.game_object.kind) # type: ignore
        if not self.cube.isAncestorOf(game_object.node_path):
            self.cube.reparentTo(game_object.node_path)
        else:
            self.cube.reparentTo(base.render)  # type: ignore
        self.cube.setHpr(self.cube, *game_object.position)

        bounds = self.cube.getTightBounds()
        if bounds:
            bounds = bounds[1] - bounds[0]
        print("Bounds of the model:", bounds)


    def tick(self):
        if self.game_object.kind != 'player':
            self.cube.setHpr(*self.game_object.position)

    def getModel(self, kind):
        obj = None
        if kind == 'world': 
            obj = base.loader.loadModel("../Models/sphere") # type: ignore
            obj.setTexture(base.loader.loadTexture('../Models/earthTex.jpg')) # type: ignore
            obj.setPosHprScale(0, 0, 0, 180, 0, 0, 7, 7, 7)
        elif kind in ["ship", "player"]:
            obj = base.loader.loadModel("../Models/ship") # type: ignore
            obj.reparentTo(self.game_object.node_path)
            obj.setName("ship")
            obj.setPosHprScale(23, 0, 0, 90, 90, 0, 0.25, 0.25, 0.25)

            captain = base.loader.loadModel("../Models/sonic/sonic") # type: ignore
            captain.reparentTo(obj)
            captain.setPosHprScale(0, -1.5, 0.5, 180, 0, 0, 0.18, 0.18, 0.18)

            if kind == "player":
                obj.setColor(brown)
            else:
                obj.setColor(red)
                captain.setColor(red)  

        elif kind == 'sun':
            obj = base.render.attachNewNode("sunOrbiter") # type: ignore
            obj.setPos(0, 0, 0) # Position of the sun in the scene
            sunlight = DirectionalLight('sunlight')
            sunlight.setColor(white)
            sunlight_node = base.render.attachNewNode(sunlight) # type: ignore
            sunlight_node.node().setShadowCaster(True)
            sunlight_node.reparentTo(obj)
            sunlight_node.setPos(0, -100, 0)
            sunlight_node.lookAt(obj)
            base.render.setLight(sunlight_node) # type: ignore
            obj
        elif kind == 'ambient':
            obj = base.render.attachNewNode(AmbientLight("Ambient")) # type: ignore
            obj.node().setColor((0.3, 0.3, 0.3, 1))
            base.render.setLight(obj) # type: ignore
        elif kind == 'flag':
            obj = base.loader.loadModel("../Models/Toothpick_flag") # type: ignore
            # obj.setTexture(base.loader.loadTexture('../Models/usaFlagTex.png')) # type: ignore
            obj.setColor(1, 0, 1, 1)  # Magenta color for the flag
            obj.reparentTo(self.game_object.node_path)
            obj.setPosHprScale(40, 0, 0, 90, 90, 180, 7, 7, 7)
            
            obj.setName("flag")


        print("Model created:", obj)

        return obj
