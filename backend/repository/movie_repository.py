from backend.database.mongodb_connection import MongoDBConnection


class MovieRepository:
    def __init__(self):
        self.mongo_conn = MongoDBConnection()
        self.mongo_conn.connect()
        self.db = self.mongo_conn.get_db()
        self.collection = self.db["movies"]

    def save_movie(self, movie_data):
        """
        Save movie data to the database. If it already exists (by TMDb id), ignore.
        """
        movie_id = movie_data.get("id")
        if not movie_id:
            raise ValueError("movie_data must contain 'id' from TMDB")

        # Avoid duplicates
        existing = self.collection.find_one({"id": movie_id})
        if existing:
            return existing["_id"]

        # Make a shallow copy so the caller's dictionary isn't mutated by PyMongo
        data_to_insert = movie_data.copy()
        result = self.collection.insert_one(data_to_insert)
        return result.inserted_id

    def save_many_movies(self, movies_list):
        """
        Save many movies to the database. Ignoring duplicates.
        """
        saved_ids = []
        for movie in movies_list:
            saved_ids.append(self.save_movie(movie))
        return saved_ids

    def get_all_movies(self, limit=50):
        """
        Return movies stored.
        """
        return list(self.collection.find().limit(limit))

    def get_movie_by_tmdb_id(self, movie_id):
        """
        Get movie by ID of TMDb.
        """
        return self.collection.find_one({"id": movie_id})

    def insert_movie(self, movie_data):
        """
        Insert a single movie document into the collection.
        """
        result = self.collection.insert_one(movie_data)
        return result.inserted_id

    def insert_many_movies(self, movies_list):
        """
        Insert multiple movie documents into the collection.
        """
        result = self.collection.insert_many(movies_list)
        return result.inserted_ids

    def find_movie(self, query):
        """
        Find a single movie document matching the query.
        """
        return self.collection.find_one(query)

    def find_movies(self, query={}, limit=50):
        """
        Find multiple movie documents matching the query.
        """
        return list(self.collection.find(query).limit(limit))

    def update_movie(self, query, update_data):
        """
        Update a single movie document matching the query.
        """
        return self.collection.update_one(query, {"$set": update_data})

    def update_many_movies(self, query, update_data):
        """
        Update multiple movie documents matching the query.
        """
        return self.collection.update_many(query, {"$set": update_data})

    def delete_movie(self, query):
        """
        Delete a single movie document matching the query.
        """
        return self.collection.delete_one(query)

    def delete_many_movies(self, query):
        """
        Delete multiple movie documents matching the query.
        """
        return self.collection.delete_many(query)

    def count_movies(self, query={}):
        """
        Count the number of movie documents matching the query.
        """
        return self.collection.count_documents(query)
