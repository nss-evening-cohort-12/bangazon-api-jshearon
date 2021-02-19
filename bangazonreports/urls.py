from django.urls import path
from .views import products_over_1000, products_under_1000, completed_orders

urlpatterns = [
    path('reports/expensiveproducts', products_over_1000),
    path('reports/inexpensiveproducts', products_under_1000),
    path('reports/completedorders', completed_orders),
]
