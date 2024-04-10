from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Genre
from ..serializers import GenreSerializer
from rest_framework import status

class AllGenresView(APIView):
    def get(self, request):
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data)


class GenreDetailView(APIView):
    def get_object(self, genre_id):
        try:
            return Genre.objects.get(pk=genre_id)
        except Genre.DoesNotExist:
            raise Http404

    def get(self, request, genre_id):
        genre = self.get_object(genre_id)
        serializer = GenreSerializer(genre)
        return Response(serializer.data)

    def put(self, request, genre_id):
        genre = self.get_object(genre_id)
        serializer = GenreSerializer(genre, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, genre_id):
        genre = self.get_object(genre_id)
        genre.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request):
        serializer = GenreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
