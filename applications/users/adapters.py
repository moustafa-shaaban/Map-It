from allauth.account.adapter import DefaultAccountAdapter

class UsersAdapter(DefaultAccountAdapter):
    def clean_username(self, username, shallow=False):
        # Custom cleaning logic
        return username.lower()
    
    def clean_email(self, email, shallow=False):
        # Custom cleaning logic
        return email.lower()