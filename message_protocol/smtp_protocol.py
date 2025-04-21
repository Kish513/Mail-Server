
import socket
class smtp_message:
    def __init__(self, mail,server_ip="127.0.0.1"):
        self.mail = mail
        self.server_ip = server_ip

    def to_string(self):
        sender = self.mail.get_sender()
        receiver = self.mail.get_receiver()
        subject = self.mail.get_subject()
        body = self.mail.get_body()
        helo_command = f"HELO {self.server_ip}"
        mail_from = f"MAIL FROM:{sender}"
        rcpt_to = f"RCPT TO:{receiver}"
        data_command = "DATA"
        email_headers = f"Subject: {subject}\nFrom: {sender}\nTo: {receiver}\n"
        email_body = f"\n{body}\n"
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


