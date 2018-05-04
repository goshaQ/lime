class Relationship:
    """
        Representation of a relationship that connects two nodes.
        
        Attributes:
            _id (int): A relationships' id.
            _is_directed (bool): Tells whether a relationship is directed or not.
            _first_node (Node): ID of the node at the start of a relationship.
            _second_node (Node): ID of the node at the end of a relationship.
            _label (Label): Label of a relationship.
            _next_prop (Property): The first property associated with a relationship.
            _first_prev_rel (Relationship): The next relationship of the start node.
            _first_next_rel (Relationship): The previous relationship of the start node.
            _second_prev_rel (Relationship): The next relationship of the end node.
            _second_next_rel (Relationship): The previous relationship of the end node.
    """

    def __init__(self, id, is_directed, first_node, second_node, label, next_prop,
                 first_prev_rel, first_next_rel, second_prev_rel, second_next_rel):
        self._id = id
        self._is_directed = is_directed
        self._first_node = first_node
        self._second_node = second_node
        self._label = label
        self._next_prop = next_prop
        self._first_prev_rel = first_prev_rel
        self._first_next_rel = first_next_rel
        self._second_prev_rel = second_prev_rel
        self._second_next_rel = second_next_rel

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, val):
        self._id = val

    @property
    def is_directed(self):
        return self._is_directed

    @is_directed.setter
    def is_directed(self, val):
        self._is_directed = val

    @property
    def first_node(self):
        return self._first_node

    @first_node.setter
    def first_node(self, val):
        self._first_node = val

    @property
    def second_node(self):
        return self._second_node

    @second_node.setter
    def second_node(self, val):
        self._second_node = val

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, val):
        self._label = val

    @property
    def next_prop(self):
        return self._next_prop

    @next_prop.setter
    def next_prop(self, val):
        self._next_prop = val

    @property
    def first_prev_rel(self):
        return self._first_prev_rel

    @first_prev_rel.setter
    def first_prev_rel(self, val):
        self._first_prev_rel = val

    @property
    def first_next_rel(self):
        return self._first_next_rel

    @first_next_rel.setter
    def first_next_rel(self, val):
        self._first_next_rel = val

    @property
    def second_prev_rel(self):
        return self._second_prev_rel

    @second_prev_rel.setter
    def second_prev_rel(self, val):
        self._second_prev_rel = val

    @property
    def second_next_rel(self):
        return self._second_next_rel

    @second_next_rel.setter
    def second_next_rel(self, val):
        self._second_next_rel = val
