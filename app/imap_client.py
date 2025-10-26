import time
import threading
import queue

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

        self.message_queue = queue.Queue(maxsize=QUEUE_MAX_LENGTH)
        self.consumer_threads = []

        self.gmail = None

    def _imap_listener(self):
        print("IMAP IDLE listening for new mail.")

        # Gmail authentication
        service = self.gmail.authenticate()

        self._start_consumers()
        self.running = True

        while self.running:
            try:
                if not self.message_queue.full():
                    results = self.gmail.search_messages(service, 
                                                         QUEUE_MAX_LENGTH - self.message_queue.qsize(), 
                                                         SEARCH_QUERY)
                
                    if results:
                        #gmail.mark_as_read(service, results)
                        print(f"Found {len(results)} results.")

                        for msg in results:
                            try:
                                self.message_queue.put(msg)
                            except queue.Full:
                                break
                    
                    else:
                        print("Server sent nothing")
                else:
                    print("Queue is full")

                time.sleep(CHECK_INTERVAL)
            
            except Exception as e:
                print(f"IMAP error: {e}. Retrying in 10s.")
                time.sleep(RETRYING_TIME)
            
        self.running = False
    
    def _start_consumers(self):
        for _ in range(POOL_MAX_LENGTH):
            consumer_thread = threading.Thread(target=self._email_consumer, daemon=True)
            consumer_thread.start()
            self.consumer_threads.append(consumer_thread)

    def _email_consumer(self):
        while not self.running or self.gmail is None:
            time.sleep(INIT_WAIT_TIME)

        service = self.gmail.authenticate()

        while self.running:
            try:
                message = self.message_queue.get(block=True, timeout=1.0)
            except queue.Empty:
                continue

            try:
                # Reading email + LLM + Ticket creation logics here
                print(self.gmail.read_message(service, message))
                time.sleep(5)
            
            except Exception as e:
                print(f"Error in consumer thread: {e}")
            finally:
                self.message_queue.task_done()

    def start(self):
        # Start IMAP listener in a background thread.
        self.gmail = Gmail()
        thread = threading.Thread(target=self._imap_listener, daemon=True)
        thread.start()
        print("EmailListener started")