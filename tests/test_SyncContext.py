"""
Test cases for the SyncContext class.
"""

import random


from folder_replicator.SyncStrategyFactory import SyncStrategyFactory
from folder_replicator.SyncContext import SyncContext


def test_sync_context(tmp_path):
    """
    Test the SyncContext class.

    Args:
        tmp_path: pathlib.Path - the temporary path created by pytest

    Returns:
        None
    """

    temp_src_dir = tmp_path / "source"
    temp_src_dir.mkdir()
    temp_dest_dir = tmp_path / "destination"
    temp_dest_dir.mkdir()
    file = temp_src_dir / "file.txt"
    file.write_text("".join([chr(random.randint(97, 122)) for _ in range(100)]))

    sync_context = SyncStrategyFactory.create_strategy(
        "local", temp_src_dir, temp_dest_dir, True, True, False
    )

    context = SyncContext(sync_context)
    assert context.get_number_of_files() == 1
    assert context.strategy.source.path == temp_src_dir
    assert context.strategy.destination.path == temp_dest_dir
    assert context.strategy.source.files.get(file) is not None
