from panda3d.core import Quat, NodePath
from pubsub import pub
from game_object import GameObject

class PlayerObject(GameObject):
    def __init__(self, position, kind, id):
        super().__init__(position, kind, id)
        pub.subscribe(self.input_event, 'input')

        self.speed = 0.1
        self.originalPosition = position

    def input_event(self, events=None):
        if events:
            if 'forward' in events:
                pass

            if 'backward' in events:
                pass

            if 'left' in events:
                pass

            if 'right' in events:
                pass

            if 'reset' in events:
                self.position = self.originalPosition