from django.urls import path
from . import views
urlpatterns=[
    path('',views.home,name='home'),
    path('login',views.login_app,name='login_account'),
    path('signup',views.Register,name='signup'),
    path('token',views.token_send,name='token_send'),
    path('verify/<tkn>',views.verify,name='verify'),
    path('error',views.error_page,name='error_page'),
    path('success',views.success,name='success'),
    path('main',views.main,name='main')

]