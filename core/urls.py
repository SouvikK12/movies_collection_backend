from django.urls import include, path
from .views import MovieApiViewSet, UserApiViewset, RequestApiViewset


urlpatterns = [
    path('register/', UserApiViewset.as_view({'post' : 'post'})),
    path('movies/', MovieApiViewSet.as_view({'get' : 'list'})),
    path('request-count/', RequestApiViewset.as_view({'get' : 'get'})),
    path('request-count/reset/', RequestApiViewset.as_view({'post' : 'post'})),
    path('collection/', include('collection.urls')),
]
