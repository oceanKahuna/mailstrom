import logging
from src.gmail_fetcher import GmailFetcher

logging.basicConfig(level=logging.INFO)

def main():
    logging.info("Starting the Gmail fetcher")
    gmail_fetcher = GmailFetcher()
    
    try:
        gmail_fetcher.connect()
        logging.info("Connected to Gmail")
        
        email_ids = gmail_fetcher.fetch_emails()
        if email_ids:
            logging.info(f"Fetched {len(email_ids)} emails.")
            for email_id in email_ids[:5]:  # Print content of first 5 emails for testing
                email_content = gmail_fetcher.fetch_email_content(email_id)
                print(email_content)
        else:
            logging.info("No emails found.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        gmail_fetcher.logout()
        logging.info("Logged out from Gmail")

if __name__ == "__main__":
    main()
