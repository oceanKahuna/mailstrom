import unittest
from src.gmail_fetcher import GmailFetcher

class TestFooterExtraction(unittest.TestCase):

    def setUp(self):
        self.gmail_fetcher = GmailFetcher(
            username="test@example.com",
            password="password",
            imap_server="imap.example.com"
        )

    def test_extract_footer(self):
        body = "Hello,\n\nThis is the main content of the email.\n\nBest,\nSender\n\nTo unsubscribe, click here."
        footer = self.gmail_fetcher.extract_footer(body, num_lines=3)
        self.assertIn("To unsubscribe, click here.", footer)
        self.assertIn("Best,", footer)

if __name__ == '__main__':
    unittest.main()
