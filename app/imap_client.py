import time
import threading

from core.constants import *
from gmail import Gmail

class EmailListener:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        
        self.mailbox = MAILBOX
        self.check_interval = CHECK_INTERVAL
        self.running = False

    def _imap_listener(self):
        print("IMAP IDLE listening for new mail.")

        # Gmail authentication
        gmail = Gmail()
        service = gmail.authenticate()

        self.running = True

        while self.running:
            try:
                results = gmail.search_messages(service, SEARCH_QUERY)
                if results:
                    #gmail.mark_as_read(service, results)
                    print(f"Found {len(results)} results.")

                    for m in results:
                        print(gmail.read_message(service, m))
                
                else:
                    print("Server sent nothing")

                time.sleep(CHECK_INTERVAL)
            
            except Exception as e:
                print(f"IMAP error: {e}. Retrying in 10s.")
                time.sleep(RETRYING_TIME)
        
        self.running = False

    def start(self):
        # Start IMAP listener in a background thread.
        thread = threading.Thread(target=self._imap_listener, daemon=True)
        thread.start()
        print("EmailListener started")