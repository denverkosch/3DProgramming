from pubsub import pub
from game_object import GameObject
from player_object import PlayerObject
from sun import Sun
from random import randint

class GameLogic:
    def __init__(self):
        self.properties = {}
        self.game_objects = {}

        self.next_id = 0 # Next available ID for a game object when it is created

    def create_object(self, position, kind, size, can_collide=True):
        obj = None
        if kind == "player":
            obj = PlayerObject(position=position, kind=kind, id=self.next_id, size=size, can_collide=can_collide)
        elif kind == "sun":
            obj = Sun(position=position, kind=kind, id=self.next_id, size=size, can_collide=can_collide)
        else:
            obj = GameObject(position=position, kind=kind, id=self.next_id, size=size, can_collide=can_collide)
        self.next_id += 1
        self.game_objects[obj.id] = obj

        pub.sendMessage('create', game_object=obj)
        return obj

    def tick(self):
        for id in self.game_objects:
            self.game_objects[id].tick()
    
    def load_world(self):
        self.create_object(position=[0, 0, 0], kind="player", size=[1, .35, 1])
        self.create_object(position=[0, 0, 0], kind="world", size=[250 ,250 ,250], can_collide=False)
        self.create_object(position=[67, 0, 0], kind="sun", size=[1, 1, 1], can_collide=False)
        self.create_object(position=[0, 0, 0], kind='ambient', size=[1, 1, 1], can_collide=False)
        self.create_object(position=[0, 0, 0], kind="flag", size=[15, 1, 1])

    # making basic, easy functions for making new objects
    def new_basic(self, size=[1, 1, 1]):
        if not self.check_basic():
            x = randint(-75, 75)
            y = randint(-75, 75)
            self.create_object(position=[x, y, 0], kind="basic", size=size)

    # Check if a basic object is in the game
    def check_basic(self):
        for id in self.game_objects:
            if self.game_objects[id].kind == "basic":
                return True
        return False


    def get_property(self, key):
        return self.properties[key] if key in self.properties else None
    
    def set_property(self, key, value):
        self.properties[key] = value