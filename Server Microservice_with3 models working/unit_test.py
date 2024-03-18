import unittest
from flask import Flask
from app import app
import subprocess
import coverage

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        pass

    def test_ping(self):
        response = self.app.get('/ping')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), 'pong')

    def test_voice_analyze_post(self):
        # Assuming you have a sample audio file for testing
        with open(r'F:\Hackathon_2024\Server Integration Models\Server Microservice_with3 models working\test\faud01.mp3', 'rb') as audio_file:
            data = {
                'audio_file': (audio_file, 'faud01.mp3')
            }
            response = self.app.post('/voice/analyze', data=data, content_type='multipart/form-data')
            self.assertEqual(response.status_code, 200)
            # Assert JSON response contains necessary fields
            self.assertIn('status', response.json)
            self.assertIn('deepFakeStatus', response.json)
            self.assertIn('emotion', response.json)
            self.assertIn('liveliness', response.json)
            self.assertIn('backgroundsound', response.json)
            self.assertIn('file-path', response.json)

    # def test_voice_analyze_get(self):
    #     response = self.app.get('/voice/analyze')
    #     self.assertEqual(response.status_code, 200)
    #     # Assert that the response contains the voice form
    #     self.assertIn(b'Voice Analysis Form', response.data)

if __name__ == '__main__':
    cov = coverage.Coverage()

    # Start coverage measurement
    cov.start()
    unittest.main()
    # Stop coverage measurement
    cov.stop()

    # Save coverage data to a file
    # Generate HTML coverage report
    subprocess.run(['coverage', 'html'])

   