from django.urls import path 
from .views import home  , userlogin , ask_bot , ask_website

urlpatterns = [
    path('',userlogin ,name = 'userlogin'),
    path('chat/',ask_bot ,name = 'chat'),
    path('home/', home ,name = 'home'),
    path('ask/', ask_website, name='ask'),

    
]