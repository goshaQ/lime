class Figure(object):
    """
        Attributes:
            x: A float value representing x position on the board
            y: A float value representing y position on the board
            orientation: A string representing orientation on the board (yaw)
            color: A string representing the color of the figure - red/green/blue
            shape: A string representing the shape of the figure - rectange/circle/triangle
            size: A string representing the size of the figure - small/medium/big
    """

    def __init__(self, id, x, y, orientation, color,
        shape, size):
        self.id = id
        self.x = x
        self.y = y
        self.orientation = orientation
        self.color = color
        self.shape = shape
        self.size = size