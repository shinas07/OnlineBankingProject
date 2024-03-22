from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',views.home,name='home'),
    path('new-page/',views.new_page,name='new_page'),
    path('show_form/', views.show_form, name='show_form'),

    path('form_view/', views.form_view, name='form_view'),
    path('get_branches/', views.get_branches, name='get_branches'),

    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    