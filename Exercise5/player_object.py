from pubsub import pub
from game_object import GameObject

class PlayerObject(GameObject):
    def __init__(self, position, kind, id, size, can_collide=True):
        super().__init__(position, kind, id, size, can_collide=can_collide)
        pub.subscribe(self.input_event, 'input')

        self.speed = 0.1

    def input_event(self, events=None):
        if events:
            if "fire" in events:
                cannonballPos = self.node_path.getHpr()
                cannonballPos[1] -= 7
                pub.sendMessage("shoot", size=[1, 1, 1], position=cannonballPos)

    def move(self, speed: list):
        self.position[0] = (speed[0]*self.speed + self.position[0])
        self.position[1] = (speed[1]*self.speed + self.position[1])
        self.position[2] = (speed[2]*self.speed + self.position[2])

        self.node_path.setHpr(self.node_path, *speed)

    def collision(self, other):
        pass