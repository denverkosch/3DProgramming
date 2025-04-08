from game_object import GameObject

class Sun(GameObject):
    def __init__(self, position, kind, id, size):
        super().__init__(position, kind, id, size)

    def tick(self):
        self.position = (self.position[0], (self.position[1] + 1) % 360, self.position[2])