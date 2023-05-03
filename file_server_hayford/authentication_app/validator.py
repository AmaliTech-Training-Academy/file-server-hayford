import re 
from django.core.exceptions import ValidationError

class PasswordValidator:
    def validate(self, password, user=None):
        password_pattern = r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$'

        if not re.match(password_pattern, password):
            raise ValidationError(
                'Password needs to have at minimum one uppercase letter, one lowercase letter, one digit, and one special character'
            )
    
    def get_help_text(self):
        return 'Your password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character.'