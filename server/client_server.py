import socket
import json
import threading
from db.UserDBInterface import UserDBInterface
from user_action_strategies.user_action_strategy import user_action_register, user_action_login, user_action_strategy, user_action_get_emails
import ssl



class client_Server:
    CLIENT_HANDLING_SERVER_PORT = 5000
    MAX_MESSGES_SIZE = 1024
    def __init__(self):
        self.ip = self.get_ip_of_device()
        self.port = self.CLIENT_HANDLING_SERVER_PORT
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.strategy = None
        # self.user_db_interface = UserDBInterface() # Removed shared instance

    def start_server(self):
        self.server_socket.bind((self.ip, self.port))
        self.server_socket.listen(5)
        print(f'Client Handling Server started on {self.ip}:{self.port}')
        self.Server_Functionality()
    
    def secure_socket(self, client_socket):
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.load_cert_chain(certfile='certificate.crt', keyfile='server\private.key')
        secured_client_socket = ssl_context.wrap_socket(client_socket, server_side=True)
        return secured_client_socket
    
    def Server_Functionality(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f'Connection from {client_address[0]}:{client_address[1]}')
            secured_client_socket =  self.secure_socket(client_socket)
            thread = threading.Thread(target=self._handle_client_thread, args=(secured_client_socket,))
            thread.start()

    def _handle_client_thread(self, client_socket):
         # Create a DB interface instance specific to this thread
         user_db_interface_thread_local = UserDBInterface()
         try:
             while True:
                 data = client_socket.recv(self.MAX_MESSGES_SIZE)
                 if not data:
                     break
                 # Pass the thread-local db interface to handle_client
                 self.handle_client(client_socket, data, user_db_interface_thread_local)
         except ConnectionResetError:
             pass # Client disconnected abruptly, handled by loop exit
         except Exception as e:
             print(f"Error handling client: {e}") # Minimal logging as before
         finally: # Ensure DB connection is closed if UserDBInterface has a close method
             if hasattr(user_db_interface_thread_local, 'close') and callable(user_db_interface_thread_local.close):
                 try:
                     user_db_interface_thread_local.close()
                 except Exception as db_close_e:
                     print(f"Error closing DB connection in thread: {db_close_e}")
             client_socket.close()


    # Added user_db_interface parameter
    def handle_client(self, client_socket, data, user_db_interface):
        data = self.decode_data(data)
        # Pass the thread-local db interface to choose_strategy
        self.choose_strategy(data, user_db_interface)
        # Ensure strategy was chosen before executing
        if self.strategy:
             data_to_return = self.strategy.execute()
             print(data_to_return)
             self.send_data(client_socket, data_to_return)
        # else: # Handling for no strategy found (optional, kept minimal)
             # print("No strategy executed.")
             # pass

#region private methods
    # Added user_db_interface parameter
    def choose_strategy(self, data, user_db_interface):
        strategy_name = data.get('strategy')
        self.strategy = None # Reset strategy before choosing
        # Pass the thread-local db interface to strategy constructors
        if strategy_name == 'register':
            # Assuming strategy constructors accept db_interface as the first arg
            self.strategy = user_action_register(user_db_interface, data)
        if strategy_name == 'login':
            self.strategy = user_action_login(user_db_interface, data)
        if strategy_name == 'get_emails':
            self.strategy = user_action_get_emails(user_db_interface, data)
        else:
            pass #NO STRATEGY FOUND

    def send_data(self, client_socket, data):
        data = json.dumps(data).encode()
        client_socket.send(data)

        
    def decode_data(self, data):
        return json.loads(data)

    def get_ip_of_device(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip

#endregion