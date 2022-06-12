# Database Backup

This project is to backup the database from EC2 Instance to s3 Bucket using python. It automatically dumps PostgreSQL backups to Amazon S3.

## Prerequisites

- Rename `.sample.env` to `.env` and add your credentials.
- Add an AWS account from `AWS Console` that has the access to the S3 bucket with the following permissions: `s3:PutObject`

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:PutObject"],
      "Resource": "arn:aws:s3:::<bucket>/<object>/*"
    }
  ]
}
```

- Run the following command to create the bucket:

```bash
aws s3 mb s3://example-backup-bucket --profile your-profile --region "ap-south-1"
```

## Usage

- Install dependencies:

  ```bash
  pip install -r requirements.txt
  ```

- Use python3 to run the script:

  ```bash
  python3 run.py
  ```

## Cron Job

### Setup in EC2 Instance

- Run the following command to setup the cron job:

  ```bash
  sudo service crond start (if not running)
  crontab -e
  ```

- Use cron to run the script every day at 02:00AM NEPALI TIME (UTC+5:45)

  ```bash
  0 22 * * * /home/ubuntu/database-backup/run.py
  ```
