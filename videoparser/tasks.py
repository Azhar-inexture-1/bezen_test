import os
import uuid
import subprocess
from boto3.exceptions import S3UploadFailedError
from celery import shared_task
from django.conf import settings
from bezen import s3_client, dynamodb_table
from videoparser.exceptions import NoSubtitlesError


@shared_task
def subtitle_extraction(file_path, file_name):
    """Extracts subtitles of video, uploads the subtitles to dynamodb and stores the video in s3 bucket.
    Parameters
    ----------
    file_path: string
        Path of video in the localstorage.
    file_name: string
        Name of the video.
    Returns
    -------
    Boolean: true or false
    """
    try:
        count = 0
        process = subprocess.Popen(
            ['ccextractor', '-stdout', '-out=ttxt', '-quiet', file_path],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL
        )
        video_name_subtitle_id = uuid.uuid4().hex
        video_name = f"{video_name_subtitle_id}_{file_name}"
        with dynamodb_table.batch_writer() as batch:
            while line_byte := process.stdout.readline():
                line = line_byte.rstrip().decode("utf-8-sig")
                count += 1
                if count == 40:
                    break
                if line == "":
                    raise NoSubtitlesError(f"failed to extract subtitles from the video, file: {file_name}")
                time_stamp = line.split("|")
                subtitle_id = uuid.uuid4().hex  # generates id for dynamodb primary key
                batch.put_item(Item={
                    'subtitle_id': subtitle_id,
                    'name': f'media/{video_name}',
                    'start': time_stamp[0],
                    'end': time_stamp[1],
                    'text': time_stamp[3].strip(),
                    'video_id': video_name_subtitle_id})  # Uploads data to dynamodb table
                print(f"Uploading: {subtitle_id}")
        dynamodb_table.put_item(Item={
                'subtitle_id': video_name_subtitle_id,
                'video_name': video_name
            })
        s3_client.upload_file(
            Filename=file_path, Bucket=settings.AWS_BUCKET_NAME,
            Key=f'media/{video_name}', ExtraArgs={'ACL': 'public-read'})  # Uploads video to s3 bucket
        return True
    except NoSubtitlesError as e:
        print(e)
    except subprocess.CalledProcessError as e:
        print(e.output)
    except FileNotFoundError as e:
        print(e.args[1])
    except S3UploadFailedError as e:
        print(e)
    except Exception as e:
        print(e)
    finally:
        os.remove(file_path)  # removes the file from localstorage
    return False
