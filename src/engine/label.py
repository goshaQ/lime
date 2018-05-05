class Label:
    """
    Representation of a label characterizing a node or property.
    
    Attributes:
        _id (int): A label's id.
        _value (str): The value of a label.
    """

    def __init__(self, id, value):
        self._id = id
        self._value = value

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, val):
        self._id = val

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val
