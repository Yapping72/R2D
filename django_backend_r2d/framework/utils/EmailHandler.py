class EmailHandler:
    @staticmethod
    def mask_email(email):
        username, domain = email.split('@')
        masked_username = username[0] + '*' * (len(username) - 2) + username[-1]
        return masked_username + '@' + domain
