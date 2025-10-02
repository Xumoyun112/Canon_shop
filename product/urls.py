from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name="product_list"),
    path("speskas/", views.speska_list, name="speska_list"),
    path("speskas/new/", views.speska_create, name="speska_create"),
    path("speskas/<int:speska_id>/", views.speska_detail, name="speska_detail"),
    path("sale/new/", views.sale_create, name="sale_create"),
    path("reports/", views.reports, name="reports"),
    path("products/add/", views.add_product, name="add_product"),
    path("products/<int:pk>/json/", views.product_detail_json, name="product_detail_json"),
    path("speska/<int:speska_id>/delete-sale/<int:sale_id>/", views.delete_sale, name="delete_sale"),
    path("speska/<int:speska_id>/finalize/", views.finalize_speska, name="finalize_speska"),
]
