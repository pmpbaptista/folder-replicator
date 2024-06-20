"""
    The Strategy interface declares operations common to all supported versions
    of sync procedure.

    The SyncContext uses this interface to call the algorithm defined by Concrete
    SyncStrategies.
"""

from abc import ABC, abstractmethod


class SyncStrategy(ABC):
    """
    The Strategy interface declares operations common to all supported versions
    of sync procedure.
    
    """
    @abstractmethod
    def sync(self, source: str, destination: str):
        """
        The sync method is the main method that the SyncContext will use to
        perform the sync operation.
        args:
            source: str
            destination: str
        returns:
            None
        """
        pass
