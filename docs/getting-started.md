# Getting Started

This is a guide to help you get started with the project. It will walk you through the steps to get the project up and running on your local machine.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- You have installed Python 3.8 or later.
- You have installed Poetry.
- You have a Linux machine. The project may work on other operating systems, but it has only been tested on Linux.

## Running the project

To set up the project, follow these steps:

1. Step 1

```sh
poetry install
```

2. Step 2

```sh
poetry run folder-replicator --help
```

### Configuration

The execution of the project can be configured using command-line arguments. You can see the available options by running the following command:

```sh
poetry run folder-replicator --help
```

Here is an example of how to run the project with some options:

```sh
poetry run folder-replicator --source /path/to/source --destination /path/to/destination --schedule="0 0 * * *" --verbose --log-file /path/to/log-file.log

```

### Environment Variables

The project uses environment variables to configure the application. You can set these variables in a `.env` file in the root of the project.

```sh
# .env
FR_VERBOSE=true
```


## Running the project (Docker)

To run the project, follow these steps:

1. Step 1
2. Step 2
3. Step 3