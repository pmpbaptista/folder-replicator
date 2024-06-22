
from folder_replicator.SyncStrategyLocal import SyncStrategyLocal
from folder_replicator.interfaces.SyncStrategy import SyncStrategy


class SyncStrategyFactory:
    """Factory class for creating SyncStrategy objects"""

    @staticmethod
    def create_strategy(strategy_type: str) -> SyncStrategy:
        """
        Create a SyncStrategy object based on the strategy_type provided.

        Args:
            strategy_type: str - the type of strategy to create

        Returns:
            SyncStrategy - the created strategy
        """

        if strategy_type == "local":
            return SyncStrategyLocal()
        else:
            raise ValueError(f"Unknown strategy type: {strategy_type}")
