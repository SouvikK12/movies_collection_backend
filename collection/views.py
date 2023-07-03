from django.shortcuts import get_object_or_404
from .serializers import CollectionSerializer, MovieSerializer
from rest_framework import status
from rest_framework.response import Response
from core.models import Collection, Movie, User
from rest_framework.parsers import JSONParser
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated


class CollectionApiViewSet(viewsets.ViewSet):

    permission_classes = [IsAuthenticated]

    parser_classes = [ JSONParser ]

    # Get the object_id
    def get_object(self, id):
        try:
            return Collection.objects.get(uuid=id, user=self.request.user)
        except Collection.DoesNotExist:
            return None


    def create(self, request):
        collection_data = request.data
        movies_data = request.data.pop("movies")

        collection_serializer = CollectionSerializer(data = collection_data)
        if collection_serializer.is_valid():
            collection = collection_serializer.save(user=request.user)

            movie_serializer = MovieSerializer(data = movies_data, many=True)
            if movie_serializer.is_valid():
                collection_instance = get_object_or_404(Collection, uuid=collection_serializer.data["uuid"])
                movie_serializer.save(collection = collection_instance)
            else:
                return Response({"success" : False, "data": None, "error" : movie_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

            return Response({'collection_uuid': collection.uuid}, status=status.HTTP_201_CREATED)
        return Response({"success" : False, "data": None, "error" : collection_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


    def list(self, request):

        collection_queryset = Collection.objects.filter(user = request.user)     

        collection_serializer = CollectionSerializer(collection_queryset,many=True)      

        res_data = {
            "collections" : collection_serializer.data
        }

        movie_genres = list(Movie.objects.filter(collection__user_id=request.user).values_list('genres', flat=True))
        
        genre_counts = {}

        for genre in movie_genres:
            individual_genres = genre.split(',')
            
            for individual_genre in individual_genres:
                individual_genre = individual_genre.strip()                
                genre_counts[individual_genre] = genre_counts.get(individual_genre, 0) + 1

        sorted_genres = sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)

        top_three_genres = ""

        for genre, count in sorted_genres[:3]:
            top_three_genres += f"{genre}, "

        top_three_genres = top_three_genres.rstrip(", ")

        res_data["favourite_genres"] = top_three_genres

        return Response({"is_success" : True, "data": res_data, "error" : None}, status=status.HTTP_200_OK)


    def retrieve(self, request, id, format=None):
        collection_queryset = self.get_object(id)
        if collection_queryset != None:
            collection_serializer = CollectionSerializer(collection_queryset)
            res_data = collection_serializer.data
            uuid = res_data.pop("uuid")

            movies_queryset = Movie.objects.filter(collection = uuid)
            movie_serializer = MovieSerializer(movies_queryset, many = True)

            res_data["movies"] = movie_serializer.data

            return Response({"success" : True, "data": res_data, "error" : None}, status=status.HTTP_200_OK)
        else:
            return Response({"success" : False, "data": None, "error" : "collection not found."}, status=status.HTTP_404_NOT_FOUND)


    def update(self, request, id, format=None):
        collection_queryset = self.get_object(id)
        if collection_queryset == None:
            return Response({"success" : False, "data": None, "error" : "collection not found."}, status=status.HTTP_404_NOT_FOUND)

        collection_serializer = CollectionSerializer(collection_queryset, data=request.data)

        if collection_serializer.is_valid():
            collection_serializer.save()

            Movie.objects.filter(collection=id).delete()

            movie_serializer = MovieSerializer(data = request.data['movies'], many=True)
            if movie_serializer.is_valid():
                collection_instance = get_object_or_404(Collection, uuid=collection_serializer.data["uuid"])
                movie_serializer.save(collection = collection_instance)
            else:
                return Response({"success" : False, "data": None, "error" : movie_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"success" : True, "data": "collection updated successfully.", "error" : None}, status=status.HTTP_200_OK)
        else:
            return Response({"success" : False, "data": None, "error" : "bad request."}, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, id, format=None):
        queryset = self.get_object(id)
        if queryset==None:
            return Response({"success" : False, "data": None, "error" : "collection not found."}, status=status.HTTP_404_NOT_FOUND)
        elif queryset:
            queryset.delete()
            return Response({"success" : True, "data": "collection deleted successfully.", "error" : None}, status=status.HTTP_200_OK)
        else:
            return Response({"success" : False, "data": None, "error" : "can not delete collection."}, status=status.HTTP_400_BAD_REQUEST)