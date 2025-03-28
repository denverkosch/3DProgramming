from direct.showbase.ShowBase import ShowBase
from direct.task import Task
import sys
from pubsub import pub
from direct.showbase.InputStateGlobal import inputState
from game_logic import GameLogic
from player_view import PlayerView

controls = {
    "r": 'reset',
}

held_keys = {
    "w": 'forward',
    "a": 'left',
    "s": 'backward',
    "d": 'right',
}

class Main(ShowBase):
    def go(self):
        pub.subscribe(self.new_player_object, 'create')
        self.player = None
        #load the world
        self.game_logic.load_world()

        self.taskMgr.add(self.tick)

        self.input_events = {}
        for key in controls:
            self.accept(key, self.input_event, [controls[key]])

        for key in held_keys:
            inputState.watchWithModifiers(held_keys[key], key)

        self.run()

    def input_event(self, event):
        self.input_events[event] = True

    def tick(self, task):
        if self.input_events:
            pub.sendMessage('input', events=self.input_events)
        
        self.move_player(self.input_events)

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

        self.taskMgr.doMethodLater(0.1, self.setCameraBehindPlayer, 'set_camera_task')

    # Delay and set the camera behind the player once the view object has been created
    def setCameraBehindPlayer(self, task):
        if not hasattr(self.player, "node_path"):
            return task.again
        ship_node = self.player.node_path.find("**/ship")
        if ship_node.isEmpty():
            print("Error: Ship node not found!")
            return task.again
        self.camera.reparentTo(ship_node)
        self.camera.setPos(0, -60, 35)
        self.camera.lookAt(ship_node)

        return task.done


    def move_player(self, events=None):
        speed = [0, 0, 0]
        delta = 1.0

        if inputState.isSet('forward'):
            speed[2] = -delta
        if inputState.isSet('backward'):
            speed[2] = delta
        if inputState.isSet('left'):
            speed[1] = delta
        if inputState.isSet('right'):
            speed[1] = -delta

        self.player.move(speed)


    def __init__(self):
        ShowBase.__init__(self)
        self.disableMouse()
        self.render.setShaderAuto()

        self.instances = []
        self.player = None
        pub.subscribe(self.new_player_object, 'create')

        # create model and view
        self.game_logic = GameLogic()
        self.player_view = PlayerView(self.game_logic)



if __name__ == '__main__':
    app = Main()
    app.go()


'''
    Notes to self:
    Need to fix the sun to start rotating around the world
    Need to add a skybox to the world object to make it look like the player is on a planet and not just floating in space (Not neccesary at the moment)
'''