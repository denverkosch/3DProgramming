from direct.showbase.ShowBase import ShowBase
from direct.task import Task
import sys
from pubsub import pub
from direct.showbase.InputStateGlobal import inputState
from game_logic import GameLogic
from player_view import PlayerView
from panda3d.core import CollisionTraverser, CollisionHandlerQueue
from direct.gui.OnscreenText import OnscreenText


controls = {
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
        pub.subscribe(self.game_logic.fire_cannonball, 'shoot')
        pub.subscribe(self.enemy_destroyed, 'enemy_destroyed')

        self.player = None
        self.enemies_spawned = 0
        self.enemies_destroyed = 0
        
        
        self.game_logic.load_world()


        self.taskMgr.add(self.tick)

        self.input_events = {}
        for key in controls:
            self.accept(key, self.input_event, [controls[key]])

        for key in held_keys:
            inputState.watchWithModifiers(held_keys[key], key)

        self.taskMgr.add(self.traverse_task, "traverse")
        self.taskMgr.add(self.spawn_enemy_loop, "spawn_enemy_task")

        self.run()

    def input_event(self, event):
        self.input_events[event] = True

    def new_collider(self, collider):
        self.cTrav.addCollider(collider, self.collision_queue)

    def traverse_task(self, task):
        self.cTrav.traverse(self.render)
        return task.cont
                               
    def tick(self, task):
        if self.game_logic.get_property("exit"):
            OnscreenText(
                text="There are too many enemies! The game is over...",
                pos=(0, 0.8),
                scale=0.07,
                fg=(1, 1, 0, 1)
            )
            self.taskMgr.doMethodLater(5, sys.exit, "terminate")

        self.cTrav.traverse(self.render)
        for entry in self.collision_queue.entries:
            into_go = entry.into_node.get_python_tag('game_object')
            from_go = entry.from_node.get_python_tag('game_object')
            into_go.collision(from_go)

        if not self.game_logic.get_property("exit"):
            if self.input_events:
                pub.sendMessage('input', events=self.input_events)
            
            self.move_player()

        self.game_logic.tick()
        self.player_view.tick()

        self.input_events.clear()
        return task.cont

    def new_object(self, game_object):
        self.new_player_object(game_object)
        self.new_cannonball_object(game_object)

    def new_player_object(self, game_object):
        if game_object.kind != 'player':
            return
        self.player = game_object

        self.taskMgr.add(self.setCameraBehindPlayer, 'set_camera_task')

    def new_cannonball_object(self, game_object):
        if game_object.kind != 'cannonball':
            return

        def remove_cannonball(cannonball):
            pub.sendMessage("remove", id=cannonball.id)

        # Set the cannonball to be removed after 1 second
        self.taskMgr.doMethodLater(1, remove_cannonball, "remove_cannonball", extraArgs=[game_object])

    def enemy_destroyed(self, enemy, cannonball):
        pub.sendMessage("remove", id=cannonball.id)
        pub.sendMessage("remove", id=enemy.id)
        self.enemies_destroyed += 1
        self.enemies_spawned -= 1
        self.hud_text.text = f"Enemies destroyed: {self.enemies_destroyed} / {self.enemies_destroyed + self.enemies_spawned}"

    def spawn_enemy_loop(self, task):
        if self.player is None:
            return task.again
        if self.enemies_spawned >= 20:
            self.game_logic.set_property("exit", True)
            return task.done
        # Spawn an enemy ship every 2 seconds
        self.game_logic.spawn_enemy()
        self.enemies_spawned += 1
        self.hud_text.text = f"Enemies destroyed: {self.enemies_destroyed} / {self.enemies_spawned}"
        self.taskMgr.doMethodLater(2, self.spawn_enemy_loop, "spawn_enemy_task")
        return task.done

    # Delay and set the camera behind the player once the view object has been created
    def setCameraBehindPlayer(self, task):
        if not hasattr(self.player, "node_path"):
            return task.again
        ship_node = self.player.node_path.find("**/model")
        if ship_node.isEmpty():
            print("Error: Ship node not found!")
            return task.again
        self.camera.reparentTo(ship_node)
        self.camera.setPos(0, -70, 45) 
        self.camera.lookAt(ship_node)

        return task.done

    def move_player(self):
        speed = [0, 0, 0]
        delta = 1.0

        if inputState.isSet('forward') and not inputState.isSet('backward'):
            speed[1] = -delta
        if inputState.isSet('backward') and not inputState.isSet('forward'):
            speed[1] = delta*0.5
        if inputState.isSet('left') and not inputState.isSet('right'):
            speed[0] = delta
        if inputState.isSet('right') and not inputState.isSet('left'):
            speed[0] = -delta

        self.player.move(speed)


    def __init__(self):
        ShowBase.__init__(self)
        self.disableMouse()
        self.render.setShaderAuto()
        from panda3d.core import TextNode
        from direct.gui.OnscreenText import OnscreenText

        self.hud_text = OnscreenText(
            text="Enemies destroyed: 0 / 0",
            pos=(-1.3, 0.9),
            scale=0.07,
            fg=(1, 1, 1, 1),
            align=TextNode.ALeft,
            mayChange=True
        )

        self.instances = []
        self.player = None
        pub.subscribe(self.new_player_object, 'create')

        # create model and view
        self.game_logic = GameLogic()
        self.player_view = PlayerView(self.game_logic)

        self.camera.reparentTo(self.render)
        self.camera.setPos(0, 0, -75)
        self.camera.lookAt(0, 0, 0)

if __name__ == '__main__':
    app = Main()
    app.go()