import json
import unittest
from unittest.mock import patch

from django.contrib.auth.models import User
from rest_framework.test import APIClient


class TestGithubOauth(unittest.TestCase):
    def setUp(self):
        self.client = APIClient()
        self.django_user = User.objects.create_user(
            id=1,
            username='test',
            email='test@test.com'
        )

    @patch('app.views.github_oauth.get_user_from_token')
    @patch('app.views.github_oauth.convert_to_auth_token')
    @patch('app.views.github_oauth.retrieve_github_user_info')
    @patch('app.views.github_oauth.generate_github_access_token')
    @patch('app.views.github_oauth.get_refresh_access_token')
    def test_github_authenticate(self, get_refresh_access_token, generate_access_token,
                                 retrieve_github_user, convert_to_auth_token,
                                 get_user_from_token):

        get_refresh_access_token.return_value = {
            'refresh': 'randomrefreshtoken',
            'access': 'randomaccesstoken'
        }

        generate_access_token.return_value = 'token'

        github_user = {'user_id': 'id1', 'avatar': 'avatar.jpg'}
        retrieve_github_user.return_value = json.dumps(github_user)

        convert_to_auth_token.return_value = 'auth_token'
        get_user_from_token.return_value = self.django_user

        mock_data = {
            'client_id': 'somerandomstring',
            'client_secret': 'anotherlongerrandomstring',
            'code': 'arandomstring01'
        }

        response = self.client.post('/github_auth/', data=mock_data)
        assert response.status_code == 201

        assert json.loads(response.content) == {
            'token': 'auth_token',
            'jwt_token': {'refresh': 'randomrefreshtoken', 'access': 'randomaccesstoken'},
            'github_user_info': '{"user_id": "id1", "avatar": "avatar.jpg"}',
            'user': {'id': 1, 'username': 'test', 'email': 'test@test.com'}
        }

        get_refresh_access_token.assert_called()
        generate_access_token.assert_called()
        retrieve_github_user.assert_called()
        convert_to_auth_token.assert_called()
        get_user_from_token.assert_called()
