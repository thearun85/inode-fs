from inode_fs.errors import NotADirectoryError
from inode_fs.inode import DirInode, Inode
from inode_fs.inode_table import InodeTable


def normalize(path: str) -> str:
    path_stack: list[str] = []
    path_list = path.split("/")
    for p in path_list:
        if p == "..":
            if path_stack:
                path_stack.pop()
        elif p == "." or p == "":
            continue
        else:
            path_stack.append(p.strip())
    return "/" + "/".join(path_stack)


def resolve(path: str, inode_table: InodeTable) -> Inode:
    path = normalize(path)
    path_list: list[str] = path.split("/")
    path_list = [p for p in path_list if p]
    cur_inode = inode_table.get(0)
    for i in range(0, len(path_list) - 1):
        if not isinstance(cur_inode, DirInode):
            raise NotADirectoryError(f"[inode-fs] Path {path} is not a directory")
        cur_inode_id = cur_inode.get_entry(path_list[i])
        cur_inode = inode_table.get(cur_inode_id)

    if path_list:
        if not isinstance(cur_inode, DirInode):
            raise NotADirectoryError(f"[inode-fs] Path {path} is not a directory")

        cur_inode_id = cur_inode.get_entry(path_list[-1])  #
        cur_inode = inode_table.get(cur_inode_id)

    return cur_inode
