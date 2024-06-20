""" Main module for the folder-replicator package. """

from folder_replicator.SyncContext import SyncContext
from folder_replicator.SyncStrategyLocal import SyncStrategyLocal


def main():
    """
    Main function for the folder-replicator package.
    args:
        None
    returns:
        None
    """

    print("Hello, world!")

    # The client code picks a concrete strategy and passes it to the context.
    # The client should be aware of the differences between strategies in order
    # to make the right choice.


    sync_context = SyncContext(SyncStrategyLocal())

    # The client code should be able to work with any strategy via the
    # SyncStrategy interface.
    sync_context.do_some_file_logic()

    sync_context.strategy.sync("my_source", "my_destination")


if __name__ == "__main__":
    main()
