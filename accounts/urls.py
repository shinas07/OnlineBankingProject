from django.urls import path
from . import views


app_name = 'accounts'
urlpatterns = [
    path('login/',views.user_login,name='login'),
    path('register/',views.register_user,name='register'),
    path('logout/',views.logout_veiw,name='logout'),


]