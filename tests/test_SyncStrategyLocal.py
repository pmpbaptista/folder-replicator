"""
Test the SyncStrategyLocal class.
"""

from folder_replicator.SyncStrategyLocal import SyncStrategyLocal


def setup_sync_strategy_local(tmp_path):
    """
    Setup the SyncStrategyLocal class for testing.

    Args:
        tmp_path: Path - the temporary path to use for testing

    Returns:
        sync_strategy_local: SyncStrategyLocal - the SyncStrategyLocal class
    """
    source = tmp_path / "source"
    source.mkdir()
    destination = tmp_path / "destination"
    destination.mkdir()
    recursive = True
    delete = True
    dry_run = False

    sync_strategy_local = SyncStrategyLocal(
        source=source,
        destination=destination,
        recursive=recursive,
        delete=delete,
        dry_run=dry_run,
    )

    return sync_strategy_local


def test_sync_strategy_local_sync(tmp_path):
    """
    Test the sync method of the SyncStrategyLocal class.

    Args:
        tmp_path: Path - the temporary path to use for testing
    """
    sync_strategy_local = setup_sync_strategy_local(tmp_path)
    sync_strategy_local.sync()
    assert sync_strategy_local.source.hash == sync_strategy_local.destination.hash


def test_sync_strategy_local_sync_not_equal(tmp_path):
    """
    Test the sync method of the SyncStrategyLocal class when the hashes are not equal.

    Args:
        tmp_path: Path - the temporary path to use for testing

    Returns:
        None
    """
    sync_strategy_local = setup_sync_strategy_local(tmp_path)
    # Create a file in the source folder
    (sync_strategy_local.source.path / "file.txt").touch()
    sync_strategy_local.source.refresh()
    assert sync_strategy_local.source.hash != sync_strategy_local.destination.hash
    sync_strategy_local.sync()
    assert sync_strategy_local.source.hash == sync_strategy_local.destination.hash


def test_sync_strategy_local_sync_delete(tmp_path):
    """
    Test the sync method of the SyncStrategyLocal class when the delete flag is True.

    Args:
        tmp_path: Path - the temporary path to use for testing

    Returns:
        None
    """
    sync_strategy_local = setup_sync_strategy_local(tmp_path)
    # Create a file in the destination folder
    (sync_strategy_local.destination.path / "file.txt").touch()
    sync_strategy_local.destination.refresh()
    assert sync_strategy_local.source.hash != sync_strategy_local.destination.hash
    sync_strategy_local.sync()
    assert sync_strategy_local.source.hash == sync_strategy_local.destination.hash
    assert not (sync_strategy_local.destination.path / "file.txt").exists()


def test_sync_strategy_local_sync_not_recursive(tmp_path):
    """
    Test the sync method of the SyncStrategyLocal class when the recursive flag is False.

    Args:
        tmp_path: Path - the temporary path to use for testing

    Returns:
        None
    """
    sync_strategy_local = setup_sync_strategy_local(tmp_path)
    sync_strategy_local.source.recursive = False
    sync_strategy_local.destination.recursive = False
    # Create a subfolder in the source folder
    (sync_strategy_local.source.path / "test").mkdir()
    # Create a file in the source folder
    (sync_strategy_local.source.path / "test/file.txt").touch()
    sync_strategy_local.source.refresh()
    assert sync_strategy_local.source.hash == sync_strategy_local.destination.hash
    sync_strategy_local.sync()
    assert sync_strategy_local.source.hash == sync_strategy_local.destination.hash


def test_sync_strategy_local_sync_dry_run(tmp_path):
    """
    Test the sync method of the SyncStrategyLocal class when the dry run flag is True.

    Args:
        tmp_path: Path - the temporary path to use for testing

    Returns:
        None
    """
    sync_strategy_local = setup_sync_strategy_local(tmp_path)
    sync_strategy_local.dry_run = True
    # Create a file in the source folder
    (sync_strategy_local.source.path / "file.txt").touch()
    sync_strategy_local.source.refresh()
    assert sync_strategy_local.source.hash != sync_strategy_local.destination.hash
    sync_strategy_local.sync()
    assert sync_strategy_local.source.hash != sync_strategy_local.destination.hash
    assert not (sync_strategy_local.destination.path / "file.txt").exists()


def test_sync_strategy_local_wrong_relative_path(tmp_path):
    """
    Test the SyncStrategyLocal class when the relative path is wrong.

    Args:
        tmp_path: Path - the temporary path to use for testing

    Returns:
        None
    """
    source = tmp_path / "source"
    source.mkdir()
    destination = tmp_path / "destination"
    destination.mkdir()
    recursive = True
    delete = True
    dry_run = False

    sync_strategy_local = SyncStrategyLocal(
        source=source,
        destination=destination,
        recursive=recursive,
        delete=delete,
        dry_run=dry_run,
    )

    assert sync_strategy_local.source.path != sync_strategy_local.destination.path
    sync_strategy_local.sync()
    assert sync_strategy_local.source.hash == sync_strategy_local.destination.hash


def test_sync_strategy_local_filenotfounderror(tmp_path):
    """
    Test the SyncStrategyLocal class when a FileNotFoundError is raised.

    Args:
        tmp_path: Path - the temporary path to use for testing

    Returns:
        None
    """
    source = tmp_path / "source"
    source.mkdir()
    destination = tmp_path / "destination"
    destination.mkdir()
    recursive = True
    delete = True
    dry_run = False

    sync_strategy_local = SyncStrategyLocal(
        source=source,
        destination=destination,
        recursive=recursive,
        delete=delete,
        dry_run=dry_run,
    )

    # Create a file in the source folder
    (sync_strategy_local.source.path / "file.txt").touch()
    sync_strategy_local.source.refresh()
    assert sync_strategy_local.source.hash != sync_strategy_local.destination.hash
    sync_strategy_local.source.path = tmp_path / "wrong"
    sync_strategy_local.sync()
    

def test_sync_strategy_local_remove_empty_folders(tmp_path):
    """
    Test the SyncStrategyLocal class when removing empty folders.

    Args:
        tmp_path: Path - the temporary path to use for testing

    Returns:
        None
    """
    sync_strategy_local = setup_sync_strategy_local(tmp_path)
    # Create a subfolder in the source folder
    (sync_strategy_local.source.path / "test").mkdir()
    # Create a file in the source folder
    (sync_strategy_local.source.path / "test/file.txt").touch()
    sync_strategy_local.source.refresh()
    assert sync_strategy_local.source.hash != sync_strategy_local.destination.hash
    sync_strategy_local.sync()
    assert sync_strategy_local.source.hash == sync_strategy_local.destination.hash
    # Remove the file in the source folder
    (sync_strategy_local.source.path / "test/file.txt").unlink()
    sync_strategy_local.sync()
    sync_strategy_local.source.refresh()
    assert not (sync_strategy_local.destination.path / "test").exists()
    assert not (sync_strategy_local.destination.path / "test/file.txt").exists()
