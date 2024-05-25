import imaplib
import email
import logging
from config import Config

class GmailFetcher:
    def __init__(self, username=Config.EMAIL_USERNAME, password=Config.EMAIL_PASSWORD, imap_server=Config.IMAP_SERVER):
        self.username = username
        self.password = password
        self.imap_server = imap_server
        self.connection = None

    def connect(self):
        logging.info("Attempting to connect to Gmail")
        try:
            self.connection = imaplib.IMAP4_SSL(self.imap_server)
            self.connection.login(self.username, self.password)
            logging.info(f"Connected to Gmail at {self.imap_server}")
        except imaplib.IMAP4.error as e:
            logging.error(f"Failed to connect to Gmail: {e}")
            raise

    def fetch_emails(self, folder="inbox", search_criteria="ALL", limit=100):
        logging.info(f"Fetching up to {limit} emails from folder: {folder} with criteria: {search_criteria}")
        if self.connection is None:
            logging.error("No connection established. Call connect() first.")
            return []

        try:
            self.connection.select(folder)
            status, messages = self.connection.search(None, search_criteria)
            if status != "OK":
                logging.error(f"Failed to search emails with criteria {search_criteria}")
                return []

            email_ids = messages[0].split()[:limit]
            logging.info(f"Found {len(email_ids)} emails")
            return email_ids
        except imaplib.IMAP4.error as e:
            logging.error(f"Failed to fetch emails: {e}")
            return []

    def fetch_email_content(self, email_id):
        logging.info(f"Fetching content for email ID: {email_id}")
        if self.connection is None:
            logging.error("No connection established. Call connect() first.")
            return None

        try:
            status, msg_data = self.connection.fetch(email_id, "(RFC822)")
            if status != "OK":
                logging.error(f"Failed to fetch email with ID {email_id}")
                return None

            msg = email.message_from_bytes(msg_data[0][1])
            logging.info(f"Fetched email content for ID: {email_id}")
            return msg
        except imaplib.IMAP4.error as e:
            logging.error(f"Failed to fetch email content: {e}")
            return None

    def extract_relevant_content(self, email_msg):
        subject = email_msg["subject"]
        from_email = email.utils.parseaddr(email_msg["From"])[1]
        body = ""

        if email_msg.is_multipart():
            for part in email_msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    break
        else:
            body = email_msg.get_payload(decode=True).decode()

        first_paragraph = body.split('\n\n')[0]
        footer = self.extract_footer(body)

        relevant_content = f"From: {from_email}\nSubject: {subject}\n\n{first_paragraph}\n\n{footer}"
        return relevant_content

    def extract_footer(self, body, num_lines=5):
        lines = body.split('\n')
        footer = []
        for line in reversed(lines):
            if "unsubscribe" in line.lower() or "opt-out" in line.lower():
                footer.append(line)
            elif len(footer) > 0 and len(footer) < num_lines:
                footer.append(line)
            elif len(footer) >= num_lines:
                break
        footer.reverse()
        return '\n'.join(footer)

    def logout(self):
        logging.info("Logging out from Gmail")
        if self.connection:
            self.connection.logout()
            logging.info("Logged out from Gmail.")
