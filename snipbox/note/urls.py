from django.urls import path

from . import views
urlpatterns = [
    path('snippet/', views.SnippetViewSet.as_view(), name='snippet-list'),
    path('snippet/<int:pk>/', views.SnippetViewSet.as_view(), name='snippet-detail'),
    path('snippet/overview/', views.SnippetOverViewSet.as_view(), name='snippet-overview'),
    path('tags/', views.TagViewSet.as_view(), name='tag-list'),
    path('tags/<int:pk>/snippets/', views.TagViewSet.as_view(), name='snippets-by-tag'),
]
