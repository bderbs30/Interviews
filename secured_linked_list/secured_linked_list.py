from secured_linked_list.secured_node import SecuredNode


class SecuredLinkedList:
    """
    A linked list where each node's hash depends on the subsequent nodes

    Notes:
        - Adding to the front is O(1) - no rehashing needed since nothing
          depends on the new head's hash yet
        - Modifications in the middle (insert, remove, update) are O(n)
          because all preceding nodes must be rehashed
        - Validation is O(n) - must check each node in the chain

    Attributes:
        head: Pointer to the first SecuredNode, or None if the list is empty
    """

    def __init__(self):

        self.head = None

    def _collect_nodes_up_to(self, index):
        """
        Traverse the list and collect nodes from head up to the given index (inclusive)
        
        Args:
            index: The last index to collect (inclusive)
        
        Returns:
            A list of SecuredNode objects from head to the specified index
            If the list is shorter than index, returns all available nodes
        
        TC O(index) 
        """
        nodes = []
        current = self.head
        i = 0
        while current is not None and i <= index:
            nodes.append(current)
            current = current.next
            i += 1
        return nodes

    def _rehash_nodes(self, nodes):
        """
        Recompute hash values for the given nodes from last to first
        
        This method rehashes only the provided nodes rather than the entire
        chain. The nodes list should contain all nodes that need rehashing,
        in head-to-tail order. The method iterates in reverse because each
        node's hash depends on the next node's hash
        
        Args:
            nodes: List of SecuredNode objects to rehash, in head-to-tail order
        
        TC O(len(nodes))
        """
        for i in range(len(nodes) - 1, -1, -1):
            nodes[i].recompute_hash()


    def add(self, value):
        """
        Add a new node with the given value to the front of the list

        Args:
            value: the string data to store in the new node

        TC O(1)
        """
        new_node = SecuredNode(value, self.head)
        self.head = new_node


    def remove(self, index):
        """
        Remove the node at the specified index

        Args:
            index: zero based position of the node to remove
        
        Raises:
            IndexError: if the list is empty or index is out of range

        TC O(index) as we need to rehash part of the list O(1) for the head
        """

        if self.head is None:
            raise IndexError("Cannot remove from empty list")

        if index < 0:
            raise IndexError("Index out of range")

        if index == 0:
            self.head = self.head.next
            return

        nodes = self._collect_nodes_up_to(index)
        nodes[index - 1].next = nodes[index].next

        self._rehash_nodes(nodes[:index])


    def insert(self, index, value):
        """
        Insert a new node with the given value at the specified index
        
        The new node takes the position at `index`, and the previous occupant
        (if any) shifts to index + 1. After insertion, all preceding nodes
        must be rehashed.
        
        Inserting at index 0 is equivalent to add() and is handled as a
        special case to avoid unnecessary rehashing
        
        Args:
            index: Zero-based position where the new node should be inserted.
                   Valid range is 0 to len(list) inclusive
            value: The string data to store in the new node
        
        Raises:
            IndexError: If index is negative or greater than list length
        
        TC O(index) due to rehashing. O(1) for inserting at head.
        """
        
        if index < 0:
            raise IndexError("Index out of range")
        
        if index == 0:
            self.add(value)
            return
        
        nodes = self._collect_nodes_up_to(index)
        next_node = nodes[index] if index < len(nodes) else None
        new_node = SecuredNode(value, next_node)
        nodes[index - 1].next = new_node
        
        self._rehash_nodes(nodes[:index])


    def is_valid_chain(self):
        """
        Check whether the entire chain has valid hashes

        Returns:
            True if all nodes have valid hashes, False if invalid for any node

        TC O(n) for valid chains but could return early for invalid nodes
        """
        return self.find_tampered_node() is None



    def find_tampered_node(self):
        """
        Find and return the first node with an invalid hash

        If a node in the middle is invalid this will return the node
        before it (the first one whose hash was invalid). This is because that node's
        hash depends on the invalid node's hash

        Returns:
            The first SecuredNode with an invalid hash, or None if the entire chain is valid


        TC O(n) as we iterate through the entire LL
        """
        current = self.head
        while current is not None:
            if not current.is_valid():
                return current
            current = current.next
        return None
        






