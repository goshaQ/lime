import config as cfg
from engine.node import Node


class GraphEngine:
    """
    The graph database engine that performs operations on data stored in the database. 
    
    Attributes:
        _lb_cache (dict): A label cache that contains all labels in the graph database.
            Has the following format:
            {'label.value': 'label'}.
        _index (dict): An index that improves the speed of data retrieval. Is built on label and at least one property.
            Has the following format:
            {'node.label.id': '{'(node.next_prop.label.id, ...)': '{'(node.next_prop.value, ...)': '(node.id, ...)'}'}'}
    """

    def __init__(self):
        # TODO: Implement
        self._lb_cache = dict()
        self._index = dict()

    def create_node(self, node):
        """
        Creates a new node.
        
        :param node: A pair (<label>, <properties>) corresponding to a node.
        :return: Void
        """

        label, next_prop = node

        # Before write to the storage dedupe the labels
        label = self._dedupe_label(label)
        next_prop = self._dedupe_next_prop(next_prop)

        # TODO: Insert into the persistent storage
        created_node = Node(cfg.INV_ID, label, next_prop)  #
        label, next_prop = created_node.label, created_node.next_prop

        # Add new labels to the corresponding cache
        self._lb_cache[label.value] = label
        while next_prop is not None:
            self._lb_cache[next_prop.label] = next_prop.label
            next_prop = next_prop.next_prop

        # Update index (if any)
        if not self._index:
            lookup = self._index_lookup((label, next_prop))
            for key, value in lookup.values():
                if value not in self._index[label.id][key]:
                    self._index[label.id][key][value] = list()
                self._index[label.id][key][value].append(created_node.id)

    def create_relationship(self, first_node, second_node, relationship):
        """
        Creates new relationships between nodes that match 'first_node' and 'second_node'.
        
        :param first_node: A pair (<label>, <properties>) corresponding to the node at the start of a relationship.
        :param second_node: A pair (<label>, <properties>) corresponding to the node at the end of a relationship.
        :param relationship: A triplet (<label>, <properties>, <direction>) corresponding to a relationship.
        :return: Void
        """
        label, next_prop, direction = relationship

        label = self._dedupe_label(label)
        next_prop = self._dedupe_next_prop(next_prop)

        is_directed = 0
        if direction == 1:
            is_directed = 1
        elif direction == -1:
            is_directed = 1
            first_node, second_node = second_node, first_node

        first_label, first_next_prop = first_node
        second_label, second_next_prop = second_node

        first_label = self._dedupe_label(first_label)
        first_next_prop = self._dedupe_next_prop(first_next_prop)
        retrieved_first_node = self._retrieve_node((first_label, first_next_prop))

        second_label = self._dedupe_label()
        second_next_prop = self._dedupe_next_prop(second_next_prop)
        retrieved_second_node = self._retrieve_node((second_label, second_next_prop))

        for first in retrieved_first_node:
            for second in retrieved_second_node:
                # TODO: Create relationship between these nodes
                pass

    def create_index(self, node):
        """
        Creates index on nodes that have label and properties in accordance with the provided template.
        
        :param node: A pair (<label>, <properties>) corresponding to the template based on which index will be created.
        :return: Void
        """

        pass

    def delete_node(self, node):
        """
        Deletes all nodes that match 'node'.
        
        :param node: A pair (<label>, <properties>) corresponding to a node.
        :return: Void
        """

        # TODO: Implement
        pass

    def delete_relationship(self, first_node, second_node, relationship):
        """
        Deletes all relationships that match 'relationship' between nodes that match 'first_node' and 'second_node'..
        
        :param first_node: A pair (<label>, <properties>) corresponding to the node at the start of a relationship.
        :param second_node: A pair (<label>, <properties>) corresponding to the node at the end of a relationship.
        :param relationship: A triplet (<label>, <properties>, <direction>) corresponding to a relationship.
        :return: Void
        """

        # TODO: Implement
        pass

    def match_pattern(self, nodes, relationships):
        """
        Matches the pattern that contain several nodes and relationships connecting them.
        
        :param nodes: List of pairs (<label>, <properties>) for each node.
        :param relationships: List of triplets (<label>, <properties>, <direction>) for each relation.
            Must be provided if 'nodes' contain more than one node.
        :return: List of all nodes that match the pattern (Might be changed?).
        """

        # TODO: Implement
        pass

    def _index_lookup(self, node):
        """
        Finds the pointer to the index record corresponding to a node. 
        
        :param node: A pair (<label>, <properties>) corresponding to a node.
        :return: Dictionary which has the following format:
            {'(node.next_prop.label.id, ...)': '(node.next_prop.value, ...)'}
        """
        label, next_prop = node

        conformity = {}
        while next_prop is not None:
            if label.id in self._index:
                keys = self._index[label.id].keys()
                for key in keys:
                    if next_prop.label.id in key:
                        if key not in conformity:
                            conformity[key] = dict()
                        conformity[key][next_prop.label.id] = next_prop.value
            next_prop = next_prop.next_prop

        result = {}
        for key, value in conformity.items():
            keys = value.keys()
            if set(key) == set(keys):
                values = value.values()
                result[key] = tuple([values[k] for k in key])

        return result

    def _retrieve_node(self, node):
        """
        Retrieves all nodes that match 'node' from the persistent storage
        
        :param node: A pair (<label>, <properties>) corresponding to a node.
        :return: List of all nodes that match 'node'.
        """

        label, next_prop = node

        nodes_to_retrieve = set()

        lookup = self._index_lookup(node) if not self._index else {}
        if not lookup:
            key, value = lookup.popitem()
            nodes_to_retrieve = self._index[label.id][key][value]

        # TODO: Retrieve nodes from the persistent storage
        retrieved_nodes = list()  #

        if not lookup:
            node_properties = set()
            while next_prop is not None:
                node_properties.add(next_prop.label.id)
                next_prop = next_prop.next_prop

            filtered_retrieved_nodes = list()
            for retrieved_node in retrieved_nodes:
                next_prop = retrieved_node.next_prop

                retrieved_node_properties = set()
                while next_prop is not None:
                    retrieved_node_properties.add(next_prop.label.id)
                    next_prop = next_prop.next_prop

                if node_properties.issubset(retrieved_node_properties):
                    filtered_retrieved_nodes.append(retrieved_node)
            retrieved_nodes = filtered_retrieved_nodes

        return retrieved_nodes

    def _dedupe_next_prop(self, next_prop):
        """
        Resolves duplicate labels of each property in the chain starting from 'next_prop'.
        
        :param next_prop: The first property in the chain the labels of which should be be deduped.
        :return: Property.
        """

        while next_prop is not None:
            next_prop.label = self._dedupe_label(next_prop.label)
            next_prop = next_prop.next_prop
        return next_prop

    def _dedupe_label(self, label):
        """
        Resolves duplicate labels.
        
        :param label: A label to be deduped.
        :return: Label.
        """

        return self._lb_cache[label.value] if label.value in self._lb_cache else label
