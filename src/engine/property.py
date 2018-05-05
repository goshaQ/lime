class Property:
    """
    Representation of a property associated with a node or relationship.
    
    Attributes:
        _id (int): A property's id.
        _type (PropertyType): The type of a property.
        _label (Label): Label of a property.
        _value (any?): The value of a property.
        _next_prop (Property): The next property associated with a node or relationship.
    """

    def __init__(self, id, type, label, value, next_prop):
        self._id = id
        self._type = type
        self._label = label
        self._value = value
        self._next_prop = next_prop

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, val):
        self._id = val

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, val):
        self._type = val

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, val):
        self._label = val

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val

    @property
    def next_prop(self):
        return self._next_prop

    @next_prop.setter
    def next_prop(self, val):
        self._next_prop = val
