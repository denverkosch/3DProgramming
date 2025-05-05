from view_object import ViewObject
from pubsub import pub

class PlayerView:
    def __init__(self, game_logic):
        self.game_logic = game_logic
        self.view_objects = {}

        pub.subscribe(self.new_game_object, 'create')
        pub.subscribe(self.remove_game_object, 'remove')

    def tick(self):
        for key in self.view_objects:
            self.view_objects[key].tick()

    def new_game_object(self, game_object):
        self.view_objects[game_object.id] = ViewObject(game_object)

    def remove_game_object(self, id):
        if id in self.view_objects:
            del self.view_objects[id]
            game_object = self.game_logic.game_objects[id]
            game_object.node_path.removeNode()
            if game_object.kind == "cannonball":
                game_object.relative_origin.removeNode()
            del self.game_logic.game_objects[id]