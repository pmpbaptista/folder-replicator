import hashlib
import pathlib


class Folder:
    """
    Represents a folder in the filesystem.
    """

    def __init__(self, path: str, recursive: bool = True, delete: bool = True) -> None:
        """
        Initialize the Folder object.

        Args:
            path (str): the path to the folder
            recursive (bool): whether to sync the folder recursively
            delete (bool): whether to delete files that are not in the source folder

        Returns:
            None
        """
        self.path = pathlib.Path(path)
        self.recursive = recursive
        self.delete = delete
        self.files = self.get_files()
        self.hash = self.__calculate_folder_hash()

    def __str__(self) -> str:
        """
        Returns a string representation of the Folder object.

        Args:
            None

        Returns:
            str: the string representation of the Folder object
        """
        return f"Folder(path={self.path.__str__()}, files={self.files})"

    def __repr__(self) -> str:
        """
        Returns a string representation of the Folder object.

        Args:
            None

        Returns:
            str: the string representation of the Folder object
        """
        return f"Folder(path={self.path}, hash={self.hash})"

    def __eq__(self, other) -> bool:
        """
        Compare two Folder objects for equality.

        Args:
            other (Folder): the other Folder object to compare

        Returns:
            bool: whether the two Folder objects are equal
        """
        return self.hash == other.hash
    
    def __calculate_folder_hash(self) -> str:
        """
        Calculate the hash of a folder.

        Args:
            None

        Returns:
            str: the hash of the folder
        """
        hasher = hashlib.md5()
        for _, hash in self.files.items():
            hasher.update(hash.__str__().encode())
            hasher.update(hash.encode())
        return hasher.hexdigest()

    def __calculate_file_hash(self, file_path: pathlib.Path) -> str:
        """
        Calculate the hash of a file.

        Args:
            file_path (pathlib.Path): the path to the file

        Returns:
            str: the hash of the file
        """
        hash = hashlib.md5()
        try:
            with open(file_path.__str__(), "rb") as file:
                while chunk := file.read(4096):
                    hash.update(chunk)
        except FileNotFoundError:
            return None
        except PermissionError:
            return None
        return hash.hexdigest()

    def get_files(self) -> dict:
        """
        Discover the files in the folder, recursively if specified.

        Args:
            None

        Returns:
            dict: a dictionary of files in the folder with the relative path as the key and the checksum as the value
        """
        if self.recursive:
            files = {file: self.__calculate_file_hash(file.resolve()) for file in self.path.rglob("*") if file.is_file()}
        else:
            files = {file: self.__calculate_file_hash(file.resolve()) for file in self.path.glob("*") if file.is_file()}

        # Sort the files by hash to ensure a consistent order
        files = {k: v for k, v in sorted(files.items(), key=lambda item: item[1])}
        return files

    def refresh(self) -> None:
        """
        Refresh the files in the folder.

        Args:
            None

        Returns:
            None
        """
        self.files = self.get_files()
        self.hash = self.__calculate_folder_hash()
