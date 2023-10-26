from dateutil.relativedelta import relativedelta
from django.contrib.auth import authenticate
from django.utils import timezone
from oauth2_provider.models import Application, AccessToken
from oauthlib.common import generate_token
from strawberry import field, type, mutation
from strawberry.types import Info

from Schema.Api import Error, FieldErrors, Success
from Schema.Permissions import IsAuthenticated
from Users.form_models import RegisterModelForm, UpdateUserModelForm
from Users.graphql.forms import UserForm, LoginForm, RegisterForm
from Users.graphql.objects import UserObject
from Users.graphql.responses import LoginResponse, AuthSuccess, EditProfileResponse


@type
class UsersQueries:
    @field(permission_classes = [])
    def profile(self, info: Info) -> UserObject:
        return info.context.request.user


@type
class UsersMutations:
    @mutation
    def login(self, form: LoginForm) -> LoginResponse:
        user = authenticate(username = form.email, password = form.password)

        if user:
            application = Application.objects.filter(name = 'Main App').first()
            new_token = generate_token()

            access_token = AccessToken.objects.create(user = user, application = application, token = new_token,
                                                      expires = timezone.now() + relativedelta(hours = 72))

            return AuthSuccess(message = 'Login realizado con éxito', process_name = 'Login', token = access_token.token,
                               expires = access_token.expires, user = access_token.user)

        return Error(message = 'Credenciales entregadas inválidas')

    @mutation
    def register(self, form: RegisterForm) -> LoginResponse:
        model_form = RegisterModelForm()
        model_form.data = form.__dict__
        model_form.is_bound = True
        model_form.is_valid()

        errors = [FieldErrors(field = k, errors = v) for k, v in model_form.errors.items()]

        if errors:
            return Error(message = 'Errores presentes en el formulario de registro', fields = errors)

        user = model_form.save()
        user.set_password(form.password)
        user.save()
        application = Application.objects.filter(name = 'Main App').first()
        new_token = generate_token()

        access_token = AccessToken.objects.create(user = user, application = application, token = new_token,
                                                  expires = timezone.now() + relativedelta(hours = 72))

        return AuthSuccess(message = 'Registro realizado con éxito', process_name = 'Register',
                           token = access_token.token, expires = access_token.expires, user = access_token.user)

    @mutation(permission_classes = [IsAuthenticated])
    def edit_profile(self, info: Info, form: UserForm) -> EditProfileResponse:
        model_form = UpdateUserModelForm(instance = info.context.request.user)
        model_form.data = form.__dict__
        model_form.is_bound = True
        model_form.is_valid()

        errors = [FieldErrors(field = k, errors = v) for k, v in model_form.errors.items()]

        if errors:
            return Error(message = 'Errores presentes en el formulario de edición del usuario', fields = errors)

        model_form.save()
        return Success(message = 'Usuario actualizado con éxito', process_name = 'UpdateUser')
