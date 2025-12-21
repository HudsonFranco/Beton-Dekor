import json
import os
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from core.models import Produto, CategoriaPrincipal, Subcategoria


class Command(BaseCommand):
    help = 'Import products from JSON backup file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            default='produtos_backup.json',
            help='Path to the JSON backup file'
        )

    def handle(self, *args, **options):
        file_path = options['file']

        if not os.path.exists(file_path):
            self.stdout.write(
                self.style.ERROR(f'File {file_path} does not exist')
            )
            return

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        imported_count = 0
        skipped_count = 0

        for item in data:
            if item['model'] == 'core.produto':
                fields = item['fields']

                # Check if product already exists
                if Produto.objects.filter(slug=fields.get('slug')).exists():
                    self.stdout.write(
                        self.style.WARNING(f"Product {fields['nome']} already exists, skipping")
                    )
                    skipped_count += 1
                    continue

                try:
                    # Get or create related objects
                    categoria_principal = None
                    if fields.get('categoria_principal'):
                        categoria_principal, _ = CategoriaPrincipal.objects.get_or_create(
                            nome=fields['categoria_principal']
                        )

                    subcategoria = None
                    if fields.get('categoria'):
                        subcategoria, _ = Subcategoria.objects.get_or_create(
                            nome=fields['categoria']
                        )

                    # Create product
                    produto = Produto.objects.create(
                        nome=fields['nome'],
                        slug=fields['slug'],
                        tag=fields.get('tag', ''),
                        categoria_principal=categoria_principal,
                        categoria=subcategoria,
                        cor=fields.get('cor'),
                        unidade_venda=fields.get('unidade_venda'),
                        dimensoes=fields.get('dimensoes'),
                        especificacoes=fields.get('especificacoes'),
                        descricao=fields.get('descricao', ''),
                    )

                    # Handle images (if they exist in media folder)
                    # Note: Images need to be manually uploaded to Render's media folder
                    # or copied from local media folder

                    self.stdout.write(
                        self.style.SUCCESS(f"Imported product: {produto.nome}")
                    )
                    imported_count += 1

                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f"Error importing {fields['nome']}: {str(e)}")
                    )
                    continue

        self.stdout.write(
            self.style.SUCCESS(
                f"Import completed: {imported_count} imported, {skipped_count} skipped"
            )
        )

        if imported_count > 0:
            self.stdout.write(
                self.style.WARNING(
                    "Note: Images need to be manually uploaded to the media folder"
                )
            )