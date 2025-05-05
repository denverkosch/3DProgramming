from game_object import GameObject
from pubsub import pub


class EnemyShip(GameObject):
    def __init__(self, position, kind, id, size, node_path=None, can_collide=True):
        super().__init__(position, kind, id, size, node_path=node_path, can_collide=can_collide)
        self.speed = .7
        self.removing = False


    def tick(self):
        self.position = (self.position[0], (self.position[1] - self.speed), self.position[2])


    def collision(self, other):
        if other.kind == "cannonball":
            self.can_collide = False
            pub.sendMessage("enemy_destroyed", enemy=self, cannonball=other)