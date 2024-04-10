from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Keyword
from ..serializers import KeywordSerializer
from rest_framework import status


class AllKeywordsView(APIView):
    def get(self, request):
        keywords = Keyword.objects.all()
        serializer = KeywordSerializer(keywords, many=True)
        return Response(serializer.data)


class KeywordDetailView(APIView):
    def get_object(self, pk):
        try:
            return Keyword.objects.get( pk=pk )
        except Keyword.DoesNotExist:
            raise Http404


    def put(self, request, keyword_id):
        keyword = self.get_object(keyword_id)
        serializer = KeywordSerializer( keyword, data=request.data )
        if serializer.is_valid():
            serializer.save()
            return Response( serializer.data )
        return Response( serializer.errors, status=status.HTTP_400_BAD_REQUEST )

    def delete(self, request, keyword_id):
        keyword = self.get_object(keyword_id)
        keyword.delete()
        return Response( status=status.HTTP_204_NO_CONTENT )

    def get(self, request, keyword_id):
        try:
            keyword = Keyword.objects.get(id=keyword_id)
            serializer = KeywordSerializer(keyword)
            return Response(serializer.data)
        except Keyword.DoesNotExist:
            return Response({'message': 'Keyword with specified ID not found.'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = KeywordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
