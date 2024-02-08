import logging
import sys
from pathlib import Path
import base64
from email.message import EmailMessage

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

ARGUMENTS_NB = 2
SCOPES = ["https://www.googleapis.com/auth/gmail.compose"]

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
    mail = None

    # TODO Add a check for the permissions in SCOPES. If not present for this function, delete then recreate the token file
    try:
        service = build("gmail", "v1", credentials=credentials)
        message = EmailMessage()

        # Headers
        message["To"] = ""
        message["From"] = ""
        message["Subject"] = "Yeah, succeeded to send an automated mail!"

        # Body
        message.set_content("Hi, this is automated mail. Please do not reply.")

        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        request_message = {"raw": encoded_message}
        mail = (
            service.users().messages().send(userId="me", body=request_message).execute()
        )
        logger.info(f"Message sent\nid: {mail['id']}")

    except HttpError as error:
        logger.exception(f"An error occurred: {error}")
        draft = None

    return mail


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

    credentials = None
    token_file = Path("token.json")
    credentials_file = Path(sys.argv[1])

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if Path(token_file).is_file():
        credentials = Credentials.from_authorized_user_file(str(token_file), SCOPES)
    # If there are no (valid) credentials, let the user log in
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                str(credentials_file), SCOPES
            )
            credentials = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(str(token_file), "w") as token:
            token.write(credentials.to_json())

    if send_mail(credentials) == None:
        return


if __name__ == "__main__":
    main()
