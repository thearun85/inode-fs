"""Custom Error implementation for the file system"""


class FileSystemError(Exception):
    """Base class for all the file system errors."""


class NotFoundError(FileSystemError):
    """Raised when path does not exists."""


class AlreadyExistsError(FileSystemError):
    """Raised when creating a node which already exists."""


class NotADirectoryError(FileSystemError):
    """Raised when trying to access an inode which is a file."""


class IsADirectoryError(FileSystemError):
    """Raised when a file operation is attempted on a directory."""
