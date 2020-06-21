from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("register", views.register, name='register'),
    path("signin", views.signin, name='signin'),
    path("signout", views.signout, name='signout'),
    path("carts", views.carts, name='carts'),
    path("<int:item_id>/delete", views.delete, name="delete"),
    path("<int:item_id>/menus", views.menus, name="menus"),
    path("payments", views.payments, name="payments"),

]
