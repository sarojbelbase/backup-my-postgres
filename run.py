from datetime import datetime
from os import environ, getcwd, path, remove
from subprocess import call

from boto3 import Session
from dateutil.tz import gettz, tzutc
from dotenv import load_dotenv

load_dotenv()

UPLOAD_FOLDER = 'backups'
DATABASE_HOST = "localhost"
S3_BUCKET = environ.get("S3_BUCKET")
ACCESS_KEY = environ.get("AWS_ACCESS_KEY_ID")
SECRET_KEY = environ.get("AWS_SECRET_ACCESS_KEY")
DATABASE_USERNAME = environ.get("DATABASE_USERNAME")
DATABASES = environ.get("DATABASES").split(",")

session = Session(
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY
)
s3 = session.resource("s3")


def get_file_from_fs(filename):
    cwd = getcwd()
    file = path.join(cwd, filename)
    return file if path.exists(file) else None


def delete_file_from_fs(filename):
    cwd = getcwd()
    file = path.join(cwd, filename)
    return remove(file) if path.exists(file) else None

def todays_datetime():
    today = datetime.utcnow()
    to_zone = gettz('Asia/Kathmandu')
    utc_datetime = today.replace(tzinfo=tzutc())
    return utc_datetime.astimezone(to_zone)


def generate_filename(database):
    now_in_nepal = todays_datetime().strftime("%Y.%m.%d.%H")
    return f"{database}_{now_in_nepal}.dump"


def dump_database(database):
    filename = generate_filename(database)
    line = ['pg_dump', '-h', DATABASE_HOST, '-U', DATABASE_USERNAME, database]
    with open(filename, 'wb') as dump:
        call(line, stdout=dump)
    return filename


def upload_this_file(file, filename):
    bucket = s3.Bucket(S3_BUCKET)
    key = f'{UPLOAD_FOLDER}/{filename}'
    bucket.upload_file(file, key)
    delete_file_from_fs(filename)
    print(f"Uploaded {filename} to S3")


def main():
    for database in DATABASES:
        filename = dump_database(database)
        file = get_file_from_fs(filename)
        upload_this_file(file, filename)
    print("Backup Complete!")


if __name__ == "__main__":
    main()
