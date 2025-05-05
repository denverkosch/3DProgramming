from game_object import GameObject


class Cannonball(GameObject):
    def __init__(self, position, kind, id, size, node_path=None, can_collide=True):
        super().__init__(position, kind, id, size, node_path=node_path, can_collide=can_collide)
        self.speed = 1.25
        self.relative_origin = base.render.attachNewNode(f"{kind}_{id}_origin") # type: ignore
        self.relative_origin.setPos(0,0,0)
        self.relative_origin.setHpr(*self.position)
        self.node_path.reparentTo(self.relative_origin)
        self.position = [0, 0, 0]
        self.node_path.setHpr(0, 0, 0)

    def tick(self):
        self.position[1] -= self.speed
