import requests
from requests.exceptions import RequestException
from rest_framework.response import Response
from rest_framework import status
from core.middlewares import RequestCounterMiddleware
from rest_framework import viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from core.models import User
from rest_framework.permissions import IsAuthenticated
from requests.adapters import HTTPAdapter
from requests.auth import HTTPBasicAuth
from requests.exceptions import RequestException
from requests.packages import urllib3


def make_authenticated_request(url):
    auth = HTTPBasicAuth('iNd3jDMYRKsN1pjQPMRz2nrq7N99q4Tsp9EY9cM0', 'Ne5DoTQt7p8qrgkPdtenTK8zd6MorcCR5vXZIJNfJwvfafZfcOs4reyasVYddTyXCz9hcL5FGGIVxw3q02ibnBLhblivqQTp4BIC93LZHj4OppuHQUzwugcYu7TIC5H1')

    session = requests.Session()
    retries = urllib3.util.retry.Retry(total=3, backoff_factor=0.5, status_forcelist=[500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retries)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    try:
        response = session.get(url, auth=auth)
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        return None
    

class MovieApiViewSet(viewsets.ViewSet):

    permission_classes = [IsAuthenticated]

    def list(self, request):

        url = 'https://demo.credy.in/api/v1/maya/movies/'
        movie_data = make_authenticated_request(url)
        movie_data["data"] = movie_data.pop("results")
        
        if movie_data is not None:
            return Response(movie_data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Error retrieving movie data'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class UserApiViewset(viewsets.ViewSet):

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if username and password:
            user = User.objects.create_user(username=username, password=password)
            refresh = RefreshToken.for_user(user)
            return Response({'access_token': str(refresh.access_token)})
        return Response({'error': 'Username and password required.'}, status=status.HTTP_400_BAD_REQUEST)
    

class RequestApiViewset(viewsets.ViewSet):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        count = RequestCounterMiddleware.request_count
        return Response({'requests': count}, status=status.HTTP_200_OK)

    def post(self, request):
        RequestCounterMiddleware.request_count = 0
        return Response({'message': 'Request count reset successfully'}, status=status.HTTP_200_OK)

