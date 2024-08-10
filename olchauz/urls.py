
from django.urls import path
from olchauz import views

urlpatterns = [
    # Category URL
    path('category/', views.CategoryListApiView.as_view(), name='category-list'),
    path('category/<slug:slug>/detail/', views.CategoryDetailApiView.as_view(), name='category-detail'),
]
