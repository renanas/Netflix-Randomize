import sys
import os
import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime

# make sure backend package is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestUserRepository(unittest.TestCase):

    def test_add_to_viewing_history(self):
        # ensure no leftover fake modules from other tests
        import importlib, sys
        for mod in ['backend.repository.user_repository', 'backend.repository']:
            sys.modules.pop(mod, None)
        ur = importlib.import_module('backend.repository.user_repository')
        UserRepository = ur.UserRepository

        # prepare mocks for connection and collection inside patched context
        with patch('backend.repository.user_repository.MongoDBConnection') as mock_conn_class:
            mock_conn = MagicMock()
            mock_conn_class.return_value = mock_conn
            mock_db = MagicMock()
            mock_conn.get_db.return_value = mock_db
            mock_collection = MagicMock()
            # ensure update_one returns object with numeric attributes
            mock_collection.update_one.return_value = MagicMock(modified_count=0, matched_count=0)
            mock_db.__getitem__.return_value = mock_collection

            repo = UserRepository()

            # patch ObjectId to identity and datetime.utcnow for deterministic output
            with patch('backend.repository.user_repository.ObjectId', side_effect=lambda x: x):
                fixed = datetime(2026, 3, 9, 20, 0, 0)
                with patch('backend.repository.user_repository.datetime') as mock_dt:
                    mock_dt.utcnow.return_value = fixed
                    result = repo.add_to_viewing_history('user123', 777)

        expected_item = {"movie_id": 777, "watched_at": fixed.isoformat()}
        mock_collection.update_one.assert_called_once_with(
            {"_id": 'user123', "user_behavior.viewing_history.movie_id": {"$ne": 777}},
            {"$push": {"user_behavior.viewing_history": expected_item}}
        )
        self.assertFalse(result)

    def test_remove_from_viewing_history(self):
        # ensure no fake modules remain
        import importlib, sys
        for mod in ['backend.repository.user_repository', 'backend.repository']:
            sys.modules.pop(mod, None)
        ur = importlib.import_module('backend.repository.user_repository')
        UserRepository = ur.UserRepository

        with patch('backend.repository.user_repository.MongoDBConnection') as mock_conn_class:
            mock_conn = MagicMock()
            mock_conn_class.return_value = mock_conn
            mock_db = MagicMock()
            mock_conn.get_db.return_value = mock_db
            mock_collection = MagicMock()
            mock_collection.update_one.return_value = MagicMock(modified_count=0)
            mock_db.__getitem__.return_value = mock_collection

            repo = UserRepository()

            with patch('backend.repository.user_repository.ObjectId', side_effect=lambda x: x):
                result = repo.remove_from_viewing_history('user123', 777)

        mock_collection.update_one.assert_called_once_with(
            {"_id": 'user123'},
            {"$pull": {"user_behavior.viewing_history": {"movie_id": 777}}}
        )
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
