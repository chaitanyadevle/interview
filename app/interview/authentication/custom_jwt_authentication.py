from core.models import User
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication

from .inter_service_token import (
    INTERSERVICE_USER_ID_IN_TOKEN, PAYLOAD_USER_ID_KEY)

ATTR_IS_INTER_SERVICE_CALL = 'is_inter_service_call'


class CustomJWTAuthentication(JWTAuthentication):

    def authenticate(self, request: Request):
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)

        is_inter_service_call = validated_token.payload[PAYLOAD_USER_ID_KEY] == INTERSERVICE_USER_ID_IN_TOKEN

        if is_inter_service_call:
            setattr(request, ATTR_IS_INTER_SERVICE_CALL, True)
            return User.objects.first(), validated_token

        return super().authenticate(request)


def is_inter_service_call(request) -> bool:
    return hasattr(request, ATTR_IS_INTER_SERVICE_CALL) \
        and getattr(request, ATTR_IS_INTER_SERVICE_CALL) is True
