from random import randint, sample
from django.db.models import Max
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework import status
from ..movie_recommendation_model import MovieRecommendationModel

from ..models import Movie
from ..serializers import MovieSerializer

class RandomMovieView(APIView):
    def get(self, request):
        max_id = Movie.objects.aggregate(max_id=Max("id"))["max_id"]

        if max_id is not None:  # Перевіряємо, чи є значення max_id
            max_attempts = 1000
            attempts = 0
            while attempts < max_attempts:
                random_id = randint(1, max_id)
                try:
                    random_movie = Movie.objects.get(id=random_id)
                    serializer = MovieSerializer(random_movie)
                    return Response(serializer.data)
                except Movie.DoesNotExist:
                    attempts += 1
            return Response({'message': 'No random movie found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'message': 'No movies found.'}, status=status.HTTP_404_NOT_FOUND)


class MovieDetailView(APIView):
    def post(self, request):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self, pk):
        try:
            return Movie.objects.get( pk=pk )
        except Movie.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        movie = self.get_object( pk )
        serializer = MovieSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response( serializer.data )
        return Response( serializer.errors, status=status.HTTP_400_BAD_REQUEST )

    def delete(self, request, pk):
        movie = self.get_object( pk )
        movie.delete()
        return Response( status=status.HTTP_204_NO_CONTENT )

    def get(self, request, pk):
        try:
            # Отримуємо фільм за його унікальним ідентифікатором (pk)
            movie = Movie.objects.get(pk=pk)
            serializer = MovieSerializer(movie)
            return Response(serializer.data)
        except Movie.DoesNotExist:
            # Якщо фільм з таким ID не знайдено, повертаємо відповідне повідомлення
            return Response({'message': 'Movie with specified ID not found.'}, status=status.HTTP_404_NOT_FOUND)



class SimilarMoviesView(APIView):
    def get(self, request, movie_id, amount):
        try:
            # Отримуємо фільм за заданим ID
            movie = Movie.objects.get(id=movie_id)

            # Виконуємо рекомендацію для цього фільму
            recommendation_model = MovieRecommendationModel([{'id': movie_id}])
            recommended_movies = recommendation_model.recommend_movies()[:amount]

            # Повертаємо список рекомендованих фільмів
            return Response(recommended_movies, status=status.HTTP_200_OK)
        except Movie.DoesNotExist:
            # Якщо фільм з даним ID не існує, повертаємо помилку 404 Not Found
            return Response({'message': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Якщо виникає будь-яка інша помилка, повертаємо 500 Internal Server Error
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






class MoviesByGenreOrKeywordView(APIView):
    def get(self, request):
        genre_id = self.request.query_params.get('genre', None)
        keyword_id = self.request.query_params.get('keyword', None)
        order = self.request.query_params.get('order', None)
        year = self.request.query_params.get('year', None)

        if genre_id:
            movies = Movie.objects.filter(genres__id=genre_id)
        elif keyword_id:
            movies = Movie.objects.filter(keywords__id=keyword_id)
        else:
            movies = Movie.objects.all()

        if order == 'rate':
            movies = movies.order_by('vote_average')
        elif order == '-rate':
            movies = movies.order_by('-vote_average')
        elif order == 'year':
            movies = movies.order_by('year')
        elif order == '-year':
            movies = movies.order_by('-year')


        if year:
            movies = movies.filter(year=year)

        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)