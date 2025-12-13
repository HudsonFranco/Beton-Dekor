"""
Versão simplificada que baixa uma imagem por vez com delays maiores.
Use este se a versão principal estiver com problemas de rate limit.
"""

import os
import requests
import time
from pathlib import Path
from django.conf import settings


def download_figma_images_simple(file_key: str, output_dir: str = None):
    """
    Versão simplificada que baixa uma imagem por vez.
    """
    token = os.environ.get('FIGMA_TOKEN')
    if not token:
        raise ValueError("FIGMA_TOKEN não encontrado")
    
    if output_dir:
        output_path = Path(output_dir)
    else:
        base_dir = Path(settings.BASE_DIR) if hasattr(settings, 'BASE_DIR') else Path.cwd()
        output_path = base_dir / "static" / "images"
    
    output_path.mkdir(parents=True, exist_ok=True)
    
    headers = {"X-Figma-Token": token}
    
    # Lista de node IDs conhecidos do seu arquivo
    nodes = [
        ("2:2", "hero-bg.jpg"),
        ("45:21", "search-icon.png"),
        ("69:20", "instagram.png"),
        ("69:21", "facebook.png"),
        ("77:45", "email.png"),
        ("146:2", "product-1.jpg"),
        ("146:4", "product-2.jpg"),
        ("146:5", "product-3.jpg"),
        ("146:6", "product-4.jpg"),
        ("146:22", "arrow-right.png"),
        ("104:35", "star.png"),
        ("104:24", "profile-2.png"),
        ("104:25", "profile-1.png"),
    ]
    
    print(f"Baixando {len(nodes)} imagens...")
    print("Aguardando 60 segundos inicialmente para resetar rate limit...")
    time.sleep(60)
    
    downloaded = 0
    
    for i, (node_id, filename) in enumerate(nodes, 1):
        filepath = output_path / filename
        
        if filepath.exists():
            print(f"[{i}/{len(nodes)}] ✓ {filename} já existe")
            downloaded += 1
            continue
        
        print(f"[{i}/{len(nodes)}] {filename}...", end=' ')
        
        # Tentar até 3 vezes
        for attempt in range(3):
            try:
                # Obter URL
                url = f"https://api.figma.com/v1/images/{file_key}?ids={node_id}&format=png"
                r = requests.get(url, headers=headers, timeout=30)
                
                if r.status_code == 200:
                    image_url = r.json().get('images', {}).get(node_id)
                    if image_url:
                        # Baixar imagem
                        img_r = requests.get(image_url, timeout=30)
                        if img_r.status_code == 200:
                            with open(filepath, 'wb') as f:
                                f.write(img_r.content)
                            size_kb = len(img_r.content) / 1024
                            print(f"✓ ({size_kb:.1f} KB)")
                            downloaded += 1
                            break
                elif r.status_code == 429:
                    wait = 60 if attempt == 0 else 90
                    print(f"⚠ Rate limit - aguardando {wait}s...", end=' ')
                    time.sleep(wait)
                    continue
                else:
                    print(f"✗ Erro {r.status_code}")
                    break
            except Exception as e:
                if attempt < 2:
                    time.sleep(30)
                    continue
                else:
                    print(f"✗ Erro")
                    break
        
        # Delay entre imagens
        if i < len(nodes):
            time.sleep(5)
    
    print(f"\n✓ Baixadas: {downloaded}/{len(nodes)}")
    return downloaded

