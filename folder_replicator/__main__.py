""" Main module for the folder-replicator package. """

import argparse

from folder_replicator.lib import logger as fr_logger
from folder_replicator.SyncContext import SyncContext
from folder_replicator.SyncStrategyLocal import SyncStrategyLocal


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

    parser.add_argument("--type", "-t", help="The type of sync to perform", choices=["local"])

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


def main():
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
    logger.info("Hello, world!")
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
