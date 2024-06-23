from folder_replicator.SyncStrategyLocal import SyncStrategyLocal
from folder_replicator.interfaces.SyncStrategy import SyncStrategy
from folder_replicator.lib import logger as fr_logger


class SyncStrategyFactory:
    """Factory class for creating SyncStrategy objects"""

    @staticmethod
    def create_strategy(
        strategy_type: str,
        source: str,
        destination: str,
        recursive: bool,
        delete: bool,
        dry_run: bool,
    ) -> SyncStrategy:
        """
        Create a SyncStrategy object based on the strategy_type provided.

        Args:
            strategy_type: str - the type of strategy to create

        Returns:
            SyncStrategy - the created strategy
        """

        logger = fr_logger.get_logger()

        if strategy_type == "local":
            logger.info("Creating local sync strategy")
            return SyncStrategyLocal(source, destination, recursive, delete, dry_run)
        else:
            logger.error(f"Unknown strategy type: {strategy_type}")
            raise ValueError(f"Unknown strategy type: {strategy_type}")
