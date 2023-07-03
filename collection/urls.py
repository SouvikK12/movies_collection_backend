from django.urls import path
from .views import CollectionApiViewSet


urlpatterns = [
    path('', CollectionApiViewSet.as_view({'post' : 'create', 'get' : 'list'})),
    path('<uuid:id>/', CollectionApiViewSet.as_view({'get' : 'retrieve', 'put' : 'update', 'delete' : 'destroy'})),
]