import socket
from message_protocol.smtp_protocol import smtp_message
import ssl
from email_classes.email import email

class SMTPClient:

    def __init__(self, server_ip="127.0.0.1", port=2525):
        # Initialize socket and server details 
        self.server_ip = server_ip
        self.port = port
        self.socket = None


    def secure_socket(self):
        #secures the socket
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        context.load_verify_locations('certificate.crt')
        context.check_hostname = False  # Disable hostname checking
        ssl_socket = context.wrap_socket(self.socket, server_hostname=self.server_ip)
        self.socket = ssl_socket


    def send_email(self, mail):
        #gets mail and sends it
        message = smtp_message(mail, self.server_ip)

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.secure_socket()

        self.socket.connect((self.server_ip, self.port))
                        
        self.socket.send(message.get_message())

        self.socket.recv(1024).decode()  # Receive server response

        self.socket.close()