import pytest

from inode_fs.errors import NotFoundError
from inode_fs.inode import DirInode, FileInode, _reset_counter
from inode_fs.inode_table import InodeTable


def test_rootdir_at_zero() -> None:
    _reset_counter()
    inode_table = InodeTable()
    assert len(inode_table.entries) == 1
    dir_node = inode_table.get(0)
    assert isinstance(dir_node, DirInode)


def test_add_fileinode() -> None:
    _reset_counter()
    inode_table = InodeTable()
    file_inode = FileInode()
    inode_table.add(file_inode)
    get_file_inode = inode_table.get(file_inode.inode_id)
    assert get_file_inode is not None
    assert isinstance(get_file_inode, FileInode)


def test_add_dirinode() -> None:
    _reset_counter()
    inode_table = InodeTable()
    dir_inode = DirInode()
    inode_table.add(dir_inode)
    get_dir_inode = inode_table.get(dir_inode.inode_id)
    assert get_dir_inode is not None
    assert isinstance(get_dir_inode, DirInode)


def test_get_missing_raises() -> None:
    _reset_counter()
    inode_table = InodeTable()
    with pytest.raises(NotFoundError):
        inode_table.get(100)
