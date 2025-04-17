import threading
from .client_server import client_Server
from .smtp_server import SMTPServer
import ssl
class final_server:
    def __init__(self):
        pass  # Remove shared instances

    
    def start_server(self):
        # Create fresh instances inside each thread
        smtp_thread = threading.Thread(target=self.run_smtp_server)
        client_thread = threading.Thread(target=self.run_client_server)
        
        smtp_thread.start()
        client_thread.start()

        smtp_thread.join()
        client_thread.join()
    
    def run_smtp_server(self):
        smtp_server = SMTPServer()  # Create a fresh instance in the new thread
        smtp_server.start_server()
    
    def run_client_server(self):
        client_server = client_Server()  # Create a fresh instance in the new thread
        client_server.start_server()