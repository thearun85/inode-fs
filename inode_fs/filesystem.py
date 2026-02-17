from inode_fs.errors import AlreadyExistsError, NotADirectoryError
from inode_fs.inode import DirInode
from inode_fs.inode_table import InodeTable
from inode_fs.path_resolver import normalize, resolve


class FileSystem:
    def __init__(self):
        self.inode_table = InodeTable()

    def mkdir(self, path: str, owner: str, group: str, mode: int) -> None:
        final_path = [p for p in normalize(path).split("/") if p]
        if final_path:
            parent_inode = resolve("/" + "/".join(final_path[0:-1]), self.inode_table)

            if not isinstance(parent_inode, DirInode):
                raise NotADirectoryError(f"[inode-fs] Path {path} is not a directory")
            new_dir_name = final_path[-1]
            new_dir_inode = DirInode(owner, group, mode)
            parent_inode.add_entry(new_dir_name, new_dir_inode.inode_id)
            new_dir_inode.link_count += 1
            self.inode_table.add(new_dir_inode)
        else:
            raise AlreadyExistsError(f"[inode-fs]Path {path} already exists")
