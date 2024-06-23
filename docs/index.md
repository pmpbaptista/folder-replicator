Welcome to the documentation for the `folder-replicator` package.

This is a Python utility for file backup and synchronization.

The design of this package is based on the [Strategy Pattern](https://en.wikipedia.org/wiki/Strategy_pattern)and
the [Factory Method Pattern](https://en.wikipedia.org/wiki/Factory_method_pattern).

The main goal of this package is to provide a simple and flexible way to synchronize files between two folders,
for now, the synchronization is only one-way, from the source folder to the destination folder.

The synchronization is done by comparing the files in the source folder with the files in the destination folder.
The files that are in the source folder but not in the destination folder are copied to the destination folder,
and the files that are in the destination folder but not in the source folder are deleted from the destination
folder (if the `delete` parameter is set to `True`).

The package provides a default strategy for synchronization, the `SyncStrategyLocal`, which uses the local file
system to copy the files.

## Table of Contents

- [Getting Started](getting-started.md)

- [Reference](reference.md)
