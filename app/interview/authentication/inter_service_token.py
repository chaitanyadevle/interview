from datetime import timedelta

from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

INTERSERVICE_USER_ID_IN_TOKEN = -99999
PAYLOAD_USER_ID_KEY = 'user_id'
TOKEN_EXPIRY_IN_HOURS = 1


class InterServiceAuthToken(RefreshToken):

    @classmethod
    def create_token(cls) -> str:
        '''
        Returns an access token string for an inter-service call
        '''
        refresh_token = cls()
        refresh_token[PAYLOAD_USER_ID_KEY] = INTERSERVICE_USER_ID_IN_TOKEN
        access_token = str(refresh_token.access_token)

        access_token = AccessToken(access_token)

        access_token.set_exp(
            lifetime=timedelta(minutes=60 * TOKEN_EXPIRY_IN_HOURS))

        return str(access_token)


def get_token_for_inter_service_call() -> str:
    return f'Bearer {InterServiceAuthToken.create_token()}'
