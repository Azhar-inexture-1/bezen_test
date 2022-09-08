# DJANGO Video Subtitle Processor

Extration of subtitle is done using CCEXTRACTOR

## Setup

### Create a virtualenv and install the requirements
```commandline
python3 -m virtualenv myvenv
# activate the virtual enviroment
source myven/bin/activate
pip install -r requirements.txt
```

### Add Configuration in .env file

Create a `.env` file at same level as your manage.py file and add your credentials, the file will automatically
be loaded.

Below is an example of `.env` file.
```commandline
SECRET_KEY=your secret key
MEDIA_URL=https://my-bucket.s3.region.amazonaws.com/
AWS_ACCESS_KEY=
AWS_SECRET_KEY=
AWS_BUCKET_NAME=
AWS_DYNAMODB_NAME=
AWS_REGION_NAME=
CELERY_BROKER_URL=redis://localhost:6379
CELERY_RESULT_BACKEND=redis://localhost:6379
```

### Install ccextractor Using apt-get on ubuntu
Update apt database with apt-get using the following command.

```commandline
sudo apt-get update
```
After updating apt database, We can install ccextractor using apt-get by running the following command:
```commandline
sudo apt-get -y install ccextractor
```

## Running the example

### Start redis backend
```commandline
$ redis-cli
redis 127.0.0.1:6379> ping
PONG
```

### Start a celery worker
You'll need a worker to get things done, run the following command in a separate terminal tab.

```bash
celery -A bezen worker --loglevel=info
```

### Start the app.

Open a new terminal tab and start the app

```bash
python manage.py runserver
```

### Endpoints
```commandline
Upload Video: http://127.0.0.1:8000/
Search Subtitle: http://127.0.0.1:8000/videos/
```