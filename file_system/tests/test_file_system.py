import pytest
from io import StringIO
from file_system.file_system import FileSystem

# setup for each test run
@pytest.fixture
def empty_fs():
    """Provide an empty FileSystem instance"""
    return FileSystem()


@pytest.fixture
def populated_fs():
    """Provide a FileSystem with a basic directory structure"""
    return FileSystem(
        {
            "/home/user/a.txt": StringIO("content a"),
            "/home/user/b.txt": StringIO("content b"),
            "/home/user/subdir/c.txt": StringIO("content c"),
        }
    )


def test_empty_initialization(empty_fs):
    """FileSystem initializes with empty root when no files provided"""
    assert empty_fs.root is not None
    assert empty_fs.root.is_directory
    assert empty_fs.root.children == {}


def test_initialization_with_files():
    """FileSystem builds tree from initial file dictionary"""
    file1 = StringIO("content1")
    file2 = StringIO("content2")
    files = {
        "/home/user/doc.txt": file1,
        "/home/user/code/main.py": file2,
    }

    fs = FileSystem(files)

    assert fs.exists("/home")
    assert fs.exists("/home/user")
    assert fs.exists("/home/user/doc.txt")
    assert fs.exists("/home/user/code/main.py")
    assert fs.is_dir("/home/user")
    assert fs.is_file("/home/user/doc.txt")


def test_add_creates_intermediate_directories(empty_fs):
    """Adding a file creates all necessary parent directories"""
    empty_fs.add("/a/b/c/file.txt", StringIO("test content"))

    assert empty_fs.is_dir("/a")
    assert empty_fs.is_dir("/a/b")
    assert empty_fs.is_dir("/a/b/c")
    assert empty_fs.is_file("/a/b/c/file.txt")


def test_add_directory_with_trailing_slash(empty_fs):
    """Paths ending with '/' create directories, not files"""
    empty_fs.add("/home/user/documents/")

    assert empty_fs.is_dir("/home/user/documents")
    assert not empty_fs.is_file("/home/user/documents")


def test_add_duplicate_file_raises_error(empty_fs):
    """Adding a file where one already exists raises ValueError"""
    empty_fs.add("/home/file.txt", StringIO("first"))

    with pytest.raises(ValueError, match="already exists"):
        empty_fs.add("/home/file.txt", StringIO("second"))


def test_add_file_through_existing_file_raises_error(empty_fs):
    """Adding a path through an existing file raises ValueError"""
    empty_fs.add("/home/file.txt", StringIO("content"))

    with pytest.raises(ValueError, match="exists as a file"):
        empty_fs.add("/home/file.txt/nested/other.txt", StringIO("other"))


def test_list_directory_returns_children(populated_fs):
    """list_directory returns names of immediate children"""
    contents = populated_fs.list_directory("/home/user")

    assert set(contents) == {"a.txt", "b.txt", "subdir"}


def test_list_nonexistent_path_raises_error(empty_fs):
    """Listing a nonexistent path raises ValueError"""
    with pytest.raises(ValueError, match="Path not found"):
        empty_fs.list_directory("/does/not/exist")


def test_delete_file(populated_fs):
    """Deleting a file removes it from parent directory"""
    populated_fs.delete("/home/user/a.txt")

    assert not populated_fs.exists("/home/user/a.txt")
    assert populated_fs.exists("/home/user")


def test_delete_nonempty_directory_raises_error(populated_fs):
    """Deleting non-empty directory without recursive flag raises error"""
    with pytest.raises(ValueError, match="Directory not empty"):
        populated_fs.delete("/home/user")


def test_delete_nonempty_directory_with_recursive(populated_fs):
    """Deleting non-empty directory with recursive=True succeeds"""
    populated_fs.delete("/home/user", recursive=True)

    assert not populated_fs.exists("/home/user")
    assert populated_fs.exists("/home")


def test_edit_file_replaces_file_object(empty_fs):
    """edit_file replaces the file object at the given path"""
    original = StringIO("original")
    replacement = StringIO("replacement")
    empty_fs.add("/home/file.txt", original)

    empty_fs.edit_file("/home/file.txt", replacement)

    retrieved = empty_fs.get_file("/home/file.txt")
    assert retrieved is replacement
    assert retrieved is not original
