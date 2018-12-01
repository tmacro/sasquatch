from .client import with_client

@with_client
def ls(client, bucket = None):
	# print(str(bucket))
	if bucket is None:
		val = client.list_buckets()
	else:
		val = client.list_objects(Bucket=bucket)
	return val

@with_client
def lv(client, bucket = None, key = None):
	if key is None:
		prefix = ''
	return client.list_object_versions(Bucket=bucket, Prefix=prefix)

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
