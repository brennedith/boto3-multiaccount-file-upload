import concurrent.futures

import environ

env = environ.Env()

accounts = [
    env.json('AWS_ACCOUNT_A'),
    env.json('AWS_ACCOUNT_B'),
]

def handleInMultipleAccounts(fn, *args):
    maxWorkers = 4
    workers = min(len(accounts), maxWorkers)
    requestIds = []

    # ProcessPoolExecutor used to
    # - handle boto3 instances per account
    # - manage concurrency
    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
        futures = []
        for account in accounts:
            futures.append(executor.submit(fn, account, *args))

        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            requestIds.append(result.get('ResponseMetadata').get('RequestId'))    

        return requestIds
