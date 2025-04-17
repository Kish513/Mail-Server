
import socket
class smtp_message:
    def __init__(self, sender, receiver, subject, body, server_ip="127.0.0.1"):
        self.sender = sender
        self.receiver = receiver
        self.subject = subject
        self.body = body
        self.server_ip = server_ip

    def to_string(self):
        helo_command = f"HELO {self.server_ip}"
        mail_from = f"MAIL FROM:{self.sender}"
        rcpt_to = f"RCPT TO:{self.receiver}"
        data_command = "DATA"
        email_headers = f"Subject: {self.subject}\nFrom: {self.sender}\nTo: {self.receiver}\n"
        email_body = f"\n{self.body}\n"
        end_of_message = "."
        quit_command = "QUIT"

        return "\n".join([
            helo_command,
            mail_from,
            rcpt_to,
            data_command,
            email_headers + email_body,
            end_of_message,
            quit_command
        ])
    
    def get_message(self):
        return self.to_string().encode()


