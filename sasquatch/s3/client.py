from functools import partial

import boto3

from ..error.user import UnknownProfileError
from ..error.user import UserErrorHelper as error
# from ..util.conf import config


def _fetch_profile(name):
	profile = config.profiles.get(name)
	if profile is None:
		error.throw(UnknownProfileError, profile=name)
	return profile

def _build_client(
		profile = None,
		access_key = None,
		secret_key = None,
		endpoint = None):
	if profile is not None:
		return build_client(**_fetch_profile(profile))
	return boto3.client(
		's3',
		aws_access_key_id=access_key,
		aws_secret_access_key=secret_key,
		endpoint_url=endpoint
	)

# CLIENT = _build_client(**config.runtime.credentials)
CLIENT = _build_client(access_key='hello', secret_key='world')

def with_client(func):
	return partial(func, CLIENT)
