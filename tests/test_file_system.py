import pytest

from inode_fs.file_system import FileSystem
from inode_fs.inode import _reset_counter, DirInode, FileInode
from inode_fs.errors import AlreadyExistsError, NotADirectoryError, NotFoundError, FileSystemError

@pytest.fixture
def get_filesystem() -> FileSystem:
    _reset_counter()
    fs = FileSystem() # type: ignore
    return fs

@pytest.fixture
def get_filesystem_with_dir_only() -> FileSystem:
    _reset_counter()
    fs = FileSystem() # type: ignore
    root_inode = fs.inode_table.get_root()
    docs_child_node = DirInode(owner="me", group="me", mode=0o755)
    docs_child_node.link_count+=1
    doc_inode = DirInode(owner="me", group="me", mode=0o755)
    doc_inode.link_count+=1
    root_inode.add_entry("docs_child", doc_inode.inode_id) #type: ignore
    image_inode = DirInode(owner="me", group="me", mode=0o755)
    image_inode.link_count+=1
    
    root_inode.add_entry("docs", doc_inode.inode_id) #type: ignore
    root_inode.add_entry("images", image_inode.inode_id) #type: ignore
    fs.inode_table.add(docs_child_node)
    fs.inode_table.add(doc_inode)
    fs.inode_table.add(image_inode)
    return fs

@pytest.fixture
def get_filesystem_with_files_only() -> FileSystem:
    _reset_counter()
    fs = FileSystem() # type: ignore
    root_inode = fs.inode_table.get_root()
    file1_inode = FileInode(owner="me", group="me", mode=0o755)
    file1_inode.link_count+=1

    file2_inode = FileInode(owner="me", group="me", mode=0o755)
    file2_inode.link_count+=1
    
    root_inode.add_entry("file1.txt", file1_inode.inode_id) #type: ignore
    root_inode.add_entry("file2.txt", file2_inode.inode_id) #type: ignore
    fs.inode_table.add(file1_inode)
    fs.inode_table.add(file2_inode)
    return fs
    
class TestMkdir:

    def test_mkdir_success(self, get_filesystem: FileSystem) -> None:
        fs = get_filesystem
        fs.mkdir(path="/docs", owner="me", group="me", mode=0o755)

    def test_mkdir_nested(self, get_filesystem: FileSystem) -> None:
        fs = get_filesystem
        root_inode = fs.inode_table.get_root()
        doc_inode = DirInode(owner="me", group="me", mode=0o755)
        root_inode.add_entry("docs", doc_inode.inode_id) # type: ignore
        doc_inode.link_count+=1
        fs.inode_table.add(doc_inode)
        fs.mkdir(path="/docs/team", owner="me", group="me", mode=0o755)

    def test_mkdir_already_exists_error(self, get_filesystem: FileSystem) -> None:
        fs = get_filesystem
        with pytest.raises(AlreadyExistsError):
            fs.mkdir(path="/", owner="me", group="me", mode=0o755)

    def test_mkdir_parent_does_not_exists(self, get_filesystem: FileSystem) -> None:
        fs = get_filesystem
        with pytest.raises(NotFoundError):
            fs.mkdir(path="/foo/bar", owner="me", group="me", mode=0o755)

    def test_mkdir_parent_is_a_file(self, get_filesystem: FileSystem) -> None:
        fs = get_filesystem
        root_inode = fs.inode_table.get_root()
        foo_inode = FileInode(owner="me", group="me", mode=0o755)
        root_inode.add_entry("foo.txt", foo_inode.inode_id) # type: ignore
        foo_inode.link_count+=1
        fs.inode_table.add(foo_inode)

        with pytest.raises(NotADirectoryError):
            fs.mkdir(path="/foo.txt/bar", owner="me", group="me", mode=0o755)

class TestLs:
    def test_ls_success(self, get_filesystem: FileSystem) -> None:
        fs = get_filesystem
        root_inode = fs.inode_table.get_root()
        doc_dir = DirInode(owner="me", group="me", mode=0o755)
        image_dir = DirInode(owner="me", group="me", mode=0o755)
        file1 = FileInode(owner="me", group="me", mode=0o755)
        file2 = FileInode(owner="me", group="me", mode=0o755)
        if not isinstance(root_inode, DirInode):
            print("Error")
        root_inode.add_entry("docs", doc_dir.inode_id) # type: ignore
        root_inode.add_entry("images", image_dir.inode_id) # type: ignore
        root_inode.add_entry("file1.txt", file1.inode_id) # type: ignore
        root_inode.add_entry("file2.txt", file2.inode_id) # type: ignore
        fs.inode_table.add(doc_dir)
        fs.inode_table.add(image_dir)
        fs.inode_table.add(file1)
        fs.inode_table.add(file2)
        lentries = fs.ls("/")
        assert len(lentries) == 4
        assert "docs" in lentries
        assert "images" in lentries
        assert "file1.txt" in lentries
        assert "file2.txt" in lentries

    def test_empty_dir(self, get_filesystem: FileSystem) -> None:
        fs = get_filesystem
        lentries = fs.ls("/")
        assert len(lentries) == 0

    def test_file(self, get_filesystem: FileSystem) -> None:
        fs = get_filesystem
        root_inode = fs.inode_table.get_root()
        file_inode = FileInode(owner="me", group="me", mode=0o755)
        root_inode.add_entry("file.txt", file_inode.inode_id) #type: ignore
        fs.inode_table.add(file_inode)

        with pytest.raises(NotADirectoryError):
            fs.ls("/file.txt")
        
    def test_path_does_not_exist(self, get_filesystem: FileSystem) -> None:
        fs = get_filesystem
        with pytest.raises(NotFoundError):
            fs.ls("/team")
        
class TestRmdir:
    def test_rmdir_success(self, get_filesystem_with_dir_only: FileSystem) -> None:
        fs = get_filesystem_with_dir_only
        fs.rmdir("/docs")

    def test_rmdir_root(self, get_filesystem: FileSystem) -> None:
        fs = get_filesystem
        with pytest.raises(FileSystemError):
            fs.rmdir("/")

    def test_rmdir_dir_with_contents(self, get_filesystem: FileSystem) -> None:
        fs = get_filesystem
        with pytest.raises(FileSystemError):
            fs.rmdir("/docs")

    def test_rmdir_file(self, get_filesystem_with_files_only: FileSystem) -> None:
        fs = get_filesystem_with_files_only
        with pytest.raises(NotADirectoryError):
            fs.rmdir("/file1.txt")
