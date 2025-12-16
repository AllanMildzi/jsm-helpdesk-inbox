import time
import threading
import queue
from imapclient import IMAPClient

from core.constants import *
from gmail import Gmail
from graphs.builder import build_graph
from utils import get_logger

logger = get_logger(__name__)

class EmailListener:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        
        self.mailbox = MAILBOX
        self.running = False

        self.message_queue = queue.Queue(maxsize=QUEUE_MAX_LENGTH)
        self.consumer_threads = []
    
    def _imap_listener(self):
        server = IMAPClient(self.host, use_uid=True, ssl=True)
        server.login(self.username, self.password)
        server.select_folder("INBOX")

        # Gmail authentication
        service = Gmail.authenticate()

        self._start_consumers()
        self.running = True

        while self.running:
            self._process_unread_messages(service)
            time.sleep(CHECK_INTERVAL)

            if self.message_queue.empty():
                break

        server.idle()
        logger.info("IMAP IDLE listening for new mail.")

        while self.running:
            try:
                responses = server.idle_check(timeout=CHECK_INTERVAL)
                if responses:
                    logger.info("New message detected.")
                    if not self.message_queue.full():
                        self._process_unread_messages(service)
                    else:
                        logger.debug("Queue is full")
                else:
                    logger.debug("No new messages.")

            except Exception as e:
                logger.exception(f"IMAP error: {e}. Retrying in 10s.")
                time.sleep(RETRYING_TIME)

        self.running = False
        server.logout()
    
    def _process_unread_messages(self, service):
        results = Gmail.search_messages(service, QUEUE_MAX_LENGTH, SEARCH_QUERY)
        
        if results:
            logger.debug(f"Found {len(results)} unread messages.")
            # Gmail.mark_as_read(service, results)

            for msg in results:
                try:
                    self.message_queue.put(msg)
                except queue.Full:
                    break
        else:
            logger.debug("No unread messages found.")

    def _start_consumers(self):
        for _ in range(POOL_MAX_LENGTH):
            consumer_thread = threading.Thread(target=self._email_consumer, daemon=True)
            consumer_thread.start()
            self.consumer_threads.append(consumer_thread)

    def _email_consumer(self):
        while not self.running:
            time.sleep(INIT_WAIT_TIME)

        service = Gmail.authenticate()

        while self.running:
            try:
                message = self.message_queue.get(block=True, timeout=QUEUE_TIMEOUT)
            except queue.Empty:
                continue

            try:
                # Reading email + LLM + Ticket creation logics here
                message_object = Gmail.read_message(service, message)

                graph = build_graph()
                graph.invoke({"email": message_object}, context={"gmail_service": service})
            
            except Exception as e:
                logger.exception(f"Error in consumer thread: {e}")
            finally:
                self.message_queue.task_done()

    def start(self):
        # Start IMAP listener in a background thread.
        thread = threading.Thread(target=self._imap_listener, daemon=True)
        thread.start()
        logger.info("EmailListener started")
    
    def stop(self):
        # Stop IMAP listener
        logger.info("Stopping EmailListener")
        
        self.running = False
        self.message_queue.join()

        time.sleep(INIT_WAIT_TIME)
        logger.info("EmailListener stopped.")