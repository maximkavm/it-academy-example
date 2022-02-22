from django.urls import path

from users.views import login, registration, logout, email_verification

app_name = 'users'

urlpatterns = [
    path('login/', login, name='login'),
    path('registration/', registration, name='registration'),
    path('logout/', logout, name='logout'),
    path('verify/<str:email>/<uuid:code>/', email_verification, name='email_verification'),
]
