from django.urls import path
from .views import products_over_1000, products_under_1000, favorited_sellers, incomplete_orders, completed_orders

urlpatterns = [
    path('reports/expensiveproducts', products_over_1000),
    path('reports/inexpensiveproducts', products_under_1000),
    path('reports/favoritesellers', favorited_sellers),
    path('reports/incompleteorders', incomplete_orders),
    path('reports/completedorders', completed_orders),
]
