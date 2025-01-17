# Generated by Django 5.1.3 on 2024-11-24 05:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mailing',
            options={'verbose_name': 'Рассылка', 'verbose_name_plural': 'Рассылки'},
        ),
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['subject'], 'verbose_name': 'Сообщение', 'verbose_name_plural': 'Сообщения'},
        ),
        migrations.AlterModelOptions(
            name='recipient',
            options={'ordering': ['email'], 'verbose_name': 'Получатель', 'verbose_name_plural': 'Получатели'},
        ),
    ]
