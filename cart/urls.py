from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.CartDetailView.as_view(), name='details'),
    path('add/<slug:slug>', views.AddToCartView.as_view(), name='add_to_cart'),
    path('update-item/<int:item_id>', views.UpdateCartItemView.as_view(), name='update_quantity'),
    path('delete-item/<int:item_id>', views.DeleteCartItemView.as_view(), name='delete_item'),
    path('clear/', views.ClearCartView.as_view(), name='clear'),
]
