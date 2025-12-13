# Download de Imagens do Figma

Módulo para baixar automaticamente todas as imagens de um arquivo Figma via API.

## Configuração

### 1. Configurar variável de ambiente

**Windows (PowerShell):**
```powershell
$env:FIGMA_TOKEN="seu_token_aqui"
```

**Windows (CMD):**
```cmd
set FIGMA_TOKEN=seu_token_aqui
```

**Linux/Mac:**
```bash
export FIGMA_TOKEN=seu_token_aqui
```

Para tornar permanente, adicione ao seu `.env` ou arquivo de configuração.

### 2. Obter o token do Figma

1. Acesse: https://www.figma.com/settings
2. Role até "Personal access tokens"
3. Clique em "Create a new personal access token"
4. Copie o token gerado

## Uso

### Opção 1: Comando Django (Recomendado)

```bash
python manage.py download_figma_images bGtm8mc5RnpGntMspMA70K
```

Com diretório customizado:
```bash
python manage.py download_figma_images bGtm8mc5RnpGntMspMA70K --output-dir static/images
```

### Opção 2: Usando a classe diretamente

```python
from utils.figma_images import FigmaImageDownloader

# Criar instância
downloader = FigmaImageDownloader(
    file_key="bGtm8mc5RnpGntMspMA70K",
    output_dir="static/images"  # opcional
)

# Baixar todas as imagens
result = downloader.download_all_images()

print(f"Baixadas {result['downloaded']} imagens")
```

### Opção 3: Função auxiliar

```python
from utils.figma_images import download_figma_images

result = download_figma_images("bGtm8mc5RnpGntMspMA70K")
```

## Estrutura de Saída

As imagens serão salvas em:
- **Padrão**: `figma_images/` (na raiz do projeto)
- **Customizado**: Diretório especificado

Um arquivo `metadata.json` será criado com informações sobre todas as imagens baixadas.

## Exemplo de Resultado

```json
{
  "file_key": "bGtm8mc5RnpGntMspMA70K",
  "total_images": 25,
  "unique_images": 13,
  "downloaded": 13,
  "failed": 0,
  "images": [
    {
      "name": "Hero Background",
      "filename": "hero_background_2afb6ed9.png",
      "path": "figma_images/hero_background_2afb6ed9.png",
      "size_kb": 245.67,
      "node_id": "2:2",
      "image_ref": "2afb6ed9fe9171ee3c9580e14c26181a57d07948"
    }
  ]
}
```

## Funcionalidades

- ✅ Busca recursiva de todos os nós com imagens
- ✅ Remove duplicatas (agrupa por imageRef)
- ✅ Baixa em lote (até 100 imagens por requisição)
- ✅ Gera nomes de arquivo baseados no nome do nó
- ✅ Salva metadados em JSON
- ✅ Tratamento de erros robusto
- ✅ Usa variáveis de ambiente para token

## Troubleshooting

### Erro: "FIGMA_TOKEN não encontrado"
Configure a variável de ambiente antes de executar.

### Erro: "Rate limit exceeded"
Aguarde alguns minutos e tente novamente. O Figma limita requisições por minuto.

### Imagens não encontradas
Verifique se o FILE_KEY está correto e se você tem acesso ao arquivo no Figma.

