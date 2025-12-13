# Docker Setup - Beton Dekor

Este projeto está configurado para rodar com Docker e PostgreSQL.

## Pré-requisitos

- Docker
- Docker Compose

## Configuração Inicial

### 1. Migrar dados do SQLite para PostgreSQL (se você já tem dados)

**ANTES de iniciar o Docker pela primeira vez:**

```bash
# Ative o ambiente virtual
.\venv\Scripts\Activate.ps1

# Exporte os dados do SQLite
python migrate_to_postgres.py
```

Isso criará um arquivo `backup.json` com todos os dados.

### 2. Iniciar Docker

```bash
# Construir e iniciar os containers
docker-compose up --build -d

# Aguardar alguns segundos para o PostgreSQL inicializar
```

### 3. Importar dados para PostgreSQL

```bash
# Importar os dados exportados
docker-compose exec web python manage.py loaddata backup.json
```

### 4. Criar superusuário

```bash
docker-compose exec web python manage.py createsuperuser
```

## Comandos Úteis

- **Iniciar containers**: `docker-compose up -d`
- **Parar containers**: `docker-compose down`
- **Ver logs**: `docker-compose logs -f`
- **Ver logs apenas do web**: `docker-compose logs -f web`
- **Acessar shell do container**: `docker-compose exec web bash`
- **Rodar migrations**: `docker-compose exec web python manage.py migrate`
- **Criar superusuário**: `docker-compose exec web python manage.py createsuperuser`
- **Acessar PostgreSQL**: `docker-compose exec db psql -U betondekor -d betondekor`

## Acessar a aplicação

- **Aplicação**: http://localhost:8000
- **PostgreSQL**: localhost:5432
  - Database: `betondekor`
  - User: `betondekor`
  - Password: `betondekor_password`

## Estrutura

- **PostgreSQL**: Container `betondekor_db` na porta 5432
- **Django**: Container `betondekor_web` na porta 8000
- **Volumes**:
  - `postgres_data`: Dados persistentes do PostgreSQL
  - `static_volume`: Arquivos estáticos coletados
  - `media_volume`: Arquivos de mídia (uploads de produtos)

## Configuração do Banco de Dados

O Django está configurado para usar PostgreSQL quando as variáveis de ambiente `DB_HOST` estão definidas (como no Docker). Caso contrário, usa SQLite para desenvolvimento local.

## Troubleshooting

### Erro de conexão com PostgreSQL
- Verifique se o container do banco está rodando: `docker-compose ps`
- Verifique os logs: `docker-compose logs db`

### Erro ao importar dados
- Certifique-se de que as migrations foram executadas: `docker-compose exec web python manage.py migrate`
- Verifique se o arquivo `backup.json` existe e está no diretório raiz

### Limpar tudo e começar do zero
```bash
docker-compose down -v  # Remove volumes também
docker-compose up --build
```
