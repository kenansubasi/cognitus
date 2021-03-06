# Generated by Django 2.2.11 on 2020-03-29 15:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.TextField(verbose_name='Label')),
                ('text', models.TextField(verbose_name='Text')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='data', to=settings.AUTH_USER_MODEL, verbose_name='Creator')),
            ],
            options={
                'verbose_name': 'Data',
                'verbose_name_plural': 'Data',
                'unique_together': {('text', 'label')},
            },
        ),
    ]
