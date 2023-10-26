from typing import Optional

from strawberry import input


@input
class UserForm:
    name: Optional[str] = None


@input
class LoginForm:
    email: Optional[str] = None
    password: Optional[str] = None


@input
class RegisterForm(UserForm, LoginForm):
    pass
