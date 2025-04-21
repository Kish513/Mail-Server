import sqlite3
from HelperClasses.User import User
from email_classes.email import email
class UserDBInterface:

    def __init__(self):
        self.connection = sqlite3.connect('db\\users.db')
        self.cursor = self.connection.cursor()


    def register_user(self, user):
        #get the user's email and password from the user object
        user_email = user.get_email()
        user_password = user.get_password()
        try:
            self.cursor.execute('''INSERT INTO users (user_email, user_password) VALUES (?,?)''', (user_email, user_password))
            self.commit_changes()
            return True
        except:
            return False

    def get_user_by_email(self, user_email):
        #get the user's email from the user object
        self.cursor.execute('''SELECT * FROM users WHERE user_email =?''', (user_email))
        user_data = self.cursor.fetchone()
        if user_data is None:
            return None
        return User(user_data[0], user_data[1])
    
    def login_user(self, user_to_login):
        #get the user's email and password from the user object
        user_email = user_to_login.get_email()
        user_password = user_to_login.get_password()
        self.cursor.execute('''SELECT * FROM users WHERE user_email =? AND user_password =?''', (user_email, user_password))
        user_data = self.cursor.fetchone()
        if user_data is None:
            return False
        return True
    
    def send_email_to_db(self, email):
        #get the email's sender, receiver, subject, and body from the email object
        sender = email.get_sender()
        receiver = email.get_receiver()
        subject = email.get_subject()
        body = email.get_body()
        
        print() #printsall the tables and location of db
        self.cursor.execute('''
        INSERT INTO mails (sender_address, receiver_address, subject, body)
        VALUES (?, ?, ?, ?);
        ''', (sender, receiver, subject, body))
        self.commit_changes()
    
    def get_emails_by_adress(self, email_adress):
        #get the user's email from the user object
        self.cursor.execute('''
        SELECT * FROM mails WHERE receiver_address =?;
        ''', (email_adress,))
        emails = self.cursor.fetchall()
        return [email(sender, receiver, subject, body) for sender, receiver, subject, body in emails]
    #endregion

    #region Private methods
    def commit_changes(self):
        #commit all changes made to the database
        self.connection.commit()

    def delete_all_data(self):
        #delete all data from both tables (users and mails)
        self.cursor.execute("DELETE FROM mails;")
        self.cursor.execute("DELETE FROM users;")
        self.commit_changes()


