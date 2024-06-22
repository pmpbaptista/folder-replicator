""" Main module for the folder-replicator package. """

import argparse
from time import sleep

from folder_replicator.SyncStrategyFactory import SyncStrategyFactory
from folder_replicator.lib import logger as fr_logger
from folder_replicator.SyncContext import SyncContext
from folder_replicator.lib.sync_scheduler import get_seconds_until_next_sync


def _parse_args():
    """
    Parse command-line arguments.

    Args:
        None

    Returns:
        args: argparse.Namespace - the parsed arguments
    """

    parser = argparse.ArgumentParser(
        description="Sync files between folders",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--type", "-t", help="The type of sync to perform", choices=["local"], default="local"
    )

    parser.add_argument("--source", "-s", help="The source folder to sync from", required=True)

    parser.add_argument(
        "--destination", "-d", help="The destination folder to sync to", required=True
    )

    parser.add_argument(
        "--schedule", "-c", help="The schedule to sync on [cron format]", default="* 1 * * *"
    )

    parser.add_argument("--dry-run", "-n", action="store_true", help="Perform a dry run")

    parser.add_argument("--recursive", "-r", action="store_true", help="Recursively sync folders")

    parser.add_argument(
        "--delete", action="store_true", help="Delete files in destination that are not in source"
    )

    parser.add_argument(
        "--log-file", "-l", help="The log file to write to", default="folder_replicator.log"
    )

    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")

    return parser.parse_args()


def _print_hello():
    """
    Print a hello message.

    Args:
        None

    Returns:
        None
    """

    print("Hello, world!")


def sync(args: argparse.Namespace, sync_context: SyncContext) -> None:
    """
    Sync files between folders.

    Args:
        args: argparse.Namespace - the parsed arguments
        sync_context: SyncContext - the sync context to use

    Returns:
        None
    """

    print(f"Next sync in {get_seconds_until_next_sync(args.schedule)} seconds")

    sync_context.do_some_file_logic()

    sync_context.strategy.sync(args.source, args.destination)


def main() -> None:
    """
    Main function for the folder-replicator package.

    Args:
        None

    Returns:
        None
    """

    _print_hello()

    args = _parse_args()
    logger = fr_logger.get_logger(verbose=args.verbose, log_file=args.log_file)
    logger.info("Starting folder-replicator")

    sync_strategy = SyncStrategyFactory.create_strategy(args.type)

    # The client code picks a concrete strategy and passes it to the context.
    # The client should be aware of the differences between strategies in order
    # to make the right choice.
    sync_context = SyncContext(sync_strategy)

    while True:
        # The client code should be able to work with any strategy via the
        # SyncStrategy interface.
        sync(args, sync_context)
        next_sync = get_seconds_until_next_sync(args.schedule)
        logger.info(f"Next sync in {next_sync} seconds")
        sleep(next_sync)


if __name__ == "__main__":
    main()
