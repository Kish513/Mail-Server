import socket
import db.UserDBInterface as UserDBInterface
import email_classes.email as email_class
import threading
from client.smtp_client import SMTPClient
import ssl
import smtplib
from email.message import EmailMessage

# Define the server and port

# Create a socket object
class SMTPServer:
    SMTP_SERVER_PORT = 2525
    MAX_MESSGE_LENGTH = 1024
    OK_RETURN_MESSAGE = "250 OK\r\n"
    def __init__(self):
        self.ip = self.get_ip_of_device()
        self.name = None
        self.port = self.SMTP_SERVER_PORT
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


        hostname, _, _ = socket.gethostbyaddr(self.ip)
        self.name = hostname

    
    def secure_socket(self, client_socket):
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain("certificate.crt", "server/private.key")
        client_socket = context.wrap_socket(client_socket, server_side=True)
        return client_socket
    
    def start_server(self):
        self.server_socket.bind((self.ip, self.port))
        self.server_socket.listen(5)
        print(f"SMTP Server is listening on {self.ip}:{self.port}")
        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"connection from {client_address[0]}:{client_address[1]}")

            client_socket = self.secure_socket(client_socket)
            self.handle_client(client_socket)
            client_socket.close()
    
    def handle_client(self, client_socket): 
        data = client_socket.recv(self.MAX_MESSGE_LENGTH).decode()
        mail_from = self.extract_mail_from(data)
        rcpt = self.extract_rcpt_to(data)
        subject = self.extract_subject(data)
        body = self.extract_body(data)
        email = email_class.email(mail_from, rcpt, subject, body)
        print(f"Received mail from {mail_from} to {rcpt}")
        return_messge = self.OK_RETURN_MESSAGE
        client_socket.send(return_messge.encode())
        server_ip = rcpt.split("@")[1]
        if server_ip == self.ip or server_ip == self.name: #If the mail has reached its destination
            print("Saving mail locally")
            interface = UserDBInterface.UserDBInterface()
            interface.send_email_to_db(email)
        elif server_ip == "gmail.com": #only if its gmail
            print("Passing a mail To gmail")
            self.send_through_gmail(email)  # send the email through Gmail if the recipient is a Gmail account address
        else:
            print(f"Passing a mail to another server --> {server_ip}")
            self.send_email_to_remote_server(email, server_ip)
        print("Succseful mail transfer")
    
    def send_email_to_remote_server(self, email, server_ip):
        #connect to the remote server as a client and pass the email using an smtp client
        smtp_client = SMTPClient(server_ip, self.SMTP_SERVER_PORT)
        smtp_client.send_email(email)
        print("Email sent to remote server")
    
    def send_through_gmail(self, email):
        msg = EmailMessage()
        msg['Subject'] = f"{email.get_subject()} - {email.get_sender()}"
        msg['From'] = 'kish.enterprise.smtp@gmail.com'
        msg['To'] = email.get_receiver()
        msg.set_content(email.get_body())

        try:
            smtp = smtplib.SMTP_SSL("smtp.gmail.com", 465) #CREATES A Connection
            smtp.login(msg['From'], 'nqjq rqwm eiox unam') #uses my secret passkey
            smtp.send_message(msg)
            print(f"Email sent to {msg['To']}")
        except Exception as e:
            print(f"Failed to send email: {e}")
        finally:
            smtp.quit()

    
    def extract_mail_from(self, data):
        data_splited = data.split("\n")
        return data_splited[1].split(":")[1]
    
    def extract_rcpt_to(self, data):
        data_splited = data.split("\n")
        return data_splited[2].split(":")[1]
    
    def extract_subject(self, data):
        data_splited = data.split("\n")
        return data_splited[4].split(":")[1].strip()
    
    def extract_body(self, data):
        data_splited = data.split("\n\n")
        return data_splited[1]
    
    def get_ip_of_device(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip

    
