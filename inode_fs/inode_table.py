from inode_fs.errors import NotFoundError
from inode_fs.inode import DirInode, Inode


class InodeTable:
    def __init__(self) -> None:
        self.entries: dict[int, Inode] = {}  # {inode_id: FileInode | DirInode}
        # Entry for root diectory `/`
        root = DirInode(
            owner="root",
            group="root",
            mode=0o755,
        )
        self.entries[root.inode_id] = root

    def add(self, inode: Inode) -> None:
        """Add an inode entry to the table"""
        self.entries[inode.inode_id] = inode

    def get(self, inode_id: int) -> Inode:
        """Fetch an inode object by inode_id if it exists,
        else throw a NotFoundError"""
        if inode_id in self.entries:
            return self.entries[inode_id]
        raise NotFoundError(f"[inode-fs] inode_id {inode_id} doesn't exist")

    def remove(self, inode_id: int) -> None:
        """Remove an inode entry from the table if it exists,
        else throw a NotFoundError"""
        if inode_id in self.entries:
            del self.entries[inode_id]
            return
        raise NotFoundError(f"[inode-fs] inode_id {inode_id} doesn't exist")
