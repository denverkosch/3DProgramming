from pubsub import pub
from game_object import GameObject
from player_object import PlayerObject
from sun import Sun
from enemy_ship import EnemyShip
from cannonball import Cannonball
from random import randint

class GameLogic:
    def __init__(self):
        self.properties = {}
        self.game_objects = {}

        self.objMap = {
            "player": PlayerObject,
            "sun": Sun,
            "ship": EnemyShip,
            "cannonball": Cannonball,
            "world": GameObject,
            "ambient": GameObject
        }

        self.next_id = 0 # Next available ID for a game object when it is created

    def create_object(self, position, kind, size, can_collide=True):
        obj = None
        if kind in self.objMap:
            obj = self.objMap[kind](position, kind, self.next_id, size, can_collide=can_collide)
        else:
            raise ValueError(f"Unknown object type: {kind}")
        self.next_id += 1
        self.game_objects[obj.id] = obj

        pub.sendMessage('create', game_object=obj)
        return obj

    def tick(self):
        for obj in list(self.game_objects.values()):
            obj.tick()
    
    def load_world(self):
        self.create_object([0, 0, 0], "player", [.35, 1, 1])
        self.create_object([0, 0, 0], "world", [250 ,250 ,250], can_collide=False)
        self.create_object([67, 0, 0], "sun", [1, 1, 1], can_collide=False)
        self.create_object([0, 0, 0], 'ambient', [1, 1, 1], can_collide=False)

    def fire_cannonball(self, position, size=[1, 1, 1]):
        self.create_object(position, "cannonball", size)

    def spawn_enemy(self, size=[.35, 1, 1]):
            x = randint(0, 360)
            y = randint(0, 360)
            self.create_object([x, y, 0], "ship", [.35, 1, 1])


    def get_property(self, key):
        return self.properties[key] if key in self.properties else None
    
    def set_property(self, key, value):
        self.properties[key] = value