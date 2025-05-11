from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework.authtoken.views import obtain_auth_token

from .views import \
    PostViewSet, CommentViewSet, GroupViewSet


router = SimpleRouter()
router.register('posts', PostViewSet)
router.register('groups', GroupViewSet)
router.register(
    r'posts/(?P<post_id>\d+)/comments', CommentViewSet, basename='comments'
)

urlpatterns = [
    path('api/v1/api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api/v1/', include(router.urls)),
]
