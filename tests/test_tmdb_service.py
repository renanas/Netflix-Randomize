import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# ensure project root is on sys.path so "backend" package is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.services.tmdb_service import fetch_popular_movies, fetch_movie_details


class TestTMDBService(unittest.TestCase):

    @patch('backend.services.tmdb_service.requests.get')
    @patch('backend.services.tmdb_service.MovieRepository')
    def test_fetch_popular_movies_does_not_mutate(self, mock_repo_cls, mock_get):
        """Returned movie dicts should not gain an "_id" after saving."""
        fake_movies = [{"id": 1, "title": "A"}]
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"results": fake_movies}
        mock_get.return_value = mock_resp

        repo_instance = MagicMock()
        mock_repo_cls.return_value = repo_instance
        repo_instance.save_many_movies.return_value = []

        result = fetch_popular_movies(page=1)
        self.assertEqual(result, fake_movies)
        # verify the list was not mutated
        self.assertNotIn("_id", fake_movies[0])

    @patch('backend.services.tmdb_service.requests.get')
    @patch('backend.services.tmdb_service.MovieRepository')
    def test_fetch_movie_details_does_not_mutate(self, mock_repo_cls, mock_get):
        fake_details = {"id": 42, "title": "Detail"}
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = fake_details
        mock_get.return_value = mock_resp

        repo_instance = MagicMock()
        mock_repo_cls.return_value = repo_instance
        repo_instance.save_movie.return_value = "some_id"

        result = fetch_movie_details(42)
        self.assertEqual(result, fake_details)
        self.assertNotIn("_id", fake_details)


if __name__ == "__main__":
    unittest.main()
