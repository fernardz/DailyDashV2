import redis
import json
from requests_oauthlib import OAuth2Session
from dotenv import dotenv_values
import boto3
from botocore.client import Config
from aws_error_utils import errors as aws_errors
import io
import logging

logging.basicConfig(format='%(message)s', level=logging.INFO)

config = dotenv_values(".env")

print(config)

redis_client = redis.StrictRedis('rasp-srv', 6379, charset="utf-8",
                                 decode_responses=True)
try:
    token = redis_client.get('STRAVA_TOKEN')
    token = json.loads(token)
except Exception as e:
    logging.ERROR('Failed communication to token storage {}'.format(e))


def token_saver(token):
    token_dict = dict(token.items())
    redis_client.set('STRAVA_TOKEN', json.dumps(token_dict))


def upload_data_to_s3(bucket_name, host, data, destination):
    s3 = boto3.resource('s3',
                        endpoint_url=host,
                        aws_access_key_id=config['S3_ACCESS_KEY'],
                        aws_secret_access_key=config['S3_SECRET'],
                        config=Config(read_timeout=0.15, connect_timeout=0.15,
                                      retries={'max_attempts': 2},
                                      signature_version='s3v4'),
                        region_name='us-east-1')
    try:
        s3.create_bucket(Bucket=bucket_name)
    except (aws_errors.BucketAlreadyOwnedByYou,
            aws_errors.BucketAlreadyExists):
        logging.debug('Bucket {} Exists'.format(bucket_name))
    except Exception as e:
        print('Issue with connection to bucket {}'.format(e))
        raise

    try:
        Bucket = s3.Bucket(bucket_name)
        Bucket.upload_fileobj(io.BytesIO(data), destination)
    except Exception as e:
        logging.critical('Error in S3 upload {}'.format(e))
        raise


client_id = config['STRAVA_CLIENT_ID']
client_secret = config['STRAVA_CLIENT_SECRET']
auth_url = "https://www.strava.com/oauth/authorize"
token_url = "https://www.strava.com/oauth/token"
refresh_url = token_url
expires_at = 1644952661
expires_in = 21600

extra = {
    'client_id': client_id,
    'client_secret': client_secret
}

activities_url = 'https://www.strava.com/api/v3/athlete/activities?'

try:
    client = OAuth2Session(client_id, token=token, auto_refresh_kwargs=extra,
                           auto_refresh_url=refresh_url,
                           token_updater=token_saver)
    response = client.get(activities_url)
    if response.status_code != 200:
        logging.error('FAILED API CALL TO API')
        raise ConnectionError
except Exception as e:
    logging.critical('Could not download from API {}'.format(e))
else:
    upload_data_to_s3('test2', 'http://localhost:9000',
                      response.content, 'test3.json')
    logging.info('File Successfuly Uploaded')
