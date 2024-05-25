import imaplib
import email
import logging
from email.header import decode_header
from src.config import Config

class GmailFetcher:
    def __init__(self, username=Config.EMAIL_USERNAME, password=Config.EMAIL_PASSWORD, imap_server=Config.IMAP_SERVER):
        self.username = username
        self.password = password
        self.imap_server = imap_server
        self.connection = None

    def connect(self):
        try:
            self.connection = imaplib.IMAP4_SSL(self.imap_server)
            self.connection.login(self.username, self.password)
            logging.info(f"Connected to Gmail at {self.imap_server}")
        except imaplib.IMAP4.error as e:
            logging.error(f"Failed to connect to Gmail: {e}")
            raise

    def fetch_emails(self, folder="inbox", search_criteria="ALL"):
        if self.connection is None:
            logging.error("No connection established. Call connect() first.")
            return []

        try:
            self.connection.select(folder)
            status, messages = self.connection.search(None, search_criteria)
            if status != "OK":
                logging.error(f"Failed to search emails with criteria {search_criteria}")
                return []

            email_ids = messages[0].split()
            return email_ids
        except imaplib.IMAP4.error as e:
            logging.error(f"Failed to fetch emails: {e}")
            return []

    def fetch_email_content(self, email_id):
        if self.connection is None:
            logging.error("No connection established. Call connect() first.")
            return None

        try:
            status, msg_data = self.connection.fetch(email_id, "(RFC822)")
            if status != "OK":
                logging.error(f"Failed to fetch email with ID {email_id}")
                return None

            msg = email.message_from_bytes(msg_data[0][1])
            return msg
        except imaplib.IMAP4.error as e:
            logging.error(f"Failed to fetch email content: {e}")
            return None

    def logout(self):
        if self.connection:
            self.connection.logout()
            logging.info("Logged out from Gmail.")
