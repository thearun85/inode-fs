from inode_fs.path_resolver import normalize, resolve
from inode_fs.inode_table import InodeTable
from inode_fs.inode import Inode, DirInode, FileInode, _reset_counter
from inode_fs.errors import NotFoundError, NotADirectoryError
import pytest

class TestNormalize:
    def test_full_path(self) -> None:
        _reset_counter()
        path = "/home/file/test.txt"
        response = normalize(path)
        assert response == "/home/file/test.txt"


    def test_ignore_current_dir(self) -> None:
        _reset_counter()
        path = "/home/./file/test.txt"
        response = normalize(path)
        assert response == "/home/file/test.txt"


    def test_parent_dir(self) -> None:
        _reset_counter()
        path = "/home/../file/test.txt"
        response = normalize(path)
        assert response == "/file/test.txt"


    def test_past_root(self) -> None:
        _reset_counter()
        path = "../home/file/test.txt"
        response = normalize(path)
        assert response == "/home/file/test.txt"


    def test_ignore_double_slash(self) -> None:
        _reset_counter()
        path = "//home//file//test.txt"
        response = normalize(path)
        assert response == "/home/file/test.txt"


    def test_ignore_trailing_slash(self) -> None:
        _reset_counter()
        path = "/home/file/test.txt/"
        response = normalize(path)
        assert response == "/home/file/test.txt"


    def test_root_only(self) -> None:
        _reset_counter()
        path = "/"
        response = normalize(path)
        assert response == "/"

class TestResolve:
    @pytest.fixture
    def get_setup(self) -> InodeTable:
        _reset_counter()
        inode_table = InodeTable()
        docs_inode = DirInode()
        report_inode = FileInode()
        docs_inode.add_entry("report.txt", report_inode.inode_id)
        file_inode = FileInode()
        root_inode = inode_table.get(0)
        if isinstance(root_inode, DirInode):
            root_inode.add_entry("docs", docs_inode.inode_id)
            root_inode.add_entry("file.txt", file_inode.inode_id)
        inode_table.add(docs_inode)
        inode_table.add(report_inode)
        inode_table.add(file_inode)

        return inode_table

    def test_root_only(self, get_setup: InodeTable) -> None:
        _reset_counter()
        inode_table = get_setup
        path = "/"
        root_node = resolve(path, inode_table)
        assert root_node == inode_table.get(0)

    def test_directory_path(self, get_setup: InodeTable) -> None:
        _reset_counter()
        inode_table = get_setup
        path = "/docs"
        docs_node = resolve(path, inode_table)
        assert isinstance(docs_node, DirInode)

    def test_file_path(self, get_setup: InodeTable) -> None:
        _reset_counter()
        inode_table = get_setup
        path = "/docs/report.txt"
        reports_node = resolve(path, inode_table)
        assert isinstance(reports_node, FileInode)

    def test_missing_directory(self, get_setup: InodeTable) -> None:
        _reset_counter()
        inode_table = get_setup
        path = "/missing"
        with pytest.raises(NotFoundError):
            missing_node = resolve(path, inode_table)

    def test_not_a_directory(self, get_setup: InodeTable) -> None:
        _reset_counter()
        inode_table = get_setup
        path = "/file.txt/docs"
        with pytest.raises(NotADirectoryError):
            error_node = resolve(path, inode_table)
