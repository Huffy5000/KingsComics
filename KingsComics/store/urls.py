from django.contrib import admin
from django.urls import path
from .views import StoreListView,ProductDetailView,AddToCart,ViewCart,RemoveItem

app_name = 'storeApp'

urlpatterns = [
    path('',StoreListView.as_view(),name = 'store-home'),
    path('comic/<int:pk>/',ProductDetailView.as_view(),name = 'store-detail'),
    path('comic/add_cart/<int:pk>/',AddToCart.as_view(),name = 'add-cart'),
    path('view_cart/',ViewCart.as_view(),name = 'view-cart'),
    path('remove_item/<int:pk>/',RemoveItem.as_view(),name = 'remove-item'),
    
]
