from panda3d.core import Quat
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
            q = Quat()
            q.setHpr((self.x_rotation, self.y_rotation, self.z_rotation))
            delta_x = None
            delta_y = None
            delta_z = None
            if 'forward' in events:
                forward = q.getForward()

                delta_x = forward[0]
                delta_y = forward[1]
                delta_z = forward[2]

            if 'backward' in events:
                forward = q.getForward()

                delta_x = -forward[0]
                delta_y = -forward[1]
                delta_z = -forward[2]

            if 'left' in events:
                right = q.getRight()

                delta_x = -right[0]
                delta_y = -right[1]
                delta_z = -right[2]

            if 'right' in events:
                right = q.getRight()

                delta_x = right[0]
                delta_y = right[1]
                delta_z = right[2]

            if 'reset' in events:
                self.position = self.originalPosition

            if delta_x is not None:
                x, y, z = self.position
                self.position = (x + delta_x*self.speed, y + delta_y*self.speed, z + delta_z*self.speed)