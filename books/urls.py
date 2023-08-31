from django.urls import path
from .views import BookListView, BookDetailView, ReviewView, LikeView, SaveView

urlpatterns = [
    path('', BookListView.as_view(), name='list'),
    path('<int:pk>', BookDetailView.as_view(), name='detail'),
    path('<int:pk>/review/', ReviewView.as_view(), name='review'),
    path('like/', LikeView.as_view(), name='like'),
    path('save/', SaveView.as_view(), name='save'),
]