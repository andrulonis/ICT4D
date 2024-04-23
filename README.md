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

