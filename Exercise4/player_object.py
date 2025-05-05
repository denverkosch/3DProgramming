from panda3d.core import NodePath
from pubsub import pub
from game_object import GameObject

class PlayerObject(GameObject):
    def __init__(self, position, kind, id, size, can_collide=True):
        super().__init__(position, kind, id, size, can_collide=can_collide)
        pub.subscribe(self.input_event, 'input')

        self.speed = 0.1
        self.originalPosition = position
        self.oldPosition = self.position.copy()
        self.can_move = True

    def input_event(self, events=None):
        if events:
            if 'reset' in events:
                self.position = self.originalPosition
                self.node_path.setHpr(self.node_path, *self.position)
            if "fire" in events:
                print("")

    def move(self, speed: list):
        self.oldPosition = self.position.copy()
        if not self.can_move and speed[2] < 0:
            speed[2] = 0
            base.taskMgr.doMethodLater(0.1, self.enable_movement, 'enable-movement-task') # type: ignore
        self.position[0] += speed[0]
        self.position[1] += speed[1]
        self.position[2] += speed[2]
        self.node_path.setHpr(self.node_path, *speed)

    def enable_movement(self, task):
        self.can_move = True
        return task.done

    def collision(self, other):
        if other.kind == "basic":
            self.can_move = False
            pub.sendMessage("found_gold")
        elif other.kind == "flag":
            pub.sendMessage("new_basic")
            