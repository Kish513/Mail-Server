from HelperClasses.User import User
import os
#An abstract class
class user_action_strategy:
    def __init__(self, user_db_interface, json_data):
        self.user_db_interface = user_db_interface
        self.json_data  = json_data
    
    def execute(self):
        pass #This will be later used for polimpohrpisem

#a strategy to login user
class user_action_login(user_action_strategy):
    def __init__(self, user_db_interface, json_data):
        super().__init__(user_db_interface, json_data)
    
    def execute(self):
        user_email = self.json_data.get('user_email') #Get the data quary
        user_password = self.json_data.get('user_password')#Get the data quary
        user = User(user_email, user_password)
        print('Login attempt for user:', user)
        login_try = self.user_db_interface.login_user(user)
        if login_try:
            print('Login successful')
            return {'status': 'Success', 'message': 'User logged in successfully'} #Return message Succes 
        else:
            print('Login failed')
            return {'status': 'Failure', 'message': 'Invalid email or password'} #Return message Failure

#a strategy to register user
class user_action_register(user_action_strategy):
    def __init__(self, user_db_interface, json_data):
        super().__init__(user_db_interface, json_data)
    
    def execute(self):
        user_email = self.json_data.get('user_email')#Get the data quary
        user_password = self.json_data.get('user_password')#Get the data quary
        user_to_add = User(user_email, user_password)
        register_try = self.user_db_interface.register_user(user_to_add)
        print('Register attempt for user:', user_to_add)
        if register_try:
            print('User registered successfully')
            return {'status': 'Success', 'message': 'User registered successfully'} #Return message Succes 
        else:
            print('Email already exists')
            return {'status': 'Failure', 'message': 'Email already exists'}#Return message Failure

#a strategy to get all the emails for a given user(user speicified in the JSON data)      
class user_action_get_emails(user_action_strategy):
    def __init__(self, user_db_interface, json_data):
        super().__init__(user_db_interface, json_data)

    def execute(self):
        email_adress = self.get_email_adress()
        print(email_adress)
        emails = self.user_db_interface.get_emails_by_adress(email_adress)
        emails = [email_messge.to_dict() for email_messge in emails] #A bullet line to turn 
        return {'status': 'Success', 'emails': emails} #Return all the email
    
    def get_email_adress(self):
        return self.json_data.get('user_email')

