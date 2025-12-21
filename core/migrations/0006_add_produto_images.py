from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_mensagemcontato'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='imagem_2',
            field=models.ImageField(blank=True, null=True, upload_to='produtos/'),
        ),
        migrations.AddField(
            model_name='produto',
            name='imagem_3',
            field=models.ImageField(blank=True, null=True, upload_to='produtos/'),
        ),
    ]
