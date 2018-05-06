class Node:
    """
    Representation of a single node.
    
    Attributes:
        _id (int): A record's id.
        _label (Label): Label of a node.
        _next_rel (Relationship): The first relationship connected to a node.
        _next_prop (Property): The first property associated with a node.
    """

    def __init__(self, id, label, next_prop=None, next_rel=None):
        self._id = id
        self._label = label
        self._next_prop = next_prop
        self._next_rel = next_rel

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, label):
        self._label = label

    @property
    def next_prop(self):
        return self._next_prop

    @next_prop.setter
    def next_prop(self, next_prop):
        self._next_prop = next_prop

    @property
    def next_rel(self):
        return self._next_rel

    @next_rel.setter
    def next_rel(self, next_rel):
        self._next_rel = next_rel
