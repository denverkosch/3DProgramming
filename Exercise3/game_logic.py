from pubsub import pub
from game_object import GameObject
from player_object import PlayerObject

class GameLogic:
    def __init__(self):
        self.properties = {}
        self.game_objects = {}

        self.next_id = 0 # Next available ID for a game object when it is created

    def create_object(self, position, kind):
        if kind == 'player':
            obj = PlayerObject(position, kind, self.next_id)
        else:
            obj = GameObject(position, kind, self.next_id)

        self.next_id += 1
        self.game_objects[obj.id] = obj

        pub.sendMessage('create', game_object=obj)
        return obj

    def tick(self):
        for id in self.game_objects:
            self.game_objects[id].tick()
    
    def load_world(self):
        self.create_object([0,0,0], "ship")
        self.create_object([0, -20, 0], "player")
        self.create_object([0, 0, 0], "world")
        self.create_object([0, 0, 0], "sun")

    def get_property(self, key):
        if key in self.properties:
            return self.properties[key]
        return None
    
    def set_property(self, key, value):
        self.properties[key] = value