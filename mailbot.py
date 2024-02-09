import sys
from pathlib import Path
import logging

from smtplib import SMTPAuthenticationError, SMTPException
from yagmail import SMTP,YagAddressError, YagConnectionClosed

ARGUMENTS_NB = 2

logger = logging.getLogger()


def check_token_path(string_path):
    """Check if the path is valid (exists AND is a file)

    Args:
        string_path (str): The relative or absolute path

    Returns:
        bool: Path valid (True) or invalid (False)
    """
    return Path(string_path).is_file()


def check_arguments(argv):
    """Check if the arguments provided are valid 

    Args:
        argv (list[str]): Arguments provided by the command line

    Returns:
        bool: Arguments are valid (True) or not (False)
    """    
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


def send_mail(credentials):
    """Sending mail using Yagmail library (Gmail with OAuth2 + SMTP)
    As this library aims only to send mails, the SCOPES are hardcoded inside it. THere is no need to bother with them.

    Args:
        credentials (Path): Path Object to the credentials

    Returns:
        Yag: Yag Object : Main object of the library used to manipulate easily messages metadata
    """
    yag = None
    try:
        yag = SMTP("mycraigdoe2@gmail.com", oauth2_file=str(credentials))
        yag.send(
            to="pierremogrison@gmail.com",
            subject="Yeah, succeeded to send an automated mail!",
            contents="Hi, this is an automated mail. Please do not reply.",
            attachments="README.md",
        )
    except SMTPException as e:
        logger.exception(e)
    except YagAddressError as e:
        logger.exception(
            f"A {type(e).__name__} occurred: The address (sender or receiver) was given in an invalid format"
        )
    except YagConnectionClosed as e:
        logger.exception(f"A {type(e).__name__} occurred: Login required again")

    return yag


def main():
    current_directory = Path.cwd()

    logging.basicConfig(
        filename=f"{current_directory.name}.log",
        filemode="w",
        encoding="UTF-8",
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%d/%m/%Y %H:%M:%S",
        level=logging.INFO,
    )

    if check_arguments(sys.argv) == False:
        raise Exception("Invalid arguments")

    credentials = Path(sys.argv[1])

    if send_mail(credentials) == None:
        return


if __name__ == "__main__":
    main()
