import logging
import os
import uuid
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from reportlab.pdfgen import canvas

from .forms import ImageUploadForm, UploadFileForm
from PIL import Image


def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = request.FILES['image']
            img = Image.open(uploaded_image)

            base_filename = str(uuid.uuid4())
            png_image_path = f'uploads/{base_filename}.png'
            jpeg_image_path = f'uploads/{base_filename}.jpeg'

            uploads_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
            if not os.path.exists(uploads_dir):
                os.makedirs(uploads_dir)

            img.save(os.path.join(uploads_dir, f'{base_filename}.png'), 'PNG')
            img.convert('RGB').save(os.path.join(uploads_dir, f'{base_filename}.jpeg'), 'JPEG')

            return render(request, 'success.html', {
                'png_image_path': png_image_path,
                'jpeg_image_path': jpeg_image_path,
                'MEDIA_URL': settings.MEDIA_URL,
            })
    else:
        form = ImageUploadForm()
    return render(request, 'uploads.html', {'form': form})


# def jpg_to_pdf(request):
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             # دریافت فایل
#             jpg_file = request.FILES['file']
#             jpg_file_path = os.path.join('media', jpg_file.name)
#
#          # ذخیره فایل JPG
#             with open(jpg_file_path, 'wb+') as destination:
#                 for chunk in jpg_file.chunks():
#                     destination.write(chunk)
#
#                 # تبدیل به PDF
#             pdf_file_path = os.path.join('media', jpg_file.name.replace('.jpg', '.pdf'))
#             img = Image.open(jpg_file_path).convert('RGB')
#             img.save(pdf_file_path)
#
#             return HttpResponse(
#                 f'File uploaded and converted to PDF: <a href="/media/{jpg_file.name.replace(".jpg", ".pdf")}"> Download PDF </a>')
#     else:
#         form = UploadFileForm()
#     return render(request, 'image_converter/image_to_pdf.html', {'form': form})
def jpg_to_pdf(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # دریافت فایل
            jpg_file = request.FILES['file']
            jpg_file_path = os.path.join('media', jpg_file.name)

            # ذخیره فایل JPG
            with open(jpg_file_path, 'wb+') as destination:
                for chunk in jpg_file.chunks():
                    destination.write(chunk)

            # تبدیل به PDF
            pdf_file_path = os.path.join('media', jpg_file.name.replace('.jpg', '.pdf'))
            img = Image.open(jpg_file_path).convert('RGB')
            img.save(pdf_file_path)

            return HttpResponse(
                f'File uploaded and converted to PDF: <a href="/media/{jpg_file.name.replace(".jpg", ".pdf")}"> Download PDF </a>')
    else:
        form = UploadFileForm()
    return render(request, 'image_converter/image_to_pdf.html', {'form': form})

    # def jpg_to_pdf(request):
#     if request.method == 'POST':
#         if 'convert' in request.POST:
#             # Get the file
#             jpg_file = request.FILES['file']
#             jpg_file_path = os.path.join('media', jpg_file.name)
#
#             # Save the JPG file
#             with open(jpg_file_path, 'wb+') as destination:
#                 for chunk in jpg_file.chunks():
#                     destination.write(chunk)
#
#             # Convert to PDF
#             pdf_file_path = os.path.join('media', jpg_file.name.replace('.jpg', '.pdf'))
#             img = Image.open(jpg_file_path).convert('RGB')
#             img.save(pdf_file_path)
#
#             # Display conversion successful message and download link
#             convert_message = "Conversion successful!"
#             download_link = f'<a href="/media/{jpg_file.name.replace(".jpg", ".pdf")}">Download PDF file</a>'
#
#             return render(request, 'image_converter/image_to_pdf.html', {
#                 'form': UploadFileForm(),
#                 'file_selected': jpg_file.name,
#                 'convert_message': convert_message,
#                 'download_link': download_link
#             })
#         else:
#             form = UploadFileForm(request.POST, request.FILES)
#             if form.is_valid():
#                 return render(request, 'image_converter/image_to_pdf.html', {
#                     'form': form,
#                     'file_selected': request.FILES['file'].name
#                 })
#     else:
#         form = UploadFileForm()
#     return render(request, 'image_converter/image_to_pdf.html', {'form': form})