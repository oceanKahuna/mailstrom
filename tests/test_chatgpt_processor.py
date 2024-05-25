import unittest
from src.chatgpt_processor import ChatGPTProcessor
from src.config import Config

class TestChatGPTProcessor(unittest.TestCase):

    def setUp(self):
        self.processor = ChatGPTProcessor(api_key=Config.OPENAI_API_KEY)

    def test_analyze_email(self):
        content = "From: test@example.com\nSubject: Test Email\n\nThis is a test email."
        response = self.processor.analyze_email(content)
        self.assertIsNotNone(response, "No response from ChatGPT")
        self.assertTrue(len(response) > 0, "Empty response from ChatGPT")

if __name__ == '__main__':
    unittest.main()
