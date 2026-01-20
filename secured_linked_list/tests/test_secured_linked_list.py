import pytest
from secured_linked_list.secured_linked_list import SecuredLinkedList


class TestSecuredLinkedList:
    """Tests for SecuredLinkedList covering core functionality and edge cases."""

    def test_add_creates_valid_chain(self):
        """Adding multiple nodes should maintain a valid hash chain."""
        sll = SecuredLinkedList()
        sll.add("c")
        sll.add("b")
        sll.add("a")

        assert sll.head.value == "a"
        assert sll.head.next.value == "b"
        assert sll.head.next.next.value == "c"
        assert sll.is_valid_chain() is True

    def test_remove_middle_node(self):
        """Removing a middle node should relink and rehash correctly."""
        sll = SecuredLinkedList()
        sll.add("c")
        sll.add("b")
        sll.add("a")

        sll.remove(1)  # Remove "b"

        assert sll.head.value == "a"
        assert sll.head.next.value == "c"
        assert sll.head.next.next is None
        assert sll.is_valid_chain() is True

    def test_insert_middle_node(self):
        """Inserting in the middle should place node correctly and rehash."""
        sll = SecuredLinkedList()
        sll.add("c")
        sll.add("a")

        sll.insert(1, "b")

        assert sll.head.value == "a"
        assert sll.head.next.value == "b"
        assert sll.head.next.next.value == "c"
        assert sll.is_valid_chain() is True

    def test_invalid_head_detected(self):
        """Invalid head's value should be detected."""
        sll = SecuredLinkedList()
        sll.add("b")
        sll.add("a")

        sll.head.value = "modified"

        assert sll.is_valid_chain() is False
        assert sll.find_tampered_node() == sll.head

    def test_invalid_tail_detected(self):
        """Invalid tail should be detected correctly."""
        sll = SecuredLinkedList()
        sll.add("b")
        sll.add("a")

        sll.head.next.value = "modified"

        assert sll.is_valid_chain() is False
        # Tail node itself is invalid because its value changed
        assert sll.find_tampered_node() == sll.head.next

    def test_empty_list_is_valid(self):
        """An empty list should be considered valid."""
        sll = SecuredLinkedList()

        assert sll.is_valid_chain() is True
        assert sll.find_tampered_node() is None

    def test_remove_from_empty_list_raises_error(self):
        """Removing from an empty list should raise IndexError."""
        sll = SecuredLinkedList()

        with pytest.raises(IndexError, match="Cannot remove from empty list"):
            sll.remove(0)

    def test_remove_negative_index_raises_error(self):
        """Negative index should raise IndexError."""
        sll = SecuredLinkedList()
        sll.add("a")

        with pytest.raises(IndexError, match="Index out of range"):
            sll.remove(-1)

    def test_insert_at_head_uses_add(self):
        """Inserting at index 0 should behave like add()."""
        sll = SecuredLinkedList()
        sll.add("b")

        sll.insert(0, "a")

        assert sll.head.value == "a"
        assert sll.head.next.value == "b"
        assert sll.is_valid_chain() is True

    def test_same_value_different_hashes(self):
        """Same value at different positions should have different hashes."""
        sll = SecuredLinkedList()
        sll.add("same")
        sll.add("same")
        sll.add("same")

        assert sll.head.hash_value != sll.head.next.hash_value
        assert sll.head.next.hash_value != sll.head.next.next.hash_value
        assert sll.is_valid_chain() is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
