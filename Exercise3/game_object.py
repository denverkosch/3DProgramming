
class GameObject:
    def __init__(self, position, kind, id, hpr=(0,0,0)):
        self.position = position
        self.kind = kind
        self.id = id
        self.hpr = hpr

    def tick(self):
        pass