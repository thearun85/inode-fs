from inode_fs.errors import AlreadyExistsError, NotADirectoryError, FileSystemError
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
    def ls(self, path: str) -> list[str]:
        path_inode = resolve(path, self.inode_table)
        if isinstance(path_inode, DirInode):
            return list(path_inode.entries.keys())
        else:
            raise NotADirectoryError(f"[inode-fs] Path {path} is not a directory")

    def rmdir(self, path: str) -> None:
        path_list  = [p for p in normalize(path).split("/") if p]
        if path_list:
            path_inode = resolve(path, self.inode_table)
            if not isinstance(path_inode, DirInode):
                raise NotADirectoryError(f"[inode-fs] Path {path} is not a directory")
            if len(path_inode.entries) > 0:
                raise FileSystemError(f"[inode-fs] Path {path} is not empty")
            parent_inode = resolve("/" + "/".join(path_list[0:-1]), self.inode_table)
            parent_inode.remove_entry(path_list[-1])
            path_inode.link_count-=1
            if path_inode.link_count == 0:
                self.inode_table.remove(path_inode.inode_id)


        else:
            raise FileSystemError(f"[inode-fs] root directory cannot be deleted")
        
