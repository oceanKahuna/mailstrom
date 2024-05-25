import logging
from gmail_fetcher import GmailFetcher
from chatgpt_processor import ChatGPTProcessor
from email_actions import EmailActions

logging.basicConfig(level=logging.INFO)

def main():
    """
    Main function to fetch emails, analyze them using ChatGPT, and perform actions based on the analysis.
    """
    logging.info("Starting the Gmail fetcher")
    gmail_fetcher = GmailFetcher()
    chatgpt_processor = ChatGPTProcessor()
    
    try:
        gmail_fetcher.connect()
        logging.info("Connected to Gmail")
        
        email_ids = gmail_fetcher.fetch_emails(limit=100)  # Limit to 100 emails
        if email_ids:
            logging.info(f"Fetched {len(email_ids)} emails.")
            email_actions = EmailActions(gmail_fetcher.connection)
            
            for email_id in email_ids:  # Process limited number of emails
                email_content = gmail_fetcher.fetch_email_content(email_id)
                if email_content:
                    relevant_content = gmail_fetcher.extract_relevant_content(email_content)
                    analysis = chatgpt_processor.analyze_email(relevant_content)
                    if analysis:
                        logging.info(f"Analysis for email ID {email_id}: {analysis}")
                        action = analysis.lower().strip()
                        email_actions.delete_or_mark_email(email_id, action)
        else:
            logging.info("No emails found.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        if gmail_fetcher.connection:
            gmail_fetcher.connection.expunge()
            gmail_fetcher.logout()
            logging.info("Logged out from Gmail")

if __name__ == "__main__":
    main()
