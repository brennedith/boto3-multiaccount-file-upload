# Mentum file upload

> Note: depending on your system's configuration, you may need to use `python3/pip3` instead of `python/pip`.

## About

Mentum's file upload service is responsible for uploading files to s3 buckets distributed in multiple AWS accounts where AssumeRoles cannot be used (e.g. different account owners, privacy laws such as GDPR, etc).

## Getting started

### Configuration

1. Before getting started, make sure you have the right python version: `python --version` should be `>=3.10.4,<4.0`.
2. Install the required dependencies: `pip install -r requirements.txt`
3. Start the Django application: `python manage.py runserver`

### Environment variables (env vars)

#### AWS accounts

This service can concurrently upload files to different AWS accounts. Every AWS account credentials secret should follow the following schema for it's env vars.

```json
{
  "access_key_id": "string",
  "secret_access_key": "string",
  "region_name": "string",
  "s3_bucket_name": "string"
}
```

Code references:

> mentumfileupload/.env
>
> file/logic/handleinmultipleaccounts.py

## Running locally

```sh
# Copy the example environment file and add the required AWS accounts objects
cp mentumfileupload/.env.example mentumfileupload/.env

# Run the test server
python manage.py runserver
```

## Building and running build locally

> Docker is required for the following commands
>
> https://www.docker.com/get-started/

```sh
# Copy the example environment file and add the required AWS accounts credentials
cp mentumfileupload/.env.example mentumfileupload/.env

# Build container image
docker build -t file-upload .

# Running container with custom env vars
docker run --env-file mentumfileupload/.env -p 8000:8000 file-upload
```

## Tests

You can run the service tests (unit and integration) running the following commands:

```sh
# Make sure you have an environment file available
cp mentumfileupload/.env.testing mentumfileupload/.env

# Run the test suite
python manage.py test
```

## Notes

### Architectural decisions

- Debug capabilities will be on until the service is productive
- Payload size limit (request headers, body, etc) is set to 5.5 mb.

  Code references:

  > mentumfileupload/settings.py

- boto3 resources depend on special (classes metadata) resources that conflict when using different AWS accounts (both configure by credentials or named profiles), hence we create different subprocess via `ProcessPoolExecutor`.

  References:

  > file/logic/handleinmultipleaccounts.py
  >
  > https://boto3.amazonaws.com/v1/documentation/api/latest/guide/resources.html#multithreading-or-multiprocessing-with-resources

## TODO:

- Find alternatives to `ProcessPoolExecutor`, follow up with `asyncio`.
