from rtree import index
from sideError import WrongSideValueError

class Engine:

    def __init__(self):
        self.idx = index.Index()
        self.count = 0
        self.by_size = dict()
        self.by_color = dict()
        self.by_shape = dict()
        print("Spatial index intialized.")
        
    """
        Add fidures to the Rtree

        Attributes:
            list_of_figures: A list with objects of type Figure.
    """
    def add_figures(self, list_of_figures):
        for f in list_of_figures:
            self.idx.insert(f.id, (f.x, f.y, f.x, f.y), f)
            self.count += 1
        self.__add_figures_by_color(list_of_figures)
        self.__add_figures_by_shape(list_of_figures)
        self.__add_figures_by_size(list_of_figures)

    def __add_figures_by_shape(self, figures):
        for f in figures:
            if f.shape in self.by_shape:
                self.by_shape[f.shape].append(f)
            else:
                self.by_shape[f.shape] = [f]

    def __add_figures_by_color(self, figures):
        for f in figures:
            if f.color in self.by_color:
                self.by_color[f.color].append(f)
            else:
                self.by_color[f.color] = [f]

    def __add_figures_by_size(self, figures):
        for f in figures:
            if f.size in self.by_size:
                self.by_size[f.size].append(f)
            else:
                self.by_size[f.size] = [f]


    """
        Get object between given coordiantes
    """
    def get_intersection_objects(self, x_left, y_bottom, x_right, y_top):
        result = [n.object for n in self.idx.intersection((x_left, y_bottom, x_right, y_top), objects=True)]
        return result


    """
        Get number of elements in the engine
    """
    def get_count(self):
        return self.count


    def get_by_size(self, size):
        return self.by_size[size]

    def get_by_color(self, color):
        return self.by_color[color]
    
    def get_by_shape(self, shape):
        return self.by_shape[shape]

    """
        Attributes:
            side: A string with side (right, left, top, bottom)
            figure: A figure object
    """
    def get_by_side(self, side, figure, k):
        if "top" == side:
            result = []
            self.__get_top(figure.x, figure.y, result, figure.name, k)
            return result
        elif "bottom" == side:
            result = []
            self.__get_bottom(figure.x, figure.y, result, figure.name, k)
            return result
        elif "right" == side:
            result = []
            self.__get_right(figure.x, figure.y, result, figure.name, k)
            return result
        elif "left" == side:
            result = []
            self.__get_left(figure.x, figure.y, result, figure.name, k)
            return result
        else:
            raise WrongSideValueError("Wrong side value") 
    
    def __get_top(self, x, y, result, name, k):
        nearest = [n.object for n in self.idx.nearest((x, y), k, objects=True)]
        temp = []
        for n in nearest:
            if n.y >= y and n.name not in result and n.name != name:
                result.append(n.name)
                temp.append(n)
        for t in temp:
            self.__get_top(t.x, t.y, result, name, k) 
    
    def __get_bottom(self, x, y, result, name, k):
        nearest = [n.object for n in self.idx.nearest((x, y), k, objects=True)]
        temp = []
        for n in nearest:
            if n.y <= y and n.name not in result and n.name != name:
                result.append(n.name)
                temp.append(n)
        for t in temp:
            self.__get_bottom(t.x, t.y, result, name, k)

    def __get_right(self, x, y, result, name, k):
        nearest = [n.object for n in self.idx.nearest((x, y), k, objects=True)]
        temp = []
        for n in nearest:
            if n.x >= x and n.name not in result and n.name != name:
                result.append(n.name)
                temp.append(n)
        for t in temp:
            self.__get_right(t.x, t.y, result, name, k)

    def __get_left(self, x, y, result, name, k):
        nearest = [n.object for n in self.idx.nearest((x, y), k, objects=True)]
        temp = []
        for n in nearest:
            if n.x <= x and n.name not in result and n.name != name:
                result.append(n.name)
                temp.append(n)
        for t in temp:
            self.__get_left(t.x, t.y, result, name, k)
            