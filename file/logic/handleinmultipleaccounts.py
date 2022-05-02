from ast import AsyncFunctionDef
import concurrent.futures
import asyncio

import environ

env = environ.Env()

# AWS Accounts
accounts = [
    env.json('AWS_ACCOUNT_A'),
    env.json('AWS_ACCOUNT_B'),
]

def getEventLoop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError as e:
        if "There is no current event loop in thread" in str(e):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return asyncio.get_event_loop()

def handleInMultipleAccounts(fn, *args):
    maxWorkers = 4
    workers = min(len(accounts), maxWorkers)
    requestIds = []

    # ProcessPoolExecutor used to
    # - handle boto3 instances per account
    # - manage concurrency
    # with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
    #     futures = []
    #     for account in accounts:
    #         futures.append(executor.submit(fn, account, *args))

    #     for future in concurrent.futures.as_completed(futures):
    #         result = future.result()
    #         requestIds.append(result.get('ResponseMetadata').get('RequestId'))    

    #     return requestIds

    loop = getEventLoop()
    tasks = [
        fn(account, *args)
        for account in accounts
    ]
    print(tasks)
    result = loop.run_until_complete(asyncio.wait(tasks))
    print(result)
    loop.close()