import os
import threading
import time

import pandas as pd
import pypandoc
import pythoncom
import win32com
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
import comtypes.client
from django.views.static import serve
from pptx import Presentation
import logging

from django.http import HttpResponse

from django.conf import settings

import tempfile

from django.views.decorators.csrf import csrf_exempt
from docx2pdf import convert

import os
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from .forms import UploadFileForm

import os
from django.shortcuts import render
from django.conf import settings
import subprocess

# def convert_file(request):
#     # Create temp directory if it doesn't exist
#     temp_dir = 'temp'
#     if not os.path.exists(temp_dir):
#         os.makedirs(temp_dir)
#
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             # Get the uploaded file
#             document = request.FILES['file']
#             file_path = os.path.join(temp_dir, document.name)
#
#             # Save the uploaded file
#             with open(file_path, 'wb+') as destination:
#                 for chunk in document.chunks():
#                     destination.write(chunk)
#
#             # Initialize COM
#             pythoncom.CoInitialize()
#             try:
#                 # Convert the file to PDF
#                 output_path = os.path.splitext(file_path)[0] + '.pdf'
#                 convert(file_path, output_path)
#
#                 # Check if conversion succeeded
#                 if os.path.exists(output_path):
#                     # به جای برگرداندن فایل، URL آن را برمی‌گردانیم
#                     file_url = request.build_absolute_uri(reverse('download_pdf', args=[os.path.basename(output_path)]))
#                     return JsonResponse({'file_url': file_url})
#             finally:
#                 # Uninitialize COM
#                 pythoncom.CoUninitialize()
#
#     else:
#         form = UploadFileForm()
#
#     return render(request, 'file_converter/file_converter.html', {'form': form})
#
#
# def download_pdf(request, filename):
#     file_path = os.path.join('temp', filename)
#     if os.path.exists(file_path):
#         with open(file_path, 'rb') as pdf_file:
#             response = HttpResponse(pdf_file.read(), content_type='application/pdf')
#             response['Content-Disposition'] = f'attachment; filename="{filename}"'
#         return response
#     return HttpResponse("File not found", status=404)
def convert_file(request):
    # Create temp directory if it doesn't exist
    temp_dir = os.path.join('temp')  # Adjust this if needed
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Get the uploaded file
            document = request.FILES['file']
            file_path = os.path.join(temp_dir, document.name)

            # Save the uploaded file
            with open(file_path, 'wb+') as destination:
                for chunk in document.chunks():
                    destination.write(chunk)

            # Initialize COM
            pythoncom.CoInitialize()
            try:
                # Convert the file to PDF
                output_path = os.path.splitext(file_path)[0] + '.pdf'
                convert(file_path, output_path)

                # Check if conversion succeeded
                if os.path.exists(output_path):
                    # Return the URL for downloading the PDF
                    file_url = request.build_absolute_uri(reverse('download_pdf', args=[os.path.basename(output_path)]))
                    return JsonResponse({'file_url': file_url})
            finally:
                # Uninitialize COM
                pythoncom.CoUninitialize()

    else:
        form = UploadFileForm()

    return render(request, 'file_converter/file_converter.html', {'form': form})

def download_pdf(request, filename):
    file_path = os.path.join('temp', filename)  # Ensure the 'temp' directory is correct
    if os.path.exists(file_path):
        with open(file_path, 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    return HttpResponse("File not found", status=404)

def ppt_to_pdf(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            ppt_file = request.FILES['file']
            ppt_file_path = os.path.join(settings.MEDIA_ROOT, ppt_file.name)

            # Save the uploaded PPT file
            with open(ppt_file_path, 'wb+') as destination:
                for chunk in ppt_file.chunks():
                    destination.write(chunk)

            # Path for the output PDF file
            pdf_file_path = ppt_file_path.replace('.pptx', '.pdf')

            # Create a PDF
            c = canvas.Canvas(pdf_file_path, pagesize=letter)
            presentation = Presentation(ppt_file_path)

            # Add slides to the PDF
            for slide in presentation.slides:
                # Draw the title, if it exists
                title = slide.shapes.title.text if slide.shapes.title else "No Title"
                c.drawString(100, 750, title)

                # You can add more slide content here, such as text boxes, images, etc.

                c.showPage()  # Create a new page for each slide

            c.save()

            # Create download link
            pdf_file_url = os.path.basename(pdf_file_path)  # Get only the file name
            return render(request, 'file_converter/success.html', {'pdf_file_url': pdf_file_url})

    else:
        form = UploadFileForm()
    return render(request, 'file_converter/ppt_to_pdf.html', {'form': form})


def download_ppt_to_pdf_file(request, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, filename)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
    else:
        return HttpResponse("File not found.", status=404)


def x_to_pdf(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            df = pd.read_excel(file)

            # Create a temporary PDF file
            pdf_file_path = os.path.join(settings.MEDIA_ROOT, 'output.pdf')

            # Create PDF
            p = canvas.Canvas(pdf_file_path, pagesize=letter)
            text = df.to_string(index=False)
            p.drawString(100, 750, text)
            p.showPage()
            p.save()

            # Return response with link to download
            download_url = f'{settings.MEDIA_URL}output.pdf'  # Ensure you have your MEDIA_URL set up
            return JsonResponse({'success': True, 'download_url': download_url})

    else:
        form = UploadFileForm()
    return render(request, 'file_converter/x_to_pdf.html', {'form': form})
# def x_to_pdf(request):
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             file = request.FILES['file']
#             df = pd.read_excel(file)
#
#             # ایجاد PDF
#             response = HttpResponse(content_type='application/pdf')
#             response['Content-Disposition'] = 'attachment; filename="output.pdf"'
#             p = canvas.Canvas(response, pagesize=letter)
#
#             # افزودن محتوای DataFrame به PDF
#             text = df.to_string(index=False)
#             p.drawString(100, 750, text)
#             p.showPage()
#             p.save()
#             return response
#     else:
#         form = UploadFileForm()
#     return render(request, 'file_converter/x_to_pdf.html', {'form': form})