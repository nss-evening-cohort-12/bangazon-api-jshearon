from django.urls import path
from .views import products_over_1000, products_under_1000, favorited_sellers

urlpatterns = [
    path('reports/expensiveproducts', products_over_1000),
    path('reports/inexpensiveproducts', products_under_1000),
    path('reports/favoritesellers', favorited_sellers),
]
