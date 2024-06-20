"""
Concrete Sync Strategy class that implements the local sync strategy.

The SyncContext uses this class to call the algorithm defined by the Concrete
SyncStrategy.
"""

from folder_replicator.interfaces.SyncStrategy import SyncStrategy


class SyncStrategyLocal(SyncStrategy):
    def sync(self, source: str, destination: str):
        print(f"Syncing {source} to {destination} using local strategy")
        # Syncing logic here
        pass
