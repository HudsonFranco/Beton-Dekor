# Beton Dekor - Projeto Django

Projeto Django para replicar o design do Figma 100% fielmente.

## Estrutura do Projeto

```
Beton Dekor/
├── betondekor/          # Configurações do projeto Django
├── core/                # App principal
├── templates/           # Templates HTML
│   └── core/
├── static/              # Arquivos estáticos (CSS, JS, imagens)
│   ├── css/
│   ├── js/
│   └── images/
├── media/               # Arquivos de mídia enviados pelos usuários
├── venv/                # Ambiente virtual Python
├── manage.py
└── requirements.txt
```

## Configuração e Instalação

### 1. Ativar o ambiente virtual

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

### 3. Executar migrações (quando necessário)

```bash
python manage.py migrate
```

### 4. Criar superusuário (opcional)

```bash
python manage.py createsuperuser
```

### 5. Executar servidor de desenvolvimento

```bash
python manage.py runserver
```

O projeto estará disponível em: http://127.0.0.1:8000/

## Próximos Passos

Para replicar 100% o design do Figma, preciso de:
1. Acesso ao arquivo Figma (pode ser necessário configurar token de API)
2. Screenshots do design
3. Detalhes sobre cores, fontes, espaçamentos e componentes

## Notas

- O projeto está configurado para desenvolvimento
- Arquivos estáticos estão configurados em `static/`
- Templates estão em `templates/`
- O foco atual é no frontend (backend será implementado depois)

