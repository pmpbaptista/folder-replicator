from __future__ import annotations

from folder_replicator.interfaces.SyncStrategy import SyncStrategy


class SyncContext:
    """
    The SyncContext defines the interface of interest to clients.
    """

    def __init__(self, strategy: SyncStrategy) -> None:
        """
        SyncContext accepts a strategy object through the constructor and saves it
        for future use.
        """

        self._strategy = strategy

    @property
    def strategy(self) -> SyncStrategy:
        """
        The SyncContext maintains a reference to one of the Strategy objects. The
        SyncContext does not know the concrete class of a strategy. It should work
        with all strategies via the SyncStrategy interface.
        """

        return self._strategy

    @strategy.setter
    def strategy(self, strategy: SyncStrategy) -> None:
        """
        SyncContext allows replacing a Strategy object at runtime.
        """

        self._strategy = strategy

    def do_some_file_logic(self) -> None:
        """
        The SyncContext can implement some logic that is common to all strategies.
        """

        # ...

        print("SyncContext: Sorting files before syncing")
        files = ["file_x", "file_a", "file_b", "file_c"]
        files.sort()
        print(files)
