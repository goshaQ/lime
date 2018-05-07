from rtree import index

class RelationCreator():

    def __init__(self):
        self._ind = index.Index()
        self._count = 0
        self._nearest = 4

    def add_objects(self, objects):
        """
        A method for adding objects to the tree
        :param objects: A two-dimensional tuple [[label, properties[0]], ..., [label, properties[0]]] with object's coordiantes
        """
        for obj in objects:
            try:
                self._ind.insert(id=self._count, coordinates=(float(obj[1].value), float(obj[1].next_prop.value), float(obj[1].value), float(obj[1].next_prop.value)), obj=obj)
                self._count += 1
            except Exception:
                print("RTFM.")

    def get_relations(self, object):
        """
        A method for getting relations for every object

        :return left: A tuple of the object [label, properties[0]] which is in the left side 
        :return right: A tuple of the object [label, properties[0]] which is in the right side
        :return top: A tuple of the object [label, properties[0]] which is in the top side
        :return down: A tuple of the object [label, properties[0]] which is in the down side
        """
        left = None
        right = None
        up = None
        down = None
        try:
            nearest = [n.object for n in self._ind.nearest((float(object[1].value), float(object[1].next_prop.value)), self._nearest, objects=True)]
            
            obj_x = float(object[1].value)
            obj_y = float(object[1].next_prop.value)
            for n in nearest:
                x = float(n[1].value)
                y = float(n[1].next_prop.value)
                if obj_x < x:
                    right = n
                elif obj_x > x:
                    left = n
                elif obj_y < y:
                    up = n
                elif obj_y > y:
                    down = n
        except Exception:
            print("RTFM.")
        return left, right, up, down
        

        