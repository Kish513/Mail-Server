

class User:

#region CTORS
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.email
#endregion
#region Getters
    def get_password(self):
        return self.password
    
    def get_email(self):
        return self.email
    
#endregion
#region Setters
#reguion Public Methods
#endregion
#region Overrides
    def __str__(self):
        return f'Email: {self.get_email()}, Password(hash): {self.get_password()}'
    
    def __eq__(self, other):
        if isinstance(other, User):
            return self._email == other._email
        return False
#endregion
