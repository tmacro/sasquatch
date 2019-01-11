from .client import with_client
import botocore

@with_client
def ls(client, bucket = None):
	if bucket is None:
		yield client.list_buckets()
	else:
		next_marker = None
		is_truncated = True
		while is_truncated:
			if next_marker:
				page = client.list_objects(Bucket=bucket, Marker=next_marker)
			else:
				page = client.list_objects(Bucket=bucket)
			yield page
			is_truncated = page.get('IsTruncated', False)
			next_marker = page.get('NextMarker', None)
			if is_truncated and next_marker is None:
				next_marker = page['Contents'][-1]['Key']

@with_client
def lv(client, bucket = None, key = None):
	if key is None:
		prefix = ''
	is_truncated = True
	next_marker = None
	next_version = None
	while is_truncated:
		if next_marker is not None and next_version is not None:
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
def head(client, bucket = None, key = None, version_id = None):
	if version_id is None:
		return client.head_object(Bucket=bucket, Key=key)
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
def get_bucket_replication(client, bucket = None):
	try:
		return client.get_bucket_replication(Bucket=bucket)
	except botocore.exceptions.ClientError:
		pass
	return None
