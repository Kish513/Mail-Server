from HelperClasses.User import User
import os
class user_action_strategy:
    def __init__(self, user_db_interface, json_data):
        self.user_db_interface = user_db_interface
        self.json_data  = json_data
    
    def execute(self):
        pass

class user_action_login(user_action_strategy):
    def __init__(self, user_db_interface, json_data):
        super().__init__(user_db_interface, json_data)
    
    def execute(self):
        user_email = self.json_data.get('user_email')
        user_password = self.json_data.get('user_password')
        user = User(user_email, user_password)
        print('Login attempt for user:', user)
        login_try = self.user_db_interface.login_user(user)
        if login_try:
            print('Login successful')
            return {'status': 'Success', 'message': 'User logged in successfully'}
        else:
            print('Login failed')
            return {'status': 'Failure', 'message': 'Invalid email or password'}   

class user_action_register(user_action_strategy):
    def __init__(self, user_db_interface, json_data):
        super().__init__(user_db_interface, json_data)
    
    def execute(self):
        user_email = self.json_data.get('user_email')
        user_password = self.json_data.get('user_password')
        user_to_add = User(user_email, user_password)
        register_try = self.user_db_interface.register_user(user_to_add)
        print('Register attempt for user:', user_to_add)
        if register_try:
            print('User registered successfully')
            return {'status': 'Success', 'message': 'User registered successfully'}
        else:
            print('Email already exists')
            return {'status': 'Failure', 'message': 'Email already exists'}
    
class user_action_send_email(user_action_strategy):
    def __init__(self, user_db_interface, json_data):
        super().__init__(user_db_interface, json_data)
    
    def execute(self):
        user_email = self.json_data.get('user_email')
        if self.check_if_email_adress_is_local(user_email):
            self.user_db_interface.send_email_to_db(user_email)
        else:
            self.send_email_to_remote_server(user_email)

    def get_local_ip(self):
        try:
            # For Windows
            result = os.popen('ipconfig').read()
            for line in result.split('\n'):
                if 'IPv4' in line:
                    return line.split(':')[1].strip()
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def check_if_email_adress_is_local(self, email):
        # Check if email address is local or not
        ip = self.get_local_ip()
        return ip == email.split('@')[1]
    
class user_action_get_emails(user_action_strategy):
    def __init__(self, user_db_interface, json_data):
        super().__init__(user_db_interface, json_data)

    def execute(self):
        email_adress = self.get_email_adress()
        print(email_adress)
        emails = self.user_db_interface.get_emails_by_adress(email_adress)
        emails = [email_messge.to_dict() for email_messge in emails]
        return {'status': 'Success', 'emails': emails}
    
    def get_email_adress(self):
        return self.json_data.get('user_email')
    
    
 
