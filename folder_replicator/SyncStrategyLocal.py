import shutil
from pathlib import Path

import folder_replicator.lib.logger as fr_logger
from folder_replicator.Folder import Folder
from folder_replicator.interfaces.SyncStrategy import SyncStrategy


class SyncStrategyLocal(SyncStrategy):
    """
    Concrete Sync Strategy class that implements the local sync strategy.

    The SyncContext uses this class to call the algorithm defined by the Concrete
    SyncStrategy.
    """

    def __init__(
        self, source: str, destination: str, recursive: bool, delete: bool, dry_run: bool
    ) -> None:
        """
        Constructor for the SyncStrategyLocal class.
        """
        self.source = Folder(source, recursive=recursive, delete=delete)
        self.destination = Folder(destination, recursive=recursive, delete=delete)
        self.dry_run = dry_run

    def sync(self) -> None:
        """
        The sync method is the main method that the SyncContext will use to
        perform the sync operation.
        """
        logger = fr_logger.get_logger()
        logger.info(f"Syncing folders {self.source.path} and {self.destination.path}")
        self.source.refresh()
        self.destination.refresh()
        if self.source.hash == self.destination.hash:
            logger.info(
                f"Folders {self.source.path}:{self.source.hash} and {self.destination.path}:{self.source.hash} are in sync"
            )
            return

        # Get files in source and destination
        source_files = self.source.files
        destination_files = self.destination.files

        # Get files that are in source but not in destination
        files_to_copy = {}
        for path, hash in source_files.items():
            if hash not in destination_files.values():
                files_to_copy[path.resolve()] = hash
        
        if logger.isEnabledFor(fr_logger.logging.DEBUG):
            logger.debug(f"Source files: {source_files}")
            logger.debug(f"Destination files: {destination_files}")
            logger.debug(f"Files to copy: {files_to_copy}")

        if self.source.delete:
            # Get files that are in destination but not in source
            files_to_delete = {}
            for path, hash in destination_files.items():
                if hash not in source_files.values():
                    files_to_delete[path.resolve()] = hash

            if logger.isEnabledFor(fr_logger.logging.DEBUG):
                logger.debug(f"Files to delete: {files_to_delete}")
            
            temp_files = []
            # Delete files from destination that are not in source
            for file in files_to_delete:
                logger.info(f"Deleting file {file}")
                if self.dry_run:
                    continue
                try:
                    # Copy files to temp file before deleting
                    temp_file = Path(f"{file}.bak")
                    temp_files.append(temp_file)
                    shutil.copy2(file, temp_file)
                    file.unlink()
                except FileNotFoundError:
                    logger.error(f"File {file} not found in destination")
                    continue
                except PermissionError:
                    logger.error(f"Permission denied to delete file {file}")
                    continue
                except Exception as e:
                    logger.error(f"Error deleting file {file}: {e}")
                    continue

        # Copy files from source to destination
        self.__copy(files_to_copy)

        if self.source.delete:
            # Clean up temp files
            self.__clean_bak_files(temp_files)

        self.source.refresh()
        self.destination.refresh()
        logger.info("Sync complete")

    def __copy(self, files_to_copy: dict) -> None:
        """
        Helper method to copy files from the source to the destination.

        Args:
            files_to_copy: dict - the files to copy

        Returns:
            None
        """
        logger = fr_logger.get_logger()
        logger.info(f"Copying folders {self.source.path} to {self.destination.path}")

        # Copy files from source to destination
        for path in files_to_copy.keys():
            source_path = path
            try:
                relative_path = source_path.relative_to(self.source.path.resolve())
            except ValueError:
                logger.error(
                    f"File {source_path} is not relative to the source directory {self.source.path}"
                )
                continue

            destination_path = self.destination.path.resolve() / relative_path
            logger.info(f"Copying file {source_path} to {destination_path}")

            if self.dry_run:
                continue

            try:
                # Create necessary directories in the destination path
                destination_path.parent.mkdir(parents=True, exist_ok=True)

                # Copy the file
                shutil.copy2(source_path, destination_path)
            except FileNotFoundError:
                logger.error(f"File {source_path} not found in source")
                continue
            except PermissionError:
                logger.error(f"Permission denied to copy file {source_path}")
                continue
            except Exception as e:
                logger.error(f"Error copying file {source_path}: {e}")
                continue

        logger.info("Copy complete")

    def __clean_bak_files(self, temp_files: list) -> None:
        """
        Helper method to clean up temp files.

        Args:
            temp_files: list - the temp files to clean up

        Returns:
            None
        """
        logger = fr_logger.get_logger()
        if logger.isEnabledFor(fr_logger.logging.DEBUG):
            logger.debug(f"Temp files: {temp_files}")
        logger.info("Cleaning up temp files")

        for file in temp_files:
            logger.info(f"Removing temp file {file}")
            if self.dry_run:
                continue
            try:
                file.unlink()
            except FileNotFoundError:
                logger.error(f"File {file} not found")
                continue
            except PermissionError:
                logger.error(f"Permission denied to delete file {file}")
                continue
            except Exception as e:
                logger.error(f"Error deleting file {file}: {e}")
                continue

        logger.info("Temp file cleanup complete")
