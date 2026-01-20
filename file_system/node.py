from typing import Dict, IO
from abc import ABC


class Node(ABC):
    """
    Base class representing a node in the file system tree

    Attributes:
        name: Name of this node (file or directory name)
    """

    def __init__(self, name: str):
        """Initialize a node with the given name"""
        self.name = name
        self.is_directory: bool = False


class FileNode(Node):
    """
    Represents a file in the file system

    Attributes:
        name: File name
        file_obj: File object associated with this node
    """

    def __init__(self, name: str, file_obj: IO):
        """Initialize a file node with a name and file object"""
        super().__init__(name)
        self.file_obj = file_obj
        self.is_directory = False


class DirectoryNode(Node):
    """
    Represents a directory in the file system

    Attributes:
        name: Directory name
        children: Mapping of child names to nodes
    """

    def __init__(self, name: str):
        """Initialize a directory node with the given name"""
        super().__init__(name)
        self.children: Dict[str, Node] = {}
        self.is_directory = True
