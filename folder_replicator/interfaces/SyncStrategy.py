from abc import ABC, abstractmethod


class SyncStrategy(ABC):
    """
    The Strategy interface declares operations common to all supported versions
    of sync procedure.

    The SyncContext uses this interface to call the algorithm defined by Concrete
    SyncStrategies.

    """

    @abstractmethod
    def sync(self):
        """
        The sync method is the main method that the SyncContext will use to
        perform the sync operation.

        Args:
            None

        Returns:
            None
        """
        pass
