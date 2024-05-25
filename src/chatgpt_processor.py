import logging
from openai import OpenAI
from config import Config

class ChatGPTProcessor:
    def __init__(self, api_key=Config.OPENAI_API_KEY):
        self.client = OpenAI(api_key=api_key)

    def analyze_email(self, subject, body):
        prompt = f"Subject: {subject}\n\n{body}\n\nAnalyze this email and provide suggestions for the following:\n1. Should we delete or mark as read? (Delete/Mark as Read)\n"

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an assistant that analyzes email content."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.7,
            )

            analysis = response.choices[0].message.content.strip()
            return analysis
        except Exception as e:
            logging.error(f"Failed to analyze email: {e}")
            return None
