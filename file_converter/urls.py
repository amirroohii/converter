import os

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.static import serve

from . import views


urlpatterns = [
    path('word-to-pdf/', views.convert_file, name='word_to_pdf'),
    path('powerpoint-to-pdf/', views.ppt_to_pdf, name='ppt_to_pdf'),
    path('excel-to-pdf/', views.x_to_pdf, name='x_to_pdf'),
    path('download_pdf/<str:filename>/', views.download_pdf, name='download_pdf'),
    path('download/<str:filename>/', views.download_ppt_to_pdf_file, name='download_ppt_to_pdf_file'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
