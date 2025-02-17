from direct.showbase.ShowBase import ShowBase
from direct.task import Task
import sys
from pubsub import pub

from game_logic import GameLogic
from player_view import PlayerView

controls = {
    "w": 'forwaard',
    "a": 'left',
    "s": 'backward',
    "d": 'right',
    "r": 'reset'
    # "w-up": 'stopForward',
    # "a-up": 'stopLeft',
    # "s-up": 'stopBackward',
    # "d-up": 'stopRight',
}

class Main(ShowBase):
    def go(self):
        pub.subscribe(self.new_player_object, 'create')
        self.player = None
        #load the world
        self.game_logic.load_world()

        self.camera.set_pos(0,-20,0)
        self.camera.look_at(0,0,0)
        self.taskMgr.add(self.tick)

        self.input_events = {}
        for key in controls:
            self.accept(key, self.input_event, [controls[key]])

        self.run()

    def input_event(self, event):
        self.input_events[event] = True

    def tick(self, task):

        if self.input_events:
            pub.sendMessage('input', events=self.input_events)
        
        #give model and view chance to do something
        self.game_logic.tick()
        self.player_view.tick()


        if self.game_logic.get_property("exit"):
            sys.exit()

        self.input_events.clear()
        return Task.cont
    
    def new_player_object(self, game_object):
        if game_object.kind != 'player':
            return
        self.player = game_object

    def __init__(self):
        ShowBase.__init__(self)
        self.disableMouse()
        self.render.setShaderAuto()

        # create model and view
        self.game_logic = GameLogic()
        self.player_view = PlayerView(self.game_logic)


if __name__ == '__main__':
    app = Main()
    app.go()