import unittest
import os
import json
from app import create_app, db


class ImageTestCase(unittest.TestCase):
    """This class represents the image test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.image = {'url': 'https://i.imgur.com/jrMxxFY.jpg'}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_image_creation(self):
        """Test API can create a image (POST request)"""
        res = self.client().post('/images/', data=self.image)
        self.assertEqual(res.status_code, 201)
        self.assertIn('https://i.imgur.com/jrMxxFY.jpg', str(res.data))

    def test_api_can_get_all_images(self):
        """Test API can get a image (GET request)."""
        res = self.client().post('/images/', data=self.image)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/images/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('https://i.imgur.com/jrMxxFY.jpg', str(res.data))

    def test_api_can_get_image_by_id(self):
        """Test API can get a single image by using it's id."""
        rv = self.client().post('/images/', data=self.image)
        self.assertEqual(rv.status_code, 201)
        result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
        result = self.client().get(
            '/images/{}'.format(result_in_json['id']))
        self.assertEqual(result.status_code, 200)
        self.assertIn('https://i.imgur.com/jrMxxFY.jpg', str(result.data))

    def test_image_can_be_edited(self):
        """Test API can edit an existing image. (PUT request)"""
        rv = self.client().post(
            '/images/',
            data={'url': 'https://i.pinimg.com/736x/d8/c7/e5/d8c7e59945e982e5f35b7c201fba038b.jpg'})
        self.assertEqual(rv.status_code, 201)
        rv = self.client().put(
            '/images/1',
            data={
                "url": "https://i.pinimg.com/originals/ff/46/3c/ff463c5381bf4c3b60cf4b7296fb984d.jpg"
            })
        self.assertEqual(rv.status_code, 200)
        results = self.client().get('/images/1')
        self.assertIn('https://i.pinimg.com/originals/ff/46/3c/ff463c5381bf4c3b60cf4b7296fb984d.jpg', str(results.data))

    def test_image_deletion(self):
        """Test API can delete an existing image. (DELETE request)."""
        rv = self.client().post(
            '/images/',
            data={'url': 'https://i.pinimg.com/736x/d8/c7/e5/d8c7e59945e982e5f35b7c201fba038b.jpg'})
        self.assertEqual(rv.status_code, 201)
        res = self.client().delete('/images/1')
        self.assertEqual(res.status_code, 200)
        # Test to see if it exists, should return a 404
        result = self.client().get('/images/1')
        self.assertEqual(result.status_code, 404)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

class PiecesTestCase(unittest.TestCase):
    """This class represents the Piecces test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.image = {'url': 'https://i.imgur.com/jrMxxFY.jpg'}
        self.pieces = {'value':'1', 'url': 'https://i.imgur.com/G1My5qP.jpeg'}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_pieces_creation(self):
        """Test API can create a object of pieces (POST request)"""
        res = self.client().post('/images/', data=self.image)
        self.assertEqual(res.status_code, 201)
        res = self.client().post('/images/1/beginner-pieces', data=self.pieces)
        self.assertEqual(res.status_code, 201)
        self.assertIn('https://i.imgur.com/G1My5qP.jpeg', str(res.data))

    def test_api_can_get_pieces_by_id(self):
        """Test API can get a set of pieces from an object (GET request)."""
        res = self.client().post('/images/', data=self.image)
        self.assertEqual(res.status_code, 201)
        res = self.client().post('/images/1/beginner-pieces', data=self.pieces)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/images/1')
        self.assertEqual(res.status_code, 200)
        self.assertIn('https://i.imgur.com/G1My5qP.jpeg', str(res.data))

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()