import logging
import os
import uuid
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from reportlab.pdfgen import canvas

from .forms import ImageUploadForm
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


def image_to_pdf(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_file = request.FILES['image']
            return convert_jpg_to_pdf(image_file)
    else:
        form = ImageUploadForm()
    return render(request, 'file_converter/image_to_pdf.html', {'form': form})


def convert_jpg_to_pdf(image_file):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="converted.pdf"'

    pdf_canvas = canvas.Canvas(response)

    image = Image.open(image_file)
    image_path = 'temp_image.jpg'
    image.save(image_path)

    pdf_canvas.drawImage(image_path, 0, 0, width=image.width, height=image.height)
    pdf_canvas.showPage()
    pdf_canvas.save()

    os.remove(image_path)

    return response



def convert_jpg_to_pdf(image):
    # Create a unique filename for the PDF
    filename = f"{uuid.uuid4()}.pdf"
    output_path = os.path.join(settings.MEDIA_ROOT, 'pdfs', filename)

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Open the image using Pillow
    with Image.open(image) as img:
        # Convert image to RGB (removes alpha channel if present)
        rgb_im = img.convert('RGB')
        # Save the image as PDF
        rgb_im.save(output_path, 'PDF', resolution=100.0)

    # Return the relative path
    return os.path.join('pdfs', filename)


logger = logging.getLogger(__name__)

@csrf_exempt
def convert_jpg_to_pdf_view(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        try:
            pdf_path = convert_jpg_to_pdf(image)
            pdf_url = request.build_absolute_uri(settings.MEDIA_URL + pdf_path)
            return JsonResponse({'success': True, 'pdf_url': pdf_url})
        except Exception as e:
            logger.error(f"Error converting image to PDF: {str(e)}", exc_info=True)
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'No file uploaded'})