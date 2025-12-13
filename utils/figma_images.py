"""
Módulo para baixar imagens do Figma via API.

Uso:
    from utils.figma_images import FigmaImageDownloader
    
    downloader = FigmaImageDownloader(file_key="bGtm8mc5RnpGntMspMA70K")
    downloader.download_all_images()
"""

import os
import requests
import json
import time
from pathlib import Path
from typing import List, Dict, Set
from django.conf import settings


class FigmaImageDownloader:
    """Classe para baixar imagens do Figma via API."""
    
    BASE_URL = "https://api.figma.com/v1"
    
    def __init__(self, file_key: str, output_dir: str = None):
        """
        Inicializa o downloader.
        
        Args:
            file_key: Chave do arquivo Figma
            output_dir: Diretório onde salvar as imagens (padrão: figma_images/)
        """
        self.file_key = file_key
        self.token = os.environ.get('FIGMA_TOKEN')
        
        if not self.token:
            raise ValueError(
                "FIGMA_TOKEN não encontrado nas variáveis de ambiente. "
                "Configure: export FIGMA_TOKEN='seu_token'"
            )
        
        # Definir diretório de saída
        if output_dir:
            self.output_dir = Path(output_dir)
        else:
            # Usar diretório base do projeto Django
            base_dir = Path(settings.BASE_DIR) if hasattr(settings, 'BASE_DIR') else Path.cwd()
            self.output_dir = base_dir / "figma_images"
        
        # Criar diretório se não existir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.headers = {
            "X-Figma-Token": self.token
        }
    
    def get_file_data(self) -> Dict:
        """
        Busca os dados do arquivo Figma.
        
        Returns:
            Dicionário com os dados do arquivo
        """
        url = f"{self.BASE_URL}/files/{self.file_key}"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erro ao buscar dados do arquivo Figma: {str(e)}")
    
    def find_image_nodes(self, node: Dict, image_nodes: List[Dict] = None) -> List[Dict]:
        """
        Percorre recursivamente a árvore de nós e encontra nós com imagens.
        
        Args:
            node: Nó atual da árvore
            image_nodes: Lista acumuladora de nós com imagens
        
        Returns:
            Lista de nós que contêm imagens
        """
        if image_nodes is None:
            image_nodes = []
        
        # Verificar se o nó tem fills com imagens
        fills = node.get('fills', [])
        for fill in fills:
            if fill.get('type') == 'IMAGE' and 'imageRef' in fill:
                # Adicionar informações do nó
                image_nodes.append({
                    'id': node.get('id'),
                    'name': node.get('name', 'unnamed'),
                    'imageRef': fill.get('imageRef'),
                    'type': node.get('type'),
                    'absoluteBoundingBox': node.get('absoluteBoundingBox', {})
                })
                break  # Um nó pode ter apenas uma imagem relevante
        
        # Recursivamente processar filhos
        children = node.get('children', [])
        for child in children:
            self.find_image_nodes(child, image_nodes)
        
        return image_nodes
    
    def get_image_urls(self, node_ids: List[str], max_retries: int = 3) -> Dict[str, str]:
        """
        Obtém as URLs das imagens para os IDs fornecidos.
        
        Args:
            node_ids: Lista de IDs dos nós
            max_retries: Número máximo de tentativas em caso de rate limit
        
        Returns:
            Dicionário mapeando node_id -> image_url
        """
        if not node_ids:
            return {}
        
        # Figma API aceita até 100 IDs por requisição
        batch_size = 100
        all_urls = {}
        
        for i in range(0, len(node_ids), batch_size):
            batch = node_ids[i:i + batch_size]
            ids_param = ','.join(batch)
            
            url = f"{self.BASE_URL}/images/{self.file_key}?ids={ids_param}&format=png"
            
            # Tentar com retry para rate limit
            for attempt in range(max_retries):
                try:
                    response = requests.get(url, headers=self.headers, timeout=30)
                    
                    if response.status_code == 200:
                        data = response.json()
                        images = data.get('images', {})
                        all_urls.update(images)
                        break  # Sucesso, sair do loop de retry
                    
                    elif response.status_code == 429:
                        # Rate limit - aguardar antes de tentar novamente
                        wait_time = (attempt + 1) * 30  # 30s, 60s, 90s
                        if attempt < max_retries - 1:
                            print(f"⚠ Rate limit detectado. Aguardando {wait_time} segundos antes de tentar novamente...")
                            time.sleep(wait_time)
                            continue
                        else:
                            print(f"✗ Rate limit persistente após {max_retries} tentativas")
                            break
                    
                    else:
                        response.raise_for_status()
                        
                except requests.exceptions.RequestException as e:
                    if attempt < max_retries - 1:
                        wait_time = (attempt + 1) * 10
                        print(f"⚠ Erro na requisição. Aguardando {wait_time} segundos...")
                        time.sleep(wait_time)
                        continue
                    else:
                        print(f"Erro ao buscar URLs das imagens: {str(e)}")
                        break
            
            # Delay entre batches para evitar rate limit
            if i + batch_size < len(node_ids):
                time.sleep(2)
        
        return all_urls
    
    def download_image(self, image_url: str, filepath: Path) -> bool:
        """
        Baixa uma imagem da URL fornecida.
        
        Args:
            image_url: URL da imagem
            filepath: Caminho onde salvar a imagem
        
        Returns:
            True se o download foi bem-sucedido, False caso contrário
        """
        try:
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            return True
        except requests.exceptions.RequestException as e:
            print(f"Erro ao baixar imagem {image_url}: {str(e)}")
            return False
    
    def download_all_images(self, save_metadata: bool = True) -> Dict:
        """
        Baixa todas as imagens do arquivo Figma.
        
        Args:
            save_metadata: Se True, salva um arquivo JSON com metadados
        
        Returns:
            Dicionário com estatísticas do download
        """
        print(f"Buscando dados do arquivo Figma (FILE_KEY: {self.file_key})...")
        file_data = self.get_file_data()
        
        # Encontrar o documento raiz
        document = file_data.get('document', {})
        
        print("Procurando nós com imagens...")
        image_nodes = self.find_image_nodes(document)
        
        if not image_nodes:
            print("Nenhuma imagem encontrada no arquivo.")
            return {
                'total': 0,
                'downloaded': 0,
                'failed': 0,
                'images': []
            }
        
        print(f"Encontradas {len(image_nodes)} imagens.")
        
        # Agrupar por imageRef para evitar downloads duplicados
        unique_images = {}
        for node in image_nodes:
            image_ref = node['imageRef']
            if image_ref not in unique_images:
                unique_images[image_ref] = node
        
        print(f"Imagens únicas: {len(unique_images)}")
        
        # Obter URLs das imagens - uma por uma para evitar rate limit
        node_ids = [node['id'] for node in unique_images.values()]
        print("Obtendo URLs das imagens (uma por uma para evitar rate limit)...")
        image_urls = {}
        
        for i, node_id in enumerate(node_ids, 1):
            print(f"[{i}/{len(node_ids)}] Obtendo URL...", end=' ')
            
            # Tentar obter URL com retry
            for attempt in range(5):
                try:
                    url = f"{self.BASE_URL}/images/{self.file_key}?ids={node_id}&format=png"
                    response = requests.get(url, headers=self.headers, timeout=30)
                    
                    if response.status_code == 200:
                        data = response.json()
                        urls = data.get('images', {})
                        if node_id in urls:
                            image_urls[node_id] = urls[node_id]
                            print("✓")
                            break
                    elif response.status_code == 429:
                        wait = min(15 * (attempt + 1), 60)  # Max 60 segundos
                        if attempt < 4:
                            print(f"⚠ Rate limit - aguardando {wait}s...", end=' ')
                            time.sleep(wait)
                            continue
                        else:
                            print("✗ Rate limit persistente")
                            break
                    else:
                        print(f"✗ Erro {response.status_code}")
                        break
                except Exception as e:
                    if attempt < 4:
                        time.sleep(5)
                        continue
                    else:
                        print(f"✗ Erro: {str(e)[:30]}")
                        break
            
            # Delay entre requisições
            if i < len(node_ids):
                time.sleep(2)
        
        # Baixar imagens
        downloaded = 0
        failed = 0
        downloaded_files = []
        
        print(f"\nBaixando imagens para: {self.output_dir}")
        print("-" * 70)
        
        for image_ref, node in unique_images.items():
            node_id = node['id']
            image_url = image_urls.get(node_id)
            
            if not image_url:
                print(f"✗ {node['name']} (ID: {node_id}) - URL não encontrada")
                failed += 1
                continue
            
            # Gerar nome do arquivo
            # Usar o nome do nó, sanitizado, ou o imageRef como fallback
            node_name = node['name'].lower().replace(' ', '_')
            # Remover caracteres inválidos
            node_name = ''.join(c for c in node_name if c.isalnum() or c in ('_', '-'))
            
            # Determinar extensão (PNG por padrão)
            extension = 'png'
            if 'jpg' in node_name or 'jpeg' in node_name:
                extension = 'jpg'
            
            filename = f"{node_name}_{image_ref[:8]}.{extension}"
            filepath = self.output_dir / filename
            
            # Baixar imagem com retry
            print(f"[{downloaded + failed + 1}/{len(unique_images)}] {node['name']}...", end=' ')
            
            success = False
            for retry in range(3):
                if self.download_image(image_url, filepath):
                    size_kb = filepath.stat().st_size / 1024
                    print(f"✓ ({size_kb:.1f} KB)")
                    downloaded += 1
                    downloaded_files.append({
                        'name': node['name'],
                        'filename': filename,
                        'path': str(filepath),
                        'size_kb': round(size_kb, 2),
                        'node_id': node_id,
                        'image_ref': image_ref
                    })
                    success = True
                    break
                elif retry < 2:
                    print(f"⚠ Tentando novamente...", end=' ')
                    time.sleep(5)
            
            if not success:
                print(f"✗")
                failed += 1
            
            # Delay entre downloads
            if downloaded + failed < len(unique_images):
                time.sleep(1)
        
        # Salvar metadados se solicitado
        if save_metadata:
            metadata_path = self.output_dir / 'metadata.json'
            metadata = {
                'file_key': self.file_key,
                'total_images': len(image_nodes),
                'unique_images': len(unique_images),
                'downloaded': downloaded,
                'failed': failed,
                'images': downloaded_files
            }
            
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            print(f"\nMetadados salvos em: {metadata_path}")
        
        # Estatísticas finais
        result = {
            'total': len(unique_images),
            'downloaded': downloaded,
            'failed': failed,
            'images': downloaded_files
        }
        
        print("\n" + "=" * 70)
        print("RESULTADO FINAL")
        print("=" * 70)
        print(f"Total de imagens: {result['total']}")
        print(f"✓ Baixadas: {result['downloaded']}")
        print(f"✗ Falhas: {result['failed']}")
        print("=" * 70)
        
        return result


def download_figma_images(file_key: str, output_dir: str = None) -> Dict:
    """
    Função auxiliar para facilitar o uso.
    
    Args:
        file_key: Chave do arquivo Figma
        output_dir: Diretório onde salvar as imagens (opcional)
    
    Returns:
        Dicionário com estatísticas do download
    
    Exemplo:
        from utils.figma_images import download_figma_images
        
        result = download_figma_images("bGtm8mc5RnpGntMspMA70K")
        print(f"Baixadas {result['downloaded']} imagens")
    """
    downloader = FigmaImageDownloader(file_key, output_dir)
    return downloader.download_all_images()

