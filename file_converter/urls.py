from django.urls import path
from . import views


urlpatterns = [
    path('word-to-pdf/', views.convert_file, name='file_converter'),
    path('download/<str:filename>/', views.download_pdf, name='download_pdf'),
]