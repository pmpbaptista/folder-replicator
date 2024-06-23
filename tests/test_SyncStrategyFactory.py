"""
Test the SyncStrategyFactory class.
"""

from folder_replicator.SyncStrategyFactory import SyncStrategyFactory
from folder_replicator.SyncStrategyLocal import SyncStrategyLocal


def test_create_strategy(tmp_path):
    """
    Test the create_strategy method of the SyncStrategyFactory class.

    Args:
        tmp_path: pathlib.Path - the temporary path created by pytest

    Returns:
        None
    """

    temp_src_dir = tmp_path / "source"
    temp_src_dir.mkdir()
    temp_dest_dir = tmp_path / "destination"
    temp_dest_dir.mkdir()
    
    strategy = SyncStrategyFactory.create_strategy(
        "local", temp_src_dir, temp_dest_dir, True, True, False
    )
    assert isinstance(strategy, SyncStrategyLocal)
    assert strategy.source.path == temp_src_dir
    assert strategy.destination.path == temp_dest_dir

def test_create_strategy_unknown(tmp_path):
    """
    Test the create_strategy method of the SyncStrategyFactory class with an unknown strategy type.
    """

    temp_src_dir = tmp_path / "source"
    temp_src_dir.mkdir()
    temp_dest_dir = tmp_path / "destination"
    temp_dest_dir.mkdir()
    
    try:
        SyncStrategyFactory.create_strategy(
            "unknown", temp_src_dir, temp_dest_dir, True, True, False
        )
    except ValueError as e:
        assert str(e) == "Unknown strategy type: unknown"
    else:
        assert False
