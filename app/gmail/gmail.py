from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from base64 import urlsafe_b64decode

from core import Config
from models.message import Message

class Gmail:
    def __init__(self):
        self.TOKEN_PATH = Config.TOKEN_PATH
        self.CREDENTIALS_PATH = Config.CREDENTIALS_PATH
        self.SCOPES = Config.SCOPES

    def authenticate(self):
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if self.TOKEN_PATH.exists():
            creds = Credentials.from_authorized_user_file(self.TOKEN_PATH, self.SCOPES)
        
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                print(f"The path is : {self.CREDENTIALS_PATH}")
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(self.CREDENTIALS_PATH), self.SCOPES
                )
                creds = flow.run_local_server(port=0)
            
            # Save the credentials for the next run
            with open(self.TOKEN_PATH, "w") as token:
                token.write(creds.to_json())

        try:
            return build("gmail", "v1", credentials=creds)

        except HttpError as error:
            print(f"An error occurred: {error}")
    
    def search_messages(self, service, query):
        result = service.users().messages().list(userId='me', 
                                                 q=query
                                                 ).execute()
        messages = []
        
        if 'messages' in result:
            messages.extend(result['messages'])
        
        while 'nextPageToken' in result:
            page_token = result['nextPageToken']
            result = service.users().messages().list(userId='me', 
                                                     q=query, 
                                                     pageToken=page_token
                                                     ).execute()
            if 'messages' in result:
                messages.extend(result['messages'])
        
        return messages
    
    def read_message(self, service, message):
        result = service.users().messages().get(userId='me', 
                                                id=message['id'], 
                                                format='full'
                                                ).execute()
        if not result:
            return None
        
        new_message = Message()

        payload = result["payload"]
        headers = payload.get("headers")
        parts = payload.get("parts")

        if headers:
            for header in headers:
                name = header.get("name")
                value = header.get("value")

                match name:
                    case "From":
                        new_message.set_sender(value)
                    case "Date":
                        new_message.set_date(value)
                    case "Subject":
                        new_message.set_subject(value)
        
        if parts:
            for part in parts:
                mimeType = part.get("mimeType")
                body = part.get("body")
                data = body.get("data")

                if mimeType == 'text/plain' and data:
                    text_content = urlsafe_b64decode(data).decode()
                    new_message.text = text_content
                    break

        return new_message
    
    def mark_as_read(self, service, messages):
        service.users().messages().batchModify(userId='me',
                                               body={
                                                   'ids': [m['id'] for m in messages],
                                                   'removeLabelIds': ['UNREAD']
                                                   }).execute()