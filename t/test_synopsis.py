import os
import json

import unittest
from unittest import TestCase

import sys
sys.path.append("../popuparchive")
sys.path.append(".")

from popuparchive import Client

import pprint

import dotenv
dotenv.load_dotenv('.env')

class TestSynopsis(TestCase):

    def setUp(self):
        self.client = Client(os.environ.get('PUA_ID'), os.environ.get('PUA_SECRET'), os.environ.get('PUA_HOST'))

    def test_constructor(self):
        self.assertTrue(self.client)

    def test_search(self):
        resp = self.client.search({'query':'test'})
        #pprint.pprint(resp)
        self.assertTrue(resp)
        self.assertEqual(resp['query'], 'test')
        self.assertEqual(resp['page'], 1)
        self.assertEqual(len( resp['results'] ), 20)
        for hit in resp['results']:
            self.assertTrue(hit['title'])

    def test_items(self):
        collections = self.client.get_collections()
        for coll in collections:
            item_id = coll['item_ids'][0]
            item_i  = self.client.get_item(coll['id'], item_id)
            item    = self.client.get('/collections/'+str(coll['id'])+'/items/'+str(item_id))
            #pprint.pprint(item)
            #pprint.pprint(item_i)
            self.assertEqual(item_i['title'], item['title'])

    def test_collections(self):
        colls = self.client.get_collections()
        for  coll in colls:
            #pprint.pprint(coll)
            coll_i = self.client.get_collection(coll['id'])
            self.assertEqual(coll_i['title'], coll['title'])

    def test_audio_files(self):
        colls = self.client.get_collections()
        coll = colls[0]
        item = self.client.create_item(coll['id'], { 
            'title': 'this is an item with remote audio files',
            'extra': {
                'callback': 'https://nosuchdomain.foo/callback/path'
            }
        })
        self.assertEqual(item['collection_id'], coll['id'])
        self.assertEqual(item['extra']['callback'], 'https://nosuchdomain.foo/callback/path')
        #pprint.pprint(item)

        remote_audio = 'https://speechmatics.com/api-samples/zero'
        audio_file = self.client.create_audio_file(item['id'], { 'remote_file_url': remote_audio })
        #pprint.pprint(audio_file)
        pua_item = self.client.get_item(coll['id'], item['id'])
        #pprint.pprint(pua_item)
        self.assertEqual(pua_item['audio_files'][0]['original'], remote_audio)
        
 

if __name__ == '__main__':
    unittest.main()
