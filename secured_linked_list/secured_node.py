def calc_hash(input: str):
    """
    Compute the hash of the given input

    Args:
        input: The string input to hash

    Returns:
        A hash value (int)
    """

    return hash(input)

# Side Note: hash(0 is not deterministic across sessions and apparently isn't cryptographically secure)
# For more secure hashing we would use SHA256 which is a 256 bit hashing algo and is more secure
# https://stackoverflow.com/questions/7646520/is-this-an-appropriate-use-of-pythons-built-in-hash-function

class SecuredNode:
    """
    Each node stores a value, a pointer to the next node, and a hash value
    that is computed from both its own value and the hash of the next node.

    Attributes:
        value: The string data stored in this node
        next: Pointer to the next SecuredNode, or None if this is the tail
        hash_value: Hash computed from this node's value and the next node's hash
    """

    def __init__(self, value, next_node=None):
        """
        The hash is automatically computed upon creation based on the node's
        value and the next node's hash (if present)
        """

        self.value = value
        self.next = next_node
        self.hash_value = self._compute_hash()
    
    def _compute_hash(self):
        """
        Compute the hash value for this node based on current state

        The hash formula:
            - If tail node (no next): hash(value)
            - Otherwise: hash((value, next.hash_value))

        Returns:
            The computed hash value
        """

        if self.next is None:
            return calc_hash(self.value)
        return calc_hash((self.value + str(self.next.hash_value)))
    
    def recompute_hash(self):
        """
        Update this node's hash_value to reflect current state

        Note: This only updates THIS node's hash. When modifying a chain,
        nodes must be rehashed from tail to head since each hash depends
        on the next node's hash
        """
        self.hash_value = self._compute_hash()
    
    def is_valid(self):
        """
        Check whether this node's stored hash matches its computed hash

        Returns:
            True if the node hasn't been tampered with, False otherwise
        """

        return self.hash_value == self._compute_hash()