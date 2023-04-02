# NFetch
Simple API for interacting with a public news fetching API

## Installation
Install the python dependencies with the following command. Use the latest python installation.
```
pip install requests
```

## API Key
Get the API key from [NewsAPI](https://newsapi.org/) and add it to your environment variable by ``export GNEWS_API_KEY='YOUR_API_KEY' ``

### Example
An example on how to use this API is shown in ``test.py``. If you need to control where to save the CACHE change the variable ``CACHE_FILE: NFetcher.py``

### Article Strcture

This API returns the following data in JSON format:

- source (object): The identifier id and a display name name for the source this article came from.
- author (string): The author of the article
- title (string): The headline or title of the article.
- description (string): A description or snippet from the article.
- url (string): The direct URL to the article.
- urlToImage (string): The URL to a relevant image for the article.
- publishedAt (string): The date and time that the article was published, in UTC (+000)
- content (string): Returns the content of article upto 200 chars
