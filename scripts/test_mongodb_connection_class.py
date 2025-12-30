import unittest
from unittest.mock import MagicMock, patch
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from backend.database.mongodb_connection import MongoDBConnection

class TestMongoDBConnection(unittest.TestCase):

    def setUp(self):
        self.uri = "mongodb+srv://test:test@cluster0.test.mongodb.net/?appName=Cluster0"
        self.db_name = "test_db"
        self.collection_name = "test_collection"
        self.connection = MongoDBConnection(self.uri, self.db_name, self.collection_name)

    @patch('backend.database.mongodb_connection.MongoClient')
    def test_connect_success(self, mock_mongo_client):
        """Test successful connection."""
        mock_client = MagicMock()
        mock_mongo_client.return_value = mock_client
        mock_client.admin.command.return_value = {"ok": 1.0}
        mock_db = MagicMock()
        mock_client.__getitem__.return_value = mock_db
        mock_collection = MagicMock()
        mock_db.__getitem__.return_value = mock_collection

        result = self.connection.connect()

        self.assertTrue(result)
        mock_mongo_client.assert_called_once_with(self.uri)
        mock_client.admin.command.assert_called_once_with("ping")
        self.assertEqual(self.connection.client, mock_client)
        self.assertEqual(self.connection.db, mock_db)
        self.assertEqual(self.connection.collection, mock_collection)

    @patch('backend.database.mongodb_connection.MongoClient')
    def test_connect_failure(self, mock_mongo_client):
        """Test connection failure."""
        mock_client = MagicMock()
        mock_mongo_client.return_value = mock_client
        mock_client.admin.command.side_effect = Exception("Connection failed")

        result = self.connection.connect()

        self.assertFalse(result)
        self.assertIsNone(self.connection.client)
        self.assertIsNone(self.connection.db)
        self.assertIsNone(self.connection.collection)

    def test_disconnect(self):
        """Test disconnection."""
        mock_client = MagicMock()
        self.connection.client = mock_client

        self.connection.disconnect()

        mock_client.close.assert_called_once()

    def test_get_collection(self):
        """Test getting collection."""
        mock_collection = MagicMock()
        self.connection.collection = mock_collection

        result = self.connection.get_collection()

        self.assertEqual(result, mock_collection)

    def test_get_db(self):
        """Test getting database."""
        mock_db = MagicMock()
        self.connection.db = mock_db

        result = self.connection.get_db()

        self.assertEqual(result, mock_db)

if __name__ == "__main__":
    unittest.main()