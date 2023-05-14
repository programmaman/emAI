import os
import unittest
from unittest.mock import MagicMock, patch
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from authenticator import get_credentials


class AuthenticateTestCase(unittest.TestCase):
    def setUp(self):
        self.token_file_path = 'token.json'
        self.credentials_file_path = 'credentials.json'

    def tearDown(self):
        if os.path.exists(self.token_file_path):
            os.remove(self.token_file_path)

    @patch('authenticate.os.path.exists')
    @patch('authenticate.Credentials.from_authorized_user_file')
    def test_existing_token(self, mock_from_authorized_user_file, mock_path_exists):
        mock_path_exists.return_value = True
        mock_credentials = MagicMock(spec=Credentials)
        mock_from_authorized_user_file.return_value = mock_credentials

        result = get_credentials()

        self.assertEqual(result, mock_credentials)
        mock_path_exists.assert_called_once_with(self.token_file_path)
        mock_from_authorized_user_file.assert_called_once_with(self.token_file_path,
                                                               ['https://www.googleapis.com/auth/gmail.readonly'])
        # Other assertions as necessary

    @patch('authenticate.os.path.exists')
    @patch('authenticate.Credentials.from_authorized_user_file')
    @patch('authenticate.Request')
    def test_invalid_credentials(self, mock_request, mock_from_authorized_user_file, mock_path_exists):
        mock_path_exists.return_value = False
        mock_credentials = MagicMock(spec=Credentials)
        mock_credentials.valid = False
        mock_credentials.refresh_token = 'refresh_token'
        mock_credentials.to_json.return_value = '{"access_token": "123456"}'
        mock_from_authorized_user_file.return_value = None
        mock_request.return_value = mock_credentials

        with patch.object(InstalledAppFlow, 'from_client_secrets_file') as mock_flow:
            mock_flow.return_value.run_local_server.return_value = mock_credentials

            result = get_credentials()

        self.assertEqual(result, mock_credentials)
        mock_path_exists.assert_called_once_with(self.token_file_path)
        mock_from_authorized_user_file.assert_not_called()
        mock_flow.assert_called_once_with(self.credentials_file_path,
                                          ['https://www.googleapis.com/auth/gmail.readonly'])
        mock_flow.return_value.run_local_server.assert_called_once_with(port=0)
        # Other assertions as necessary


if __name__ == '__main__':
    unittest.main()
