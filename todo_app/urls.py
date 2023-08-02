# todo_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.ListListView.as_view(), name="index"),
    path("list/<int:list_id>/", views.ItemListView.as_view(), name="list"),
    # url to add new list
    path("list/add/", views.ListCreate.as_view(), name="list-add"),
    # url to add new item in a list
    path("list/<int:list_id>/item/add/", views.ItemCreate.as_view(), name="item-add"),
    # url to edit an existing item
    path("list/<int:list_id>/item/<int:pk>/", views.ItemUpdate.as_view(), name="item-update"),
    path("list/<int:pk>/delete/", views.ListDelete.as_view(), name="list-delete"),
    path("list/<int:list_id>/item/<int:pk>/delete/", views.ItemDelete.as_view(), name="item-delete",
    )

]
