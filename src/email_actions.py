import logging

class EmailActions:
    def __init__(self, connection):
        self.connection = connection

    def delete_or_mark_email(self, email_id, action):
        if action.lower() == "delete":
            logging.info(f"Deleting email ID {email_id}")
            self.connection.store(email_id, '+FLAGS', '\\Deleted')
        elif action.lower() == "mark as read":
            logging.info(f"Marking email ID {email_id} as read")
            self.connection.store(email_id, '+FLAGS', '\\Seen')
        else:
            logging.error(f"Unknown action {action} for email ID {email_id}")

    def expunge(self):
        self.connection.expunge()
