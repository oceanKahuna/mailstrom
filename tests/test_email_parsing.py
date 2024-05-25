import unittest
from email.message import EmailMessage
from src.gmail_fetcher import GmailFetcher

class TestEmailParsing(unittest.TestCase):

    def setUp(self):
        self.gmail_fetcher = GmailFetcher(
            username="test@example.com",
            password="password",
            imap_server="imap.example.com"
        )

    def test_extract_relevant_content(self):
        msg = EmailMessage()
        msg["Subject"] = "Test Subject"
        msg["From"] = "sender@example.com"
        msg.set_content("This is the first paragraph.\n\nThis is the second paragraph.\n\nBest,\nSender")

        content = self.gmail_fetcher.extract_relevant_content(msg)
        self.assertIn("Test Subject", content)
        self.assertIn("sender@example.com", content)
        self.assertIn("This is the first paragraph.", content)
        self.assertIn("Best,\nSender", content)

if __name__ == '__main__':
    unittest.main()
