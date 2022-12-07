from django.urls import path
from . import views


urlpatterns = [
    path('', views.StartingPage.as_view(), name='starting_page'),
    path('posts', views.AllPosts.as_view(), name='posts-page'),
    path('posts/<slug:slug>', views.PostDetail.as_view(), name='post_detail_page'),
    path('read-later', views.ReadLaterView.as_view(), name="read-later"),
]