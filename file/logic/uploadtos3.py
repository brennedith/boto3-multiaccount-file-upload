import asyncio

import boto3

async def uploadToS3(account, file, filename):
    session = boto3.session.Session(
        aws_access_key_id=account.get('access_key_id'),
        aws_secret_access_key=account.get('secret_access_key'),
        region_name=account.get('region_name'),
    )
    # FIXME: Reuse sessions between processes/requests
    client = session.client('s3')
    bucketName = account.get('s3_bucket_name')

    return client.put_object(
        Bucket=bucketName,
        Key=filename, 
        Body=file, 
        ACL='private',
    )
