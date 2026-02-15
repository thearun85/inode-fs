import pytest

from inode_fs.path_resolver import normalize

def test_full_path() -> None:
    path = "/home/file/test.txt"
    response = normalize(path)
    assert response == "/home/file/test.txt"

def test_ignore_current_dir() -> None:
    path = "/home/./file/test.txt"
    response = normalize(path)
    assert response == "/home/file/test.txt"

def test_parent_dir() -> None:
    path = "/home/../file/test.txt"
    response = normalize(path)
    assert response == "/file/test.txt"

def test_past_root() -> None:
    path = "../home/file/test.txt"
    response = normalize(path)
    assert response == "/home/file/test.txt"

def test_ignore_double_slash() -> None:
    path = "//home//file//test.txt"
    response = normalize(path)
    assert response == "/home/file/test.txt"

def test_ignore_trailing_slash() -> None:
    path = "/home/file/test.txt/"
    response = normalize(path)
    assert response == "/home/file/test.txt"

def test_root_only() -> None:
    path = "/"
    response = normalize(path)
    assert response == "/"
