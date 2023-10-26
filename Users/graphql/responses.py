from strawberry import type, union
from strawberry.schema.types.base_scalars import DateTime

from Schema.Api import Error, Success
from Users.graphql.objects import UserObject


@type
class AuthSuccess(Success):
    token: str
    expires: DateTime
    user: UserObject


LoginResponse = union('LoginResponse', (AuthSuccess, Error))
EditProfileResponse = union('EditProfileResponse', (Success, Error))
