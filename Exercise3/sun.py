from game_object import GameObject

class Sun(GameObject):
    def __init__(self, position, kind, id):
        super().__init__(position, kind, id)


    def tick(self):
        #rotating eternally
        print(self)
        self.position = (self.position[0], (self.position[1] + 1) % 360, self.position[2])
        print("sun position", self.position)