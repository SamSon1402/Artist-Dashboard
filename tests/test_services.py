import unittest
from unittest.mock import patch, MagicMock
from services.spotify_service import SpotifyService

class TestSpotifyService(unittest.TestCase):
    
    def setUp(self):
        self.spotify_service = SpotifyService()
    
    @patch('services.spotify_service.requests.post')
    def test_authenticate(self, mock_post):
        # Mock the response from requests.post
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'access_token': 'test_token',
            'expires_in': 3600
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        # Call the authenticate method
        result = self.spotify_service.authenticate()
        
        # Check that authentication was successful
        self.assertTrue(result)
        self.assertEqual(self.spotify_service.access_token, 'test_token')
        self.assertIsNotNone(self.spotify_service.token_expiry)
    
    @patch('services.spotify_service.requests.get')
    @patch('services.spotify_service.SpotifyService.authenticate')
    def test_get_artist(self, mock_authenticate, mock_get):
        # Setup mocks
        mock_authenticate.return_value = True
        
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'id': 'artist_id',
            'name': 'Test Artist',
            'popularity': 85,
            'followers': {'total': 1000000}
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Call the get_artist method
        artist = self.spotify_service.get_artist('artist_id')
        
        # Check that we got the expected result
        self.assertEqual(artist['id'], 'artist_id')
        self.assertEqual(artist['name'], 'Test Artist')
        
        # Check that the API was called with the right parameters
        mock_get.assert_called_once()
        call_args = mock_get.call_args[0][0]
        self.assertIn('artists/artist_id', call_args)
    
    @patch('services.spotify_service.requests.get')
    @patch('services.spotify_service.SpotifyService.authenticate')
    def test_get_artist_by_name(self, mock_authenticate, mock_get):
        # Setup mocks
        mock_authenticate.return_value = True
        
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'artists': {
                'items': [
                    {
                        'id': 'artist_id',
                        'name': 'Test Artist',
                        'popularity': 85
                    }
                ]
            }
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Call the get_artist_by_name method
        artist = self.spotify_service.get_artist_by_name('Test Artist')
        
        # Check that we got the expected result
        self.assertEqual(artist['id'], 'artist_id')
        self.assertEqual(artist['name'], 'Test Artist')
        
        # Check that the API was called with the right parameters
        mock_get.assert_called_once()
        call_args = mock_get.call_args[1]['params']
        self.assertEqual(call_args['q'], 'Test Artist')
        self.assertEqual(call_args['type'], 'artist')

# Similar tests would be written for other service classes

if __name__ == '__main__':
    unittest.main()