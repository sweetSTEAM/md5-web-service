from django.test import SimpleTestCase
import time
import json


# Invalid url, invalid guid
class BadInfoTest(SimpleTestCase):
    def test_post(self):
        response = self.client.post("/api/post_link/", json.dumps(
            {"url": "1337"}), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_get(self):
        response = self.client.get('/api/get_status/' + '1337/',
                                   content_type='application/json')
        self.assertEqual(response.status_code, 404)


# Getting hash of file test
class HashTest(SimpleTestCase):
    def test_hash(self):
        # Getting guid
        response = self.client.post("/api/post_link/",
            json.dumps({
                "url":"https://www.dropbox.com/s/snrupwmhwg40qgl/F.cpp?dl=1"}),
            content_type="application/json")
        self.assertEqual(response.status_code, 202)
        self.guid = response.data['guid']
        # Checking background start
        # time.sleep(0.1)
        response = self.client.get('/api/get_status/' + self.guid + '/')
        self.assertEqual(response.status_code, 409)
        # Waiting for download
        while (self.client.get(
            '/api/get_status/' + self.guid + '/').status_code == 409):
            time.sleep(1)
        # Checking answer
        response = self.client.get('/api/get_status/' + self.guid + '/',
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['info'],
                         'd47681286ad532eba1d89b0bc7e823e7')
