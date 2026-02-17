"""Tests for inode implementation."""

import time

import pytest

from inode_fs.errors import AlreadyExistsError, NotFoundError
from inode_fs.inode import (
    DirInode,
    FileInode,
    NodeType,
    _allocate_inode,
    _reset_counter,
)


def test_allocate_node_increments() -> None:
    _reset_counter()
    inode_id1 = _allocate_inode()
    inode_id2 = _allocate_inode()
    assert inode_id1 == 0
    assert inode_id2 == 1


def test_create_filenode_with_defaults() -> None:
    _reset_counter()
    before = time.time()
    file_inode = FileInode()
    assert file_inode.inode_id == 0
    assert file_inode.owner == "root"
    assert file_inode.group == "root"
    assert file_inode.mode == 0o755

    assert file_inode.size == 0
    assert file_inode.node_type == NodeType.FILE
    assert file_inode.link_count == 0
    assert file_inode.created_at >= before
    assert file_inode.modified_at >= before
    assert file_inode.accessed_at >= before
    assert file_inode.created_at == file_inode.modified_at == file_inode.accessed_at


def test_create_dir_with_defaults() -> None:
    _reset_counter()
    before = time.time()
    dir_inode = DirInode()
    assert dir_inode.inode_id == 0
    assert dir_inode.owner == "root"
    assert dir_inode.group == "root"
    assert dir_inode.mode == 0o755

    assert dir_inode.entry_count == 0
    assert dir_inode.node_type == NodeType.DIRECTORY
    assert dir_inode.link_count == 0
    assert dir_inode.created_at >= before
    assert dir_inode.modified_at >= before
    assert dir_inode.accessed_at >= before
    assert dir_inode.created_at == dir_inode.modified_at == dir_inode.accessed_at


def test_dirnode_add_entry() -> None:
    _reset_counter()
    dir_inode_root = DirInode()
    dir_inode_root.add_entry("home", 2)
    assert len(dir_inode_root.entries) == 1
    home_inode = dir_inode_root.get_entry("home")
    assert home_inode is not None
    assert home_inode == 2


def test_dirnode_already_exists_error() -> None:
    _reset_counter()
    dir_inode_root = DirInode()
    dir_inode_root.add_entry("home", 2)
    with pytest.raises(AlreadyExistsError):
        dir_inode_root.add_entry("home", 3)


def test_dirnode_missing_name() -> None:
    _reset_counter()
    dir_inode_root = DirInode()
    with pytest.raises(NotFoundError):
        dir_inode_root.get_entry("home")


def test_dirnode_remove_entry() -> None:
    _reset_counter()
    dir_inode_root = DirInode()
    dir_inode_root.add_entry("home", 2)
    assert len(dir_inode_root.entries) == 1
    home_inode = dir_inode_root.get_entry("home")
    assert home_inode is not None
    assert home_inode == 2

    dir_inode_root.remove_entry("home")
    assert len(dir_inode_root.entries) == 0


def test_dirnode_remove_entry_missing() -> None:
    _reset_counter()
    dir_inode_root = DirInode()
    with pytest.raises(NotFoundError):
        dir_inode_root.remove_entry("home")
