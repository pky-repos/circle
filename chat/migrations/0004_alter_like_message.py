# Generated by Django 4.1.7 on 2023-03-09 14:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_rename_group_message_chat_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='message',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='likes', to='chat.message'),
        ),
    ]
