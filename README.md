Pop Up Archive API Python Client
=========================================

Python client SDK for https://www.popuparchive.com/

See docs at https://developer.popuparchive.com/

OAuth credentials are available from https://www.popuparchive.com/oauth/applications

Example:

```python
from popuparchive import Client

# create a client
client = Client(oauth_id, oauth_secret)

# get all your collections
collections = client.get_collections()

# create an item in collection 1234
item = client.create_item(1234, {
    'title': 'this is an item with remote audio files',
    'extra': {
        'callback': 'https://nosuchdomain.foo/callback/path',
    }
})

# create an audio file for the new item
audio_file = client.create_audio_file(
    item['id'],
    'http://example.com/foo.mp3'
)

# fetch a collection with id 1234
coll = client.get('/collections/1234')
# or more idiomatically
coll = client.get_collection(1234)

# fetch a specific item
item = client.get('/collections/1234/items/5678')
# or idiomatically
item = client.get_item(1234, 5678)

# search
res = client.search({ 'q':'test' })
for item in res['results']:
  print "[%s] %s (%s)" % ( item['id'], item['title'], item['collection_title'] )

```

## Development

To run the unit tests, create a **.env** file in the checkout
with the following environment variables set to meaningful values:

```
AS_ID=somestring
AS_SECRET=sekritstring
AS_HOST=http://popuparchive.dev
```
Make sure you have [tox](https://tox.readthedocs.io/en/latest/) installed.
If you wish to test all supported Python versions, use [pyenv](https://github.com/yyuu/pyenv) to install them.

Then run the tests:

```bash
tox
```
