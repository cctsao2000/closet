import re

from django.core.exceptions import ValidationError

# User.
def validate_username(username):
    pattern = r'^[a-zA-Z0-9]+$'
    if not re.match(pattern, username):
        raise ValidationError(
            message='請輸入由大小寫英文與數字組成的使用者名稱！'
        )

def validate_phone(phone):
    pattern = r'09\d{8}$'
    if not re.match(pattern, phone):
        raise ValidationError(
            message='請輸入 09 開頭的 10 碼手機號碼！'
        )

def validate_email(email):
    pattern = r'^[a-zA-Z0-9_\-\.]+@[a-zA-Z0-9_\-\.]+\.([a-zA-Z]{2,5})$'
    if not re.match(pattern, email):
        raise ValidationError(
            message='請輸入符合格式的電子郵件！'
        )

