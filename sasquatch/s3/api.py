import botocore

from ..util.log import Log, log_call
from .client import with_client

_log = Log('s3.api')

@with_client
@log_call('s3.api', 'Making api call `{func}` {kwargs}')
def ls(client, bucket = None):
	if bucket is None:
		_log.debug("Bucket not provided, listing user's buckets")
		yield client.list_buckets()
	else:
		_log.debug('Bucket provided, listing objects in s3://%s'%bucket)
		next_marker = None
		is_truncated = True
		while is_truncated:
			if next_marker:
				_log.debug('Fetching next page for %s'%bucket)
				page = client.list_objects(Bucket=bucket, Marker=next_marker)
			else:
				page = client.list_objects(Bucket=bucket)
			yield page
			is_truncated = page.get('IsTruncated', False)
			next_marker = page.get('NextMarker', None)
			if is_truncated and next_marker is None:
				next_marker = page['Contents'][-1]['Key']

@with_client
@log_call('s3.api', 'Making api call `{func}` {kwargs}')
def lv(client, bucket = None, key = None):
	if key is None:
		prefix = ''
		_log.debug('No prefix provided, defaulting to empty string')
	else:
		prefix = key
		_log.debug('Using prefix `%s`'%prefix)
	is_truncated = True
	next_marker = None
	next_version = None
	while is_truncated:
		if next_marker is not None and next_version is not None:
			_log.debug('Fetching next page for %s'%bucket)
			page = client.list_object_versions(
						Bucket=bucket,
						Prefix=prefix,
						KeyMarker=next_marker,
						VersionIdMarker=next_version
					)
		else:
			page = client.list_object_versions(
						Bucket=bucket,
						Prefix=prefix
					)
		yield page
		is_truncated = page.get('IsTruncated', False)
		next_marker = page.get('NextKeyMarker', None)
		next_version = page.get('NextVersionIdMarker', None)

@with_client
@log_call('s3.api', 'Making api call `{func}` {kwargs}')
def head(client, bucket = None, key = None, version_id = None):
	if version_id is None:
		_log.debug('No VersionId provided, HEADing %s'%key)
		return client.head_object(Bucket=bucket, Key=key)
	_log.debug('Got VersionId HEADing %s ver: %s'%(key, version_id))
	return client.head_object(Bucket=bucket, Key=key, VersionId=version_id)

@with_client
def get(client, bucket = None, key = None, version_id = None):
	pass

@with_client
def put(client, bucket = None, key = None):
	pass

@with_client
def cp(client, target_bucket = None, target_key = None, bucket = None, key = None):
	pass

@with_client
@log_call('s3.api', 'Making api call `{func}` {kwargs}')
def get_bucket_replication(client, bucket = None):
	try:
		_log.debug('Getting ReplicationConfig for %s'%bucket)
		return client.get_bucket_replication(Bucket=bucket)
	except botocore.exceptions.ClientError:
		pass
	return None
