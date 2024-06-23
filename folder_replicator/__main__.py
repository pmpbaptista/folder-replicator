""" Main module for the folder-replicator package. """

import argparse
from time import sleep

from folder_replicator.lib import logger as fr_logger
from folder_replicator.lib.sync_scheduler import get_seconds_until_next_sync
from folder_replicator.SyncStrategyFactory import SyncStrategyFactory
from folder_replicator.SyncContext import SyncContext


def _parse_args() -> argparse.Namespace:
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
        "--type",
        "-t",
        help="The type of sync to perform",
        choices=["local"],
        default="local",
        type=str,
    )

    parser.add_argument(
        "--source",
        "-s",
        help="The source folder to sync from",
        required=True,
        type=str,
    )

    parser.add_argument(
        "--destination",
        "-d",
        help="The destination folder to sync to",
        required=True,
        type=str,
    )

    parser.add_argument(
        "--schedule",
        "-c",
        help="The schedule to sync on [cron format]",
        default="* 1 * * *",
        type=str,
    )

    parser.add_argument(
        "--dry-run", "-n", action="store_true", help="Perform a dry run", required=False
    )

    parser.add_argument(
        "--recursive",
        "-r",
        action="store_true",
        help="Recursively sync folders",
        required=False,
        default=True,
    )

    parser.add_argument(
        "--delete",
        action="store_true",
        help="Delete files in destination that are not in source",
        required=False,
        default=True,
    )

    parser.add_argument(
        "--log-file",
        "-l",
        help="The log file to write to",
        default="folder_replicator.log",
        required=False,
    )

    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")

    return parser.parse_args()


def main() -> None:
    """
    Main function for the folder-replicator package.

    Args:
        None

    Returns:
        None
    """

    args = _parse_args()
    logger = fr_logger.get_logger(verbose=args.verbose, log_file=args.log_file)
    logger.info("Starting folder-replicator")

    sync_strategy = SyncStrategyFactory.create_strategy(
        args.type, args.source, args.destination, args.recursive, args.delete, args.dry_run
    )

    # The client code picks a concrete strategy and passes it to the context.
    # The client should be aware of the differences between strategies in order
    # to make the right choice.
    sync_context = SyncContext(sync_strategy)

    while True:
        sync_context._strategy.sync()
        sleep(5)

        next_sync = get_seconds_until_next_sync(args.schedule)
        logger.info(f"Next sync in {next_sync} seconds")

        sleep(next_sync)


if __name__ == "__main__":
    main()

def _print_hello() -> None:
    """
    Print "Hello, world!" to the console.

    Args:
        None

    Returns:
        None
    """

    print("Hello, world!")
