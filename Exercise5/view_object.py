from colors import brown, white, red, dimWhite, gold
from panda3d.core import DirectionalLight, AmbientLight, CollisionNode, CollisionBox, BitMask32, CollisionSphere
from pubsub import pub


class ViewObject:
    def __init__(self, game_object):
        
        self.game_object = game_object

        self.cube = self.getModel(self.game_object.kind) # type: ignore

        if not self.cube.isAncestorOf(game_object.node_path):
            self.cube.reparentTo(game_object.node_path)
        else:
            self.cube.reparentTo(base.render)  # type: ignore


        if self.game_object.kind in ['ship', 'player']:
            self.cube.setPos(self.game_object.node_path, 0, 0, 18)
        elif self.game_object.kind == 'cannonball':
            self.cube.setPos(self.game_object.node_path, 0, 0, 18.25)
            

        corners = self.cube.getTightBounds()
        size = self.game_object.size
        if corners:
            # print(game_object.kind, game_object.position)
            bounds = corners[1] - corners[0]
            # print("Bounds of the model:", bounds)


            avg_bound = (bounds.x + bounds.y + bounds.z) / 3
            if avg_bound < 0.1:
                self.cube.setScale(10) 
                bounds *= 10

            # print(f"Size of the model ({game_object.kind}): {size}")
            x_scale = size[0] / bounds.x
            y_scale = size[1] / bounds.y
            z_scale = size[2] / bounds.z

            # print(f"Scale factors: {x_scale}, {y_scale}, {z_scale}")

            self.cube.setScale(x_scale, y_scale, z_scale)

            corners = self.cube.getTightBounds()
            bounds = corners[1] - corners[0]
                
            center = (corners[0] + corners[1]) * 0.5

            if self.game_object.can_collide:
                if self.game_object.kind == 'basic':
                    solid = CollisionSphere(center, bounds.x/2)
                else:
                    solid = CollisionBox(center, bounds.x/2, bounds.y/2, bounds.z/2)

                collider_node = CollisionNode(f"{self.game_object.kind}_collider")
                collider_node.addSolid(solid)
                collider_node.setFromCollideMask(BitMask32.bit(1))
                collider_node.setIntoCollideMask(BitMask32.bit(1))

                self.collider = self.game_object.node_path.attachNewNode(collider_node)
                self.collider.setPosHpr(0, 0, 0, 0, 0, 0)
                self.collider.set_python_tag("game_object", self.game_object)

                self.collider.show()

                pub.sendMessage("collider", collider=self.collider)

    def tick(self):
        if self.game_object.kind != 'player':
            self.game_object.node_path.setHpr(*self.game_object.position)

    def getModel(self, kind):
        obj = None
        if kind == 'world': 
            obj = base.loader.loadModel("../Models/sphere") # type: ignore
            obj.setTexture(base.loader.loadTexture('../Models/earthTex.jpg')) # type: ignore
            obj.setPosHprScale(0, 0, 0, 180, 0, 0, 7, 7, 7)
        elif kind in ["ship", "player"]:
            obj = base.loader.loadModel("../Models/ship") # type: ignore
            obj.reparentTo(self.game_object.node_path)
            obj.setName("model")
            obj.setScale(0.25, 0.25, 0.25)

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
            sunlight = DirectionalLight('sunlight')
            sunlight.setColor(white)
            sunlight_node = base.render.attachNewNode(sunlight) # type: ignore
            sunlight_node.node().setShadowCaster(True)
            sunlight_node.reparentTo(obj)
            sunlight_node.lookAt(obj)
            base.render.setLight(sunlight_node) # type: ignore
        elif kind == 'ambient':
            obj = base.render.attachNewNode(AmbientLight("Ambient")) # type: ignore
            obj.node().setColor(dimWhite)
            base.render.setLight(obj) # type: ignore
        elif kind == 'cannonball':
            obj = base.loader.loadModel("../Models/sphere") # type: ignore
            obj.reparentTo(self.game_object.node_path)
            obj.setName("model")
            obj.setColor(gold)

        return obj
