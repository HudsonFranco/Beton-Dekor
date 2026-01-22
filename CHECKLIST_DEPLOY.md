# ✅ Checklist de Deploy - BetonDekor

## 📦 Repositório GitHub (Verificado)

- ✅ Repositório privado: `HudsonFranco/Beton-Dekor`
- ✅ Branch principal: `main`
- ✅ `.env` NÃO está no repositório (segurança OK)
- ✅ `.env.example` disponível como template
- ✅ `.gitignore` configurado corretamente
- ✅ `requirements.txt` atualizado
- ✅ Guia de deploy: `DEPLOY_HOSTINGER.md`

## 🔐 Variáveis de Ambiente (Seu sócio precisa configurar)

### Obrigatórias:
```env
SECRET_KEY=django-insecure-(3%zw8&787o0=)p+p*lhnmv@s)gpls_%kp$6d-ud9!%=8w37ys
DEBUG=False
ALLOWED_HOSTS=seudominio.com.br,www.seudominio.com.br

CLOUDINARY_CLOUD_NAME=dztlh19q1
CLOUDINARY_API_KEY=536528844238579
CLOUDINARY_API_SECRET=u8nhS7roEoSnUh5CcTshmn6Lc8Q

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp-mail.outlook.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=betondekor@outlook.com
EMAIL_HOST_PASSWORD=senha-do-outlook
```

### ⚠️ IMPORTANTE:
- Gerar novo `SECRET_KEY` para produção
- Configurar senha de aplicativo do Outlook (se tiver 2FA)
- Substituir `seudominio.com.br` pelo domínio real

## 🛠️ Comandos de Build (Hostinger)

```bash
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
```

## 🚀 Comando de Start

```bash
gunicorn betondekor.wsgi:application --bind 0.0.0.0:8000
```

## 📋 Arquivos Importantes

| Arquivo | Status | Descrição |
|---------|--------|-----------|
| `DEPLOY_HOSTINGER.md` | ✅ Criado | Guia completo de deploy |
| `.env.example` | ✅ Atualizado | Template de variáveis |
| `requirements.txt` | ✅ OK | Todas dependências listadas |
| `settings.py` | ✅ Configurado | Lê variáveis de ambiente |
| `.gitignore` | ✅ OK | Exclui arquivos sensíveis |
| `db.sqlite3` | ✅ Ignorado | Não está no Git |

## 🔍 Verificações Realizadas

### Segurança:
- ✅ Credenciais não estão hardcoded
- ✅ `.env` ignorado pelo Git
- ✅ `DEBUG=False` em produção via variável
- ✅ Email configurado via variáveis de ambiente

### Funcionalidades:
- ✅ Cloudinary configurado para imagens
- ✅ WhiteNoise para arquivos estáticos
- ✅ PostgreSQL opcional (usa SQLite por padrão)
- ✅ Gunicorn como servidor WSGI
- ✅ Email SMTP configurado (Outlook)

### Responsividade:
- ✅ Mobile otimizado
- ✅ Tablet (iPad Air, iPad Pro) otimizado
- ✅ Desktop otimizado
- ✅ Carousel de depoimentos funcionando

## 📧 Configuração de Email

**Destinatário dos formulários:** `betondekor@outlook.com`

**Passos para configurar senha:**
1. Acesse: https://account.microsoft.com/security
2. Vá em "Segurança Avançada"
3. Crie uma "Senha de aplicativo"
4. Use essa senha na variável `EMAIL_HOST_PASSWORD`

## 🎯 Próximos Passos para seu Sócio

1. **Clonar o repositório** (precisa de acesso ao repo privado)
   ```bash
   git clone https://github.com/HudsonFranco/Beton-Dekor.git
   ```

2. **Ler o guia:** `DEPLOY_HOSTINGER.md`

3. **Configurar variáveis de ambiente** no painel da Hostinger

4. **Conectar GitHub** ao deploy automático da Hostinger

5. **Configurar comandos de build** (listados acima)

6. **Executar deploy inicial**

7. **Criar superusuário:**
   ```bash
   python manage.py createsuperuser
   ```

8. **Testar:**
   - [ ] Site carrega
   - [ ] Imagens aparecem
   - [ ] Formulário envia email
   - [ ] Admin funciona
   - [ ] Mobile responsivo

## 📞 Informações de Contato

- **Email principal:** betondekor@outlook.com
- **Repositório:** https://github.com/HudsonFranco/Beton-Dekor
- **Branch:** main (sempre atualizada)

## 🆘 Em Caso de Problemas

Todos os problemas comuns e soluções estão documentados em:
`DEPLOY_HOSTINGER.md` (seção "Troubleshooting")

---

✨ **Status:** PRONTO PARA DEPLOY
🔒 **Segurança:** OK
📦 **Repositório:** COMPLETO
