from django.urls import include, path
from rest_framework.routers import SimpleRouter

from postlist import views

app_name = 'postlist'
post_list_api_router = SimpleRouter()
post_list_api_router.register(
    'posts',
    views.PostAPIViewSet,
    basename='postlist-api',
)

urlpatterns = [
    path('', include(post_list_api_router.urls)),
]
