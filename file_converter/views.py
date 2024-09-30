import os
import pypandoc
from django.shortcuts import render
from django.http import HttpResponse
from .forms import UploadFileForm

import io
import os
from django.http import HttpResponse
from django.shortcuts import render
from .forms import UploadFileForm
from docx import Document
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


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
            convert_docx_to_pdf(file_path, output_path)

            # Check if conversion succeeded
            if os.path.exists(output_path):
                with open(output_path, 'rb') as pdf_file:
                    response = HttpResponse(pdf_file.read(), content_type='application/pdf')
                    response['Content-Disposition'] = f'attachment; filename="{os.path.basename(output_path)}"'

                # Cleanup the temporary files
                os.remove(file_path)
                os.remove(output_path)
                return response

    else:
        form = UploadFileForm()

    return render(request, 'file_converter/file_converter.html', {'form': form})


def convert_docx_to_pdf(docx_path, pdf_path):
    doc = Document(docx_path)

    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)

    for paragraph in doc.paragraphs:
        can.drawString(50, 700, paragraph.text)
        can.showPage()

    can.save()

    packet.seek(0)
    with open(pdf_path, 'wb') as f:
        f.write(packet.read())