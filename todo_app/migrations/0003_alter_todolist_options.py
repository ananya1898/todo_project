# Generated by Django 4.2.2 on 2023-06-27 14:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo_app', '0002_todoitem'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='todolist',
            options={'ordering': ['title']},
        ),
    ]