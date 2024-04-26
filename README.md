# AgriSpeak

The backend for the AgriSpeak forecast voice application.

## Features

AgriSpeak allows users to call a phone number and receive rainfall forecast information. The following features are supported:
- [x] 24 hour rainfall forecast
- [x] Information about the previous day's rainfall 
- [x] Estimated remaining duration of current rainfall
- [x] Multiple languages
- [x] User feedback system

When a user calls a number that uses AgriSpeak, they are presented four options:
1. Get information about the rainfall in the past 24 hours.
2. Get information about the rainfall in the next 24 hours.
3. Get the duration of the current rainfall, if there is any. This was found to be an important factor since rainfall often lasts for long periods at a time, as noted by our contact person.
4. Submit feedback through voice.

Operators can log into the admin panel to listen to the feedback submitted through option 4 and delete them once they are processed.

## System architecture

![](./infra.svg)

## Prerequisites

You will need:
- A weatherapi.com account with a generated API key.
- An Amazon S3, Cloudflare R2 or similar file storage solution.
- A running PostgreSQL instance.

## Deploy

### Dependencies

First, create a virtual environment using the command below:

```sh
python3 -m venv .venv
```

Then activate it:

```sh
. .venv/bin/activate
```

Install the required dependencies into the virtual environment:

```sh
pip3 install -r requirements.txt
```

### Enter environment variables

The application requires multiple environment variables to be set in order to function properly. Make a copy of `.env.template` and name it `.env` and add your values.
The table below explains what the environment variable values mean. All are required.

|Environment variable|Description|
|--------------------|-----------|
| `WEATHER_API_KEY`           | weatherapi.com API key. Make an account and provide the API key here |
| `SECRET_KEY`                | Used by Django for security purposes. Can be anything, as long as it is kept secret. |
| `AWS_STORAGE_BUCKET_NAME`   | The name of your AWS S3 bucket. Cloudflare R2 is also supported. |
| `AWS_S3_ENDPOINT_URL`       | The URL of the bucket, provided by S3/R2. |
| `AWS_S3_ACCESS_KEY_ID`      |  The ID of the access key, provided by S3/R2. |
| `AWS_S3_SECRET_ACCESS_KEY`  | The access key for the bucket, be sure to keep this a secret. Provided by S3/R2. |
| `POSTGRES_DB`               | This project assumes there already exists a running postgres database somewhere, provide the name of the database here. |
| `POSTRGRES_USER`            | The username of a postgres user. |
| `POSTGRES_PASSWORD`         | The password of the above user. Be sure to keep this secret. |
| `POSTGRES_HOST`             | The hostname of the connection to the database. If hosted locally this will be `localhost` or similar. |
| `POSTGRES_PORT`             | The port of the connection to the database. |
| `HOST`                      | The domain name or IP where the service will be accessible. This is needed for the feedback submission flow where the caller will make a POST request to send their recorded feedback to the server. We need the hostname to know where to insert into the VXML file the destination of the request. |

### Perform database migrations

Run the database migrations to make your Postgres instance ready for running AgriSpeak.

```sh
python3 manage.py migrate
```

If the environment variables were correctly set, and the instance is running, then the above will perform all the required migrations on the database.
This will create the required tables for AgriSpeak to function.

### Run

The below command will run the server on the default port and IP.

```
python3 manage.py runserver
```

## Usage

The API exposes one endpoint that returns the main VXML file. To view it, make a GET request to `http://<host>:<port>/forecast`. This will redirect you to the English version of the service. 

**Other languages**

Navigate to `http://<host>:<port>/<lang>/forecast` to retrieve the VXML file in other languages, where `<lang>` is the requested language. Please consult the below table for which value to use in place of `<lang>`:

|Language|`<lang>`|
|--------|--------|
|English (default)|`en`|
|French|`fr`|

**Submitting feedback**

In a call flow where the caller types '4', indicating they want to submit feedback, their recorded feedback will be sent to the service with a POST request to `http://<host>:<port>/<lang>/feedback`. In this case, `<lang>` is determined by the original language of their call. For example, if the user called a number that used the VXML pointing to `http://<host>:<port>/en/forecast`, then their feedback is submitted to `http://<host>:<port>/en/feedback`.

If you want to test this endpoint manually, make a POST request to `http://<host>:<port>/<lang>/feedback` with a wav file attached under the `msg` body parameter.

**Viewing and deleting feedback**

Visit `http://<host>:<port>/` to reach the admin panel where, after logging in, you can see all the submitted feedbacks and their languages, play back the audio, and delete them if they have been processed.

*Note:* You need to have an admin account to login here. To create one, run the following:

```sh
python manage.py createsuperuser
```
