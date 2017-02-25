# URL Shortenere Backend

USB - **U**RL **S**hortener **B**ackend

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

# Installation

# Usage

## API

### GET /:id or GET /links/:id

#### Description

Try to perform a redirect by given short URL, considering a device type.

#### Parameters

* **id** - string, representing the identifier of the short URL (match this regexp `^[a-zA-Z0-9]{6,}$`).

#### Body

None.

#### Return

* **301** (Moved Permanently) - successful redirect;
* **404** (Not Found) - can't find any match for given id.

### GET /links

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

### POST /links

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

* **200** (OK) - short URL successfully created;
* **409** (Conflict) - given long URL already shortened.

For both cases we'll have response body in JSON format. Response body is like this:

```json
{"url": "..."}
```

where:

* **url** - short URL.

### PATCH /links/:id

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

* **204** (No Content) - update was successful;
* **404** (Not Found) - the short URL isn't found.

In both cases you will not get any response body.

# Development

## Tests

You can run full test suite by executing following command:

```
nosetests
```
