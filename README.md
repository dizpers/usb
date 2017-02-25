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

# Development

## Tests

You can run full test suite by executing following command:

```
nosetests
```
