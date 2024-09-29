
import os
import uuid
from django.conf import settings
from django.shortcuts import render
from .forms import ImageUploadForm
from PIL import Image

def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = request.FILES['image']
            img = Image.open(uploaded_image)

            # تولید نام فایل جدید
            base_filename = str(uuid.uuid4())
            png_image_path = f'uploads/{base_filename}.png'
            jpeg_image_path = f'uploads/{base_filename}.jpeg'

            # ایجاد دایرکتوری uploads اگر وجود ندارد
            uploads_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
            if not os.path.exists(uploads_dir):
                os.makedirs(uploads_dir)

            # ذخیره تصاویر به فرمت‌های مختلف
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