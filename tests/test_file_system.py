import pytest

from inode_fs.filesystem import FileSystem
from inode_fs.inode import _reset_counter, DirInode, FileInode
from inode_fs.errors import AlreadyExistsError, NotADirectoryError, NotFoundError

class TestMkdir:
    @pytest.fixture
    def get_filesystem(self):
        _reset_counter()
        fs = FileSystem()
        return fs

    def test_mkdir_success(self, get_filesystem) -> None:
        fs = get_filesystem
        fs.mkdir(path="/docs", owner="me", group="me", mode=0o755)

    def test_mkdir_nested(self, get_filesystem) -> None:
        fs = get_filesystem
        root_inode = fs.inode_table.get(0)
        doc_inode = DirInode(owner="me", group="me", mode=0o755)
        root_inode.add_entry("docs", doc_inode.inode_id)
        doc_inode.link_count+=1
        fs.inode_table.add(doc_inode)
        fs.mkdir(path="/docs/team", owner="me", group="me", mode=0o755)

    def test_mkdir_already_exists_error(self, get_filesystem) -> None:
        fs = get_filesystem
        with pytest.raises(AlreadyExistsError):
            fs.mkdir(path="/", owner="me", group="me", mode=0o755)

    def test_mkdir_parent_does_not_exists(self, get_filesystem) -> None:
        fs = get_filesystem
        with pytest.raises(NotFoundError):
            fs.mkdir(path="/foo/bar", owner="me", group="me", mode=0o755)

    def test_mkdir_parent_is_a_file(self, get_filesystem) -> None:
        fs = get_filesystem
        root_inode = fs.inode_table.get(0)
        foo_inode = FileInode(owner="me", group="me", mode=0o755)
        root_inode.add_entry("foo.txt", foo_inode.inode_id)
        foo_inode.link_count+=1
        fs.inode_table.add(foo_inode)

        with pytest.raises(NotADirectoryError):
            fs.mkdir(path="/foo.txt/bar", owner="me", group="me", mode=0o755)
