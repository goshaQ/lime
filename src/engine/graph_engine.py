class GraphEngine:
    """
        The graph database engine that performs operations on data stored in the database. 
    """

    def __init__(self):
        # TODO: Implement
        pass

    def create_node(self, node):
        """
        Creates new node 'node'.
        
        :param node: A pair (<label>, <properties>) corresponding to a node.
        :return: Void
        """

        # TODO: Implement
        pass

    def create_relationship(self, first_node, second_node, relationship):
        """
        Creates new relationships 'relationship' between nodes that match 'first_node' and 'second_node'.
        
        :param first_node: A pair (<label>, <properties>) corresponding to the node at the start of a relationship.
        :param second_node: A pair (<label>, <properties>) corresponding to the node at the end of a relationship.
        :param relationship: A triplet (<label>, <properties>, <direction>) corresponding to a relationship.
        :return: Void
        """

        # TODO: Implement
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
