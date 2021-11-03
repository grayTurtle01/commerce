from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_product", views.add_product, name="add_product"),
    path("delete_product/<int:product_id>", views.delete_product, name="delete_product"),
    path("edit_product/<int:product_id>", views.edit_product, name="edit_product"),
    path("show_product/<int:product_id>", views.show_product, name="show_product"),
    path('add_book_watchlist/<int:product_id>', views.add_book_watchlist, name="add_book_watchlist"),
    path('change_price/<int:product_id>', views.change_price, name="change_price"),
    path('show_profile/<str:creator>', views.show_profile, name="show_profile"),
    path('close_bid/<int:product_id>', views.close_bid, name="close_bid"),
    path('show_watchlist/', views.show_watchlist, name="show_watchlist"),
    path('add_comment/<int:product_id>', views.add_comment, name="add_comment"),

    path("upload_file", views.upload_file, name="upload_file"),

]
