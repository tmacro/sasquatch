from functools import partial

import boto3

from ..error.user import UnknownProfileError
from ..error.user import UserErrorHelper as error
from ..util.conf import config


def _fetch_profile(name):
	profile = getattr(config.profiles, name, None)
	if profile is None:
		error.throw(UnknownProfileError, profile=name)
	return profile._asdict()

def _build_client(
		profile = None,
		aws_access_key_id = None,
		aws_secret_access_key = None,
		endpoint = None):
	if profile is not None:
		return _build_client(**_fetch_profile(profile))
	elif not profile and not aws_access_key_id and not aws_access_key_id and not endpoint:
		return _build_client(profile='default')
	else:
		return boto3.client(
			's3',
			aws_access_key_id=aws_access_key_id,
			aws_secret_access_key=aws_secret_access_key,
			endpoint_url=endpoint
		)

CLIENT = _build_client(**config.runtime.credentials._asdict())
# CLIENT = _build_client(access_key='hello', secret_key='world')

def with_client(func):
	return partial(func, CLIENT)
