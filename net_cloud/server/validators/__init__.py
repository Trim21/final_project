# validators.py
from validator import Validator, StringField


class RegisterValidator(Validator):
    username = StringField(max_length=20, required=True)
    password = StringField(min_length=6, max_length=20, required=True)


class LoginValidator(Validator):
    username = StringField(max_length=20, required=True)
    password = StringField(min_length=6, max_length=20, required=True)
