import unittest
import os
import json
from app import create_app, db

class UserTestCase(unittest.TestCase):
    """This class represents the user test case"""
    def setUp(self):
        """Test variable and initialise app."""
        self.app = create_app(config_name="testing")
        self.client= self.app.test_client
        self.user = {'username':'bob1', 'name':'bob', 'email':'bob@email.com', 'password':'password1'}
        with self.app.app_context():
            db.create_all()
    
    def test_user_creation(self):
        """Test API can create a user (POST request)"""
        res = self.client().post('/users/', data=self.user)
        self.assertEqual(res.status_code, 201)
        self.assertIn('bob1', str(res.data))
        self.assertIn('bob', str(res.data))
        self.assertIn('bob@email.com', str(res.data))
        self.assertIn('password1', str(res.data))

    def test_api_can_get_all_users(self):
        """Test API can get users (GET request)."""
        res = self.client().post('/users/', data=self.user)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/users/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('bob1', str(res.data))

    def test_api_can_get_user_by_id(self):
        """Test API can get a single user by using it's id."""
        rv = self.client().post('/users/', data=self.user)
        self.assertEqual(rv.status_code, 201)
        result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
        result = self.client().get(
            '/users/{}'.format(result_in_json['id']))
        self.assertEqual(result.status_code, 200)
        self.assertIn('bob1', str(result.data))

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

class ImageTestCase(unittest.TestCase):
    """This class represents the image test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.user = {'username':'bob1', 'name':'bob', 'email':'bob@email.com', 'password':'password1'}
        self.image = {'url': 'https://i.imgur.com/jrMxxFY.jpg', 'diff':'4', 'user_id':'1'}
        with self.app.app_context():
            db.create_all()
        res = self.client().post('/users/', data=self.user)

    def test_image_creation(self):
        """Test API can create a image (POST request)"""
        res = self.client().post('/images/', data=self.image)
        self.assertEqual(res.status_code, 201)
        self.assertIn('https://i.imgur.com/jrMxxFY.jpg', str(res.data))
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

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

class TileTestCase(unittest.TestCase):
    """This class represents the Tile test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.tile = {'url': 'https://files.slack.com/files-pri/T1VHRHZE2-FNLFH4VQT/c1.png'}
        with self.app.app_context():
            db.create_all()

    def test_tile_creation(self):
        """Test API can create a tile (POST request)"""
        res = self.client().post('/tiles/', data=self.tile)
        self.assertEqual(res.status_code, 201)
        self.assertIn('https://files.slack.com/files-pri/T1VHRHZE2-FNLFH4VQT/c1.png', str(res.data))

    def test_api_can_get_all_tiles(self):
        """Test API can get a tile (GET request)."""
        res = self.client().post('/tiles/', data=self.tile)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/tiles/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('https://files.slack.com/files-pri/T1VHRHZE2-FNLFH4VQT/c1.png', str(res.data))

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()