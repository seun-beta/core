import json
import logging
import os
import requests

from dotenv import load_dotenv

load_dotenv()


def generate_gitlab_access_token(code, grant_type, redirect_uri):
    """
    create an access token to gitlab OAuth2.
    :code: code generated by client from http://gitlab.com/oauth/authorize/
    :grant_type: credential representing the resource owner's authorization from
    https://docs.gitlab.com/ee/api/oauth2.html#web-application-flow
    :redirect_uri: redirect uri from https://gitlab.com/-/profile/applications
    :return: json data on user's api
    """
    client_id = os.getenv("SOCIAL_AUTH_GITLAB_KEY")
    client_secret = os.getenv("SOCIAL_AUTH_GITLAB_SECRET")

    if not client_id or not client_secret:
        raise ValueError("Gitlab application client id or client secret is missing.")
        logging.critical("Gitlab application client id or client secret is missing.")

    gitlab_response = requests.post(
        "https://gitlab.com/oauth/token",
        params={
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code,
            "grant_type": grant_type,
            "redirect_uri": redirect_uri,
        },
        headers={"content-type": "application/json"},
    )
    assert (
        gitlab_response.status_code == 200
    ), f"ERROR: {gitlab_response.status_code}, {gitlab_response.text}"

    content = json.loads(gitlab_response.content)
    access_token = content.get("access_token")

    if not access_token:
        raise PermissionError(gitlab_response)
        logging.warning("Wrong access token")
    return access_token


def retrieve_gitlab_user_info(access_token):
    """
    using the access token returned by github, retrieve the user's info from the github api
    :access_token: access token generated from github
    """
    response = requests.get(
        "https://gitlab.com/api/v4/user",
        params={"token": access_token},
        headers={
            "Authorization": f"Bearer {access_token}",
            "content-type": "application/json",
        },
    )
    return response.json()
