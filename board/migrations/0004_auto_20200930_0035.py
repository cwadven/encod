# Generated by Django 3.1.1 on 2020-09-29 15:35

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('board', '0003_board_ended'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='voter',
            field=models.ManyToManyField(blank=True, related_name='voter_total', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='voteboard',
            name='voter',
            field=models.ManyToManyField(blank=True, related_name='voter_user', to=settings.AUTH_USER_MODEL),
        ),
    ]