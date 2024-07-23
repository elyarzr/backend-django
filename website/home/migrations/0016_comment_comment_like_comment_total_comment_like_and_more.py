# Generated by Django 4.2.12 on 2024-05-29 10:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0015_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='comment_like',
            field=models.ManyToManyField(blank=True, related_name='com_like', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='total_comment_like',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='comment',
            name='reply',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment_reply', to='home.comment'),
        ),
    ]
