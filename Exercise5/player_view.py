from view_object import ViewObject
from pubsub import pub

class PlayerView:
    def __init__(self, game_logic):
        self.game_logic = game_logic
        self.view_objects = {}

        pub.subscribe(self.new_game_object, 'create')

    def tick(self):
        for key in self.view_objects:
            self.view_objects[key].tick()

    def new_game_object(self, game_object):
        self.view_objects[game_object.id] = ViewObject(game_object)