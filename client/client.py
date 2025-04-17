from HelperClasses.User import User
import socket
import json
from email_classes.email import email
import threading
from  .smtp_client import SMTPClient
from message_protocol.protocol import message_protocol
import hashlib
import ssl

PORT = 5000
class Client():
    def __init__(self, email, password, server_ip):
        self.server_ip = server_ip
        self.user = User(email, password)
        self.is_logged_in = False
        self.socket_to_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Wrap socket with SSL
        self.ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        self.ssl_context.load_verify_locations('certificate.crt')
        self.ssl_context.check_hostname = False  # Disable hostname checking
        self.socket_to_server = self.ssl_context.wrap_socket(self.socket_to_server, server_hostname=self.server_ip)

        self.socket_to_server.connect((self.server_ip, PORT))
        print('Connected to server')
    
    def get_user(self):
        return self.user
    
    def get_email_address(self):
        return self.user.get_email()

    def login(self):
        email = self.user.get_email()
        password = self.user.get_password()
        password_hash = hashlib.sha256(password.encode()).hexdigest() 
        strategy = 'login'
        message = message_protocol({'strategy': strategy,'user_email': email, 'user_password': password_hash})
        self.send_data_to_server(message.get_message())
        data = self.wait_for_message()
        return self.get_json_status(data) == 'Success'
    
    def sign_up(self):
        email = self.user.get_email()
        password = self.user.get_password()
        password_hash = hashlib.sha256(password.encode()).hexdigest() 
        strategy ='register'
        message = message_protocol({'strategy': strategy,'user_email': email, 'user_password': password_hash})
        self.send_data_to_server(message.get_message())
        data = self.wait_for_message()
        return self.get_json_status(data) == 'Success'
    
    def get_emails(self):
        email_adress = self.user.get_email()
        strategy ='get_emails'
        message = message_protocol({'strategy': strategy,'user_email': email_adress})
        self.send_data_to_server(message.get_message())
        data = self.wait_for_message()        
        mails_messges = []
        for email_messge in json.loads(data).get('emails'):
            mails_messges.append(email(email_messge))
        return mails_messges
    def send_email_message(self, sender, receiver, subject, body):
        smtp_client = SMTPClient(self.server_ip)
        thread = threading.Thread(target=smtp_client.send_email, args=(sender, receiver, subject, body))
        thread.start()
    #region server manegmment methods
    def send_data_to_server(self, data_encoded):
        self.socket_to_server.send(data_encoded)
    
    def wait_for_message(self):
        response = self.socket_to_server.recv(1024).decode()
        return response
    
    def get_json_status(self, data):
        return json.loads(data)['status']
    #endregion
            

