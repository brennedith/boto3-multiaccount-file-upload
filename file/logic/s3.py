import json
import concurrent.futures

import boto3
import environ

from .utils import prependTimeAndSlug

env = environ.Env()

awsAccountA = json.loads(env('AWS_ACCOUNT_A'))
awsAccountB = json.loads(env('AWS_ACCOUNT_B'))
accounts = [awsAccountA, awsAccountB]

def uploadFile(credentials, file, filename):
    session = boto3.session.Session(
        aws_access_key_id=credentials.get('access_key_id'),
        aws_secret_access_key=credentials.get('secret_access_key'),
        region_name=credentials.get('region_name'),
    )
    # FIXME: Reuse sessions between requests
    client = session.client('s3')
    bucketName = credentials.get('s3_bucket_name')

    return client.put_object(
        Bucket=bucketName,
        Key=filename, 
        Body=file, 
        ACL='private',
    )


def uploadToMultipleAccounts(file, name):
    maxWorkers = 4
    workers = min(len(accounts), maxWorkers)
    requestIds = []
    filename = prependTimeAndSlug(name)

    # ProcessPoolExecutor used to
    # - handle boto3 instances per account
    # - manage concurrency
    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
        futures = []
        for account in accounts:
            futures.append(executor.submit(uploadFile, account, file, filename))

        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            requestIds.append(result.get('ResponseMetadata').get('RequestId'))    

        return requestIds
