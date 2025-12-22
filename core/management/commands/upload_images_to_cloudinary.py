import os
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.conf import settings
from core.models import Produto
import cloudinary.uploader


class Command(BaseCommand):
    help = 'Upload product images to Cloudinary and update model fields'

    def handle(self, *args, **options):
        # Ensure Cloudinary is configured
        if not hasattr(settings, 'CLOUDINARY_STORAGE') and 'cloudinary' not in str(settings.DEFAULT_FILE_STORAGE):
            self.stdout.write(self.style.WARNING('Cloudinary not configured as default storage. Using direct upload.'))

        produtos = Produto.objects.all()
        updated_count = 0

        for produto in produtos:
            self.stdout.write(f'Processing {produto.nome}...')

            # Upload imagem
            if produto.imagem:
                image_path = None
                if hasattr(produto.imagem, 'path') and os.path.exists(produto.imagem.path):
                    image_path = produto.imagem.path
                elif isinstance(produto.imagem, str) and produto.imagem.startswith('produtos/'):
                    # If it's a string path, construct full path
                    image_path = os.path.join(settings.MEDIA_ROOT, produto.imagem)

                if image_path and os.path.exists(image_path):
                    try:
                        # Upload to Cloudinary
                        result = cloudinary.uploader.upload(image_path)
                        produto.imagem = result['public_id']
                        self.stdout.write(f'  Uploaded imagem: {result["url"]}')
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'  Error uploading imagem: {e}'))
                else:
                    self.stdout.write(f'  Image file not found for imagem: {produto.imagem}')

            # Upload imagem_2
            if produto.imagem_2:
                image_path = None
                if hasattr(produto.imagem_2, 'path') and os.path.exists(produto.imagem_2.path):
                    image_path = produto.imagem_2.path
                elif isinstance(produto.imagem_2, str) and produto.imagem_2.startswith('produtos/'):
                    image_path = os.path.join(settings.MEDIA_ROOT, produto.imagem_2)

                if image_path and os.path.exists(image_path):
                    try:
                        result = cloudinary.uploader.upload(image_path)
                        produto.imagem_2 = result['public_id']
                        self.stdout.write(f'  Uploaded imagem_2: {result["url"]}')
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'  Error uploading imagem_2: {e}'))
                else:
                    self.stdout.write(f'  Image file not found for imagem_2: {produto.imagem_2}')

            # Upload imagem_3
            if produto.imagem_3:
                image_path = None
                if hasattr(produto.imagem_3, 'path') and os.path.exists(produto.imagem_3.path):
                    image_path = produto.imagem_3.path
                elif isinstance(produto.imagem_3, str) and produto.imagem_3.startswith('produtos/'):
                    image_path = os.path.join(settings.MEDIA_ROOT, produto.imagem_3)

                if image_path and os.path.exists(image_path):
                    try:
                        result = cloudinary.uploader.upload(image_path)
                        produto.imagem_3 = result['public_id']
                        self.stdout.write(f'  Uploaded imagem_3: {result["url"]}')
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'  Error uploading imagem_3: {e}'))
                else:
                    self.stdout.write(f'  Image file not found for imagem_3: {produto.imagem_3}')

            if produto.imagem or produto.imagem_2 or produto.imagem_3:
                produto.save()
                updated_count += 1

        self.stdout.write(self.style.SUCCESS(f'Updated {updated_count} products'))