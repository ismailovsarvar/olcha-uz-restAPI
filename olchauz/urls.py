from django.urls import path
from olchauz.views import category, group, product

urlpatterns = [
    # Category URL
    path('category/', category.CategoryListCreateApiView.as_view(), name='category-list'),
    path('category/<slug:slug>/detail/', category.CategoryDetailGenericApiView.as_view(), name='category-detail'),

    # Group URL
    path('group/', group.GroupCreateApiView.as_view(), name='group-list'),
    path('group/<slug:slug>/detail/', group.GroupDetailApiView.as_view(), name='group-detail'),

    # Product URL
    path('product/', product.ProductCreateApiView.as_view(), name='product-list'),
    path('product/<slug:slug>/detail/', product.ProductDetailApiView.as_view(), name='product-detail'),

    # Product Attribute URL
    path('product-attribute/', product.ProductAttributeCreateApiView.as_view()),
    path('product-attribute/<slug:slug>/detail/', product.ProductAttributeDetailApiView.as_view()),
]
