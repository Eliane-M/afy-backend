from django.urls import path
from api.views.auth.login import login_api
from api.views.auth.logout import logout_api
from api.views.auth.register import new_user
from api.views.auth.reset import password_reset_request, password_reset_confirm

urlpatterns = [
    path('login/', login_api, name='login_api'),
    path('logout/', logout_api, name='logout_api'),
    path('register/', new_user, name='new_user'),
    path('password_reset/', password_reset_request, name='password_reset'),
    path('reset_confirm/', password_reset_confirm, name='password_reset_confirm'),
]