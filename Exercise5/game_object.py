
class GameObject:
    def __init__(self, position, kind, id, size, node_path=None, can_collide=True):
        self.position = position
        self.kind = kind
        self.id = id
        self.size = size
        self.node_path = base.render.attachNewNode( f"{kind}" ) if node_path is None else node_path # type: ignore
        self.can_collide = can_collide


    @property
    def can_collide(self):
        return self._can_collide
    
    @can_collide.setter
    def can_collide(self, value):
        self._can_collide = value

    @property
    def position(self):
        return self._position
    
    @position.setter
    def position(self, value):
        if not hasattr(self, '_position') or self._position is None:
            self._position = [v for v in value]
        else:
            self._position[0] = value[0]
            self._position[1] = value[1]
            self._position[2] = value[2]

    @property
    def kind(self):
        return self._kind
    
    @kind.setter
    def kind(self, value):
        self._kind = value

    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, value):
        self._id = value

    @property
    def size(self):
        return self._size
    
    @size.setter
    def size(self, value):
        self._size = value

    @property
    def node_path(self):
        return self._node_path
    
    @node_path.setter
    def node_path(self, value):
        self._node_path = value

    def tick(self):
        pass

    def collision(self, other):
        pass