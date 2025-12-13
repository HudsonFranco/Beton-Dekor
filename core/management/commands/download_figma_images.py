"""
Comando Django para baixar imagens do Figma.

Uso:
    python manage.py download_figma_images bGtm8mc5RnpGntMspMA70K
    
    ou com diretório customizado:
    python manage.py download_figma_images bGtm8mc5RnpGntMspMA70K --output-dir static/images
"""

from django.core.management.base import BaseCommand
from utils.figma_images import FigmaImageDownloader


class Command(BaseCommand):
    help = 'Baixa todas as imagens de um arquivo Figma'

    def add_arguments(self, parser):
        parser.add_argument(
            'file_key',
            type=str,
            help='Chave do arquivo Figma (FILE_KEY)'
        )
        parser.add_argument(
            '--output-dir',
            type=str,
            default=None,
            help='Diretório onde salvar as imagens (padrão: figma_images/)'
        )

    def handle(self, *args, **options):
        file_key = options['file_key']
        output_dir = options.get('output_dir')
        
        self.stdout.write(self.style.SUCCESS(f'Iniciando download de imagens do Figma...'))
        self.stdout.write(f'FILE_KEY: {file_key}')
        
        try:
            downloader = FigmaImageDownloader(file_key, output_dir)
            result = downloader.download_all_images()
            
            self.stdout.write(self.style.SUCCESS(
                f'\n✓ Download concluído! '
                f'{result["downloaded"]}/{result["total"]} imagens baixadas.'
            ))
            
            if result['failed'] > 0:
                self.stdout.write(self.style.WARNING(
                    f'⚠ {result["failed"]} imagens falharam ao baixar.'
                ))
                
        except ValueError as e:
            self.stdout.write(self.style.ERROR(f'Erro: {str(e)}'))
            self.stdout.write(
                'Configure a variável de ambiente FIGMA_TOKEN:\n'
                '  Windows: set FIGMA_TOKEN=seu_token\n'
                '  Linux/Mac: export FIGMA_TOKEN=seu_token'
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao baixar imagens: {str(e)}'))

