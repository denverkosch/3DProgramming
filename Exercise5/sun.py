from game_object import GameObject

class Sun(GameObject):
    def __init__(self, position, kind, id, size, can_collide=False):
        super().__init__(position, kind, id, size, can_collide=can_collide)

    def tick(self):
        self.position = (self.position[0], (self.position[1] + 1) % 360, self.position[2])