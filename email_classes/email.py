class email: 

    def __init__(self, sender=None, receiver=None, subject=None, body=None):
        # Constructor for email class. Initializes sender, receiver, subject, and body properties.
        if isinstance(sender, dict):  # If first argument is a dictionary, use it
            email_data = sender
            self.sender = email_data.get('sender', "")
            self.receiver = email_data.get('receiver', "")
            self.subject = email_data.get('subject', "")
            self.body = email_data.get('body', "")
        else:  # Otherwise, use regular parameters
            self.sender = sender or ""
            self.receiver = receiver or ""
            self.subject = subject or ""
            self.body = body or ""

    def get_sender(self):
        # Returns the sender of the email.
        return self.sender
    
    def get_receiver(self):
        # Returns the receiver of the email.
        return self.receiver
    
    def get_subject(self):
        # Returns the subject of the email.
        return self.subject
    
    def get_body(self):
        # Returns the body of the email.
        return self.body
    
    def to_dict(self):
        # Returns a dictionary representation of the email, with keys "sender", "receiver", "subject", and "body".  This dictionary can be used to recreate the original email object.  For example:
        return {
            'sender': self.sender,
            'receiver': self.receiver,
            'subject': self.subject,
            'body': self.body
        }


