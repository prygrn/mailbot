import logging
import sys
from pathlib import Path

ARGUMENTS_NB = 2

logger = logging.getLogger()


def check_token_path(string_path):
    return Path(string_path).is_file()


def check_arguments(argv):
    if len(argv) != ARGUMENTS_NB:
        logger.critical(
            """This tool requires the following arguments:
                     - path/to/the/credentials/file"""
        )
        return False

    if check_token_path(argv[1]):
        oauth_token = argv[1]
        return True
    else:
        logger.critical("The file specified does not exist")
        return False


if __name__ == "__main__":
    current_directory = Path.cwd()

    logging.basicConfig(
        filename=f"{current_directory.name}.log",
        filemode="w",
        encoding="UTF-8",
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%d/%m/%Y %H:%M:%S",
        level=logging.INFO,
    )

    print(sys.argv)
    print(type(sys.argv))

    if check_arguments(sys.argv) == False:
        raise Exception("Invalid arguments")
