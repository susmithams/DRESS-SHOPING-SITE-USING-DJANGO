from django.urls import path
from .views import *
urlpatterns=[
    path('index/',index),
    path('sellerreg/',register_seller),
    path('login/',login_view),
    path('profile/',profile_view),
path('sellerproductupload/',sellerproductupload),
    path('delete/<int:cartid>',deleteitem),
    path('edit/<int:cartid>',edititem),
]