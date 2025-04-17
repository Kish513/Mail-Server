import sqlite3
from HelperClasses.User import User
from email_classes.email import email
class UserDBInterface:
    #region ctors
    def __init__(self):
        self.connection = sqlite3.connect('db\\users.db')
        self.cursor = self.connection.cursor()
    #endregion
    #region Public methods
    def register_user(self, user):
        user_email = user.get_email()
        user_password = user.get_password()
        try:
            self.cursor.execute('''INSERT INTO users (user_email, user_password) VALUES (?,?)''', (user_email, user_password))
            self.commit_changes()
            return True
        except:
            return False

    def get_user_by_email(self, user_email):
        self.cursor.execute('''SELECT * FROM users WHERE user_email =?''', (user_email))
        user_data = self.cursor.fetchone()
        if user_data is None:
            return None
        return User(user_data[0], user_data[1])
    
    def login_user(self, user_to_login):
        user_email = user_to_login.get_email()
        user_password = user_to_login.get_password()
        self.cursor.execute('''SELECT * FROM users WHERE user_email =? AND user_password =?''', (user_email, user_password))
        user_data = self.cursor.fetchone()
        if user_data is None:
            return False
        return True
    
    def send_email_to_db(self, email):
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
        self.cursor.execute('''
        SELECT * FROM mails WHERE receiver_address =?;
        ''', (email_adress,))
        emails = self.cursor.fetchall()
        return [email(sender, receiver, subject, body) for sender, receiver, subject, body in emails]
    #endregion

    #region Private methods
    def commit_changes(self):
        self.connection.commit()

    def change_somthing_in_db(self):
        self.cursor.execute("PRAGMA foreign_keys = ON;")
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS mails (
                sender_address TEXT NOT NULL,
                receiver_address TEXT NOT NULL,
                subject TEXT NOT NULL,
                body TEXT NOT NULL,
                FOREIGN KEY (sender_address) REFERENCES users(email_address) ON DELETE CASCADE,
                FOREIGN KEY (receiver_address) REFERENCES users(email_address) ON DELETE CASCADE
            );
        ''')
        self.connection.commit()
    #endregion

