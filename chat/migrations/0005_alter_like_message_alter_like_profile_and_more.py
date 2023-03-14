# Generated by Django 4.1.7 on 2023-03-11 19:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_rename_group_profile_chat_group'),
        ('chat', '0004_alter_like_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='message',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='likes', to='chat.message'),
        ),
        migrations.AlterField(
            model_name='like',
            name='profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.profile'),
        ),
        migrations.AlterField(
            model_name='message',
            name='chat_group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='chat.chatgroup'),
        ),
        migrations.AlterField(
            model_name='message',
            name='profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.profile'),
        ),
    ]