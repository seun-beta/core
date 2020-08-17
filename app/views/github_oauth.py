import os

from dotenv import load_dotenv
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..oauth import (convert_to_auth_token, generate_github_access_token,
                     retrieve_github_user_info, get_user_from_token)
from ..serializers import DefaultUserSerializer

load_dotenv()

# GITHUB ID AND SECRET
SOCIAL_AUTH_GITHUB_KEY = os.getenv('SOCIAL_AUTH_GITHUB_KEY')
SOCIAL_AUTH_GITHUB_SECRET = os.getenv('SOCIAL_AUTH_GITHUB_SECRET')

# OAUTH TOOLKIT ID AND SECRET
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')


@api_view(['POST'])
def github_authenticate(request):
    github_token = generate_github_access_token(
        github_client_id=SOCIAL_AUTH_GITHUB_KEY,
        github_client_secret=SOCIAL_AUTH_GITHUB_SECRET,
        github_code=request.data['code']
    )

    github_user = retrieve_github_user_info(
        token=github_token
    )

    django_auth_token = convert_to_auth_token(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        backend='github',
        token=github_token
    )

    user = get_user_from_token(django_auth_token)

    return Response(
        {'token': django_auth_token,
         'github_user_info': github_user,
         'user': DefaultUserSerializer(user).data
         },
        status=status.HTTP_201_CREATED
    )