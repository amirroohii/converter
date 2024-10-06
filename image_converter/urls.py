from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_image, name='upload_image'),
    path('jpg-to-pdf/', views.jpg_to_pdf, name='jpg-to-pdf')

]