class email:
    def __init__(self, sender=None, receiver=None, subject=None, body=None):
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
        return self.sender
    
    def get_receiver(self):
        return self.receiver
    
    def get_subject(self):
        return self.subject
    
    def get_body(self):
        return self.body
    
    def to_dict(self):
        return {
            'sender': self.sender,
            'receiver': self.receiver,
            'subject': self.subject,
            'body': self.body
        }


