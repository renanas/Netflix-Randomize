import unittest
from unittest.mock import MagicMock, patch
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from backend.repository.movie_repository import MovieRepository

class TestMovieRepository(unittest.TestCase):

    @patch('backend.repository.movie_repository.MongoDBConnection')
    def test_save_movie_new(self, mock_conn_class):
        """Test saving a new movie."""
        mock_conn = MagicMock()
        mock_conn_class.return_value = mock_conn
        mock_db = MagicMock()
        mock_conn.get_db.return_value = mock_db
        mock_collection = MagicMock()
        mock_db.__getitem__.return_value = mock_collection

        repo = MovieRepository()
        movie_data = {"id": 123, "title": "Test Movie"}
        mock_collection.find_one.return_value = None
        mock_insert = MagicMock()
        mock_insert.inserted_id = "inserted_id_123"
        mock_collection.insert_one.return_value = mock_insert

        result = repo.save_movie(movie_data)

        self.assertEqual(result, "inserted_id_123")
        mock_collection.find_one.assert_called_once_with({"id": 123})
        # ensure the repository copied the dict; we can't rely on object equality
        mock_collection.insert_one.assert_called_once()
        self.assertNotIn("_id", movie_data, "original movie_data should not be mutated")

    @patch('backend.repository.movie_repository.MongoDBConnection')
    def test_save_movie_existing(self, mock_conn_class):
        """Test saving an existing movie."""
        mock_conn = MagicMock()
        mock_conn_class.return_value = mock_conn
        mock_db = MagicMock()
        mock_conn.get_db.return_value = mock_db
        mock_collection = MagicMock()
        mock_db.__getitem__.return_value = mock_collection

        repo = MovieRepository()
        existing_movie = {"_id": "existing_id", "id": 123, "title": "Existing Movie"}
        mock_collection.find_one.return_value = existing_movie

        movie_data = {"id": 123, "title": "Test Movie"}
        result = repo.save_movie(movie_data)

        self.assertEqual(result, "existing_id")
        mock_collection.find_one.assert_called_once_with({"id": 123})
        mock_collection.insert_one.assert_not_called()

    @patch('backend.repository.movie_repository.MongoDBConnection')
    def test_save_movie_no_id(self, mock_conn_class):
        """Test saving a movie without ID."""
        mock_conn = MagicMock()
        mock_conn_class.return_value = mock_conn
        mock_db = MagicMock()
        mock_conn.get_db.return_value = mock_db
        mock_collection = MagicMock()
        mock_db.__getitem__.return_value = mock_collection

        repo = MovieRepository()
        movie_data = {"title": "Test Movie"}
        with self.assertRaises(ValueError) as context:
            repo.save_movie(movie_data)
        self.assertIn("movie_data must contain 'id' from TMDB", str(context.exception))

    @patch('backend.repository.movie_repository.MongoDBConnection')
    def test_save_many_movies(self, mock_conn_class):
        """Test saving multiple movies."""
        mock_conn = MagicMock()
        mock_conn_class.return_value = mock_conn
        mock_db = MagicMock()
        mock_conn.get_db.return_value = mock_db
        mock_collection = MagicMock()
        mock_db.__getitem__.return_value = mock_collection

        repo = MovieRepository()
        mock_collection.find_one.return_value = None
        mock_collection.insert_one.side_effect = [
            MagicMock(inserted_id="id1"),
            MagicMock(inserted_id="id2")
        ]

        movies = [
            {"id": 1, "title": "Movie 1"},
            {"id": 2, "title": "Movie 2"}
        ]
        result = repo.save_many_movies(movies)

        self.assertEqual(result, ["id1", "id2"])
        self.assertEqual(mock_collection.insert_one.call_count, 2)
        # the original movie dicts shouldn't have been mutated by PyMongo
        for m in movies:
            self.assertNotIn("_id", m)

    @patch('backend.repository.movie_repository.MongoDBConnection')
    def test_get_all_movies(self, mock_conn_class):
        """Test getting all movies."""
        mock_conn = MagicMock()
        mock_conn_class.return_value = mock_conn
        mock_db = MagicMock()
        mock_conn.get_db.return_value = mock_db
        mock_collection = MagicMock()
        mock_db.__getitem__.return_value = mock_collection

        repo = MovieRepository()
        mock_collection.find.return_value.limit.return_value = ["movie1", "movie2"]
        
        result = repo.get_all_movies(limit=10)
        
        self.assertEqual(result, ["movie1", "movie2"])
        mock_collection.find.assert_called_once()
        mock_collection.find.return_value.limit.assert_called_once_with(10)

    @patch('backend.repository.movie_repository.MongoDBConnection')
    def test_get_movie_by_tmdb_id(self, mock_conn_class):
        """Test getting movie by TMDB ID."""
        mock_conn = MagicMock()
        mock_conn_class.return_value = mock_conn
        mock_db = MagicMock()
        mock_conn.get_db.return_value = mock_db
        mock_collection = MagicMock()
        mock_db.__getitem__.return_value = mock_collection

        repo = MovieRepository()
        mock_collection.find_one.return_value = {"id": 123, "title": "Test Movie"}
        
        result = repo.get_movie_by_tmdb_id(123)
        
        self.assertEqual(result, {"id": 123, "title": "Test Movie"})
        mock_collection.find_one.assert_called_once_with({"id": 123})

if __name__ == "__main__":
    unittest.main()