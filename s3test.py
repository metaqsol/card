import boto3
import json
from botocore.client import Config

# JSON 파일에서 설정 읽기
def load_config(config_file):
    with open(config_file, 'r') as file:
        config = json.load(file)
    return config

# S3 호환 클라이언트 생성
def create_s3_client(endpoint_url, access_key, secret_key):
    return boto3.client(
        's3',
        endpoint_url=endpoint_url,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        config=Config(signature_version='s3v4')
    )

# S3 버킷 목록을 가져오는 함수 (테스트 목적)
def list_bucket_contents(s3_client, bucket_name):
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        if 'Contents' in response:
            print(f"Contents of bucket '{bucket_name}':")
            for obj in response['Contents']:
                print(f" - {obj['Key']}")
        else:
            print(f"The bucket '{bucket_name}' is empty.")
    except Exception as e:
        print(f"Error accessing the bucket: {e}")

# JSON 설정 파일 경로
config_file = 'video_config.json'

# 설정 로드 및 S3 접속 테스트
config = load_config(config_file)
s3_client = create_s3_client(config['endpoint_url'], config['access_key'], config['secret_key'])

# 버킷 내 파일 목록을 가져와 출력
list_bucket_contents(s3_client, config['bucket_name'])
