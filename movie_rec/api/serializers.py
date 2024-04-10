from rest_framework import serializers
from .models import Movie, Genre, Keyword
from django.core.exceptions import ObjectDoesNotExist
import logging

class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'


class KeywordSerializer( serializers.ModelSerializer ):
    class Meta:
        model = Keyword
        fields = '__all__'



class MovieSerializer(serializers.ModelSerializer):
    logger = logging.getLogger( __name__ )
    genres = GenreSerializer(many=True, required=False)
    keywords = KeywordSerializer(many=True, required=False)


    class Meta:
        model = Movie
        fields = '__all__'

    def create(self, validated_data):
        genres_data = validated_data.pop( 'genres', [] )
        keywords_data = validated_data.pop( 'keywords', [] )

        genres_ids = []
        for genre_data in genres_data:
            self.logger.info( f"genre_data: {genre_data}" )
            try:
                if "id" in genre_data:
                    genre = Genre.objects.get( id=genre_data["id"] )
                elif "genre" in genre_data:
                    genre, _ = Genre.objects.get_or_create( genre=genre_data['genre'] )
                elif "tmdb_id" in genre_data:
                    genre = Genre.objects.get( tmdb_id=genre_data['tmdb_id'] )
                else:
                    raise KeyError( "Neither 'id' nor 'name' provided for genre." )
                if genre:
                    genres_ids.append(genre.id )
            except Genre.DoesNotExist:
                raise serializers.ValidationError( f"Genre with provided data {genre_data} does not exist." )

        keywords_ids = []
        for keyword_data in keywords_data:
            try:
                if 'id' in keyword_data:
                    keyword = Keyword.objects.filter( id=int(keyword_data['id']) ).first()
                elif 'keyword' in keyword_data:
                    keyword, _ = Keyword.objects.get_or_create( keyword=keyword_data['keyword'] )
                elif 'tmdb_id' in keyword_data:
                    keyword = Keyword.objects.filter( tmdb_id=int(keyword_data['tmdb_id']) ).first()
                else:
                    raise KeyError( "Neither 'id' nor 'name' provided for keyword." )
                if keyword:
                    keywords_ids.append( keyword.id )
            except Keyword.DoesNotExist:
                raise serializers.ValidationError( f"Keyword with provided data {keyword_data} does not exist." )

        movie = Movie.objects.create( **validated_data )
        movie.genres.set( genres_ids )
        movie.keywords.set( keywords_ids )

        return movie


