# TheguardianScrapper
A Scrapy webscraper that can scrape and store articles of theguardian.com 
## Installation
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install required libraries.
```bash
pip install -r requirements.txt
```
## Usage
To start scraping, make sure to create a cluster in [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) and 
use your connection credentials.
Update [settings.py](./TheguardianScrapper/settings.py):
```python
MONGO_URI = 'Connection URI'
MONGO_DATABASE = 'Database Name'
```
Then, run the command :
```bash
scrapy crawl theguardian
```
To run the server API use the same credentials for MongoDB in [server.py](./settings.py).
Then, run the command : 
```bash
env FLASK_APP=server.py flask run
```
## API 
The guardian spider crawls the following data:
| Key  | Type |Description|
| ------------- | ------------- | ------------- |
| author  | Array of strings  |Author(s) of the article.|
| headline  | String | Headline of the article. |
| content  | String | The article's content (text only). |
| standfirst  | String | The article's standfirst (text only). |
| label | Array of strings | The article's tags |
| url  | String | The article's page url. |
| published_at  | Date | Published date of the article. |

The server API provides the following: 
#### GET /articles
Get the list of crawled articles. 
* Path parameters :

| Key  | Type |Default value| Description |
| ------------- | ------------- | ------------- | ------------- |
| `page`   | integer | 1 | Specify which page to query |
| `num_articles`   | integer | 5 | Specify number of articles in each page |

* Response : 

```javascript
{ 
  'status' : 'success',
  'page' : 'page number',
  'num_articles_found' : 'the total number of articles queried',
  'num_articles_per_page' : 'the number of articles in each page',
  'results' : [array of items queried]
}
```
#### GET /search/(content | headline | author)
Search for articles either keywords in content or headline, or author name.
* Path parameters :

| Key  | Type |Default value| Description |
| ------------- | ------------- | ------------- | ------------- |
| `page`   | integer | 1 | Specify which page to query |
| `num_articles`   | integer | 5 | Specify number of articles in each page |
| `query`   | string | empty | Pass a text query to search. This value should be URI encoded. |

* Response : 

```javascript
{ 
  'status' : 'success',
  'page' : 'page number',
  'num_articles_found' : 'the total number of articles queried',
  'num_articles_per_page' : 'the number of articles in each page',
  'results' : [array of items queried]
}
```

## Known Issues

* Article content selectors need improvements.
* Search regexs need improvements.

## TODO 

* Use Readability framework to improve content selector. 
