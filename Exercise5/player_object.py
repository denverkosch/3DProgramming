from panda3d.core import NodePath
from pubsub import pub
from game_object import GameObject

class PlayerObject(GameObject):
    def __init__(self, position, kind, id, size, can_collide=True):
        super().__init__(position, kind, id, size, can_collide=can_collide)
        pub.subscribe(self.input_event, 'input')

        self.speed = 0.1
        self.originalPosition = position

    def input_event(self, events=None):
        if events:
            if 'forward' in events:
                self.position[2] -= self.speed
            if 'backward' in events:
                self.position[2] += self.speed
            if 'left' in events:
                self.position[1] += self.speed
            if 'right' in events:
                self.position[1] -= self.speed
            if 'reset' in events:
                self.position = self.originalPosition
            if "fire" in events:
                print("")

        self.node_path.setHpr(self.node_path, *self.position)

    def move(self, speed: list):
        self.position[0] += speed[0]
        self.position[1] += speed[1]
        self.position[2] += speed[2]
        self.node_path.setHpr(self.node_path, *speed)

    def collision(self, other):
        if other.kind == "basic":
            pub.sendMessage("found_gold")
        elif other.kind == "flag":
            pub.sendMessage("new_basic")