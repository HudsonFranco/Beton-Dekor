from django.core.management.base import BaseCommand
from core.models import CategoriaPrincipal, Subcategoria

class Command(BaseCommand):
    help = 'Popula o banco de dados com as categorias iniciais'

    def handle(self, *args, **options):
        # Definir categorias e subcategorias
        categorias_data = [
            {
                'nome': 'Revestimento 3D cimentício',
                'ordem': 1,
                'subcategorias': [
                    {'nome': 'Amadeirados', 'ordem': 1},
                    {'nome': 'Brick´s/Tijolinho', 'ordem': 2},
                    {'nome': 'Clássicos', 'ordem': 3},
                    {'nome': 'Geométricos', 'ordem': 4},
                    {'nome': 'Mosaicos', 'ordem': 5},
                ]
            },
            {
                'nome': 'Artefatos Cimentícios',
                'ordem': 2,
                'subcategorias': [
                    {'nome': 'Lajota Piso', 'ordem': 1},
                    {'nome': 'Pingadeira', 'ordem': 2},
                ]
            },
            {
                'nome': 'Cube Concreto',
                'ordem': 3,
                'subcategorias': [
                    {'nome': 'Cuba redonda', 'ordem': 1},
                    {'nome': 'Cuba quadrada', 'ordem': 2},
                ]
            },
            {
                'nome': 'Linha Jardim',
                'ordem': 4,
                'subcategorias': [
                    {'nome': 'Pisante', 'ordem': 1},
                    {'nome': 'Guia jardim', 'ordem': 2},
                    {'nome': 'Concregrama', 'ordem': 3},
                ]
            },
            {
                'nome': 'Elemento Vazado Cobogó',
                'ordem': 5,
                'subcategorias': [
                    {'nome': 'Cobogó 40x40', 'ordem': 1},
                    {'nome': 'Cobogó 30x30', 'ordem': 2},
                    {'nome': 'Cobogó Dupla face 30x30', 'ordem': 3},
                ]
            },
        ]

        # Criar categorias e subcategorias
        for cat_data in categorias_data:
            categoria, created = CategoriaPrincipal.objects.get_or_create(
                nome=cat_data['nome'],
                defaults={'ordem': cat_data['ordem'], 'ativo': True}
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Categoria criada: {categoria.nome}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Categoria já existe: {categoria.nome}')
                )
            
            # Criar subcategorias
            for sub_data in cat_data['subcategorias']:
                subcategoria, sub_created = Subcategoria.objects.get_or_create(
                    categoria_principal=categoria,
                    nome=sub_data['nome'],
                    defaults={'ordem': sub_data['ordem'], 'ativo': True}
                )
                
                if sub_created:
                    self.stdout.write(
                        self.style.SUCCESS(f'  - Subcategoria criada: {subcategoria.nome}')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'  - Subcategoria já existe: {subcategoria.nome}')
                    )
        
        self.stdout.write(
            self.style.SUCCESS('\nCategorias populadas com sucesso!')
        )

