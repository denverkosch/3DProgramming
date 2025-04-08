from direct.showbase.ShowBase import ShowBase
from direct.task import Task
import sys
from pubsub import pub
from direct.showbase.InputStateGlobal import inputState
from game_logic import GameLogic
from player_view import PlayerView
from panda3d.core import LineSegs

controls = {
    "r": 'reset',
    "space": "fire"
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
        self.flag = None
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
        
        self.move_player()

        self.game_logic.tick()
        self.player_view.tick()


        if self.game_logic.get_property("exit"):
            sys.exit()

        self.input_events.clear()
        return task.cont
    
    def new_player_object(self, game_object):
        if game_object.kind == "flag":
            self.flag = game_object

            return
        if game_object.kind != 'player':
            return
        self.player = game_object

        self.taskMgr.add(self.setCameraBehindPlayer, 'set_camera_task')

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

    def move_player(self):
        speed = [0, 0, 0]
        delta = 1.0

        if inputState.isSet('forward') and not inputState.isSet('backward'):
            speed[2] = -delta
        if inputState.isSet('backward') and not inputState.isSet('forward'):
            speed[2] = delta*0.5
        if inputState.isSet('left') and not inputState.isSet('right'):
            speed[1] = delta
        if inputState.isSet('right') and not inputState.isSet('left'):
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

        self.create_world_axes()  # Create world axes for reference


    def create_world_axes(self):
        axis = LineSegs()
        axis.setThickness(2.0)

        # Z-axis (Red)
        axis.setColor(1, 0, 0, 1)
        axis.moveTo(0, 0, -100)
        axis.drawTo(0, 0, 100)

        # X-axis (Green)
        axis.setColor(0, 1, 0, 1)
        axis.moveTo(-100, 0, 0)
        axis.drawTo(100, 0, 0)

        # Y-axis (Blue)
        axis.setColor(0, 0, 1, 1)
        axis.moveTo(0, -100, 0)
        axis.drawTo(0, 100, 0)

        axis_node = axis.create()
        self.render.attachNewNode(axis_node)

if __name__ == '__main__':
    app = Main()
    app.go()


'''
    Notes to self:

    -   Need to add a skybox to the world object to make it look like the player is 
        on a planet and not just floating in space (Not neccesary at the moment)
'''