# AgriSpeak

The backend for the AgriSpeak forecast voice application.

## Features

AgriSpeak allows users to call a phone number and receive rainfall forecast information. The following features are supported:
- [x] 24 hour rainfall forecast
- [x] Information about the previous day's rainfall 
- [x] Estimated remaining duration of current rainfall
- [x] Multiple languages
- [ ] User feedback system

## System architecture

TODO: @Daanvduin

## Installation

### One click Vercel deployment

Click here to deploy with Vercel:

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fandrulonis%2FICT4D&env=WEATHER_API_KEY,SECRET_KEY&envDescription=WEATHER_API_KEY%20is%20your%20weatherapi.com%20API%20key.%20SECRET_KEY%20will%20be%20used%20for%20the%20Django%20secret%20key.%20It%20can%20be%20anything%2C%20if%20kept%20secret.&project-name=agrispeak&repository-name=agrispeak)

### Manual

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

## Environment variables

The application requires multiple environment variables to be set in order to function properly. Make a copy of `.env.template` and name it `.env`. Add the required values where required. The Django `SECRET_KEY` can be anything, as long as it is kept secret.

## Run

The below command will run the server on the default port and IP.

```
python3 manage.py runserver
```

## Usage

The API exposes one endpoint at the root URL that returns the VXML file. To view it, make a GET request to `http://<ip-address>:<port>/`. This will redirect you to the English version of the service. 

**Other languages**

Navigate to `http://<ip-address>:<port>/<lang>` to retrieve the VXML file in other languages, where `<lang>` is the requested language. Please consult the below table for which value to use in place of `<lang>`:

|Language|`<lang>`|
|--------|--------|
|English (default)|`en`|
|French|`fr`| 

