import os
from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import Produto
import cloudinary.uploader

class Command(BaseCommand):
    help = 'Migrate existing static images to Cloudinary and update product fields'

    def handle(self, *args, **options):
        produtos = Produto.objects.exclude(imagem_nome='')

        for produto in produtos:
            imagem_nome = produto.imagem_nome.strip()
            if not imagem_nome:
                continue

            # Clean the filename like in the model
            if imagem_nome.startswith('http'):
                continue  # Skip URLs
            elif imagem_nome.startswith(settings.STATIC_URL):
                imagem_nome = imagem_nome.replace(settings.STATIC_URL, '').lstrip('/')
            elif imagem_nome.startswith('static/'):
                imagem_nome = imagem_nome.replace('static/', '', 1)
            if imagem_nome.startswith('images/'):
                imagem_nome = imagem_nome.replace('images/', '', 1)

            file_path = os.path.join(settings.BASE_DIR, 'static', 'images', imagem_nome)
            if not os.path.exists(file_path):
                self.stdout.write(self.style.WARNING(f"File {file_path} not found for {produto.nome}"))
                continue

            try:
                result = cloudinary.uploader.upload(file_path, folder='produtos/')
                produto.imagem = result['public_id']
                produto.imagem_nome = ''
                produto.save()
                self.stdout.write(self.style.SUCCESS(f"Migrated image for {produto.nome}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error migrating {produto.nome}: {e}"))

        self.stdout.write(self.style.SUCCESS("Migration completed"))