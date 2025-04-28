import random
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
import sys
from pubsub import pub
from direct.showbase.InputStateGlobal import inputState
from game_logic import GameLogic
from player_view import PlayerView
from panda3d.core import LineSegs, CollisionTraverser, CollisionHandlerQueue
from direct.gui.OnscreenText import OnscreenText

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
        self.cTrav = CollisionTraverser()

        self.collision_queue = CollisionHandlerQueue()

        pub.subscribe(self.new_collider, 'collider')
        pub.subscribe(self.new_object, 'create')
        pub.subscribe(self.hitFlag, "new_basic")
        pub.subscribe(self.endGame, "found_gold")
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

        self.taskMgr.add(self.traverse_task, "traverse")

        self.run()

    def input_event(self, event):
        self.input_events[event] = True

    def new_collider(self, collider):
        self.cTrav.addCollider(collider, self.collision_queue)

    def traverse_task(self, task):
        self.cTrav.traverse(self.render)
        return task.cont

    def hitFlag(self):
        self.game_logic.new_basic()
        text = OnscreenText(
            text="You have reached the flag! The gold appears...",
            pos=(0, 0.8),
            scale=0.07,
            fg=(1, 1, 0, 1)
        )

        def remove_text(task):
            text.destroy()
            return Task.done
        
        self.taskMgr.doMethodLater(5, remove_text, "removeGoldText")

                               
    def tick(self, task):
        for entry in self.collision_queue.entries:
            into_go = entry.into_node.get_python_tag('game_object')
            from_go = entry.from_node.get_python_tag('game_object')
            into_go.collision(from_go)
            from_go.collision(into_go)


        if self.input_events:
            pub.sendMessage('input', events=self.input_events)
        
        self.move_player()

        self.game_logic.tick()
        self.player_view.tick()


        if self.game_logic.get_property("exit"):
            text = OnscreenText(
                text="You have found the gold! The game is over...",
                pos=(0, 0.8),
                scale=0.07,
                fg=(1, 1, 0, 1)
            )
            
            self.taskMgr.doMethodLater(5, sys.exit, "terminate")

        self.input_events.clear()
        return task.cont


    def new_object(self, game_object):
        self.new_player_object(game_object)
        self.new_flag_object(game_object)

    def new_player_object(self, game_object):
        if game_object.kind != 'player':
            return
        self.player = game_object

        self.taskMgr.add(self.setCameraBehindPlayer, 'set_camera_task')

    def new_flag_object(self, game_object):
        if game_object.kind != 'basic':
            return
        self.flag = game_object


    # Delay and set the camera behind the player once the view object has been created
    def setCameraBehindPlayer(self, task):
        if not hasattr(self.player, "node_path"):
            return task.again
        ship_node = self.player.node_path.find("**/model")
        if ship_node.isEmpty():
            print("Error: Ship node not found!")
            return task.again
        self.camera.reparentTo(ship_node)
        self.camera.setPos(0, -60, 45)
        # self.camera.setPos(0, -60, 0)
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

    def endGame(self):
        self.game_logic.set_property("exit", True)


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

        self.camera.reparentTo(self.render)
        self.camera.setPos(0, 0, -75)
        self.camera.lookAt(0, 0, 0)



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