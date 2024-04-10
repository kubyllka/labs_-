from django.urls import path

from .api_views.genre_views import AllGenresView, GenreDetailView
from .api_views.keyword_views import AllKeywordsView, KeywordDetailView

from .api_views.movie_views import RandomMovieView, MovieDetailView, \
    SimilarMoviesView, MoviesByGenreOrKeywordView

urlpatterns = [
    path('random_movie/', RandomMovieView.as_view(), name='random_movie' ),
    path('movies/<int:pk>/', MovieDetailView.as_view(), name='movie-detail'),
    path('genres/', AllGenresView.as_view(), name='all_genres'),
    path('keywords/', AllKeywordsView.as_view(), name='all_keywords'),
    path('genres/<int:genre_id>/', GenreDetailView.as_view(), name='genre_by_id'),
    path('keywords/<int:keyword_id>/', KeywordDetailView.as_view(), name='keyword_by_id'),
    path('movies/create/', MovieDetailView.as_view(), name='create_movie'),
    path('genres/create/', GenreDetailView.as_view(), name='create_genre'),
    path('keywords/create/', KeywordDetailView.as_view(), name='create_keyword'),
    path('movies/similarto/<int:movie_id>/<int:amount>/', SimilarMoviesView.as_view(), name='similar_movies'),
    path('movies/', MoviesByGenreOrKeywordView.as_view(), name='movie-list' ),
]

