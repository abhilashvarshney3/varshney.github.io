from post.views import index, NewPost, PostDetails, tags, search, like, favorite, deletepost
from django.urls import path

urlpatterns = [
    path('', index, name='index'),
    path('newpost/', NewPost, name='newpost'),
    path('<uuid:post_id>', PostDetails, name='postdetails'),
    path('<uuid:post_id>/like', like, name='postlike'),
    path('<uuid:post_id>/favorite', favorite, name='postfavorite'),
    path('<uuid:post_id>/deletepost', deletepost, name='deletepost'),
    path('tags/<slug:tag_slug>', tags, name='tags'),
    path('search/', search, name='search'),
    
    
]