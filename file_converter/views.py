import os
import pypandoc
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse

from .forms import UploadFileForm

import io
import os
from django.http import HttpResponse
from django.shortcuts import render
from .forms import UploadFileForm
from docx import Document
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

from docx2pdf import convert


def convert_file(request):
    # Create temp directory if it doesn't exist
    temp_dir = 'temp'
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

            # Convert the file to PDF
            output_path = os.path.splitext(file_path)[0] + '.pdf'
            convert(file_path, output_path)

            # Check if conversion succeeded
            if os.path.exists(output_path):
                # به جای برگرداندن فایل، URL آن را برمی‌گردانیم
                file_url = request.build_absolute_uri(reverse('download_pdf', args=[os.path.basename(output_path)]))
                return JsonResponse({'file_url': file_url})

    else:
        form = UploadFileForm()

    return render(request, 'file_converter/file_converter.html', {'form': form})


def download_pdf(request, filename):
    file_path = os.path.join('temp', filename)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    return HttpResponse("File not found", status=404)
