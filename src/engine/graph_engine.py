import config as cfg

from src.engine.node import Node
from src.engine.relationship import Relationship

from src.io.io import Io


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
        self._io = Io()
        self._lb_cache = self._init_lb_cache()
        self._index = dict()

    def _init_lb_cache(self):
        """
        Initializes the label cache.
        
        :return: Dictionary which has the following format:
            {'label.value': 'label'}.
        """

        lb_cache = dict()
        for label in self._io.get_labels_by_id(set()):
            lb_cache[label.value] = label
        return lb_cache

    def create_node(self, node):
        """
        Creates the new node.
        
        :param node: A pair (<label>, <properties>) corresponding to a node.
        :return: Void
        """

        label, next_prop = node

        # Before write to the storage dedupe the labels
        label = self._dedupe_label(label)
        next_prop = self._dedupe_next_prop(next_prop)

        created_node = self._io.write_node(Node(cfg.INV_ID, label, next_prop))
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

        retrieved_first_node = self._retrieve_node(first_node)
        retrieved_second_node = self._retrieve_node(second_node)

        for first in retrieved_first_node:
            for second in retrieved_second_node:
                first_prev_rel = first.next_rel
                if first_prev_rel is not None:
                    while first_prev_rel.next_rel is not None:
                        first_prev_rel = first_prev_rel.next_rel
                second_prev_rel = second.next_rel
                if second_prev_rel is not None:
                    while second_prev_rel.next_rel is not None:
                        second_prev_rel = second_prev_rel.next_rel

                created_relationship = self._io.write_relation(
                    Relationship(cfg.INV_ID, is_directed, first, second, label, next_prop,
                                 first_prev_rel, None, second_prev_rel, None))
                label, next_prop = created_relationship.label, created_relationship.next_prop

                # Add new labels to the corresponding cache
                self._lb_cache[label.value] = label
                while next_prop is not None:
                    self._lb_cache[next_prop.label] = next_prop.label
                    next_prop = next_prop.next_prop

    def create_index(self, node):
        """
        Creates index on nodes that have label and properties in accordance with the provided template.
        
        :param node: A pair (<label>, <properties>) corresponding to the template based on which index will be created.
        :return: Void
        """

        label, next_prop = node

        label = self._dedupe_label(label)
        next_prop = self._dedupe_next_prop(next_prop)
        key_property = tuple(self._unroll_next_prop(next_prop).keys())

        if label.id not in self._index:
            self._index[label.id] = dict()
        self._index[label.id][key_property] = dict()

        retrieved_node = self._retrieve_node((label, next_prop))
        for ind_node in retrieved_node:
            properties = self._unroll_next_prop(ind_node.next_prop)

            key_value = list()
            for k in key_property:
                key_value.append(properties[k])
            key_value = tuple(key_value)

            if key_value not in self._index[label.id][key_property]:
                self._index[label.id][key_property] = list()
            self._index[label.id][key_property][key_value].append(ind_node.id)

    def delete_node(self, node):
        """
        Deletes all nodes that match 'node'.
        
        :param node: A pair (<label>, <properties>) corresponding to a node.
        :return: Void
        """

        retrieved_node = self._retrieve_node(node)
        for ind_node in retrieved_node:
            self._io.del_node(ind_node.id)

    def delete_relationship(self, first_node, second_node, relationship):
        """
        Deletes all relationships that match 'relationship' between nodes that match 'first_node' and 'second_node'.
        
        :param first_node: A pair (<label>, <properties>) corresponding to the node at the start of a relationship.
        :param second_node: A pair (<label>, <properties>) corresponding to the node at the end of a relationship.
        :param relationship: A triplet (<label>, <properties>, <direction>) corresponding to a relationship.
        :return: Void
        """

        retrieved_relationship = self._retrieve_relationship(first_node, second_node, relationship)
        for ind_relationship_id in [relationship_id for _, _, relationship_id in retrieved_relationship]:
            self._io.del_relation(ind_relationship_id)

    def match_pattern(self, nodes, relationships):
        """
        Matches the pattern that contain several nodes and relationships connecting them.
        
        :param nodes: List of pairs (<label>, <properties>) for each node.
        :param relationships: List of triplets (<label>, <properties>, <direction>) for each relation.
            Must be provided if 'nodes' contain more than one node.
        :return: Dictionary which has the following format:
            {'idx of the obj': 'nodes'}
        """

        retrieved_node = dict()
        if len(nodes) == 1:
            retrieved_node[0] = self._retrieve_node(nodes.pop())
        else:
            iterator = iter(nodes)
            for first_node, second_node, relationship in zip(zip(iterator, iterator), relationships):
                # For now assume that this chain contains only one relationship
                retrieved_relationship = self._retrieve_relationship(first_node, second_node, relationship)
                retrieved_node[0] = [first_node for first_node, _, _ in retrieved_relationship]
                retrieved_node[1] = [second_node for _, second_node, _ in retrieved_relationship]

        return retrieved_node

    def _index_lookup(self, node):
        """
        Finds the pointer to the index record corresponding to a node. 
        
        :param node: A pair (<label>, <properties>) corresponding to a node.
        :return: Dictionary which has the following format:
            {'(node.next_prop.label.id, ...)': '(node.next_prop.value, ...)'}
        """
        label, next_prop = node

        conformity = dict()
        while next_prop is not None:
            if label.id in self._index:
                keys = self._index[label.id].keys()
                for key in keys:
                    if next_prop.label.id in key:
                        if key not in conformity:
                            conformity[key] = dict()
                        conformity[key][next_prop.label.id] = next_prop.value
            next_prop = next_prop.next_prop

        result = dict()
        for key, value in conformity.items():
            keys = value.keys()
            if set(key) == set(keys):
                values = value.values()
                result[key] = tuple([values[k] for k in key])

        return result

    def _retrieve_relationship(self, first_node, second_node, relationship):
        """
        Retrieves all relationships that match 'relationship' between nodes that match 'first_node' and 'second_node'.
        
        :param first_node: A pair (<label>, <properties>) corresponding to the node at the start of a relationship OR
            list of already retrieved nodes.
        :param second_node: A pair (<label>, <properties>) corresponding to the node at the end of a relationship OR
            list of already retrieved nodes.
        :param relationship: A triplet (<label>, <properties>, <direction>) corresponding to a relationship.
        :return: List of triplets (<first_node>, <second_node>, <relationship_id>).
        """

        label, next_prop, direction = relationship
        label = self._dedupe_label(label)
        next_prop = self._dedupe_next_prop(next_prop)
        rel_properties = self._unroll_next_prop(next_prop)

        is_directed = 0
        if direction == 1:
            is_directed = 1
        elif direction == -1:
            is_directed = 1
            first_node, second_node = second_node, first_node

        retrieved_first_node = dict()
        if type(first_node) is tuple:
            for first in self._retrieve_node(first_node):
                retrieved_first_node[first.id] = first
        else:
            for first in first_node:
                retrieved_first_node[first.id] = first

        second_label = second_next_prop = second_properties = None
        retrieved_second_node = dict()
        if type(second_node) is tuple:
            second_label, second_next_prop = second_node

            second_label = self._dedupe_label(second_label)
            second_next_prop = self._dedupe_next_prop(second_next_prop)
            second_properties = self._unroll_next_prop(second_next_prop)
        else:
            for second in second_node:
                retrieved_second_node[second.id] = second

        retrieved_relationship = list()
        for first in retrieved_first_node:
            first_next_rel = first.next_rel
            while first_next_rel is not None:
                if type(first_next_rel) is not Relationship:
                    first_next_rel = self._io.read_relation(first_next_rel)

                appropriate = first_next_rel.label.id == label.id
                appropriate = appropriate and ((is_directed and
                              (not first_next_rel.is_directed or first_next_rel.first_node == first.id)) or
                              (not is_directed and not first_next_rel.is_directed))

                first_next_rel_properties = self._unroll_next_prop(first_next_rel.next_prop)
                appropriate = appropriate and (first_next_rel.next_prop is None or
                              (first_next_rel_properties is not None and
                              all(first_next_rel_properties[k] == v for k, v in rel_properties.items())))

                if appropriate:
                    second = None
                    if not retrieved_second_node:
                        if first_next_rel.second_node in retrieved_second_node:
                            second = retrieved_second_node[first_next_rel.second_node]
                    else:
                        second = self._io.read_node(first_next_rel.second_node)
                        retrieved_second_properties = self._unroll_next_prop(second.next_prop)

                        if second.label.id != second_label.id or (not (second_next_prop is None or
                                (retrieved_second_properties is not None and
                                    all(retrieved_second_properties[k] == v for k, v in second_properties.items())))):
                            second = None

                    if second is not None:
                        retrieved_relationship.append((first, second, first_next_rel.id))
                    first_next_rel = first_next_rel.first_next_rel
        return retrieved_relationship

    def _retrieve_node(self, node):
        """
        Retrieves all nodes that match 'node' from the persistent storage.
        
        :param node: A pair (<label>, <properties>) corresponding to a node.
        :return: List of all nodes that match 'node'.
        """

        label, next_prop = node

        label = self._dedupe_label(label)
        next_prop = self._dedupe_next_prop(next_prop)

        nodes_to_retrieve = set()

        # Perform lookup to find indexes
        lookup = self._index_lookup(node) if not self._index else dict()
        if not lookup:
            key, value = lookup.popitem()
            nodes_to_retrieve = self._index[label.id][key][value]

        retrieved_nodes = self._io.get_nodes_by_id(nodes_to_retrieve)

        # Filter the retrieved nodes
        node_properties = self._unroll_next_prop(next_prop)

        filtered_retrieved_nodes = list()
        for retrieved_node in retrieved_nodes:
            if retrieved_node.label.id == label.id:
                retrieved_node_properties = self._unroll_next_prop(retrieved_node.next_prop)

                if next_prop is None or (retrieved_node_properties is not None and
                        all(retrieved_node_properties[k] == v for k, v in node_properties.items())):
                    filtered_retrieved_nodes.append(retrieved_node)
        return filtered_retrieved_nodes

    @staticmethod
    def _unroll_next_prop(next_prop):
        """
        Unrolls the chain of properties starting from the provided link 'next_prop'.
        
        :param next_prop: The first link in the chain which should be be unrolled.
        :return: Dictionary which has the following format:
            {'next_prop.label.id': 'next_prop.value'}
        """

        properties = dict()
        while next_prop is not None:
            properties[next_prop.label.id] = next_prop.value
            next_prop = next_prop.next_prop
        return properties

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
