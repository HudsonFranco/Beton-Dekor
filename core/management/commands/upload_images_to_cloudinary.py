import os
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from core.models import Produto
import cloudinary.uploader


class Command(BaseCommand):
    help = 'Upload product images to Cloudinary and update model fields'

    def handle(self, *args, **options):
        produtos = Produto.objects.all()
        updated_count = 0

        for produto in produtos:
            self.stdout.write(f'Processing {produto.nome}...')

            # Upload imagem
            if produto.imagem and hasattr(produto.imagem, 'path') and os.path.exists(produto.imagem.path):
                try:
                    # Upload to Cloudinary
                    result = cloudinary.uploader.upload(produto.imagem.path)
                    produto.imagem = result['public_id'] + '.' + result['format']
                    self.stdout.write(f'  Uploaded imagem: {result["url"]}')
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'  Error uploading imagem: {e}'))

            # Upload imagem_2
            if produto.imagem_2 and hasattr(produto.imagem_2, 'path') and os.path.exists(produto.imagem_2.path):
                try:
                    result = cloudinary.uploader.upload(produto.imagem_2.path)
                    produto.imagem_2 = result['public_id'] + '.' + result['format']
                    self.stdout.write(f'  Uploaded imagem_2: {result["url"]}')
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'  Error uploading imagem_2: {e}'))

            # Upload imagem_3
            if produto.imagem_3 and hasattr(produto.imagem_3, 'path') and os.path.exists(produto.imagem_3.path):
                try:
                    result = cloudinary.uploader.upload(produto.imagem_3.path)
                    produto.imagem_3 = result['public_id'] + '.' + result['format']
                    self.stdout.write(f'  Uploaded imagem_3: {result["url"]}')
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'  Error uploading imagem_3: {e}'))

            if produto.imagem or produto.imagem_2 or produto.imagem_3:
                produto.save()
                updated_count += 1

        self.stdout.write(self.style.SUCCESS(f'Updated {updated_count} products'))