import time
from abc import ABC
from enum import Enum, auto
from threading import RLock

_next_inode_id: int = 0
_inode_lock = RLock()


def _allocate_inode() -> int:
    """Thread safe method to get an unique inode id"""
    global _next_inode_id
    with _inode_lock:
        inode_id = _next_inode_id
        _next_inode_id += 1
        return inode_id


def _reset_counter() -> None:
    """Dangerous - Used only for testing."""
    global _next_inode_id
    _next_inode_id = 0


class NodeType(Enum):
    """To distinguish between a file and a directory."""

    FILE = auto()
    DIRECTORY = auto()


class Inode(ABC):
    def __init__(self, owner: str, group: str, mode: int) -> None:
        """Initialize an inode structure during a file/ directory creation"""
        now = time.time()
        self.inode_id: int = _allocate_inode()
        self.owner: str = owner
        self.group: str = group
        self.mode: int = mode
        # timestamps
        self.created_at: float = now
        self.modified_at: float = now
        self.accessed_at: float = now

        self.link_count: int = 0


class FileInode(Inode):
    node_type: NodeType = NodeType.FILE

    def __init__(
        self, owner: str = "root", group: str = "root", mode: int = 0o755
    ) -> None:
        super().__init__(owner, group, mode)
        self.content: bytes = b""

    @property
    def size(self) -> int:
        return len(self.content)


class DirInode(Inode):
    node_type: NodeType = NodeType.DIRECTORY

    def __init__(
        self, owner: str = "root", group: str = "root", mode: int = 0o755
    ) -> None:
        super().__init__(owner, group, mode)
        self.entries: dict[str, int] = {}  # {"name": inode_id}

    @property
    def entry_count(self) -> int:
        return len(self.entries)
