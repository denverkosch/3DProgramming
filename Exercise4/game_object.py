class GameObject:
    def __init__(self, position, kind, id):
        self.position = position
        self.kind = kind
        self.id = id

    @property
    def position(self):
        return self._position
    
    @position.setter
    def position(self, value):
        self._position = value

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

    def tick(self):
        pass