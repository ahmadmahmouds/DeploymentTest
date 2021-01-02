from django.urls import path
from . import views
urlpatterns=[
    path('',views.index),
    path('register',views.register),
    path('logout',views.logout),
    path('login',views.login),
    path('show_register_form',views.showRegisterForm),
    path("show_login_form",views.showLoginForm),
    path('validateEmailByAjax',views.validateEmailByAjax,name="validateEmailByAjax"),
    path('validateFirstNameByAjax',views.validateFirstNameByAjax,name="validateFirstNameByAjax"),
    path('validateLastNameByAjax',views.validateLastNameByAjax,name="validateLastNameByAjax"),
    path('validatePasswordByAjax',views.validatePasswordByAjax,name="validatePasswordByAjax"),
    path('show_all_book',views.showAllBook),
    path('add_book',views.addBook),
    path('show_form/<int:id>',views.show),
    path('show_form/add_to_favorite/<int:id>',views.addFavorite),
    path('show_form/un_favorite/<int:id>',views.unfavorite),
    path('editForm/<int:id>',views.editForm),
    

]