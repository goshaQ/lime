from rtree import index

class Engine:

    def __init__(self):
        self.idx = index.Index()
        self.count = 0
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