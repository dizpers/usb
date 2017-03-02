# URL Shortener Backend

USB - **U**RL **S**hortener **B**ackend

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**

- [Intro](#intro)
- [Description](#description)
  - [Requirements](#requirements)
  - [Considerations](#considerations)
- [Requirements](#requirements-1)
- [Installation](#installation)
- [Usage](#usage)
  - [Management commands](#management-commands)
  - [API](#api)
    - [GET /:id or GET /urls/:id](#get-id-or-get-urlsid)
    - [GET /urls](#get-urls)
    - [POST /urls](#post-urls)
    - [PATCH /urls/:id](#patch-urlsid)
- [Development](#development)
  - [Tests](#tests)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# Intro

This project is the part of my application to [Joor](http://jooraccess.com/) company. Please, see the description of 
requirements below.

# Description

## Requirements

These are the business rules that need to be fulfilled:

1. User should be able to submit any URL and get a standardized, shortened URL back

2. User should be able to configure a shortened URL to redirect to different targets based on the device type (mobile,
tablet, desktop) of the user navigating to the shortened URL

3. Navigating to a shortened URL should redirect to the appropriate target URL

4. User should be able to retrieve a list of all existing shortened URLs, including time since creation and target URLs
(each with number of redirects)

5. API requests and responses should be JSON formatted.

6. Write tests to prove functionality.

## Considerations

These are some guidelines for scope and technology choice:

1. Don't worry about any user registration or authentication.

2. Use PHP, Python, or JavaScript with whatever web framework you prefer.

3. Use a relational database; I recommend SQLite for ease of use.

4. Please share this via a Github repository that we can clone.

5. Please provide instructions to set up, test and run the API in a local environment on Linux or Mac in a README file.

6. Building a front-end client for this API is not part of the assignment.

7. Deploying this API is not part of the assignment.

# Requirements

This projects requires you to have:

* **git**;
* **Python>=3.6**;
* **virtualenv**.

# Installation

Clone the repository:

```
git clone git@github.com:dizpers/usb.git
```

Go to the project directory:

```
cd usb
```

Create virtual environment. Following command will create it in `.env` directory with `python3` executable:

```
virtualenv -p python3 .env
```

Activate that environment. For bash it will be:

```
source .env/bin/activate
```

Install both product and development python dependencies:

```
pip install -U -r requirements.txt
pip install -U -r requirements-dev.txt
```

Create and the local settings file by copying the template:

```
mv usb/config/local.py.example usb/config/local.py
```

I recommend you to run full test suite to be sure that all is working fine:

```
nosetests
```

Create DB structures:

```
./manage.py createdb
```

From this moment you're ready to run the application. You can do it via manage command like this:

```
./manage.py runserver
```

# Usage

## Management commands

This project is equipped with special management command. You can run it with one of the following commands (considering
that you're in the project root directory right now):

```
python manage.py
./manage.py
```

Execution of that command will print you the list of available arguments and options. You can use following commands
within management tool:

* **createdb** - creates the database with all necessary structures;
* **dropdb** - clean the database;
* **runserver** - run the server;
* **shell** - (i)python shell with the context of the application;
* **show-urls** - prints all the urls matching routes in the project.

## API

### GET /:id or GET /urls/:id

#### Description

Try to perform a redirect by given short URL, considering a device type.

#### Parameters

* **id** - string, representing the identifier of the short URL (match this regexp `^[a-zA-Z0-9]{6,}$`).

#### Body

None.

#### Return

* **301** (Moved Permanently) - successful redirect;
* **404** (Not Found) - can't find any match for given id.

Actual redirect code (301 or whatever) can be set in settings. In case when short URL id was successfully found, you'll
get `Location` header value set to target URL.

### GET /urls

#### Description

Get a list of all existing shortened URLs, including time since creation and target URLs (each with number of 
redirects).

#### Parameters

None.

#### Body

None.

#### Return

* **200** (OK) - a list is successfully generated.

JSON object of the following structure is returned:

```json
{"short1": [
  {"type": "desktop", "url": "...", "redirects": 23, "datetime": ""}
  {"type": "tablet", "url": "...", "redirects": 23, "datetime": ""}
  {"type": "mobile", "url": "...", "redirects": 23, "datetime": ""}
],
"short2": []
}
```

where:

* **short1**, **short2**, ..., **shortN** - short URL;
* **type** - device type (one of the `desktop`, `tablet` and `mobile`);
* **url** - long URL for current short URL and the device type;
* **redirects** - number of redirects for current long URL;
* **datetime** - datetime (in UNIX format with milliseconds) of long URL addition (when it was shortened)

### POST /urls

#### Description

Create new short link by given long URL.

#### Parameters

None.

#### Body

Request body follows JSON format and looks like this:

```json
{"url": "..."}
```

where:

* **url** - long URL to be shortened.

#### Return

* **200** (OK) - short URL successfully created.

Response body is following JSON format and looks like this:

```json
{"url": "..."}
```

where:

* **url** - short URL.

### PATCH /urls/:id

#### Description

Update the short link to specify links for some device type(s).

#### Parameters

* **id** - string, representing the identifier of the short URL (match this regexp `^[a-zA-Z0-9]{6,}$`).

#### Body

Request body follows JSON format and looks like this:

```json
{"desktop": "..."}
```

or

```json
{"mobile": "...", "desktop": "...", "tablet": "..."}
```

where:

* **desktop** - long URL for desktop device;
* **tablet** - long URL for tablet device;
* **mobile** - long URL for mobile device.

You must specify at least one of the parameters above (`desktop`, `tablet` or `mobile`), in any order.

#### Return

* **200** (OK) - update was successful;
* **404** (Not Found) - the short URL isn't found.

In both cases you will get empty JSON object in a body.

# Development

Please, make sure that while developing:

* you're using local settings file (`usb/config/local.py`);
* you've already installed development requirements (`pip install -U -r requirements-dev.txt`).

## Tests

You can run full test suite by executing following command:

```
nosetests
```
