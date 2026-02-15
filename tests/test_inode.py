"""Tests for inode implementation."""

import time

from inode_fs.inode import (
    DirInode,
    FileInode,
    NodeType,
    _allocate_inode,
    _reset_counter,
)


def test_allocate_node_increments() -> None:
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
