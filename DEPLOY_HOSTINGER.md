# 🚀 Deploy BetonDekor na Hostinger

## 📋 Pré-requisitos

- Conta Hostinger com plano que suporte Python/Django
- Acesso ao repositório GitHub (privado): `HudsonFranco/Beton-Dekor`
- Credenciais Cloudinary para upload de imagens

## 🔧 Passos para Deploy

### 1️⃣ Configurar Variáveis de Ambiente na Hostinger

No painel da Hostinger, configure as seguintes variáveis de ambiente:

```env
# Django Settings
SECRET_KEY=django-insecure-(3%zw8&787o0=)p+p*lhnmv@s)gpls_%kp$6d-ud9!%=8w37ys
DEBUG=False
ALLOWED_HOSTS=seudominio.com.br,www.seudominio.com.br

# Cloudinary Configuration (obrigatório para imagens)
CLOUDINARY_CLOUD_NAME=dztlh19q1
CLOUDINARY_API_KEY=536528844238579
CLOUDINARY_API_SECRET=u8nhS7roEoSnUh5CcTshmn6Lc8Q

# Email Configuration (para formulário de contato)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp-mail.outlook.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=betondekor@outlook.com
EMAIL_HOST_PASSWORD=sua-senha-do-outlook
```

⚠️ **IMPORTANTE**: 
- Substitua `seudominio.com.br` pelo domínio real
- Para emails, se tiver 2FA no Outlook, gere uma "senha de aplicativo"
- Em produção, gere um novo SECRET_KEY com: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`

### 2️⃣ Conectar GitHub à Hostinger

1. Acesse o painel da Hostinger
2. Vá em **"Git Deployment"** ou **"Deploy"**
3. Conecte ao repositório: `HudsonFranco/Beton-Dekor`
4. Branch: `main`
5. Repositório é **privado** - forneça credenciais de acesso

### 3️⃣ Configurar Build/Deploy

Configure os comandos de build na Hostinger:

```bash
# Instalar dependências
pip install -r requirements.txt

# Coletar arquivos estáticos
python manage.py collectstatic --noinput

# Executar migrações do banco
python manage.py migrate
```

### 4️⃣ Configurar Servidor Web

**Comando de Start:**
```bash
gunicorn betondekor.wsgi:application --bind 0.0.0.0:8000
```

**Arquivo WSGI:** `betondekor/wsgi.py`

### 5️⃣ Banco de Dados

**Opção 1: SQLite (padrão, mais simples)**
- Não precisa configurar nada
- Banco local: `db.sqlite3`
- ⚠️ Backups manuais necessários

**Opção 2: PostgreSQL (recomendado para produção)**
- Configure as variáveis adicionais:
```env
DB_HOST=seu-host-postgresql.hostinger.com
DB_PORT=5432
DB_NAME=nome_do_banco
DB_USER=usuario_banco
DB_PASSWORD=senha_banco
```

## 📁 Estrutura do Projeto

```
Beton Dekor/
├── betondekor/          # Configurações Django
│   ├── settings.py      # Lê variáveis de ambiente
│   ├── urls.py
│   └── wsgi.py         # Entry point para Gunicorn
├── core/               # App principal
│   ├── models.py       # Produtos, Categorias, Mensagens
│   ├── views.py        # Lógica de negócio
│   └── urls.py
├── static/             # Arquivos estáticos (CSS, JS, imagens)
├── templates/          # Templates HTML
├── media/              # Uploads de usuários (via Cloudinary)
├── requirements.txt    # Dependências Python
├── manage.py          # Django CLI
└── .env.example       # Template de variáveis (NÃO usar em produção)
```

## ✅ Checklist Pós-Deploy

- [ ] Site carrega corretamente no domínio
- [ ] Imagens dos produtos aparecem (Cloudinary funcionando)
- [ ] Formulário "Entre em Contato" envia emails para `betondekor@outlook.com`
- [ ] Páginas responsivas em mobile/tablet
- [ ] Admin Django acessível em `/admin`
- [ ] Criar superusuário: `python manage.py createsuperuser`
- [ ] SSL/HTTPS configurado (geralmente automático na Hostinger)

## 🔒 Segurança

- ✅ `.env` não está no repositório (ignorado pelo `.gitignore`)
- ✅ Credenciais via variáveis de ambiente
- ✅ `DEBUG=False` em produção
- ✅ `SECRET_KEY` única para produção
- ✅ HTTPS obrigatório (Hostinger fornece SSL gratuito)

## 📧 Configuração de Email

Para receber emails do formulário de contato:

1. Use `betondekor@outlook.com`
2. No Outlook, vá em: **Configurações > Segurança > Senhas de aplicativo**
3. Gere uma senha específica para o Django
4. Use essa senha na variável `EMAIL_HOST_PASSWORD`

## 🆘 Troubleshooting

**Imagens não aparecem:**
- Verifique credenciais Cloudinary nas variáveis de ambiente
- Execute: `python manage.py collectstatic --noinput`

**Erro 500:**
- Verifique logs da Hostinger
- Confirme que `DEBUG=False` e `ALLOWED_HOSTS` está configurado

**Emails não enviam:**
- Confirme configurações SMTP do Outlook
- Verifique se a senha de aplicativo está correta

**CSS/JS não carregam:**
- Execute `python manage.py collectstatic --noinput`
- Verifique configuração do WhiteNoise

## 📞 Contato de Desenvolvimento

- Repositório: https://github.com/HudsonFranco/Beton-Dekor
- Email: betondekor@outlook.com

---

✨ **Projeto pronto para produção!**
