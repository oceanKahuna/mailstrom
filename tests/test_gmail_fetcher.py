import unittest
from src.gmail_fetcher import GmailFetcher
from src.config import Config

class TestGmailFetcher(unittest.TestCase):

    def setUp(self):
        self.gmail_fetcher = GmailFetcher(
            username=Config.EMAIL_USERNAME,
            password=Config.EMAIL_PASSWORD,
            imap_server=Config.IMAP_SERVER
        )
        self.gmail_fetcher.connect()

    def tearDown(self):
        self.gmail_fetcher.logout()

    def test_fetch_emails(self):
        emails = self.gmail_fetcher.fetch_emails(limit=1)
        self.assertTrue(len(emails) > 0, "No emails fetched")
        email_content = self.gmail_fetcher.fetch_email_content(emails[0])
        self.assertIsNotNone(email_content, "Failed to fetch email content")

if __name__ == '__main__':
    unittest.main()
