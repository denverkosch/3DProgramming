from pubsub import pub
from game_object import GameObject
from player_object import PlayerObject
from sun import Sun

class GameLogic:
    def __init__(self):
        self.properties = {}
        self.game_objects = {}

        self.next_id = 0 # Next available ID for a game object when it is created

    def create_object(self, position, kind):
        obj = None
        if kind == "player":
            obj = PlayerObject(position=position, kind=kind, id=self.next_id)
        elif kind == "sun":
            obj = Sun(position=position, kind=kind, id=self.next_id)
        else:
            obj = GameObject(position=position, kind=kind, id=self.next_id)

        self.next_id += 1
        self.game_objects[obj.id] = obj

        pub.sendMessage('create', game_object=obj)
        return obj

    def tick(self):
        for id in self.game_objects:
            self.game_objects[id].tick()
    
    def load_world(self):
        self.create_object(position=[0, 0, 0], kind="player")
        self.create_object(position=[0, 0, 0], kind="world")
        self.create_object(position=[90-23, 0, 0], kind="sun")
        self.create_object(position=[0,0,0], kind='ambient')


    def get_property(self, key):
        return self.properties[key] if key in self.properties else None
    
    def set_property(self, key, value):
        self.properties[key] = value