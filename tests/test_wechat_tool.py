import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import json

# Add the scripts directory to Python path
import pathlib
current_dir = pathlib.Path(__file__).parent
project_root = current_dir.parent
scripts_dir = project_root / "scripts"
sys.path.append(str(scripts_dir))

from utils.wechat_tool import send_wechat_message


class TestWeChatTool(unittest.TestCase):
    """Test cases for the WeChat messaging tool."""

    def test_empty_webhook_key(self):
        """Test that empty webhook key causes system exit."""
        with self.assertRaises(SystemExit):
            send_wechat_message("")
    
    @patch('utils.wechat_tool.requests.post')
    def test_successful_message_send(self, mock_post):
        """Test successful message sending with mocked response."""
        # Set up mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = json.dumps({"errcode": 0, "errmsg": "ok"})
        mock_post.return_value = mock_response
        
        # Call the function
        status_code, response_text = send_wechat_message("test_key", "test message")
        
        # Verify results
        self.assertEqual(status_code, 200)
        self.assertEqual(response_text, mock_response.text)
        
        # Verify the correct URL and data were used
        expected_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=test_key"
        expected_data = {
            "msgtype": "text",
            "text": {
                "content": "test message"
            }
        }
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        self.assertEqual(call_args[0][0], expected_url)
        self.assertEqual(call_args[1]['json'], expected_data)
    
    @patch('utils.wechat_tool.requests.post')
    def test_failed_message_send(self, mock_post):
        """Test system exit on failed message sending."""
        # Set up mock response for error
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = json.dumps({"errcode": 40014, "errmsg": "invalid webhook key"})
        mock_post.return_value = mock_response
        
        # Test that system exit occurs
        with self.assertRaises(SystemExit):
            send_wechat_message("invalid_key")
    
    @patch('utils.wechat_tool.requests.post')
    def test_request_exception(self, mock_post):
        """Test system exit on request exception."""
        # Set up mock to raise exception
        mock_post.side_effect = Exception("Network error")
        
        # Test that system exit occurs
        with self.assertRaises(SystemExit):
            send_wechat_message("test_key")


if __name__ == '__main__':
    unittest.main()