import requests


class oAuth2Client:
    def __init__(self, client_id, client_secret, redirect_uri, authorize_url, token_url, resource_owner_url):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.authorize_url = authorize_url
        self.token_url = token_url
        self.resource_owner_url = resource_owner_url

    def get_authorization_url(self):
        return f"{self.authorize_url}?client_id={self.client_id}&redirect_uri={self.redirect_uri}&response_type=code"

    def get_access_token(self, auth_code):
        payload = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': auth_code,
            'redirect_uri': self.redirect_uri,
            'grant_type': 'authorization_code'
        }
        response = requests.post(self.token_url, data=payload)
        return response.json()

    def get_user_details(self, access_token):
        response = requests.get(self.resource_owner_url, headers={'Authorization': f'Bearer {access_token}'})
        return response.json()
