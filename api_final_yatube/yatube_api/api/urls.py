from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import (
    PostViewSet,
    CommentViewSet,
    GroupViewSet,
    FollowViewSet
)

router = SimpleRouter()
router.register('posts', PostViewSet)
router.register('groups', GroupViewSet)
router.register('follow', FollowViewSet)
router.register(
    r'posts/(?P<post_id>\d+)/comments', CommentViewSet, basename='comments'
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
