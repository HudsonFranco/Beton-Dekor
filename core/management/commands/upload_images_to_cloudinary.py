import os
from django.core.management.base import BaseCommand
from core.models import Produto
from cloudinary import uploader

class Command(BaseCommand):
    help = 'Upload existing product images to Cloudinary'

    def handle(self, *args, **options):
        produtos = Produto.objects.all()
        for produto in produtos:
            self.stdout.write(f"Processing {produto.nome}")
            # Upload imagem
            if produto.imagem and hasattr(produto.imagem, 'path'):
                try:
                    with open(produto.imagem.path, 'rb') as f:
                        result = uploader.upload(f, folder='produtos/')
                        produto.imagem = result['public_id']
                        produto.save()
                        self.stdout.write(f"Uploaded imagem for {produto.nome}")
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error uploading imagem for {produto.nome}: {e}"))
            # imagem_2
            if produto.imagem_2 and hasattr(produto.imagem_2, 'path'):
                try:
                    with open(produto.imagem_2.path, 'rb') as f:
                        result = uploader.upload(f, folder='produtos/')
                        produto.imagem_2 = result['public_id']
                        produto.save()
                        self.stdout.write(f"Uploaded imagem_2 for {produto.nome}")
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error uploading imagem_2 for {produto.nome}: {e}"))
            # imagem_3
            if produto.imagem_3 and hasattr(produto.imagem_3, 'path'):
                try:
                    with open(produto.imagem_3.path, 'rb') as f:
                        result = uploader.upload(f, folder='produtos/')
                        produto.imagem_3 = result['public_id']
                        produto.save()
                        self.stdout.write(f"Uploaded imagem_3 for {produto.nome}")
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error uploading imagem_3 for {produto.nome}: {e}"))
        self.stdout.write(self.style.SUCCESS("Upload completed"))