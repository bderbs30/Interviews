from typing import Dict, List, Optional, Tuple, IO

from file_system.node import DirectoryNode, FileNode, Node


class FileSystem:
    """
    In-memory file system using a tree-based structure

    Provides operations for managing files and directories using absolute
    paths. Internally, the tree stores directories as nodes containing
    references to children

    Attributes:
        root: Root directory node
    """

    def __init__(self, files: Optional[Dict[str, IO]] = None):
        """
        Initialize the file system with an optional dictionary of files

        Args:
            files: Mapping of absolute file paths to file objects. Paths
                ending with "/" are treated as directories. If None, an
                empty file system is created

        Raises:
            ValueError: If there is a path conflict during initialization
        """
        self.root = DirectoryNode("")

        if files:
            for path, file_obj in files.items():
                self.add(path, file_obj)

    def _parse_path(self, path: str) -> List[str]:
        """
        Parse an absolute path into its component parts

        Splits on "/" and filters out empty segments

        Args:
            path: Absolute path to parse

        Returns:
            List of path components
        """
        paths = []
        for component in path.split("/"):
            if component:
                paths.append(component)
        return paths

    def _traverse_to(self, path: str) -> Optional[Node]:
        """
        Traverse to the node at the given path

        Args:
            path: Absolute path to traverse to

        Returns:
            Node at the given path, or None if the path does not exist or a
            non-directory is encountered during traversal
        """
        components = self._parse_path(path)

        current = self.root
        for component in components:
            if not current.is_directory:
                return None
            if component not in current.children:
                return None
            current = current.children[component]

        return current

    def _traverse_to_parent(self, path: str):
        """
        Traverse to the parent directory of the given path

        Args:
            path: Absolute path whose parent to find

        Returns:
            Tuple of (parent_directory, child_name). Returns (None, "") if
            the path is invalid or the parent cannot be reached
        """
        components = self._parse_path(path)

        if not components:
            return None, ""

        # retrieve the last section of the path
        child_name = components[-1]

        if len(components) == 1:
            return self.root, child_name

        parent_path = "/" + "/".join(components[:-1])  # rebuild absolute path to the parent directory
        parent = self._traverse_to(parent_path)

        if parent is None or not parent.is_directory:
            return None, ""

        return parent, child_name

    def add(self, path: str, file_obj: Optional[IO] = None) -> None:
        """
        Add a file or directory at the given path

        Creates intermediate directories as needed. If file_obj is None or
        the path ends with "/", a directory is created

        Args:
            path: Absolute path where the file or directory should be
                created
            file_obj: File object to associate with the file. Pass None to
                create a directory

        Raises:
            ValueError: If the path conflicts with an existing file or
            directory
        """
        components = self._parse_path(path)

        if not components:
            raise ValueError("Cannot add to root path")

        is_directory = path.endswith("/") or file_obj is None

        if is_directory:
            dir_components = components
            file_name = None
        else:
            dir_components = components[:-1]
            file_name = components[-1]

        current = self.root
        for dir_name in dir_components:
            if dir_name not in current.children:
                current.children[dir_name] = DirectoryNode(dir_name)

            child = current.children[dir_name]
            if not child.is_directory:
                raise ValueError(f"Path conflict: '{dir_name}' exists as a file")
            current = child

        if file_name is not None:
            if file_name in current.children:
                raise ValueError(f"Path conflict: '{file_name}' already exists")
            current.children[file_name] = FileNode(file_name, file_obj)

    def delete(self, path: str, recursive: bool = False) -> None:
        """
        Delete a file or directory at the given path

        Args:
            path: Absolute path of the file or directory to delete
            recursive: If True, allows deletion of non-empty directories.
                If False, raises an error when attempting to delete a
                non-empty directory. Defaults to False

        Raises:
            ValueError: If the path does not exist or if attempting to
            delete a non-empty directory without recursive=True
        """
        parent, child_name = self._traverse_to_parent(path)

        if parent is None or child_name not in parent.children:
            raise ValueError(f"Path not found: {path}")

        child = parent.children[child_name]

        if child.is_directory and child.children and not recursive:
            raise ValueError(
                f"Directory not empty: {path}. Use recursive=True to delete"
            )

        del parent.children[child_name]

    def list_directory(self, path: str) -> List[str]:
        """
        List the contents of a directory

        Args:
            path: Absolute path of the directory to list

        Returns:
            Names of files and subdirectories in the directory

        Raises:
            ValueError: If the path does not exist or is not a directory
        """
        node = self._traverse_to(path)

        if node is None:
            raise ValueError(f"Path not found: {path}")
        if not node.is_directory:
            raise ValueError(f"Not a directory: {path}")

        return list(node.children.keys())

    def get_file(self, path: str) -> IO:
        """
        Retrieve the file object at the given path

        Args:
            path: Absolute path of the file to retrieve

        Returns:
            File object associated with the file

        Raises:
            ValueError: If the path does not exist or is a directory
        """
        node = self._traverse_to(path)

        if node is None:
            raise ValueError(f"Path not found: {path}")
        if node.is_directory:
            raise ValueError(f"Path is a directory, not a file: {path}")

        return node.file_obj

    def edit_file(self, path: str, new_file_obj: IO) -> None:
        """
        Replace the file object at the given path

        Args:
            path: Absolute path of the file to edit
            new_file_obj: New file object to associate with the file

        Raises:
            ValueError: If the path does not exist or is a directory
        """
        node = self._traverse_to(path)

        if node is None:
            raise ValueError(f"Path not found: {path}")
        if node.is_directory:
            raise ValueError(f"Cannot edit a directory: {path}")

        node.file_obj = new_file_obj

    def exists(self, path: str) -> bool:
        """
        Check if a file or directory exists at the given path

        Args:
            path: Absolute path to check

        Returns:
            True if a file or directory exists at the path, False otherwise
        """
        return self._traverse_to(path) is not None

    def is_file(self, path: str) -> bool:
        """
        Check if the path points to a file

        Args:
            path: Absolute path to check

        Returns:
            True if the path exists and is a file, False otherwise
        """
        node = self._traverse_to(path)
        return node is not None and not node.is_directory

    def is_dir(self, path: str) -> bool:
        """
        Check if the path points to a directory

        Args:
            path: Absolute path to check

        Returns:
            True if the path exists and is a directory, False otherwise
        """
        node = self._traverse_to(path)
        return node is not None and node.is_directory
