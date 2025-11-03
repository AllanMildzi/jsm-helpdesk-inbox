import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.message import EmailMessage

from core import Config
from utils import get_logger

logger = get_logger(__name__)

class Gmail:
    def authenticate():
        TOKEN_PATH = Config.TOKEN_PATH
        CREDENTIALS_PATH = Config.CREDENTIALS_PATH
        SCOPES = Config.SCOPES
        
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if TOKEN_PATH.exists():
            creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
        
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                logger.debug(f"The path is : {CREDENTIALS_PATH}")
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(CREDENTIALS_PATH), SCOPES
                )
                creds = flow.run_local_server(port=0)
            
            # Save the credentials for the next run
            with open(TOKEN_PATH, "w") as token:
                token.write(creds.to_json())

        try:
            return build("gmail", "v1", credentials=creds)

        except HttpError as error:
            logger.exception(f"An error occurred: {error}")
    
    @classmethod
    def search_messages(cls, service, max_results, query):
        result = service.users().messages().list(userId='me', 
                                                 maxResults=max_results,
                                                 q=query,
                                                 ).execute()
        messages = []
        
        if 'messages' in result:
            messages.extend(result['messages'])
        
        return messages
    
    @classmethod
    def read_message(cls, service, message):
        try:
            result = service.users().messages().get(userId='me', 
                                                    id=message['id'], 
                                                    format='full'
                                                    ).execute()
            if not result:
                return None
            
            input_message = EmailMessage()

            payload = result["payload"]
            headers = payload.get("headers")
            parts = payload.get("parts")

            if headers:
                for header in headers:
                    name = header.get("name")
                    value = header.get("value")

                    match name:
                        case "From":
                            input_message["From"] = value
                        case "To":
                            input_message["To"] = value
                        case "Date":
                            input_message["Date"] = value
                        case "Subject":
                            input_message["Subject"] = value
            
            if parts:
                for part in parts:
                    mimeType = part.get("mimeType")
                    body = part.get("body")
                    data = body.get("data")

                    if mimeType == 'text/plain' and data:
                        input_message.set_content(data)
                        break
        
        except HttpError as error:
            logger.exception(f"An error occurred: {error}")
            input_message = None

        return input_message
    
    @classmethod
    def mark_as_read(cls, service, messages):
        service.users().messages().batchModify(userId='me',
                                               body={
                                                   'ids': [m['id'] for m in messages],
                                                   'removeLabelIds': ['UNREAD']
                                                   }).execute()
    
    @classmethod
    def send_message(cls, service, sender, recipient, subject, content):
        try:
            message = EmailMessage()

            message.set_content(content)

            message["To"] = recipient
            message["From"] = sender
            message["Subject"] = subject

            # encoded message
            encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

            create_message = {"raw": encoded_message}
            send_message = (
                service.users()
                .messages()
                .send(userId="me", body=create_message)
                .execute()
            )
        
        except HttpError as error:
            logger.exception(f"An error occurred: {error}")
            send_message = None
        
        return send_message