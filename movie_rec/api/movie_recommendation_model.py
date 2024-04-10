import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from .models import Movie


class MovieRecommendationModel:

    def __init__(self, user_movies):
        movie_ids = [user_movie['id'] for user_movie in user_movies]
        self.movies = Movie.objects.exclude(id__in=movie_ids)
        self.user_movies = Movie.objects.filter(id__in=movie_ids)
        self.movie_vectors = self.calculate_movie_vectors(self.movies)
        self.user_movie_vectors = self.calculate_movie_vectors(self.user_movies)
        self.vectorizer = self.create_vectorizer()

    def calculate_movie_vectors(self, input_movies):
        movie_vectors = []
        for movie in input_movies:
            genres_string = ' '.join([str(genre) for genre in movie.genres.all()])
            keywords_string = ' '.join([str(keyword) for keyword in movie.keywords.all()])
            text = movie.overview + ' ' + genres_string + ' ' + keywords_string
            movie_vectors.append(text)
        return movie_vectors

    def create_vectorizer(self):
        vectorizer = TfidfVectorizer()
        vectors = self.movie_vectors + self.user_movie_vectors
        vectorizer.fit(vectors)

        return vectorizer

    def recommend_movies(self):
        user_vectors_tfidf = self.vectorizer.transform(self.user_movie_vectors)
        all_movies_vectors_tfidf = self.vectorizer.transform(self.movie_vectors)

        average_user_vector = np.asarray(user_vectors_tfidf.mean(axis=0))  # Перетворення у масив

        similarities = cosine_similarity(average_user_vector, all_movies_vectors_tfidf)

        recommended_movies_indices = similarities.argsort(axis=1)[:, ::-1]
        recommended_movies_indices = recommended_movies_indices.tolist()
        recommended_movies = [{
            'id': self.movies[i].id,
            'title': self.movies[i].title,
            'overview': self.movies[i].overview,
            'poster_path': self.movies[i].poster_path,
            'year': self.movies[i].year,
            'vote_average': self.movies[i].vote_average,
            'trailer_link': self.movies[i].trailer_link,
            'genres': [str(genre) for genre in self.movies[i].genres.all()],
            'keywords': [str(keyword) for keyword in self.movies[i].keywords.all()]
        } for indices in recommended_movies_indices for i in indices]

        return recommended_movies
