from django.urls import path
from .views import *
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', PostListView.as_view(), name='news'),
    path('<int:pk>', PostDetailView.as_view(), name='post'),
    path('search/', PostSearchView.as_view(), name='post_search'),
    path('add/', PostAddView.as_view(), name='post_add'),
    path('<int:pk>/edit', PostUpdateView.as_view(), name='post_edit'),
    path('<int:pk>/delete', PostDeleteView.as_view(), name='post_delete'),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('categories/', CategoriesListView.as_view(), name='categories_list'),
    path('categories/<int:pk>', cache_page(60*5)(PostsCategoryListView.as_view()), name='posts_category'),
    path('subscribe/', subscribe, name='subscribe'),
    path('like/', like, name='like'),
    path('dislike/', dislike, name='dislike'),
]