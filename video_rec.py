import os
import json
import boto3
import ffmpeg
import threading
from datetime import datetime, timedelta
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

# 스트림을 받아 로컬 파일로 저장하는 함수 (연속적으로 캡처)
def capture_stream_continuously(stream_url, output_file, duration=3600):
    ffmpeg.input(stream_url).output(output_file, t=duration).run()

# S3에 파일 업로드 함수 (별도 스레드에서 실행)
def upload_to_s3_and_delete(s3_client, bucket_name, file_path, s3_key):
    try:
        s3_client.upload_file(file_path, bucket_name, s3_key)
        print(f"Uploaded {file_path} to s3://{bucket_name}/{s3_key}")
        os.remove(file_path)
        print(f"Deleted local file: {file_path}")
    except Exception as e:
        print(f"Error uploading {file_path}: {e}")

# S3에서 1주일 이상된 파일 삭제 함수 (별도 스레드에서 실행)
def delete_old_files(s3_client, bucket_name, retention_days=7):
    now = datetime.now()
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    
    if 'Contents' in response:
        for obj in response['Contents']:
            last_modified = obj['LastModified']
            file_age = now - last_modified.replace(tzinfo=None)
            if file_age > timedelta(days=retention_days):
                s3_client.delete_object(Bucket=bucket_name, Key=obj['Key'])
                print(f"Deleted {obj['Key']} from s3://{bucket_name}")

# 연속 비디오 캡처 및 업로드 반복 함수 (스레드에서 실행)
def continuous_capture_and_upload(s3_client, stream_url, stream_name, bucket_name, interval_hours=1, retention_days=7):
    while True:
        current_time = datetime.now().strftime('%y%m%d_%H%M')
        output_file = f'{stream_name}_{current_time}.mp4'
        s3_key = f'{stream_name}/{current_time}.mp4'
        capture_stream_continuously(stream_url, output_file, duration=3600)
        threading.Thread(target=upload_to_s3_and_delete, args=(s3_client, bucket_name, output_file, s3_key)).start()
        threading.Thread(target=delete_old_files, args=(s3_client, bucket_name, retention_days)).start()

# 여러 개의 스트림을 처리하는 메인 함수
def run_multiple_streams(config_file):
    config = load_config(config_file)
    s3_client = create_s3_client(config['endpoint_url'], config['access_key'], config['secret_key'])

    threads = []
    for stream_name, stream_url in config['streams'].items():
        thread = threading.Thread(target=continuous_capture_and_upload, args=(s3_client, stream_url, stream_name, config['bucket_name']))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()

# JSON 설정 파일 경로
config_file = 'video_config.json'

# 다중 스트림을 동시에 실행
run_multiple_streams(config_file)
