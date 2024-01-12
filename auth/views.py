from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .client import oAuth2Client
from config.settings import (
    CLIENT_SECRET,
    CLIENT_ID,
    REDIRECT_URI,
    RESOURCE_OWNER_URL,
    TOKEN_URL,
    AUTHORIZE_URL,
)


class OAuthAuthorizationView(APIView):
    def get(self, request, *args, **kwargs):
        client = oAuth2Client(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
            authorize_url=AUTHORIZE_URL,
            token_url=TOKEN_URL,
            resource_owner_url=RESOURCE_OWNER_URL
        )
        authorization_url = client.get_authorization_url()
        return Response(
            {
                'authorization_url': authorization_url
            },
            status=status.HTTP_200_OK)


class OAuthCallbackView(APIView):
    def get(self, request, *args, **kwargs):
        full_info = {}
        auth_code = self.kwargs.get('code')
        if not auth_code:
            return Response(
                {
                    'status': False,
                    'error': 'Authorization code is missing'
                },
                status=status.HTTP_400_BAD_REQUEST)

        client = oAuth2Client(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
            authorize_url=AUTHORIZE_URL,
            token_url=TOKEN_URL,
            resource_owner_url=RESOURCE_OWNER_URL
        )
        access_token_response = client.get_access_token(auth_code)

        if 'access_token' in access_token_response:
            access_token = access_token_response['access_token']
            user_details = client.get_user_details(access_token)
            full_info['details'] = user_details
            full_info['token'] = access_token
            return Response(full_info, status=status.HTTP_200_OK)
        else:
            return Response(
                {
                    'status': False,
                    'error': 'Failed to obtain access token'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
